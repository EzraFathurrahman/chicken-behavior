from flask import Flask, render_template, request, make_response
import os
import shutil
import random
import string
from services.backend_anomaly.detector.ssd import MobileNetSSD
from services.backend_anomaly.inputs.video import Video
from services.backend_aggressive.yolo_video import detect_video
from services.backend_aggressive.yolo_video import write_analysis
from services.backend_aggressive.yolo_video import calculate_average
from services.backend_aggressive.yolo_video import get_time
from services.backend_anomaly.outputs.table_output import TableOutput
from services.backend_anomaly.anomaly_detection.isolation_forest import IForest

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

#convert avi to mp4
def convert_avi_to_mp4(avi_file_path, output_name):
    os.system('ffmpeg -i {} {}'.format(avi_file_path, output_name))
    return True

#make session id to differentiate file
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

@app.route("/aggressive-results",methods=['POST'])
def aggressive_results():

    f = request.files['file']

    session_id = get_session_id()

    tempFolder='static/temp'
    if os.path.isdir(tempFolder):
        shutil.rmtree(tempFolder)
      
    os.makedirs(tempFolder)

    f.save('static/temp/{}_{}'.format(session_id, f.filename))

    detect_video('static/temp/{}_{}'.format(session_id, f.filename),session_id,f.filename)

    average = calculate_average('static/temp/{}_confidences.txt'.format(f.filename))
    write_analysis('static/temp/{}_analysis.txt'.format(session_id), average)
    time=get_time()

    convert_avi_to_mp4('static/temp/{}_yolo_output.avi'.format(session_id),
                       'static/temp/{}_yolo_output.mp4'.format(session_id))
    
    
    return render_template('aggressive_results.html', session_id=session_id, video_source='static/temp/{}_yolo_output.mp4'.format(session_id),average=average,time=time)
    
@app.route("/anomaly")
def anomaly():
    return render_template('anomaly.html')


@app.route("/anomaly-result", methods=['POST'])
def anomaly_result():
    f = request.files['file']
    session_id = get_session_id()

    tempFolder='static/temp'
    if os.path.isdir(tempFolder):
        shutil.rmtree(tempFolder)
      
    os.makedirs(tempFolder)

    f.save('static/temp/{}_{}'.format(session_id, f.filename))

    video = Video('static/temp/{}_{}'.format(session_id, f.filename))
    net = MobileNetSSD(video)
    skip_frames = 30

    while True:
        read_output = video.read_next_frame()

        if not read_output:
            break
        elif read_output["total_frame"] % skip_frames == 0:
            net.detect(read_output["frame"],
                       read_output["width"], read_output["height"])
        else:
            net.update_tracker_position()

        net.centroid_update(read_output["frame"])

        video.write(read_output["frame"])

    video.stop()

    convert_avi_to_mp4('static/temp/{}_output.avi'.format(session_id),
                       'static/temp/{}_output.mp4'.format(session_id))

    data = net.save_tabular_output()
    table = TableOutput(data, session_id)
    if table.make_plot():

        isolation_forest = IForest()
        max_min_result = isolation_forest.find_max_min_runtime(table.get_contents())
        isolation_result = isolation_forest.detect_anomaly(max_min_result)

        isolation_result.to_excel(
            'static/temp/{}_anomaly_table.xlsx'.format(session_id), index=False)  

        return render_template('anomaly-result.html', session_id=session_id, video_source='static/temp/{}_output.mp4'.format(session_id), first_image_source='static/temp/{}_0.png'.format(session_id), id_length=len(table.get_ids()), id = table.get_ids(), first=isolation_result['first_occurrence'].values.tolist(), last=isolation_result['last_occurrence'].values.tolist(), period=isolation_result['period_detected'].values.tolist(), anomaly=isolation_result['anomaly_score'].values.tolist())
    
    else:
        return render_template('anomaly-result.html', session_id=session_id, video_source='static/temp/{}_output.mp4'.format(session_id), first_image_source= False)
