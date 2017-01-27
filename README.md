# FaceNet implementation in Tensorflow
This is a TensorFlow implementation of the face recognizer described in the paper
["FaceNet: A Unified Embedding for Face Recognition and Clustering"](http://arxiv.org/abs/1503.03832). The project also uses ideas from the paper ["A Discriminative Feature Learning Approach for Deep Face Recognition"](http://ydwen.github.io/papers/WenECCV16.pdf) as well as the paper ["Deep Face Recognition"](http://www.robots.ox.ac.uk/~vgg/publications/2015/Parkhi15/parkhi15.pdf) from the [Visual Geometry Group](http://www.robots.ox.ac.uk/~vgg/) at Oxford.

## Tensorflow release
Currently this repo is compatible with Tensorflow r0.12.

## Notes
**2017-01-27: Added a model trained on a subset of the MS-Celeb-1M dataset. The LFW accuracy of this model is around 0.994.<br>
2017-01-02: Updated to code to run with Tensorflow r0.12. Not sure if it runs with older versions of Tensorflow though.**

## Pre-trained models
| Model name      | LFW accuracy | Training dataset |
|-----------------|--------------|------------------|
| [20170127-100647]() | 0.986        | CASIA-WebFace    |
| [20170125-122324](https://drive.google.com/file/d/0B5MzpY9kBtDVZEV3QmVmeGpSVWc/view?usp=sharing) | 0.994        | MS-Celeb-1M      |

## Inspiration
The code is heavly inspired by the [OpenFace](https://github.com/cmusatyalab/openface) implementation.

## Training data
The [CASIA-WebFace](http://www.cbsr.ia.ac.cn/english/CASIA-WebFace-Database.html) dataset has been used for training. This training set consists of total of 453 453 images over 10 575 identities after face detection. Some performance improvement has been seen if the dataset has been filtered before training. Some more information about how this was done will come later.
The best performing model has been trained on a subset of the [MS-Celeb-1M](https://www.microsoft.com/en-us/research/project/ms-celeb-1m-challenge-recognizing-one-million-celebrities-real-world/) dataset. This dataset is significantly larger but also contains significantly more label noise, and therefore it is crucial to apply dataset filtering on this dataset.


## Pre-processing

### Face alignment using MTCNN
One problem with the above approach seems to be that the Dlib face detector misses some of the hard examples (partial occlusion, siluettes, etc). This makes the training set to "easy" which causes the model to perform worse on other benchmarks.
To solve this, other face landmark detectors has been tested. One face landmark detector that has proven to work very well in this setting is the
[Multi-task CNN](https://kpzhang93.github.io/MTCNN_face_detection_alignment/index.html). A Matlab/Caffe implementation can be found [here](https://github.com/kpzhang93/MTCNN_face_detection_alignment) and this has been used for face alignment with very good results. Experimental code that has been used to align the training datasets can be found [here](https://github.com/davidsandberg/facenet/blob/master/tmp/align_dataset.m). However, work is ongoing to reimplement MTCNN face alignment in Python/Tensorflow. Currently some work still remains on this but the implementation can be found [here](https://github.com/davidsandberg/facenet/tree/master/src/align).

## Running training
Currently, the best results are achieved by training the model as a classifier with the addition of [Center loss](http://ydwen.github.io/papers/WenECCV16.pdf). Details on how to train a model as a classifier can be found on the page [Classifier training of Inception-ResNet-v1](https://github.com/davidsandberg/facenet/wiki/Classifier-training-of-inception-resnet-v1).

## Pre-trained model
### Inception-ResNet-v1 model
Currently, the best performing model is an Inception-Resnet-v1 model trained on CASIA-Webface aligned with [MTCNN](https://github.com/davidsandberg/facenet/blob/master/tmp/align_dataset.m). This alignment step requires Matlab and Caffe installed which requires some extra work. This will be easier when the [Python/Tensorflow implementation](https://github.com/davidsandberg/facenet/tree/master/src/align) is fully functional.

## Performance
The accuracy on LFW for the model [20161116-234200](https://drive.google.com/file/d/0B5MzpY9kBtDVSTgxX25ZQzNTMGc/view?usp=sharing) is 0.980+-0.006. A description of how to run the test can be found on the page [Validate on LFW](https://github.com/davidsandberg/facenet/wiki/Validate-on-lfw).
