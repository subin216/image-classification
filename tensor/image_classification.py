# python3 image_classification.py

# Image Classification with Inception-v3 model
# adapted from https://www.tensorflow.org/api_docs/python/tf/keras/applications/InceptionV3
# adapted from https://www.tensorflow.org/tutorials/images/transfer_learning

# import necessary libraries
import numpy as np
import os
import sys
import re
import tensorflow.compat.v1 as tf

# There are 3 files in model/imagenet for Inception-v3 model
# downloaded from 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
# (1) classify_image_graph_def.pb: model's graph file
# (2) imagenet_2012_challenge_label_map_proto.pbtxt: imagenet_synset file
#     ex) entry { target_class: 823, target_class_string: "n07932039" }
# (3) imagenet_synset_to_human_label_map.txt: mapping file to make imagenet_synset human readable
#      ex) n14899328 culture medium, medium

# decide how many guess will be shown
num_guess = 10
# set the path to download Inception-v3 
result_dir = 'model/imagenet'


# create graph from saved graph_def.pb
def create_graph():
  with tf.gfile.FastGFile(os.path.join(result_dir, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')


# guess image to classify
def guess_image(image):
  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()

  create_graph()

  with tf.Session() as session:
    # put image file into graph and run softmax tensor
    # softmax:0 is the tensor does normalized prediction for 1000 labels
    softmax_tensor = session.graph.get_tensor_by_name('softmax:0')

    # DecodeJpeg/contents:0 is the tensor has image's JPEG encoding
    predictions = session.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)

    lookup = LookUp()

    top_results = predictions.argsort()[-num_guess:][::-1]
    for node_id in top_results:
      words = lookup.id_to_string(node_id)
      score = predictions[node_id]
      print('%s (accuracy score = %.6f)' % (words, score))



# convert node to humanreadable labels
# adapted from https://stackoverflow.com/questions/75891/algorithm-for-finding-similar-images
class LookUp(object):

  def __init__(self, synset_label_path=None, human_label_path=None):
    if not synset_label_path:
      synset_label_path = os.path.join(result_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not human_label_path:
      human_label_path = os.path.join(result_dir, 'imagenet_synset_to_human_label_map.txt')
    self.lookup = self.load(synset_label_path, human_label_path)

  def load(self, synset_label_path, human_label_path):
    # maps uid and human readable string on the data from human labels
    # n14899328 culture medium, medium -> humans[14899328] = culture medium, medium
    human_label_lines = tf.gfile.GFile(human_label_path).readlines()
    humans = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in human_label_lines:
      parsed = p.findall(line)
      uid = parsed[0]
      humans[uid] = parsed[2]

    # maps target class number and target class_string on the data from synset labels
    # entry { target_class: 823, target_class_string: "n07932039" } -> synsets[823] = 07932039
    synset_label_lines = tf.gfile.GFile(synset_label_path).readlines()
    synsets = {}
    for line in synset_label_lines:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        synsets[target_class] = target_class_string[1:-2]

    # humans[123] = apple, apples
    # synsets[555] = 123
    # result => synset_to_string[555] = apple, apples
    synset_to_string = {}
    for key, val in synsets.items():
      if val in humans:
        human_string = humans[val]
        synset_to_string[key] = human_string
    return synset_to_string

  def id_to_string(self, id):
    if id in self.lookup:
      return self.lookup[id]
    return ''


def main(args=None):
  # this image is from javascript front-end by user through spring server
  image = os.path.join('image.jpg')
  guess_image(image)


if __name__ == '__main__':
  tf.app.run()
