var $els = $('.sidebar .menu a, .sidebar .menu header');
var count = $els.length;
var grouplength = Math.ceil(count/3);
var groupNumber = 0;
var i = 1;
$('.sidebar .menu').css('--count',count+'');
$els.each(function(j){
    if ( i > grouplength ) {
        groupNumber++;
        i=1;
    }
    $(this).attr('data-group',groupNumber);
    i++;
});

$('.sidebar .menu footer button').on('click',function(e){
    e.preventDefault();
    $els.each(function(j){
        $(this).css('--top',$(this)[0].getBoundingClientRect().top + ($(this).attr('data-group') * -15) - 20);
        $(this).css('--delay-in',j*.1+'s');
        $(this).css('--delay-out',(count-j)*.1+'s');
    });
    $('.sidebar .menu').toggleClass('closed');
    e.stopPropagation();
});

// run animation once at beginning for demo
setTimeout(function(){
    $('.sidebar .menu footer button').click();
    setTimeout(function(){
        $('.sidebar .menu footer button').click();
    }, (count * 100) + 500 );
}, 1000);
