# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple image classification with Inception.

Run image classification with Inception trained on ImageNet 2012 Challenge data
set.

This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.

Change the --image_file argument to any jpg image to compute a
classification of that image.

Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.

https://tensorflow.org/tutorials/image_recognition/
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

def ClassifyImage(image):
    # _image is a path to image file provided from other script
    _image = image
    

    _animals = '''tench, Tinca tinca, goldfish, Carassius auratus, great white shark, white shark, man-eater, man-eating shark, Carcharodon, carcharias, 
                  hammerhead, hammerhead shark, electric ray, crampfish, numbfish, torpedo, stingray, cock, hen, ostrich, Struthio camelus,
                  brambling, Fringilla montifringilla, goldfinch, Carduelis carduelis, house finch, linnet, Carpodacus mexicanus,
                  junco, snowbird, indigo bunting, indigo finch, indigo bird, Passerina cyanea, robin, American robin, Turdus migratorius,
                  bulbul, jay, magpie, chickadee, water ouzel, dipper, kite, bald eagle, American eagle, Haliaeetus leucocephalus,
                  vulture, great grey owl, great gray owl, Strix nebulosa, European fire salamander, Salamandra salamandra, common newt, Triturus vulgaris,
                  eft, spotted salamander, Ambystoma maculatum, axolotl, mud puppy, Ambystoma mexicanum, bullfrog, Rana catesbeiana,
                  tree frog, tree-frog, tailed frog, bell toad, ribbed toad, tailed toad, Ascaphus trui, loggerhead, loggerhead turtle, Caretta caretta,
                  leatherback turtle, leatherback, leathery turtle, Dermochelys coriacea, mud turtle, terrapin, box turtle, box tortoise, banded gecko,
                  common iguana, iguana, Iguana iguana, American chameleon, anole, Anolis carolinensis, whiptail, whiptail lizard, agama,
                  frilled lizard, Chlamydosaurus kingi, alligator lizard, Gila monster, Heloderma suspectum, green lizard, Lacerta viridis,
                  African chameleon, Chamaeleo chamaeleon, Komodo dragon, Komodo lizard, dragon lizard, giant lizard, Varanus komodoensis,
                  African crocodile, Nile crocodile, Crocodylus niloticus, American alligator, Alligator mississipiensis, triceratops,
                  thunder snake, worm snake, Carphophis amoenus, ringneck snake, ring-necked snake, ring snake, hognose snake, puff adder, sand viper,
                  green snake, grass snake, king snake, kingsnake, garter snake, grass snake, water snake, vine snake, night snake, Hypsiglena torquata,
                  boa constrictor, Constrictor constrictor, rock python, rock snake, Python sebae, Indian cobra, Naja naja, green mamba, sea snake,
                  horned viper, cerastes, sand viper, horned asp, Cerastes cornutus, diamondback, diamondback rattlesnake, Crotalus adamanteus,
                  sidewinder, horned rattlesnake, Crotalus cerastes, trilobite, harvestman, daddy longlegs, Phalangium opilio, scorpion,
                  black and gold garden spider, Argiope aurantia, barn spider, Araneus cavaticus, garden spider, Aranea diademata,
                  black widow, Latrodectus mactans, tarantula, wolf spider, hunting spider, tick, centipede, black grouse, ptarmigan,
                  ruffed grouse, partridge, Bonasa umbellus, prairie chicken, prairie grouse, prairie fowl, peacock, quail, partridge,
                  African grey, African gray, Psittacus erithacus, macaw, sulphur-crested cockatoo, Kakatoe galerita, Cacatua galerita, lorikeet,
                  coucal, bee eater, hornbill, hummingbird, jacamar, toucan, drake, red-breasted merganser, Mergus serrator, goose, black swan, Cygnus atratus,
                  tusker, echidna, spiny anteater, anteater, platypus, duckbill, duckbilled platypus, duck-billed platypus, Ornithorhynchus anatinus,
                  wallaby, brush kangaroo, koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus, wombat, jellyfish, sea anemone, anemone, brain coral,
                  flatworm, platyhelminth, nematode, nematode worm, roundworm, conch, snail, slug, sea slug, nudibranch, chiton, coat-of-mail shell, sea cradle, polyplacophore,
                  chambered nautilus, pearly nautilus, nautilus, Dungeness crab, Cancer magister, rock crab, Cancer irroratus, fiddler crab,
                  king crab, Alaska crab, Alaskan king crab, Alaska king crab, Paralithodes camtschatica, American lobster, Northern lobster, Maine lobster, Homarus americanus,
                  spiny lobster, langouste, rock lobster, crawfish, crayfish, sea crawfish, crayfish, crawfish, crawdad, crawdaddy, hermit crab, isopod, white stork, Ciconia ciconia,
                  black stork, Ciconia nigra, spoonbill, flamingo, little blue heron, Egretta caerulea, American egret, great white heron, Egretta albus, bittern, crane,
                  limpkin, Aramus pictus, European gallinule, Porphyrio porphyrio, American coot, marsh hen, mud hen, water hen, Fulica americana, bustard, ruddy turnstone,
                  Arenaria interpres, red-backed sandpiper, dunlin, Erolia alpina, redshank, Tringa totanus, dowitcher, oystercatcher, oyster catcher, pelican, king penguin,
                  Aptenodytes patagonica, albatross, mollymawk, grey whale, gray whale, devilfish, Eschrichtius gibbosus, Eschrichtius robustus, killer whale, killer, orca,
                  grampus, sea wolf, Orcinus orca, dugong, Dugong dugon, sea lion, timber wolf, grey wolf, gray wolf, Canis lupus, white wolf, Arctic wolf,
                  Canis lupus tundrarum, red wolf, maned wolf, Canis rufus, Canis niger, coyote, prairie wolf, brush wolf, Canis latrans,
                  dingo, warrigal, warragal, Canis dingo, dhole, Cuon alpinus, African hunting dog, hyena dog, Cape hunting dog, Lycaon pictus,
                  hyena, hyaena, red fox, Vulpes vulpes, kit fox, Vulpes macrotis, Arctic fox, white fox, Alopex lagopus, grey fox, gray fox,
                  Urocyon cinereoargenteus, cougar, puma, catamount, mountain lion, painter, panther, Felis concolor,lynx, catamount, leopard,
                  Panthera pardus, snow leopard, ounce, Panthera uncia, jaguar, panther, Panthera onca, Felis onca,
                  lion, king of beasts, Panthera leo, tiger, Panthera tigris, cheetah, chetah, Acinonyx jubatus, brown bear, bruin, Ursus arctos,
                  American black bear, black bear, Ursus americanus, Euarctos americanus, ice bear, polar bear, Ursus Maritimus, Thalarctos maritimus,
                  sloth bear, Melursus ursinus, Ursus ursinus, mongoose, meerkat, mierkat, tiger beetle, ladybug, ladybeetle,
                  lady beetle, ladybird, ladybird beetle, ground beetle, carabid beetle, long-horned beetle, longicorn, longicorn beetle,
                  leaf beetle, chrysomelid, dung beetle, rhinoceros beetle, weevil, fly, bee, ant, emmet, pismire, grasshopper, hopper, cricket,
                  walking stick, walkingstick, stick insect, cockroach, roach, mantis, mantid, cicada, cicala, leafhopper, lacewing, lacewing fly,
                  dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk, damselfly,
                  admiral, ringlet, ringlet butterfly, monarch, monarch butterfly, milkweed butterfly, Danaus plexippus, cabbage butterfly,
                  sulphur butterfly, sulfur butterfly, lycaenid, lycaenid butterfly, starfish, sea star, sea urchin, sea cucumber, holothurian,
                  wood rabbit, cottontail, cottontail rabbit, hare, Angora, Angora rabbit, hamster, porcupine, hedgehog, fox squirrel,
                  eastern fox squirrel, Sciurus niger, marmot, beaver, guinea pig, Cavia cobaya, sorrel, zebra, hog, pig, grunter, squealer, Sus scrofa,
                  wild boar, boar, Sus scrofa, warthog, hippopotamus, hippo, river horse, Hippopotamus amphibius, ox, water buffalo, water ox, Asiatic buffalo,
                  Bubalus bubalis, bison, ram, tup, bighorn, bighorn sheep, cimarron, Rocky Mountain bighorn, Rocky Mountain sheep, Ovis canadensis,
                  ibex, Capra ibex, hartebeest, impala, Aepyceros melampus, gazelle, Arabian camel, dromedary, Camelus dromedarius, llama, weasel, mink,
                  polecat, fitch, foulmart, foumart, Mustela putorius, black-footed ferret, ferret, Mustela nigripes, otter, skunk, polecat, wood pussy,
                  badger, armadillo, three-toed sloth, ai, Bradypus tridactylus, orangutan, orang, orangutang, Pongo pygmaeus,
                  gorilla, Gorilla gorilla, chimpanzee, chimp, Pan troglodytes, gibbon, Hylobates lar, siamang, Hylobates syndactylus, Symphalangus syndactylus,
                  guenon, guenon monkey, patas, hussar monkey, Erythrocebus patas, baboon, macaque, langur, colobus, colobus monkey, proboscis monkey, Nasalis larvatus,
                  marmoset, capuchin, ringtail, Cebus capucinus, howler monkey, howler, titi, titi monkey, spider monkey, Ateles geoffroyi,
                  squirrel monkey, Saimiri sciureus, Madagascar cat, ring-tailed lemur, Lemur catta, indri, indris, Indri indri, Indri brevicaudatus,
                  Indian elephant, Elephas maximus, African elephant, Loxodonta africana, lesser panda, red panda, panda, bear cat, cat bear, Ailurus fulgens,
                  giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca, barracouta, snoek, eel, coho, cohoe, coho salmon, blue jack, silver salmon, Oncorhynchus kisutch,
                  rock beauty, Holocanthus tricolor, anemone fish, sturgeon, gar, garfish, garpike, billfish, Lepisosteus osseus, lionfish, puffer, pufferfish, blowfish, globefish'''

    _buildings = '''altar, bakery, bakeshop, bakehouse, barber chair, barbershop, barn,
                  beacon, lighthouse, beacon light, pharos, bell cote, bell cot, boathouse,
                  bookcase, bookshop, bookstore, bookstall, butcher shop, meat market, castle,
                  church, church building, cinema, movie theater, movie theatre, movie house, picture palace,
                  confectionery, confectionary, candy store, dock, dockage, docking facility,
                  dome, entertainment center, greenhouse, nursery, glasshouse,
                  grocery store, grocery, food market, market, home theater, home theatre,
                  lumbermill, sawmill, monastery, mosque, palace, patio, terrace,
                  prison, prison house, restaurant, eating house, eating place, eatery,
                  shoe shop, shoe-shop, shoe store, shoji, sliding door, stupa, tope,
                  thatch, thatched roof, tile roof, tobacco shop, tobacconist shop, tobacconist,
                  toyshop, triumphal arch, water tower, yurt'''


    FLAGS = None

    # pylint: disable=line-too-long
    DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
    # pylint: enable=line-too-long


    class NodeLookup(object):
      """Converts integer node ID's to human readable labels."""

      def __init__(self,
                   label_lookup_path=None,
                   uid_lookup_path=None):
        if not label_lookup_path:
          label_lookup_path = os.path.join(
              FLAGS.model_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
        if not uid_lookup_path:
          uid_lookup_path = os.path.join(
              FLAGS.model_dir, 'imagenet_synset_to_human_label_map.txt')
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

      def load(self, label_lookup_path, uid_lookup_path):
        """Loads a human readable English name for each softmax node.

        Args:
          label_lookup_path: string UID to integer node ID.
          uid_lookup_path: string UID to human-readable string.

        Returns:
          dict from integer node ID to human-readable string.
        """
        if not tf.gfile.Exists(uid_lookup_path):
          tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
          tf.logging.fatal('File does not exist %s', label_lookup_path)

        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
          parsed_items = p.findall(line)
          uid = parsed_items[0]
          human_string = parsed_items[2]
          uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
          if line.startswith('  target_class:'):
            target_class = int(line.split(': ')[1])
          if line.startswith('  target_class_string:'):
            target_class_string = line.split(': ')[1]
            node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
          if val not in uid_to_human:
            tf.logging.fatal('Failed to locate: %s', val)
          
          name = uid_to_human[val]
          if name in _buildings:
              name = 'building'
          node_id_to_name[key] = name

        return node_id_to_name

      def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
          return ''
        return self.node_lookup[node_id]


    def create_graph():
      """Creates a graph from saved GraphDef file and returns a saver."""
      # Creates graph from saved graph_def.pb.
      with tf.gfile.FastGFile(os.path.join(
          FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


    def run_inference_on_image(image):
      """Runs inference on an image.

      Args:
        image: Image file name.

      Returns:
        Five predictions
      """
      
      if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image)
      image_data = tf.gfile.FastGFile(image, 'rb').read()

      # Creates graph from saved GraphDef.
      create_graph()
      with tf.Session() as sess:
        # Some useful tensors:
        # 'softmax:0': A tensor containing the normalized prediction across
        #   1000 labels.
        # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
        #   float description of the image.
        # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
        #   encoding of the image.
        # Runs the softmax tensor by feeding the image_data as input to the graph.
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
        # Creates node ID --> English string lookup.
        node_lookup = NodeLookup()

        top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
        imageTags = []

        for node_id in top_k:
          human_string = node_lookup.id_to_string(node_id)
          #score = predictions[node_id]
          imageTags.append(human_string)
          #print('%s (score = %.5f)' % (human_string, score))
          
        # Returns five predictions in a easily readable form
        return '\n'.join(imageTags)


    def maybe_download_and_extract():
      """Download and extract model tar file."""
      dest_directory = FLAGS.model_dir
      if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
      filename = DATA_URL.split('/')[-1]
      filepath = os.path.join(dest_directory, filename)
      if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
          sys.stdout.write('\r>> Downloading %s %.1f%%' % (
              filename, float(count * block_size) / float(total_size) * 100.0))
          sys.stdout.flush()
        filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
      tarfile.open(filepath, 'r:gz').extractall(dest_directory)

    def main():
      maybe_download_and_extract()
      result = run_inference_on_image(_image)
      # Returns five predictions in a easily readable form
      return result
      

    if __name__ == 'classify_image':
      parser = argparse.ArgumentParser()
      # classify_image_graph_def.pb:
      #   Binary representation of the GraphDef protocol buffer.
      # imagenet_synset_to_human_label_map.txt:
      #   Map from synset ID to a human readable string.
      # imagenet_2012_challenge_label_map_proto.pbtxt:
      #   Text representation of a protocol buffer mapping a label to synset ID.
      parser.add_argument(
          '--model_dir',
          type=str,
          default='/tmp/imagenet',
          #default=os.path.split(os.getcwd())[0] + '/imagenet/test',
          help="""\
          Path to classify_image_graph_def.pb,
          imagenet_synset_to_human_label_map.txt, and
          imagenet_2012_challenge_label_map_proto.pbtxt.\
          """
      )
      parser.add_argument(
          '--image_file',
          type=str,
          default='',
          help='Absolute path to image file.'
      )
      parser.add_argument(
          '--num_top_predictions',
          type=int,
          default=5,
          help='Display this many predictions.'
      )
      FLAGS, unparsed = parser.parse_known_args()
      
    return main()
    
