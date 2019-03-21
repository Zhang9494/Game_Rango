$(document).ready(function() {
    $("#likes").click(function(){
        var gameid;
        gameid = $(this).attr("data-gameid");
        $.get('/game/like/', {"game_id": gameid}, function(data){
            $("#like_count").html(data);
            $("#likes").hide();
            });
     });
});

