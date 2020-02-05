$(document).ready(function(){
    $(window).scroll(function(){
        // console.log($(window).scrollTop());
        if($(window).scrollTop() > $('#banner').height() ){
            $('.navbar').css('position','fixed');
            $('main').css("margin-top",  $('.navbar').height() );
        }
        else{
            $('.navbar').css('position','relative');
            $('main').css("margin-top",'0px');
        }
    });
});