$(document).ready(function(){
    $(window).scroll(function(){
        if($(window).scrollTop() > 100){
            $('.navbar').css('position','fixed');
        }
        else{
            $('.navbar').css('position','relative');
        }
    });
});