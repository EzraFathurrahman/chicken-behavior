$(document).ready(function() {
    $('#ringtone')[0].play();
    $('<div></div>').dialog({
      title: 'Detection Completed',
      resizable: false,
      modal: true,
      width: '300px',
      buttons: {
        OK: function() {
          $(this).dialog('close');
        }
      },
      open: function() {
        
        var message = 'Your Video is ready to download';
        $(this).html(message);
      }
    });
  });