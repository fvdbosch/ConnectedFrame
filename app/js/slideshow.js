$(document).ready(function(){
    $("#next").click(function(){
        $("#currentImage").attr("src","./img/2.JPG");
    });
    $("#previous").click(function(){
        $("#currentImage").attr("src","./img/1.JPG");
    });
});