$(document).ready(function() {

    var total = $('.carousel-item').length;
    var currIndex = $('div.active').index() + 1;
    console.log(total);
    console.log(currIndex);
    $('.num').html('' + currIndex + '/' + total + '');
    $('#prev').hide();
    if (total == currIndex) {
        $('#next').hide();
    }

    $('#next, #prev').click(function() {
        console.log('clicked');
        var button = $(this).attr("id");
        if(button == "next") {
            currIndex++;
        }
        else {
            currIndex--;
        }
        if (currIndex == total) {
            $('#next').hide();
            $('#prev').show();
        }
        else if (currIndex == 1) {
            $('#prev').hide();
            $('#next').show();
        }
        else{
            $('#prev').show();
            $('#next').show();
        }
        
        $('.num').html('' + currIndex + '/' + total + '');
    });



    $("body").on("click", '.flip-card', function() {
        $(this).toggleClass('is-flipped');
    });
});