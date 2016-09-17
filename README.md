# classifyME
ClassifyME is an Automatic Image Classification Engine being developed for low power (Raspberry Pi like) computing devices. A master-slave configuration testbed is in active development. Here is the gist of what we are trying to do.

Capture a picture (Using a camera module) in master node (read Raspberry Pi 3). The image is sent to a server (slave node) for image classification. A classifier is trained on the ImageNet dataset using Caffe and the trained model is used to make classifications.

At present, whenever we take a picture in the master node, a script automatically grabs the picture and sends it over to the slave node for the heavylifting. An automated script in the slave node fetch the image and sends it through the deep-learning pipeline. The predicted labels are sent back to the master node and is presented back.

A GUI is in active development. Also, the automation scripts are being looked into as well. There are good scope for improvement (this is just a bare skeleton now) and we love to have collaborations.

### Basic Usage

1. Clone the repo in both master and slave node.
2. In Slave-node (Server with Caffe) run:

        tmux new -d -s auto 'sh classifyME/src/automateClassification.sh' \; attach

NOTE: To detach from the `tmux` session, press `Ctrl+B` and then press `D` to detach. To attach back into the `tmux` session, type `tmux a -t auto`

3. Once the automation scripts are up and running, to take a picture and start the pipeline, just run (in Master node):

        python /path/to/classifyME/classifyME.py

Please raise an issue if the code breaks. It is a very simple and straight forward idea now, not much development put into it at all. I am doing this project to get us aquainted with Computer Vision and automation.
