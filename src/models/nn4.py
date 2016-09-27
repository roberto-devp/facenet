# pylint: disable=missing-docstring
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import models.network as network

def inference(images, keep_probability, phase_train=True, weight_decay=0.0):
    """ Define an inference network for face recognition based 
           on inception modules using batch normalization
    
    Args:
      images: The images to run inference on, dimensions batch_size x height x width x channels
      phase_train: True if batch normalization should operate in training mode
    """
    endpoints = {}
    net = network.conv(images, 3, 64, 7, 7, 2, 2, 'SAME', 'conv1_7x7', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['conv1'] = net
    net = network.mpool(net,  3, 3, 2, 2, 'SAME', 'pool1')
    endpoints['pool1'] = net
    net = network.conv(net,  64, 64, 1, 1, 1, 1, 'SAME', 'conv2_1x1', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['conv2_1x1'] = net
    net = network.conv(net,  64, 192, 3, 3, 1, 1, 'SAME', 'conv3_3x3', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['conv3_3x3'] = net
    net = network.mpool(net,  3, 3, 2, 2, 'SAME', 'pool3')
    endpoints['pool3'] = net
  
    net = network.inception(net, 192, 1, 64, 96, 128, 16, 32, 3, 32, 1, 'MAX', 'incept3a', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept3a'] = net
    net = network.inception(net, 256, 1, 64, 96, 128, 32, 64, 3, 64, 1, 'MAX', 'incept3b', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept3b'] = net
    net = network.inception(net, 320, 2, 0, 128, 256, 32, 64, 3, 0, 2, 'MAX', 'incept3c', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept3c'] = net
    
    net = network.inception(net, 640, 1, 256, 96, 192, 32, 64, 3, 128, 1, 'MAX', 'incept4a', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept4a'] = net
    net = network.inception(net, 640, 1, 224, 112, 224, 32, 64, 3, 128, 1, 'MAX', 'incept4b', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept4b'] = net
    net = network.inception(net, 640, 1, 192, 128, 256, 32, 64, 3, 128, 1, 'MAX', 'incept4c', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept4c'] = net
    net = network.inception(net, 640, 1, 160, 144, 288, 32, 64, 3, 128, 1, 'MAX', 'incept4d', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept4d'] = net
    net = network.inception(net, 640, 2, 0, 160, 256, 64, 128, 3, 0, 2, 'MAX', 'incept4e', phase_train=phase_train, use_batch_norm=True)
    endpoints['incept4e'] = net
    
    net = network.inception(net, 1024, 1, 384, 192, 384, 0, 0, 3, 128, 1, 'MAX', 'incept5a', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept5a'] = net
    net = network.inception(net, 896, 1, 384, 192, 384, 0, 0, 3, 128, 1, 'MAX', 'incept5b', phase_train=phase_train, use_batch_norm=True, weight_decay=weight_decay)
    endpoints['incept5b'] = net
    net = network.apool(net,  3, 3, 1, 1, 'VALID', 'pool6')
    endpoints['pool6'] = net
    net = tf.reshape(net, [-1, 896])
    endpoints['prelogits'] = net
    net = tf.nn.dropout(net, keep_probability)
    endpoints['dropout'] = net
    
    return net, endpoints
