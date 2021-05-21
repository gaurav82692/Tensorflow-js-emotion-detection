import os
from flask import Flask, request, render_template, send_from_directory, redirect,url_for, Response
import cv2

from PIL import Image, ImageOps
import numpy as np


np.set_printoptions(suppress=True)

app = Flask(__name__)
#run_with_ngrok(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/org')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
 

    # Replace this with the path to your image
    text="Rust detected"
    folder='static/org'
    ex=folder+'/'+filename
    #image = Image.open(ex)
    img=cv2.imread(ex)
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,70,70])
    upper_red = np.array([20,200,150])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    lower_red = np.array([170,70,70])
    upper_red = np.array([180,200,150])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    mask = mask0+mask1
    al = cv2.bitwise_and(img,img,mask=mask)
    dst = cv2.addWeighted(img,0,al,0.9,0)
    cv2.imwrite("static/res/"+ str(ex.split("/")[-1].split(".")[0])+'_rgb.jpg',dst)
    #rgb_img = Image.fromarray(al,'RGB')
    #rgb_img.save("static/"+ str(ex.split("/")[-1].split(".")[0])+'_rgb.jpg')
    filename =str(ex.split("/")[-1].split(".")[0])+'_rgb.jpg'
    
    #cv2_imshow(img)
    
    return render_template("complete_display_image.html",image_name=filename,image_org=ex)

    
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/res", filename)

@app.route('/<filename>')
def send_image_static(filename):
    return send_from_directory("static/org", filename)

@app.route('/go back')
def back():
    return redirect("http://codebugged.com/", code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=2222,debug=True)