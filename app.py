import os
from pdf2docx import Converter,parse
from flask import Flask, request, json
from pytube import YouTube
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/'

@app.route('/<int:number>/')
def incrementer(number):
    return "Incremented number is " + str(number+1)

@app.route('/', methods=['GET', 'POST'])
def front_page():
    return "hello dosto"
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = "my.pdf"
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #   f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
   
@app.route('/convert',methods=["GET","POST"])
def convert_file():
    if request.method == 'POST':
        pdf_file = "static/img/my.pdf"
        docx_file = os.path.expanduser(f"~/Downloads/random.docx")

        # convert pdf to docx
        parse(pdf_file, docx_file)  
        return "conveted to docs"
   
@app.route('/download',methods=["GET","POST"])

def download():
    url=json.loads(request.data)
    print(url['data'])
    yt = YouTube(url['data'])
    try:
        yt.streams.get_lowest_resolution().download(os.path.expanduser("~/Downloads"))
    except:
        print("Some Error!")
    print('downloaded')
    return url

app.run()