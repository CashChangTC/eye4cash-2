
#%%

import tensorflow as tf
import numpy as np
import os

#

def get_files(file_dir):
    '''
    Args:
        file_dir: file directory
    Returns:
        list of images and labels
    '''

    coin_1c = []
    label_1c = []
    coin_10c = []
    label_10c = []
    coin_25c = []
    label_25c = []
    for folder in os.listdir(file_dir):
        folderPath = "{0}/{1}/".format(file_dir,folder)
        for file in os.listdir(folderPath):
            if folder=='1c':
                coin_1c.append(folderPath + file)
                label_1c.append(0)
            if folder=='10c':
                coin_10c.append(folderPath + file)
                label_10c.append(1)
            if folder=='25c':
                coin_25c.append(folderPath + file)
                label_25c.append(2)

    print('There are %d $1Cent\nThere are %d $10Cent\nThere are %d $25Cent' %(len(coin_1c), len(coin_10c), len(coin_25c)))
    
    image_list=np.hstack((coin_1c, coin_10c, coin_25c))
    label_list=np.hstack((label_1c, label_10c, label_25c,))
    
    temp = np.array([image_list, label_list])
    temp = temp.transpose()
    np.random.shuffle(temp)
    
    image_list = list(temp[:, 0])
    label_list = list(temp[:, 1])
    label_list = [int(i) for i in label_list]
    
    
    return image_list, label_list

	#%%

def get_batch(image, label, image_W, image_H, batch_size, capacity):
    '''
    Args:
        image: list type
        label: list type
        image_W: image width
        image_H: image height
        batch_size: batch size
        capacity: the maximum elements in queue
    Returns:
        image_batch: 4D tensor [batch_size, width, height, 3], dtype=tf.float32
        label_batch: 1D tensor [batch_size], dtype=tf.int32
    '''
    
    image = tf.cast(image, tf.string)
    label = tf.cast(label, tf.int32)

    # make an input queue
    input_queue = tf.train.slice_input_producer([image, label])
    
    label = input_queue[1]
    image_contents = tf.read_file(input_queue[0])
    image = tf.image.decode_jpeg(image_contents, channels=3)
    
    ######################################
    # data argumentation should go to here
    ######################################
    
    image = tf.image.resize_image_with_crop_or_pad(image, image_H, image_W)
    
    image = tf.image.per_image_standardization(image)
    
    image_batch, label_batch = tf.train.batch([image, label],
                                                batch_size= batch_size,
                                                num_threads= 64, 
                                                capacity = capacity)
    
    #you can also use shuffle_batch 
    image_batch, label_batch = tf.train.shuffle_batch([image,label],
                                                      batch_size=batch_size,
                                                      num_threads=64,
                                                      capacity=capacity,
                                                      min_after_dequeue=capacity-1)
    
    label_batch = tf.reshape(label_batch, [batch_size])
    image_batch = tf.cast(image_batch, tf.float32)
    
    return image_batch, label_batch

