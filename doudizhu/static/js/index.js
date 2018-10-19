/**
 * Created by tarena on 18-9-28.
 */
// $(function(){
//     $.get('/index/getindexdata/',function(data){
//         $('.l2 span').html(data.uname);
//         $('.l3 span').html(data.ucoin);
//
//     },'json')
// })
// $(function(){
//     $('.l1 img').click(function(){
//         $.get('/tuichu/',function(){
//
//         })
//     })
// })

//创建房间
function CreateRoom(){
    $('#create').click(function(){
        var roomname = {'roomname':$('[name=roomname]').val()};
        $.get('/room/createroom',roomname,function(data){
            if (data.error){
                alert(data.error);
            }else{
                location.href='/room/getroom/?id=' + data.id
            }
        },'json')
    })
}
//加入房间
function JoinRoom(){
    $('#join').click(function(){
        var roomname = {'roomname':$('[name=roomname]').val()};
        $.get('/room/joinroom',roomname,function(data){
            if(data.error){
                alert(data.error)
            }else{
                location.href='/room/getroom/?id=' + data.id;
            }
        },'json')
    })
}
$(function(){
    CreateRoom();
    JoinRoom();
});

