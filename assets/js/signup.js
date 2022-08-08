$(function(){

    var error_name = false;
    var error_password = false;
    var error_check_password = false;
    var error_email = false;
    var error_check = false;


    $('#signup-username').blur(function() {
        check_user_name();
    });

    $('#signup-email').blur(function() {
        check_email();
    });

    $('#signup-password').blur(function() {
        check_pwd();
    });

    $('#signup-check').blur(function() {
        check_cpwd();
    });

    function check_user_name(){
        var len = $('#signup-username').val().length;
        if(len<5||len>20)
        {
            $('#signup-username').next().html('请输入5-20个字符的用户名')
            $('#signup-username').next().show();
            error_name = true;
        }
        else
        {
            $('#signup-username').next().hide();
            error_name = false;
        }
    }

    function check_pwd(){
        var len = $('#signup-password').val().length;
        if(len<8||len>20)
        {
            $('#signup-password').next().html('密码最少8位，最长20位')
            $('#signup-password').next().show();
            error_password = true;
        }
        else
        {
            $('#signup-password').next().hide();
            error_password = false;
        }
    }


    function check_cpwd(){
        var pass = $('#signup-password').val();
        var cpass = $('#signup-check').val();

        if(pass!=cpass)
        {
            $('#signup-check').next().html('两次输入的密码不一致')
            $('#signup-check').next().show();
            error_check_password = true;
        }
        else
        {
            $('#signup-check').next().hide();
            error_check_password = false;
        }

    }

    function check_email(){
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if(re.test($('#signup-email').val()))
        {
            $('#signup-email').next().hide();
            error_email = false;
        }
        else
        {
            $('#signup-email').next().html('邮箱格式不正确')
            $('#signup-email').next().show();
            // error_check_password = true;
            error_email = true;
        }
        

    }

    $('#RegisterForm').submit(function() {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();

        if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
        {
            return true;
        }
        else
        {
            return false;
        }

    });

})