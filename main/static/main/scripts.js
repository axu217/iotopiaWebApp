$(document).ready(function() {

    $('#deviceChange1, #deviceChange2, #deviceChange3').click(function() {

        $(this).closest('.device').find('.deviceControl').animate({
                'left': "0%"
            },
            500,
            function() {

            });
    });

    $('.formReturnButton').click(function() {

        $(this).closest('.device').find('.deviceControl').animate({
                'left': "100%"
            },
            500,
            function() {

            });
    });

    $('.userPanelSend').click(function() {
        $(this).closest('.userPanel').find('.userPanelSendForm').animate({
                'left': "0%"
            },
            500,
            function() {

            });

    });

    $('.sendCreditReturnButton').click(function() {
        $(this).closest('.userPanel').find('.userPanelSendForm').animate({
                'left': "100%"
            },
            500,
            function() {

            });

    });




});