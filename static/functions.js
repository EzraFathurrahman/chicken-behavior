function change_attachment_text(){
    document.getElementById("attachment-text").innerHTML = "Video Attached!";
}

function check_submission_conditions(event){
    if(document.getElementById("video-input").files.length == 0) {
        event.preventDefault();
        document.getElementById("attachment-text").innerHTML = "No video file attached. Please insert a MP4 video!";
    }
    else {
        document.getElementById("drop-area").innerHTML = '<div class="loader"></div>';
    }
}