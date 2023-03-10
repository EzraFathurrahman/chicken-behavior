from flask import Flask, render_template, request, make_response
import os, random, string
from services.backend_anomaly.detector.ssd import MobileNetSSD
from services.backend_anomaly.inputs.video import Video
from services.backend_anomaly.preprocessing.sort import sort
from services.backend_anomaly.preprocessing.max_min_runtime import max_min_runtime
from services.backend_anomaly.preprocessing.split_object_id import split_object_id
from services.backend_anomaly.preprocessing.plot import make_plot
from services.backend_anomaly.anomaly_detection.isolation_forest import isolation_forest

app = Flask(__name__)

def convert_avi_to_mp4(avi_file_path, output_name):
    os.system('ffmpeg -i {} {}'.format(avi_file_path, output_name))
    return True

def get_session_id():
    character_list = ""
    character_list += string.ascii_letters
    character_list += string.digits
    
    session_id = ""
    for i in range(16):
        session_id += random.choice(character_list)
    
    return session_id

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
    session_id = get_session_id()
    f.save('static/temp/{}_{}'.format(session_id, f.filename))
    
    video = Video('static/temp/{}_{}'.format(session_id, f.filename))
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

    convert_avi_to_mp4('static/temp/{}_output.avi'.format(session_id), 'static/temp/{}_output.mp4'.format(session_id))

    data = net.save_output()

    data_sorted = sort(data)
    ids, dataframes = split_object_id(data_sorted)
    for i in ids:
        dataframes[i] = dataframes[i].reset_index().drop(["index"], axis = 1)
        make_plot(dataframes[i], i, session_id)

    max_min_result = max_min_runtime(data)
    isolation_result = isolation_forest(max_min_result)

    isolation_result.to_excel('static/temp/{}_anomaly_table.xlsx'.format(session_id), index = False)

    os.remove('static/temp/{}_{}'.format(session_id, f.filename))
    os.remove('static/temp/{}_output.avi'.format(session_id))

    return render_template('anomaly-result.html', session_id = session_id, video_source = 'static/temp/{}_output.mp4'.format(session_id), first_image_source = 'static/temp/{}_0.png'.format(session_id), id_length = len(ids), id = ids, first = isolation_result['first_occurrence'].values.tolist(), last = isolation_result['last_occurrence'].values.tolist(), period = isolation_result['period_detected'].values.tolist(), anomaly = isolation_result['anomaly_score'].values.tolist())
