from flask import Flask,jsonify, render_template, send_file, request
from werkzeug.utils import secure_filename
import cv2
import os
import base64
import json
from PIL import Image
import PIL
import io
import os
import glob

app = Flask(__name__, template_folder='../templates')

model_face = os.path.join(os.path.dirname(__file__), './models/haarcascade_frontalface_alt2.xml')
model_esc = os.path.join(os.path.dirname(__file__), './models/cascade_escritorio.xml')
model_monitor = os.path.join(os.path.dirname(__file__), './models/cascade_monitor.xml')
model_laptop = os.path.join(os.path.dirname(__file__), './models/cascade_laptop.xml')
model_silla = os.path.join(os.path.dirname(__file__), './models/cascade_silla.xml')

#funcion identificar objetos
def generate():
    file_name = os.path.join(os.path.dirname(__file__), './images/foto1.jpg')
    #assert os.path.exists(file_name)
    img = cv2.imread(file_name)
    #img = cv2.imread('.app/images/foto4.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     
    face_cascade = cv2.CascadeClassifier(model_face)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    i=0
    for (x, y, w, h) in faces:
        cv2.rectangle(img,(x, y),(x+w, y+h),(0, 0, 255), 2) 
        cv2.putText(img,'Rostro'+str(i+1), (x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
        faces = img[y:y + h, x:x + w]
        #cv2.imshow("face",faces) 
        i=i+1
        cv2.imwrite('./app/resultado/rostro'+str(i)+'.jpg', faces) 
    
    #modelMonitors
    monitor_cascade = cv2.CascadeClassifier(model_monitor)
    monitors = monitor_cascade.detectMultiScale(gray, 1.1, 4)
    i=0
    for (x, y, w, h) in monitors:
        cv2.rectangle(img,(x, y),(x+w, y+h),(0, 0, 255), 2) 
        cv2.putText(img,'Monitor'+str(i), (x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
        monitors = img[y:y + h, x:x + w]
        i=i+1
        cv2.imwrite('./app/resultado/monitor'+str(i)+'.jpg', monitors) 
    
    #modelEscritorio
    esc_cascade = cv2.CascadeClassifier(model_esc)
    escritorio = esc_cascade.detectMultiScale(gray, 1.1, 4)
    i=0
    for (x, y, w, h) in escritorio:
        cv2.rectangle(img,(x, y),(x+w, y+h),(0, 0, 255), 2) 
        cv2.putText(img,'Escritorio'+str(i), (x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
        escritorio = img[y:y + h, x:x + w]
        i=i+1
        cv2.imwrite('./app/resultado/escritorio'+str(i)+'.jpg', escritorio)
    
    #modelLaptop
    laptop_cascade = cv2.CascadeClassifier(model_laptop)
    laptop = laptop_cascade.detectMultiScale(gray, 1.1, 4)
    i=0
    for (x, y, w, h) in laptop:
        cv2.rectangle(img,(x, y),(x+w, y+h),(0, 0, 255), 2) 
        cv2.putText(img,'Laptop'+str(i), (x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
        laptop = img[y:y + h, x:x + w]
        i=i+1
        cv2.imwrite('./app/resultado/laptop'+str(i)+'.jpg', laptop)
    
    #modelSilla
    silla_cascade = cv2.CascadeClassifier(model_silla)
    silla = silla_cascade.detectMultiScale(gray, 1.1, 4)
    i=0
    for (x, y, w, h) in silla:
        cv2.rectangle(img,(x, y),(x+w, y+h),(0, 0, 255), 2) 
        cv2.putText(img,'Silla'+str(i), (x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)
        silla = img[y:y + h, x:x + w]
        i=i+1
        cv2.imwrite('./app/resultado/silla'+str(i)+'.jpg', silla)

    cv2.imwrite('./app/resultado/detected.jpg', img)
    #cv2.imshow('img', img)
    cv2.waitKey()

    return 'Archivo procesado!!'

@app.route('/get_image',methods=['GET'])
def get_image():
    #if request.args.get('type') == '1':
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/detected.jpg')):
       filename = './resultado/detected.jpg'
    else:
       filename = './images/foto1.jpg'
    return send_file(filename, mimetype='image/jpg')

#api get generate
@app.route('/images',methods=['GET'])
def get_data():
    return jsonify(generate())  #llama la funcion

#api get index page ok
@app.route('/')
def index():   
    data = {}
    data['objetos'] = []
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/rostro1.jpg')): #si existe ver
        img1 = os.path.join(os.path.dirname(__file__), './resultado/rostro1.jpg')
        with open(img1, mode='rb') as file:
            img1 = file.read()
        obj1 = base64.encodebytes(img1).decode('utf-8')
        json_data = {"name":'rostro 1',"image":obj1}
        data['objetos'].append(json_data)
    
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/rostro2.jpg')): #si existe ver
        img2 = os.path.join(os.path.dirname(__file__), './resultado/rostro2.jpg')
        with open(img2, mode='rb') as file:
            img2 = file.read()
        obj2 = base64.encodebytes(img2).decode('utf-8')
        json_data = {"name":'Rostro 2',"image":obj2}
        data['objetos'].append(json_data)
    
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/rostro3.jpg')): #si existe ver
        img2 = os.path.join(os.path.dirname(__file__), './resultado/rostro3.jpg')
        with open(img2, mode='rb') as file:
            img2 = file.read()
        obj2 = base64.encodebytes(img2).decode('utf-8')
        json_data = {"name":'Rostro 3',"image":obj2}
        data['objetos'].append(json_data)
    
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/rostro4.jpg')): #si existe ver
        img2 = os.path.join(os.path.dirname(__file__), './resultado/rostro4.jpg')
        with open(img2, mode='rb') as file:
            img2 = file.read()
        obj2 = base64.encodebytes(img2).decode('utf-8')
        json_data = {"name":'Rostro 4',"image":obj2}
        data['objetos'].append(json_data)

    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/monitor1.jpg')): #si existe ver
        img2 = os.path.join(os.path.dirname(__file__), './resultado/monitor1.jpg')
        with open(img2, mode='rb') as file:
            img2 = file.read()
        obj2 = base64.encodebytes(img2).decode('utf-8')
        json_data = {"name":'Monitor 1',"image":obj2}
        data['objetos'].append(json_data)
    
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/escritorio1.jpg')): #si existe ver
        img2 = os.path.join(os.path.dirname(__file__), './resultado/escritorio1.jpg')
        with open(img2, mode='rb') as file:
            img2 = file.read()
        obj2 = base64.encodebytes(img2).decode('utf-8')
        json_data = {"name":'Escritorio 1',"image":obj2}
        data['objetos'].append(json_data)
    
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/laptop1.jpg')): #si existe ver
        img2 = os.path.join(os.path.dirname(__file__), './resultado/laptop1.jpg')
        with open(img2, mode='rb') as file:
            img2 = file.read()
        obj2 = base64.encodebytes(img2).decode('utf-8')
        json_data = {"name":'Laptop 1',"image":obj2}
        data['objetos'].append(json_data)
    
    if os.path.exists(os.path.join(os.path.dirname(__file__), './resultado/silla1.jpg')): #si existe ver
        img2 = os.path.join(os.path.dirname(__file__), './resultado/silla1.jpg')
        with open(img2, mode='rb') as file:
            img2 = file.read()
        obj2 = base64.encodebytes(img2).decode('utf-8')
        json_data = {"name":'Silla 1',"image":obj2}
        data['objetos'].append(json_data)

    #data = json.loads(data)
    #print(data) 
    return render_template('index.html', data=data['objetos'])

#api post image ok
@app.route('/send_image', methods=['POST'])
def send_image(): 
    if request.method == 'POST':
      f = request.files['file']
      f.filename = "foto1.jpg"  #rename file
      file = secure_filename(f.filename)
      f.save(os.path.join(os.path.dirname(__file__), './images/'+file))  #save file in app file
      return 'ARCHIVO CARGADO !!'

#api delete
@app.route('/delete',methods=['GET'])
def delete():
    py_files = glob.glob(os.path.join(os.path.dirname(__file__),'./resultado/*.jpg'))
    print('del: ',py_files)
    for py_file in py_files:
        try:
            os.remove(py_file)
        except OSError as e:
            return(f"Error:{ e.strerror}") #print
    return 'Archivos eliminados'

#api get test
@app.route('/test',methods=['GET'])
def get_data1():
    return jsonify({'Mensaje':'Bienvenido'})

#execeute server
if __name__=="__main__":
    app.run(debug=True)