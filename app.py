from flask import Flask, send_file
from io import BytesIO

import os
from pdf2docx import parse
from flask import Flask, request, json
from pytube import YouTube

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/'

@app.route('/<int:number>/')
def incrementer(number):
    return "Incremented number is " + str(number+1)

@app.route('/')
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

        pdf_file = "static/img/my.pdf"
        docx_file="static/docx/random.docx"
        # docx_file = os.path.expanduser(f"~/Downloads/random.docx")

        # convert pdf to docx
        parse(pdf_file, docx_file)

        return send_file(docx_file,as_attachment=True)

@app.route('/download',methods=["GET","POST"])

def download():
    if request.method == 'POST':

        url=json.loads(request.data)
    
        yt = YouTube(url['data'])
        video=yt.streams.get_lowest_resolution().download()
        fname=video.split("//")[-1]
        return send_file(
            fname,
            as_attachment=True)


if __name__ == '__main__':
    app.run()
