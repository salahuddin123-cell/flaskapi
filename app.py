from pathlib import Path
from flask import Flask, jsonify, send_file, render_template
from io import BytesIO
from flask_cors import CORS

import os
from pdf2docx import parse,Converter
from flask import Flask, request, json
from pytube import YouTube
# from googleapiclient.discovery import build
from pytube import Search

app = Flask(__name__, template_folder='templates')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resource={
#     r"/*":{
#         "origins":"*"
#     }
# })
app.config['UPLOAD_FOLDER'] = 'static/img/'

count=0
reslist=[]
sresult=[]
api_key='AIzaSyALfHNwBfbZKWS540LcJdqGTzBfRXzeQLc'
@app.route('/')
def showtemplate():
    return render_template('index.html',data=count)
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
    cv = Converter(pdf_file)
    cv.convert(docx_file)      # all pages by default
    cv.close()

    return send_file(docx_file, as_attachment=True)

@app.route('/progress', methods=["GET", "POST"])
def progress():
    if request.method=='GET':
        return {"count":count}

# @app.route('/getstreams', methods=["GET", "POST","options"])
# def getstreams():
#     if request.method=='POST':
#         url = json.loads(request.data)['url']
#         yt = YouTube(url)
        
#         for stream in yt.streams:
            
#             if(str(stream.resolution).endswith("p") and str(stream.resolution) not in reslist):
#                 reslist.append(stream.resolution)
#                 print(stream)
#             else:
#                 print("not now")
        
#         return jsonify({"data":reslist})
#     else:
#         return { "message":"not availabe"}
@app.route('/getresult', methods=["POST","OPTIONS","GET"])
def search_youtube():
    
    if request.method=='POST':
        try:
            query = json.loads(request.data)['query']
            s = Search(query)
            
            for v in s.results:
                sresult.append({
                    "title":v.title,
                    "watch_url":v.watch_url,
                    "thumbnail_url":v.thumbnail_url

                })
                #print(f"{v.title}\n{v.watch_url}\n")
                
            return jsonify({"data":sresult})
        except Exception as e:
           
            return {'data':str(e)},400
    else:
        return jsonify({"data":"user not available"})
     

@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == 'POST':

        url = json.loads(request.data)['url']
        quality=json.loads(request.data)['quality']
        # url=request.form["url"]
        # quality=request.form["quality"]
        print(url,quality)
       
        
        #qulity=request.form['quality']
        yt = YouTube(url,on_progress_callback=on_progress)
        tail = str(os.path.split(yt.title))
        
        download_folder=str(os.path.join(Path.home(),"Downloads"))
       
        if quality=='high':
            video = yt.streams.get_highest_resolution().download(download_folder)
        elif quality=='low':
             video = yt.streams.get_lowest_resolution().download(download_folder)
        elif quality=="mp3":
            video = yt.streams.filter(only_audio=True).first().download(filename=tail.strip(" | ").replace("(\'\',","").replace('")','') + ".mp3",output_path=download_folder)
        else:
            try:
                video=yt.streams.filter(res=quality).first().download(download_folder)
            except Exception as e:
                if int(quality.strip('p'))<=360:
                    video = yt.streams.get_lowest_resolution().download(download_folder)
                else:
                    video = yt.streams.get_highest_resolution().download(download_folder)


        fname = video.split("//")[-1]
        print(fname)
        return send_file(
            fname,
            as_attachment=True,attachment_filename='video.mp4'),201



def on_progress(stream, chunk, bytes_remaining):
    global count
    total_size = stream.filesize
    bytes_download = total_size - bytes_remaining
    perecentage_of_completion = bytes_download / total_size * 100
    per = str(int(perecentage_of_completion))
    print(per)
    count=per
    


            


if __name__ == '__main__':
    app.run()
