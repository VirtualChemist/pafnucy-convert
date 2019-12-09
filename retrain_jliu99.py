# before running this script clone Pafnucy's repository and create the environment:
# $ git clone https://gitlab.com/cheminfIBB/pafnucy
# $ cd pafnucy
# $ conda env create -f environment_gpu.yml


import numpy as np
import h5py
import tensorflow as tf
import csv

from tfbio.data import make_grid

# load Pafnucy
graph = tf.Graph()

with graph.as_default():
    saver = tf.train.import_meta_graph('results/batch5-2017-06-05T07:58:47-best.meta')

# get placeholders for input, prediction and target
x = graph.get_tensor_by_name('input/structure:0')
y = graph.get_tensor_by_name('output/prediction:0')
t = graph.get_tensor_by_name('input/affinity:0')

keep_prob = graph.get_tensor_by_name('fully_connected/keep_prob:0')

# BEGIN ADDING CODE -------------------------------------------------------------
#tvars = tf.trainable_variables()
to_run = ['fully_connected/fc0/w:0', 
            'fully_connected/fc0/b:0', 
            'fully_connected/fc1/w:0',
            'fully_connected/fc1/b:0',
            'fully_connected/fc2/w:0',
            'fully_connected/fc2/b:0',
            'output/w:0',
            'output/b:0']
optimizer = tf.train.AdamOptimizer(learning_rate, name='optimizer')
train = optimizer.minimize(cost, var_list=to_run, global_step=global_step,
                                       name='train')
# END ADDING CODE ---------------------------------------------------------------

#train = graph.get_tensor_by_name('training/train:0')


# load some data
x_ = []
y_ = []
used = []
with h5py.File('/home/jspayd/smiles-convert/our_train.hdf', 'r') as f:
    with open('/home/jspayd/smiles-convert/affinities.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)[1:]
        for name, _ in rows:
            if name in f and name not in used:
                used.append(name)
                coords = (f[name][:, :3])
                features = (f[name][:, 3:])
                grid = make_grid(coords, features)
                x_.append(grid)
                y_.append(f[name].attrs['affinity'].mean())

x_ = np.vstack(x_)
y_ = np.reshape(y_, (-1, 1))
print('target values:', y_)

# re-train Pafnucy
with tf.Session(graph=graph) as session:
    saver.restore(session, 'results/batch5-2017-06-05T07:58:47-best')
    print('predictions before training:',
          session.run(y, feed_dict={x: x_, keep_prob: 1.0}))

    to_stop =[
        graph.get_tensor_by_name('convolution/conv0/w/optimizer:0'),
        graph.get_tensor_by_name('convolution/conv1/w/optimizer:0'),
        graph.get_tensor_by_name('convolution/conv2/w/optimizer:0'),
        #graph.get_tensor_by_name('fully_connected/fc0/w/optimizer:0'),
        #graph.get_tensor_by_name('fully_connected/fc1/w/optimizer:0'),
        #graph.get_tensor_by_name('fully_connected/fc2/w/optimizer:0'),
    ]
    feed_dict = {x: x_, t: y_, keep_prob: 1.0}
    for tensor in to_stop:
        feed_dict[tensor] = tf.stop_gradient(tensor)
    for _ in range(15):
        session.run(train, feed_dict=feed_dict)
    print('predictions after training:',
          session.run(y, feed_dict={x: x_, keep_prob: 1.0}))
    saver.save(session, 'pafnucy_retrained4')

# load and use the new model
new_graph = tf.Graph()

with new_graph.as_default():
    saver = tf.train.import_meta_graph('pafnucy_retrained4.meta')

x = new_graph.get_tensor_by_name('input/structure:0')
y = new_graph.get_tensor_by_name('output/prediction:0')
keep_prob = new_graph.get_tensor_by_name('fully_connected/keep_prob:0')

with tf.Session(graph=new_graph) as session:
    saver.restore(session, 'pafnucy_retrained4')
    print('predictions with loaded model:',
          session.run(y, feed_dict={x: x_, keep_prob: 1.0}))
