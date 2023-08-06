'''
Function:
    test the segmentor
Author:
    Zhenchao Jin
'''
import os
import cv2
import copy
import torch
import pickle
import warnings
import argparse
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist
from modules import *
from tqdm import tqdm
from cfgs import BuildConfig
warnings.filterwarnings('ignore')


'''parse arguments in command line'''
def parseArgs():
    parser = argparse.ArgumentParser(description='SSSegmentation is an open source strongly supervised semantic segmentation toolbox based on PyTorch')
    parser.add_argument('--local_rank', dest='local_rank', help='node rank for distributed testing', default=0, type=int)
    parser.add_argument('--nproc_per_node', dest='nproc_per_node', help='number of process per node', default=4, type=int)
    parser.add_argument('--cfgfilepath', dest='cfgfilepath', help='config file path you want to use', type=str, required=True)
    parser.add_argument('--evalmode', dest='evalmode', help='evaluate mode, support online and offline', default='offline', type=str)
    parser.add_argument('--checkpointspath', dest='checkpointspath', help='checkpoints you want to resume from', type=str, required=True)
    args = parser.parse_args()
    return args


'''Tester'''
class Tester():
    def __init__(self, **kwargs):
        # set attribute
        for key, value in kwargs.items(): setattr(self, key, value)
        self.use_cuda = torch.cuda.is_available()
        # modify config for consistency
        if not self.use_cuda:
            if self.cmd_args.local_rank == 0: self.logger_handle.warning('Cuda is not available, only cpu is used to test the segmentor...')
            self.cfg.SEGMENTOR_CFG['distributed']['is_on'] = False
            self.cfg.DATALOADER_CFG['test']['type'] = 'nondistributed'
        if self.cfg.SEGMENTOR_CFG['distributed']['is_on']:
            self.cfg.SEGMENTOR_CFG['is_multi_gpus'] = True
            self.cfg.DATALOADER_CFG['test']['type'] = 'distributed'
            self.cfg.DATALOADER_CFG['test']['batch_size'] = self.cmd_args.nproc_per_node
        # init distributed testing if necessary
        distributed_cfg = self.cfg.SEGMENTOR_CFG['distributed']
        if distributed_cfg['is_on']:
            dist.init_process_group(backend=distributed_cfg.get('backend', 'nccl'))
    '''start tester'''
    def start(self, all_preds, all_gts):
        cfg, logger_handle, use_cuda, cmd_args, cfg_file_path = self.cfg, self.logger_handle, self.use_cuda, self.cmd_args, self.cfg_file_path
        distributed_cfg, common_cfg = self.cfg.SEGMENTOR_CFG['distributed'], self.cfg.COMMON_CFG['train']
        # instanced dataset and dataloader
        dataset = BuildDataset(mode='TEST', logger_handle=logger_handle, dataset_cfg=copy.deepcopy(cfg.DATASET_CFG))
        assert dataset.num_classes == cfg.SEGMENTOR_CFG['num_classes'], 'parsed config file %s error...' % cfg_file_path
        dataloader_cfg = copy.deepcopy(cfg.DATALOADER_CFG)
        if distributed_cfg['is_on']:
            batch_size, num_workers = dataloader_cfg['test']['batch_size'], dataloader_cfg['test']['num_workers']
            batch_size //= self.ngpus_per_node
            num_workers //= self.ngpus_per_node
            assert batch_size * self.ngpus_per_node == dataloader_cfg['test']['batch_size'], 'unsuitable batch_size...'
            assert num_workers * self.ngpus_per_node == dataloader_cfg['test']['num_workers'], 'unsuitable num_workers...'
            dataloader_cfg['test'].update({'batch_size': batch_size, 'num_workers': num_workers})
        dataloader = BuildParallelDataloader(mode='TEST', dataset=dataset, cfg=copy.deepcopy(dataloader_cfg))
        # instanced segmentor
        cfg.SEGMENTOR_CFG['backbone']['pretrained'] = False
        segmentor = BuildSegmentor(segmentor_cfg=copy.deepcopy(cfg.SEGMENTOR_CFG), mode='TEST')
        if distributed_cfg['is_on']:
            torch.cuda.set_device(cmd_args.local_rank)
            segmentor.cuda(cmd_args.local_rank)
        else:
            if use_cuda: segmentor = segmentor.cuda()
        # load checkpoints
        checkpoints = loadcheckpoints(cmd_args.checkpointspath, logger_handle=logger_handle, cmd_args=cmd_args)
        try:
            segmentor.load_state_dict(checkpoints['model'])
        except Exception as e:
            logger_handle.warning(str(e) + '\n' + 'Try to load checkpoints by using strict=False...')
            segmentor.load_state_dict(checkpoints['model'], strict=False)
        # parallel
        if use_cuda and cfg.SEGMENTOR_CFG['is_multi_gpus']:
            is_distributed_on = cfg.SEGMENTOR_CFG['distributed']['is_on']
            segmentor = BuildParallelModel(segmentor, is_distributed_on, device_ids=[cmd_args.local_rank] if is_distributed_on else None)
        # print information
        if cmd_args.local_rank == 0:
            logger_handle.info('Dataset: %s-%s, Number of images: %s' % (cfg.DATASET_CFG['type'], cfg.DATASET_CFG['test']['set'], len(dataset)))
            logger_handle.info('Segmentor: %s, Backbone: %s-%s' % (cfg.SEGMENTOR_CFG['type'], cfg.SEGMENTOR_CFG['backbone']['series'], cfg.SEGMENTOR_CFG['backbone']['type']))
            logger_handle.info('Resume from: %s' % cmd_args.checkpointspath)
            logger_handle.info('Config file path: %s' % cfg_file_path)
        # set eval
        segmentor.eval()
        # start to test
        FloatTensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor
        inference_cfg = copy.deepcopy(cfg.INFERENCE_CFG)
        with torch.no_grad():
            if cfg.SEGMENTOR_CFG['distributed']['is_on']: dataloader.sampler.set_epoch(0)
            pbar = tqdm(enumerate(dataloader))
            for batch_idx, samples in pbar:
                pbar.set_description('Processing %s/%s in rank %s' % (batch_idx+1, len(dataloader), cmd_args.local_rank))
                imageids, images, widths, heights, gts = samples['id'], samples['image'], samples['width'], samples['height'], samples['groundtruth']
                infer_tricks, align_corners = inference_cfg['tricks'], segmentor.align_corners if hasattr(segmentor, 'align_corners') else segmentor.module.align_corners
                cascade_cfg = infer_tricks.get('cascade', {'key_for_pre_output': 'memory_gather_logits', 'times': 1, 'forward_default_args': None})
                for idx in range(cascade_cfg['times']):
                    forward_args = None
                    if idx > 0: 
                        outputs_list = [
                            F.interpolate(outputs, size=outputs_list[-1].shape[2:], mode='bilinear', align_corners=align_corners) for outputs in outputs_list
                        ]
                        forward_args = {cascade_cfg['key_for_pre_output']: sum(outputs_list) / len(outputs_list)}
                        if cascade_cfg['forward_default_args'] is not None: forward_args.update(cascade_cfg['forward_default_args'])
                    outputs_list = self.auginference(
                        segmentor=segmentor,
                        images=images,
                        inference_cfg=inference_cfg,
                        num_classes=dataset.num_classes,
                        FloatTensor=FloatTensor,
                        align_corners=align_corners,
                        forward_args=forward_args,
                    )
                for idx in range(len(outputs_list[0])):
                    output = [
                        F.interpolate(outputs[idx: idx+1], size=(heights[idx], widths[idx]), mode='bilinear', align_corners=align_corners) for outputs in outputs_list
                    ]
                    output = sum(output) / len(output)
                    pred = (torch.argmax(output[0], dim=0)).cpu().numpy().astype(np.int32)
                    all_preds.append([imageids[idx], pred])
                    gt = gts[idx].cpu().numpy().astype(np.int32)
                    gt[gt >= dataset.num_classes] = -1
                    all_gts.append(gt)
    '''inference with augmentations'''
    def auginference(self, segmentor, images, inference_cfg, num_classes, FloatTensor, align_corners, forward_args=None):
        infer_tricks, outputs_list = inference_cfg['tricks'], []
        for scale_factor in infer_tricks['multiscale']:
            images_scale = F.interpolate(images, scale_factor=scale_factor, mode='bilinear', align_corners=align_corners)
            outputs = self.inference(
                segmentor=segmentor, 
                images=images_scale.type(FloatTensor), 
                inference_cfg=inference_cfg, 
                num_classes=num_classes, 
                forward_args=forward_args,
            ).cpu()
            outputs_list.append(outputs)
            if infer_tricks['flip']:
                images_flip = torch.from_numpy(np.flip(images_scale.cpu().numpy(), axis=3).copy())
                outputs_flip = self.inference(
                    segmentor=segmentor, 
                    images=images_flip.type(FloatTensor), 
                    inference_cfg=inference_cfg, 
                    num_classes=num_classes, 
                    forward_args=forward_args,
                )
                fix_ann_pairs = inference_cfg.get('fix_ann_pairs', None)
                if fix_ann_pairs is None:
                    for aug_opt in self.cfg.DATASET_CFG['train']['aug_opts']:
                        if 'RandomFlip' in aug_opt: fix_ann_pairs = aug_opt[-1].get('fix_ann_pairs', None)
                if fix_ann_pairs is not None:
                    outputs_flip_clone = outputs_flip.data.clone()
                    for (pair_a, pair_b) in fix_ann_pairs:
                        outputs_flip[:, pair_a, :, :] = outputs_flip_clone[:, pair_b, :, :]
                        outputs_flip[:, pair_b, :, :] = outputs_flip_clone[:, pair_a, :, :]
                outputs_flip = torch.from_numpy(np.flip(outputs_flip.cpu().numpy(), axis=3).copy()).type_as(outputs)
                outputs_list.append(outputs_flip)
        return outputs_list
    '''inference'''
    def inference(self, segmentor, images, inference_cfg, num_classes, forward_args=None):
        assert inference_cfg['mode'] in ['whole', 'slide']
        use_probs_before_resize = inference_cfg['tricks']['use_probs_before_resize']
        if inference_cfg['mode'] == 'whole':
            if forward_args is None:
                outputs = segmentor(images)
            else:
                outputs = segmentor(images, **forward_args)
            if use_probs_before_resize: outputs = F.softmax(outputs, dim=1)
        else:
            align_corners = segmentor.align_corners if hasattr(segmentor, 'align_corners') else segmentor.module.align_corners
            opts = inference_cfg['opts']
            stride_h, stride_w = opts['stride']
            cropsize_h, cropsize_w = opts['cropsize']
            batch_size, _, image_h, image_w = images.size()
            num_grids_h = max(image_h - cropsize_h + stride_h - 1, 0) // stride_h + 1
            num_grids_w = max(image_w - cropsize_w + stride_w - 1, 0) // stride_w + 1
            outputs = images.new_zeros((batch_size, num_classes, image_h, image_w))
            count_mat = images.new_zeros((batch_size, 1, image_h, image_w))
            for h_idx in range(num_grids_h):
                for w_idx in range(num_grids_w):
                    x1, y1 = w_idx * stride_w, h_idx * stride_h
                    x2, y2 = min(x1 + cropsize_w, image_w), min(y1 + cropsize_h, image_h)
                    x1, y1 = max(x2 - cropsize_w, 0), max(y2 - cropsize_h, 0)
                    crop_images = images[:, :, y1:y2, x1:x2]
                    if forward_args is None:
                        outputs_crop = segmentor(crop_images)
                    else:
                        outputs_crop = segmentor(crop_images, **forward_args)
                    outputs_crop = F.interpolate(outputs_crop, size=crop_images.size()[2:], mode='bilinear', align_corners=align_corners)
                    if use_probs_before_resize: outputs_crop = F.softmax(outputs_crop, dim=1)
                    outputs += F.pad(outputs_crop, (int(x1), int(outputs.shape[3] - x2), int(y1), int(outputs.shape[2] - y2)))
                    count_mat[:, :, y1:y2, x1:x2] += 1
            assert (count_mat == 0).sum() == 0
            outputs = outputs / count_mat
        return outputs


