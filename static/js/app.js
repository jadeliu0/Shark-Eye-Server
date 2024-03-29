$(function() {
    $('#submit').click(function() {
        event.preventDefault();
        var form_data = new FormData($('#uploadform')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log('Success!');
            $("#resultFilename").text(data['name']);
            $("#resultFilesize").text(data['size']);
        }).fail(function(data){
            alert('error in upload!');
        });
    });
});
$(function() {
    $('#detect').click(function() {
        event.preventDefault();
        var form_data = new FormData($('#detectform')[0]);
        $.ajax({
            type: 'POST',
            url: '/detectajax',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log('Success!');
            $("#resultDetection").text(data['detectresult']);
            $("#resultType").text(data['detecttype']);
        }).fail(function(data){
            alert('error in detection!');
        });
    });
}); 
