
# coding: utf-8

# In[1]:


from PIL import Image
import matplotlib.pyplot as plt
import input_data
import numpy as np
import os
import tensorflow as tf
import model

def get_test_image(filepath):
    '''Randomly pick one image from training data
    Return: ndarray
    '''
    if os.path.exists(filepath):
        img_dir = filepath
        print ("get image name = {0}".format(img_dir))
        image = Image.open(img_dir)
        image = image.resize([208, 208])
        image = np.array(image)
        return image
    else:
        raise FileExistsError()

def evaluate_one_image(filePath):
    '''Test one image against the saved models and parameters
    '''
    image_array = get_test_image(filePath)
    #print (image_array.shape)
    with tf.Graph().as_default():
        BATCH_SIZE = 1
        N_CLASSES = 3
        image = tf.cast(image_array, tf.float32)
        image = tf.image.per_image_standardization(image)
        image = tf.reshape(image, [1, 208, 208, 3])
        logit = model.inference(image, BATCH_SIZE, N_CLASSES)
        
        logit = tf.nn.softmax(logit)
        
        x = tf.placeholder(tf.float32, shape=[208, 208, 3])
        logs_train_dir = '/raidHDD/experimentData/Dev/Knife/hackthon/model1'
                       
        saver = tf.train.Saver()
        
        with tf.Session() as sess:

            ckpt = tf.train.get_checkpoint_state(logs_train_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                saver.restore(sess, "/raidHDD/experimentData/Dev/Knife/hackthon/model1/model.ckpt-9999")
                print("===>"+ckpt.model_checkpoint_path)
            else:
                print('No checkpoint file found')
            
            prediction = sess.run(logit, feed_dict={x: image_array})
            max_index = np.argmax(prediction)

            predClass = -1
            if max_index==0:
                print('This is a $1Cent USD with possibility %.6f' %prediction[:, 0])
                predClass = 0
            if max_index==1:
                print('This is a $10Cent USD with possibility %.6f' %prediction[:, 1])
                predClass = 1
            if max_index==2:
                print('This is a $25Cent USD with possibility %.6f' %prediction[:, 2])
                predClass = 2
            return predClass

