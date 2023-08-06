#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 12:37:56 2021
@author: nwoye chinedu i.
icube, unistra
"""

import numpy as np
from sklearn.metrics import average_precision_score
import warnings


"""
t50metrics.

An example python library for surgical action triplet evaluation.
"""

__version__ = "0.1.0"
__author__ = 'Chinedu Nwoye'
__credits__ = 'CAMMA, ICube Lab, University of Strasbourg, France'


class Recognition(object):
    """
    Class: compute (mean) Average Precision
    
    @args
    ----
        num_class: int, optional. The number of class of the classification task (default = 6)
            
    @attributes
    ----------
    video_log :   2D array
        holds the AP performance for all logged videos
    predictions:    2D array
        holds the accumulated predictions before a reset()
    targets:        2D array
        holds the accumulated groundtruths before a reset()
    
    @methods
    -------
    GENERIC
    -------
    update(targets, predictions): 
        call per iteration to update the class accumulators for predictions and corresponding groundtruths.    
    reset(): 
        call at the beginning of new experiment or epoch to reset all accumulators.    
    compute(): 
        call at any point to check the performance of all seen examples after the last reset() call.
        
    FRAME-WISE
    ----------
    compute_global_AP(): compute the framewise AP and mAP
    
    VIDEO-WISE
    ----------         
    video_end(): 
        call at the end of every video during inference to log performance per video
    compute_video_AP(): 
        call at any time, usually at the end of experiment or inference, to obtain the performance of all tested videos.  
    compute_per_video_mAP(self):
        show mAP per video (not very useful)

    OTHERS
    ------
    topk(k):
        obtain top k=[5,10,20, etc] performance
    topClass(k):
        obtain top-k correctly detected classes      
    """
    
    def __init__(self, num_class=6):
        np.seterr(divide='ignore', invalid='ignore')
        self.num_class = num_class
        self.reset()
        self.reset_video()
        self.reset_global()
        
        
    def update(self, tragets, predictions):
        """
        update prediction function
        @args
        -----
        targets: 2D array, float
            groundtruth of shape (F, C) where F = number of frames, C = number of class
        predictions: 2D array, int
            model prediction of the shape as the groundtruth
        """
        self.predictions = np.append(self.predictions, predictions, axis=0)
        self.tragets     = np.append(self.tragets, tragets, axis=0)
        self.global_predictions = np.append(self.global_predictions, predictions, axis=0)
        self.global_tragets     = np.append(self.global_tragets, tragets, axis=0)

    def reset(self):
        "call at the beginning of new experiment or epoch to reset the accumulators for preditions and groundtruths."
        self.predictions = np.empty(shape = [0,self.num_class], dtype=np.float)
        self.tragets     = np.empty(shape = [0,self.num_class], dtype=np.int)

    def compute_AP(self):
        """
        compute performance for all seen examples after a reset()
        @return
        -------
        classwise: 1D array, float
            AP performance per class
        mean: float
            mean AP performance
        """
        classwise = average_precision_score(self.tragets, self.predictions, average=None)
        mean      = np.nanmean(classwise)
        return classwise, mean
     
    def reset_global(self):
        "call at the beginning of new experiment"
        self.global_predictions = np.empty(shape = [0,self.num_class], dtype=np.float)
        self.global_tragets     = np.empty(shape = [0,self.num_class], dtype=np.int)
        self.reset()
        self.reset_video()
    
    def compute_global_AP(self):
        """
        compute performance for all seen examples after a reset()
        @return
        -------
        classwise: 1D array, float
            AP performance per class
        mean: float
            mean AP performance
        """
        classwise = average_precision_score(self.global_tragets, self.global_predictions, average=None)
        mean      = np.nanmean(classwise)
        return classwise, mean
    
    def reset_video(self):
        "used internally, call at the begining of an experiment or inference"
        self.video_log = np.empty(shape = [0,self.num_class], dtype=np.float)
        self.reset()

    def video_end(self):
        "call to signal the end of current video. Needed during inference to log performance per video"
        classwise, _    = self.compute_AP()
        self.video_log  = np.append(self.video_log, classwise.reshape([1,-1]), axis=0)
        self.reset()
    
    def compute_video_AP(self):
        """
        compute performance video-wise
        @return
        -------
        classwise: 1D array, float
            AP performance per class for all videos
        mean: float
            mean AP performance for all videos
        """
        with warnings.catch_warnings():
            warnings.filterwarnings(action='ignore', message='Mean of empty slice')
            classwise = np.nanmean(self.video_log, axis=0)
            mean      = np.nanmean(classwise)
        return classwise, mean
    
    def compute_per_video_mAP(self):
        """ get AP per video """
        print("VIDEO HISTORY", self.video_log)
        return np.nanmean(self.video_log, axis=1)

    def topk(self, k=5):
        """
        compute performance for all seen examples after a reset()
        
        @args
        ----
        k: int
            number of chances of correct prediction
            
        @return
        ----
        mean: float
            mean top-k performance
        """
        correct = 0.0
        total   = 0
        for gt, pd in zip(self.global_tragets, self.global_predictions):
            gt_pos  = np.nonzero(gt)[0]
            pd_idx  = (-pd).argsort()[:k]
            correct += len(set(gt_pos).intersection(set(pd_idx)))
            total   += len(gt_pos)
        if total==0: total=1
        return correct/total

    def topClass(self, k=10):
        # NotImplementedError("Function not supported yet!")
        classwise = average_precision_score(self.global_tragets, self.global_predictions, average=None)
        pd_idx    = (-classwise).argsort()[:k]
        output    = {x:classwise[x] for x in pd_idx}
        return output
        
        
        



class Disentangle(object):
    """
    Class: filter a triplet prediction into the components (such as instrument i, verb v, target t, instrument-verb iv, instrument-target it, etc)
    
    @args
    ----
        url: str. path to the dictionary map file of the dataset decomposition labels
            
    @params
    ----------
    bank :   2D array
        holds the dictionary mapping of all components
    
    @methods
    -------
    extract(input, componet): 
        call filter a component labels from the inputs labels     
    """


    def __init__(self, url="./maps.txt"):
        self.bank = np.genfromtxt(url, dtype=int, comments='#', delimiter=',', skip_header=0)
        
    def decompose(self, data):
        """ Extract the component labels from the triplets.
            @args:
                inputs: a 1D vector of dimension (n), where n = number of triplet classes;
                        with values int(0 or 1) for target labels and float[0, 1] for predicted labels.
                component: a string for the component to extract; 
                        (e.g.: i for instrument, v for verb, t for target, iv for instrument-verb pair, it for instrument-target pair and vt (unused) for verb-target pair)
            @return:
                output: int or float sparse encoding 1D vector of dimension (n), where n = number of component's classes.
        """
        txt2id = {'ivt':0, 'i':1, 'v':2, 't':3, 'iv':4, 'it':5, 'vt':6} 
        inputs, component = data
        key    = txt2id[component]
        index  = sorted(np.unique(self.bank[:,key]))
        output = []
        for idx in index:
            same_class = [i for i,x in enumerate(self.bank[:,key]) if x==idx]
            y = np.max(inputs[same_class])
            output.append( y )        
        return output
    
    def extract(self, inputs, componet="i"):
        """
        Extract a component label from the triplet label
        @args
        ----
        inputs: 2D array,
            triplet labels, either predicted label or the groundtruth
        component: str,
            the symbol of the component to extract, choose from
            i: instrument
            v: verb
            t: target
            iv: instrument-verb
            it: instrument-target
            vt: verb-target (not useful)

        @return
        ------
        label: 2D array,
            filtered component's labels of the same shape and data type as the inputs
        """           
        return map(self.decompose, (inputs, componet))




class meanAccumulator(object):
    def __init__(self):      
        self.reset()

    def update(self, value):
        if value==value:
            self.sum   += value
            self.count += 1

    def reset(self):
        self.sum   = 0.0
        self.count = 0

    def average(self):
        return self.sum/self.count
