import time
from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from werkzeug import secure_filename

app = Flask(__name__)
import logging
import s3_utils
import os
from detect import getDetectionResult


basedir = os.path.abspath(os.path.dirname(__file__))


app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':

        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    elif endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploadajax', methods=['POST'])
def uploadfile():
    if request.method == 'POST':
        files = request.files['file']
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)
            app.logger.info('FileName: ' + filename)
            updir = os.path.join(basedir, 'upload/')
            files.save(os.path.join(updir, filename))
            s3Url = s3_utils.upload(os.path.join(updir, filename), filename, s3_utils.FileType.upload)
            file_size = os.path.getsize(os.path.join(updir, filename))
            return jsonify(name=s3Url, size=file_size)

@app.route('/detectajax', methods=['POST'])
def detect():
    if request.method == 'POST':
        s3url = request.form['s3url']
        downloadDir = os.path.join(basedir, 'download')
        filePath = s3_utils.download(s3url, downloadDir)
        start_time = time.time()
        filePath, detType = getDetectionResult(filePath)
        print "detection result stored in %s" % filePath
        print "--- took %s seconds for detection ---" % (time.time() - start_time)
        return jsonify(detectresult=filePath, detecttype=detType)

if __name__ == '__main__':
    app.run(debug=True)
