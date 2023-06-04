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



function download_aggressive_results(session_id, id_length){
    var zip = new JSZip();
    
    JSZipUtils.getBinaryContent(`static/temp/${session_id}_yolo_output.mp4`, function (err, data) {
        zip.file("video_output.mp4", data, {binary:true});
        
        zip.generateAsync({type:"blob"}).then(function(content) {
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(content);
            link.download = "aggressive_output.zip";
            link.click();
            
       
        
        
        });
    });
}