/**
 * Created by tarena on 18-9-30.
 */
$(function(){
    $('#b1').click(function(){
        var url = '/';
        var data = {"csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val(),
        "uphone":$('[name=uphone]').val(),
        "upwd":$('[name=upwd]').val(),
        "apwd":$('[name=apwd]').val()};

        $.post(url,data,function(data){
            if(data.error){

                alert(data.error);
            }else{

                location.href='/index';
            }
        },'json');
    });
    $('[name=apwd]').click(function(){
        if($('[name=apwd]').val()=='N'){
            $('[name=apwd]').val('T')
        }else{
            $('[name=apwd]').val('N')
        }
    })
});
