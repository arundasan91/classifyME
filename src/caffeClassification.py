import numpy as np
import sys, os, caffe,time

# Log time to find total time taken to classify the image
startTime=time.time()

# Set current directory to currDir
currDir = os.getcwd()

# Change to src/temp/ directory
os.chdir("/home/cc/classifyME/src/temp/")
os.system("rm output_label_classifyME.txt")

# Define Caffe root and start classification
caffe_root = '/home/cc/caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')

caffe.set_mode_cpu()

# For testing purposes, use:    python caffeClassification.py image.jpg
try:
    sys.argv[1]
except IndexError:
    arg = False
else:
    arg = True

if arg == True:
    image_input = sys.argv[1]
else:
    image_input = '/home/cc/imagesFromRpi/new_image.jpg'

# Print the file name and continue classification
print "Input image file name ", image_input

model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)
# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(50,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # image size is 227x227

# copy the image data into the memory allocated for the net
image = caffe.io.load_image(image_input)
#print image

transformed_image = transformer.preprocess('data', image)
net.blobs['data'].data[...] = transformed_image

# perform classification
output = net.forward()

output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

# print 'predicted class is:', output_prob.argmax()

# load ImageNet labels
labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'

labels = np.loadtxt(labels_file, str, delimiter='\t')

output_label = labels[output_prob.argmax()]
output_label_only = output_label[10:]
print 'output label:', output_label
print 'output label only', output_label_only

# sort top five predictions from softmax output
#top_inds = output_prob.argsort()[::-1][:5]  # reverse sort and take five largest items
#print 'probabilities and labels:'
#out = zip(output_prob[top_inds], labels[top_inds])
#print out

#currDir = os.getcwd()
#os.chdir(currDir+'/temp/')
fileBacktoRpi = open("output_label_classifyME.txt", "w+")
fileBacktoRpi.write(str(output_label_only))
fileBacktoRpi.close()

# SCP the predicted label to the IOT device
os.system('scp output_label_classifyME.txt das@das-pi:/home/das/classifyME/src/temp/output_label_classifyME.txt')

# Log and print the time taken to classify and send the image.
endTime = time.time()
print "It took ", endTime-startTime, " seconds to classify the image"
