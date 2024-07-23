   
     $(window).on('load',function(e){
        $("#onclick-4").attr('class','display-none');
     });

    $("#onclick-1").on('click',function(e){
        $("#show-answer").load("1.html");
    });

    $("#onclick-2").on('click',function(e){
        $("#show-answer").load("2.html");
    });

    $("#onclick-3").on('click',function(e){
        $("#head-menu").load("3.html");
        $("#onclick-3").attr('class','display-none');
        $("#onclick-4").attr('class','display-block-color-red');
    });

    $("#onclick-4").on('click',function(e){
        $("#nav").attr('class','display-none');
        $("#onclick-3").attr('class','display-block');
        $("#onclick-4").attr('class','display-none');
    });

    $("#onclick-5").on('click',function(e){
        $("#show-answer").load("4.php");
    });





 