'''main'''
def main():
    # parse arguments
    args = parseArgs()
    cfg, cfg_file_path = BuildConfig(args.cfgfilepath)
    # check backup dir
    common_cfg = cfg.COMMON_CFG['test']
    checkdir(common_cfg['backupdir'])
    # initialize logger_handle
    logger_handle = Logger(common_cfg['logfilepath'])
    # number of gpus, for distribued testing, only support a process for a GPU
    ngpus_per_node = torch.cuda.device_count()
    if (ngpus_per_node != args.nproc_per_node) and cfg.SEGMENTOR_CFG['distributed']['is_on']:
        if args.local_rank == 0: logger_handle.warning('ngpus_per_node is not equal to nproc_per_node, force ngpus_per_node = nproc_per_node by default...')
        ngpus_per_node = args.nproc_per_node
    # instanced Tester
    all_preds, all_gts = [], []
    client = Tester(cfg=cfg, ngpus_per_node=ngpus_per_node, logger_handle=logger_handle, cmd_args=args, cfg_file_path=cfg_file_path)
    client.start(all_preds, all_gts)
    # save results and evaluate
    if cfg.SEGMENTOR_CFG['distributed']['is_on']:
        backupdir = common_cfg['backupdir']
        filename = common_cfg['resultsavepath'].split('/')[-1].split('.')[0] + f'_{args.local_rank}.' + common_cfg['resultsavepath'].split('.')[-1]
        with open(os.path.join(backupdir, filename), 'wb') as fp:
            pickle.dump([all_preds, all_gts], fp)
        rank = torch.tensor([args.local_rank], device='cuda')
        rank_list = [rank.clone() for _ in range(args.nproc_per_node)]
        dist.all_gather(rank_list, rank)
        logger_handle.info('Rank %s finished...' % int(rank.item()))
        if args.local_rank == 0:
            all_preds_gather, all_gts_gather = [], []
            for rank in rank_list:
                rank = str(int(rank.item()))
                filename = common_cfg['resultsavepath'].split('/')[-1].split('.')[0] + f'_{rank}.' + common_cfg['resultsavepath'].split('.')[-1]
                fp = open(os.path.join(backupdir, filename), 'rb')
                all_preds, all_gts = pickle.load(fp)
                all_preds_gather += all_preds
                all_gts_gather += all_gts
            all_preds, all_gts = all_preds_gather, all_gts_gather
    else:
        with open(common_cfg['resultsavepath'], 'wb') as fp:
            pickle.dump([all_preds, all_gts], fp)
    if args.local_rank == 0:
        all_preds_filtered, all_gts_filtered, all_ids = [], [], []
        for idx, pred in enumerate(all_preds):
            if pred[0] in all_ids: continue
            all_ids.append(pred[0])
            all_preds_filtered.append(pred[1])
            all_gts_filtered.append(all_gts[idx])
        all_preds, all_gts = all_preds_filtered, all_gts_filtered
        logger_handle.info('All Finished, all_preds: %s, all_gts: %s' % (len(all_preds), len(all_gts)))
        dataset = BuildDataset(mode='TEST', logger_handle=logger_handle, dataset_cfg=copy.deepcopy(cfg.DATASET_CFG))
        if args.evalmode == 'offline':
            result = dataset.evaluate(
                predictions=all_preds, 
                groundtruths=all_gts, 
                metric_list=cfg.INFERENCE_CFG.get('metric_list', ['iou', 'miou']),
                num_classes=cfg.SEGMENTOR_CFG['num_classes'],
                ignore_index=-1,
            )
            logger_handle.info(result)
        else:
            dataset.formatresults(all_preds, all_ids)


'''debug'''
if __name__ == '__main__':
    with torch.no_grad():
        main()