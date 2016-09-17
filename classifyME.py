#!/usr/bin/env python

#One Window, working snippet. Possible base to work on.
import Tkinter as tk
from Tkinter import *
import PIL,cv2,os,time,os.path
from PIL import Image, ImageTk
import tkFont
import tkMessageBox

#Log local time
currTime = time.strftime("%Y%m%d-%H%M%S")

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("classifyME - Automatic Image Classification Engine")
window.config(background="#FFFFFF")
#Custom Font
customFont = tkFont.Font(family="Helvetica", size=12)

#Graphics window
imageFrame = tk.Frame(window, relief=RAISED, width=640, height=480)
imageFrame.grid(row=0, column=0, padx=5, pady=5)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(3, show_frame) 

def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = cap.read()
    return im

def take_photo():
    # Show photo captured label
    lab = tk.Label(sliderFrame, text = 'Photo Captured')
    lab.pack(fill="both", expand="yes", padx=10, pady=10)
    ramp_frames = 30
    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    for i in range(ramp_frames):
     temp = get_image()
    # Take the actual image we want to keep
    camera_capture = get_image()
    # Define file where image is to be saved
    file = "/home/das/classifyME/cameraImages/new_image.jpg"
    # Write the image to file.
    cv2.imwrite(file, camera_capture)
    print("Taking image...")
    # Rename and archive the image.
    os.chdir("/home/das/classifyME/cameraImages/")
    print "Moving Captured Image to Server......."
    # Move the image to the server for computation
    os.system('scp new_image.jpg cc@arun-master:/home/cc/imagesFromRpi/')
    print "File Sent"
    newFileName="image_" + currTime + ".jpg"
    os.rename("new_image.jpg", newFileName)
    os.system("mv "+ newFileName + " processedPictures/" + newFileName)
    print "Processed File Moved to " + "/home/das/classifyME/cameraImages/processedPictures/"
    lab.pack_forget()
    # Show the prediction
    show_pred()
    # Show button 1 again
    button1.pack(side="bottom", fill="both", expand="yes", padx=5, pady=5)
    
def browse_photo():
    file = ""
    print("Browse photos, under construction")

def show_pred():
    # Remove the old predicted labels
    os.system('rm /home/das/classifyME/src/temp/output_label_classifyME.txt')
    # Remove button1 until message box is closed
    button1.pack_forget()
    print("Please wait while the image is classified")
    
    # Check continuously for the predicted label file and fetch it whenever it arrives.
    wait_time_start=time.time()
    noLabel=True
    while noLabel:
        try:
            if os.path.isfile("/home/das/classifyME/src/temp/output_label_classifyME.txt"):
                predFile = open("/home/das/classifyME/src/temp/output_label_classifyME.txt", "r+")
                noLabel=False
            wait_time_end = time.time()
            if ((wait_time_end - wait_time_start > 6) & (os.path.isfile("/home/das/classifyME/src/temp/output_label_classifyME.txt") == False)):
                os.system('scp cc@129.114.111.53:/home/cc/classifyME/src/temp/output_label_classifyME.txt /home/das/classifyME/src/temp/output_label_classifyME.txt')
                predFile = open("/home/das/classifyME/src/temp/output_label_classifyME.txt", "r+")
                noLabel=False
        except IOError:
            pass
        time.sleep(1)
    # Read the predicted label file
    pred = predFile.read(50)
    #print "Image Classification Complete\nPredicted Label is " + pred 
    #prediction = tk.Label(sliderFrame, text = pred, font = customFont)
    #prediction.pack(side="bottom",fill="both",expand="yes",padx=5, pady=5)
    # Printing the predicted label
    out_Pred = "Predicted label is " + pred
    tkMessageBox.showinfo(message= out_Pred)

#Slider window (slider controls stage position)
sliderFrame = tk.Frame(window, width=640, height=100)
sliderFrame.grid(row = 640, column=0, padx=5, pady=5)

# Button to take photo inside GUI
button1 = Button(sliderFrame, text = 'Take Photo', command = take_photo)
button1.pack(side="bottom", fill="both", expand="yes", padx=5, pady=5)

# Browse capability to select images: to be added in V2
#button2 = Button(sliderFrame, text = 'Browse Photo', command = browse_photo)
#button2.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

show_frame()  #Display
window.mainloop()  #Starts GUI
cap.release()  #Stop Camera

"""
def movePic():
    os.chdir("/home/das/classifyME/cameraImages/")
    print "Moving Captured Image to Server......."
    os.system('scp new_image.jpg cc@arun-master:/home/cc/imagesFromRpi/')
    print "File Sent"
    newFileName="image_" + currTime + ".jpg"
    os.rename("new_image.jpg", newFileName)
    os.system("mv "+ newFileName + " processedPictures/" + newFileName)
    print "Processed File Moved to " + "/home/das/classifyME/cameraImages/processedPictures/"
"""
