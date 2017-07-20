
# coding: utf-8

import os
import numpy as np
import tensorflow as tf
import input_data
import model

#%%

N_CLASSES = 3
IMG_W = 208
IMG_H = 208
BATCH_SIZE = 16
CAPACITY = 2000
MAX_STEP = 10000 
learning_rate = 0.0001
removeLogFIle =True

#%%
def run_training():
    
    #train set path
    train_dir = '/raidHDD/experimentData/Dev/Knife/hackthon/upup7/'
	#output model path
    logs_train_dir = '/raidHDD/experimentData/Dev/Knife/hackthon/modelX'
    if removeLogFIle:
        if os.path.exists(logs_train_dir):
            for logFile in os.listdir(logs_train_dir):
                os.remove("{0}/{1}".format(logs_train_dir,logFile))
            print("Delete Log file success...")
    train, train_label = input_data.get_files(train_dir)
    
    train_batch, train_label_batch = input_data.get_batch(train,
                                                          train_label,
                                                          IMG_W,
                                                          IMG_H,
                                                          BATCH_SIZE, 
                                                          CAPACITY)      
    train_logits = model.inference(train_batch, BATCH_SIZE, N_CLASSES)
    train_loss = model.losses(train_logits, train_label_batch)        
    train_op = model.trainning(train_loss, learning_rate)
    train__acc = model.evaluation(train_logits, train_label_batch)
       
    summary_op = tf.summary.merge_all()
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.8  #0.8 =GPU_memory usage
    sess = tf.Session(config=config)
    train_writer = tf.summary.FileWriter(logs_train_dir, sess.graph)
    saver = tf.train.Saver()
    
    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    
    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                    break
            _, tra_loss, tra_acc = sess.run([train_op, train_loss, train__acc])
               
            if step % 50 == 0:
                print('Step %d, train loss = %.2f, train accuracy = %.2f%%' %(step, tra_loss, tra_acc*100.0))
                summary_str = sess.run(summary_op)
                train_writer.add_summary(summary_str, step)
                train_writer.flush()
            #only save end model
            if (step + 1) == MAX_STEP:
                checkpoint_path = os.path.join(logs_train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=step)
                
    except tf.errors.OutOfRangeError:
        print('Done training -- epoch limit reached')
    finally:
        coord.request_stop()
        
    coord.join(threads)
    sess.close()
    

run_training()



