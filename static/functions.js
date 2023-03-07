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