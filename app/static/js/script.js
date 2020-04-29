$('button#btn').click(function() {
    $.ajax({
        url: "/_get_data/",
        type: "POST",
        success: function(resp){
            $('tbody#response').append(resp.data);
        }
    });
});