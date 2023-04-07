from flask import Flask, send_file, render_template
from io import BytesIO
from flask_cors import CORS

import os
from pdf2docx import parse
from flask import Flask, request, json
from pytube import YouTube

app = Flask(__name__, template_folder='templates')
CORS(app)
# cors = CORS(app, resource={
#     r"/*":{
#         "origins":"*"
#     }
# })
app.config['UPLOAD_FOLDER'] = 'static/img/'


@app.route('/')
def showtemplate():
    return render_template('index.html')
@app.route('/pdf2doc')
def showtemplate2():
    return render_template('pdf2docx.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = "my.pdf"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #   f.save(secure_filename(f.filename))
        return render_template('uploaded.html')


@app.route('/convert', methods=["GET", "POST"])
def convert_file():

    pdf_file = "static/img/my.pdf"
    docx_file = "static/docx/random.docx"
    # docx_file = os.path.expanduser(f"~/Downloads/random.docx")

    # convert pdf to docx
    parse(pdf_file, docx_file)

    return send_file(docx_file, as_attachment=True)


@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == 'POST':

        # url = json.loads(request.data)
        url=request.form["url"]
        qulity=request.form['quality']
        yt = YouTube(url)
        file_name = 'my_video.mp4'
        file_name2="my_audio.mp3"
        if qulity=='high':
            video = yt.streams.get_highest_resolution().download(filename=file_name)
        elif qulity=='low':
             video = yt.streams.get_lowest_resolution().download(filename=file_name)
        else:
            video = yt.streams.filter(only_audio=True).first().download(filename=file_name2)
        fname = video.split("//")[-1]
        print(fname)
        return send_file(
            fname,
            as_attachment=True)



if __name__ == '__main__':
    app.run()
