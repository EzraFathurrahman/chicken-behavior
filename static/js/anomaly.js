function change_attachment_text(){
    document.getElementById("attachment-text").innerHTML = "Video Attached!";
}

function check_submission_conditions(event){
    if(document.getElementById("video-input").files.length == 0) {
        event.preventDefault();
        document.getElementById("attachment-text").innerHTML = "No video file attached. Please insert a MP4 video!";
    }
    else {
        document.getElementById("attachment-text").innerHTML = "Processing. It may take a while..."
        document.getElementById("upload-video-box").style.display = "none";
        document.getElementById("drag-drop-message").style.display = "none";
        document.getElementById("loading-animation").style.display = "block";
    }
}

function prev_slide(length, id, session_id){
    id = parseInt(id.split(" ")[1], 10);
    if (id == 0)
    {
        document.getElementById("object-id").innerHTML = `ID ${length - 1}`;
        document.getElementById("object-plot").src = `static/temp/${session_id}_${length - 1}.png`;
    }
    else
    {
        document.getElementById("object-id").innerHTML = `ID ${id - 1}`;
        document.getElementById("object-plot").src = `static/temp/${session_id}_${id - 1}.png`;
    }
}

function next_slide(length, id, session_id){
    id = parseInt(id.split(" ")[1], 10);
    if (id == length - 1)
    {
        document.getElementById("object-id").innerHTML = "ID 0";
        document.getElementById("object-plot").src = `static/temp/${session_id}_0.png`;
    }
    else
    {
        document.getElementById("object-id").innerHTML = `ID ${id + 1}`;
        document.getElementById("object-plot").src = `static/temp/${session_id}_${id + 1}.png`;
    }
}

function download_anomaly_results(session_id, id_length){
    var zip = new JSZip();
        
    JSZipUtils.getBinaryContent(`static/temp/${session_id}_output.mp4`, function (err, data) {
        zip.file("video_output.mp4", data, {binary:true});
            
        var imagePromises = [];
        for (let i = 0; i < id_length; i++){
            imagePromises.push(JSZipUtils.getBinaryContent(`static/temp/${session_id}_${i}.png`));
        }
            
        Promise.all(imagePromises).then(function (results) {
            results.forEach(function (data, index) {
                zip.file(`${index}.png`, data, {binary:true});
            });

            JSZipUtils.getBinaryContent(`static/temp/${session_id}_anomaly_table.xlsx`, function (err, data) {
                zip.file("anomaly_table.xlsx", data, {binary:true});
            
                zip.generateAsync({type:"blob"}).then(function(content) {
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(content);
                    link.download = "anomaly_output.zip";
                    link.click();
                });
            });
        });
    });
}