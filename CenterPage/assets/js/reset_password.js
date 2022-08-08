$(function(){
    var error_password = false;
    var error_check_password = false;
    
    $('#new_password').blur(function() {
        check_pwd();
    });

    $('#check_password').blur(function() {
        check_cpwd();
    });
    
    function check_pwd(){
        var len = $('#new_password').val().length;
        if(len<8||len>20)
        {
            $('#new_password').next().html('密码最少8位，最长20位')
            $('#new_password').next().show();
            error_password = true;
        }
        else
        {
            $('#new_password').next().hide();
            error_password = false;
        }
    }


    function check_cpwd(){
        var pass = $('#new_password').val();
        var cpass = $('#check_password').val();

        if(pass!=cpass)
        {
            $('#check_password').next().html('两次输入的密码不一致')
            $('#check_password').next().show();
            error_check_password = true;
        }
        else
        {
            $('#check_password').next().hide();
            error_check_password = false;
        }

    }
    

    $('#modify_password').submit(function() {
        check_pwd();
        check_cpwd();
        
        if(error_password == false && error_check_password == false)
        {
            return true;
        }
        else
        {
            return false;
        }

    });

})