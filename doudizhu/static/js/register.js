/**
 * Created by tarena on 18-9-29.
 */

//name验证
function verification_name(){
    var uname = $('[name="uname"]').val();
    if (3<=uname.length && uname.length<=8){
        return true;
    }else{
        return false;
    }
}
//手机号验证
function verification_phone(){
    var phone = $('[name="uphone"]').val();
    if(phone.length==10||phone.length==11){
        return true;
    }else{
        return false;
    }
}
//密码验证
function verification_pwd(){
    var pwd = $('[name=upwd]').val();
    if(pwd.length>=6 && pwd.length<=18){
        return true;
    }else{
        return false;
    }
}
//确认密码
function verification_cpwd(){
    var cpwd = $('[name=cpwd]').val();
    var upwd = $('[name=upwd]').val();
    if(cpwd == upwd){
        return true;
    }else{
        return false;
    }
}
//name Ajax 验证

function name_Ajax(){
    name = $('[name=uname]').val();
    $.get('/name_Ajax/',{'uname':name},function(data){
        var AJ = data.data;
        if(AJ){
            $('.s1').html('*')
        }else{
            $('.s1').html('*用户名已存在')
        }
    },'json')
}

$(function(){
    $('[name="uname"]').blur(function(){
        if(!verification_name()){
            $('.s1').html('*名称不符合规范')
        }else{
            name_Ajax();
            $('.s1').html('*')
        }
    });
    $('[name="upwd"]').blur(function(){
        if(!verification_pwd()){
            $('.s3').html('*密码不符合规范')
        }else{
            $('.s3').html('*')
        }
        });
    $('[name="cpwd"]').blur(function(){
        if(!verification_cpwd()){
            $('.s4').html('*两次输入不一致')
        }else{
            $('.s4').html('*')
        }
        });
    $('[name="uphone"]').blur(function(){
        if(!verification_phone()){
            $('.s2').html('*手机号不正确')
        }else{
            $('.s2').html('*')
        }
    });
    $('form').submit(function(){
        return verification_name()&&verification_phone()&&verification_pwd()&&verification_cpwd()
    })
});

