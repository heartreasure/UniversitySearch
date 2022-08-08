$(function(){
    $('#feedback_form').submit(function() {

        var name = $('#name').val();
        var email = $('#email').val();
        var subject = $('#subject').val();
        var feedback = $('#feedback').val();
        
        if(name==''||email==''||subject==''||feedback==''){
            $('.feedback_msg').show();
            return false;
        }
        else {
            return true;
        }
            

    });

})