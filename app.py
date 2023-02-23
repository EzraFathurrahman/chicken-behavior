from flask import Flask, render_template, request
from subprocess import call
from services.backend_anomaly.detector.ssd import MobileNetSSD
from services.backend_anomaly.inputs.video import Video
from services.backend_anomaly.preprocessing.sort import sort
from services.backend_anomaly.preprocessing.max_min_runtime import max_min_runtime
from services.backend_anomaly.preprocessing.split_object_id import split_object_id
from services.backend_anomaly.preprocessing.plot import make_plot
from services.backend_anomaly.anomaly_detection.isolation_forest import isolation_forest

ALLOWED_EXTENSIONS = 'mp4'

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_avi_to_mp4(avi_file_path):
    os.popen("ffmpeg -i {} -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 temp/output_mp4.mp4".format(avi_file_path))

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/aggressive")
def aggressive():
    return render_template('aggressive.html')

@app.route("/feed")
def feed():
    return render_template('feed.html')

@app.route("/anomaly")
def anomaly():
    return render_template('anomaly.html')

@app.route("/anomaly-result", methods = ['POST'])
def anomaly_result():
    f = request.files['file']
    f.save('static/temp/{}'.format(f.filename))
    
    video = Video('static/temp/{}'.format(f.filename))
    net = MobileNetSSD(video)
    skip_frames = 30
    
    while True:
        read_output = video.read_next_frame()
        
        if not read_output:
            break
        elif read_output["total_frame"] % skip_frames == 0:
            net.detect(read_output["frame"], read_output["width"], read_output["height"])
        else:
            net.update_tracker_position()
    
        net.centroid_update(read_output["frame"])
        
        video.write(read_output["frame"])
    
    video.stop()

    data = net.save_output()

    data_sorted = sort(data)
    ids, dataframes = split_object_id(data_sorted)
    for i in ids:
        dataframes[i] = dataframes[i].reset_index().drop(["index"], axis = 1)
        make_plot(dataframes[i], i)
    
    #max_min_result = max_min_runtime(data)
    #isolation_result = isolation_forest(max_min_result)

    return render_template('anomaly-result.html')