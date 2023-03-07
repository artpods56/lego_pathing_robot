import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.datasets import mnist



tf.logging.set_verbosity(tf.logging.ERROR)

data = mnist.train.images
labels = np.asarray(mnist.train.labels, dtype=np.int32)
test_data = mnist.test.images
test_labels = np.asarray(mnist.test.labels, dtype=np.int32)

max_examples = 10000
data = data[:max_examples]
labels = labels[:max_examples]

def display(i):
	img = test_data[i]
	plt.title('label : {}'.format(test_labels[i]))
	plt.imshow(img.reshape((28, 28)))
	
# image in TensorFlow is 28 by 28 px
display(0)
