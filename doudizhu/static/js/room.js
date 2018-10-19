var Nu = 0;
//获取页面数据
function get_data(){
    var room_id =  id();
    var room_root = $('#room_root').html();
    $.get('/room/get_room_data',{"room_id":room_id,"room_root":room_root},function(data){
        Nu = data.book+1;
        if(data.book == 1){
            $('#s_1').html(data.data[0])
        }else if(data.book == 2){
            $('#s_1').html(data.data[0]);
            $('#s_2').html(data.data[1]);
        }

    },'json')
}
//退出房间
function signout(){
    Nu -= 1;
    d = {
        'room_id':id(),
        'nu':Nu
    };
    if($('#room_root').html()==uname()){
        d = {
        'room_id':id(),
        'nu':Nu,
        'room_root':1
        };
    }
    $.get('/room/signout/',d,function(){
        location.href = '/'
    })
}
//开始游戏
function start(){
    $.get('/game/page',{'room_id':id()},function(data){
        if(data.error){
            alert(data.error)
        }else{
            location.href = '/game/getpage?room_id='+data.room_id
        }
    },'json')
}
//保持长连接更新房间玩家信息
function long_connect(v){
    //if(new Date()-t >= 600){
    //    return
    //}
    if(Nu<3){
        $.ajax({
        url:'/room/long_connect',
        data:{'room_id':id(),'v':v},
        datatype:'json',
        timeout:10000,
        error:function(XMLHttpRequest, textStatus, errorThrown){
                if(textStatus >= 'timeout'){
                    long_connect(v)
                }else{
                    long_connect(v)
                }
            },
        success:function(data){
            var data = eval('(' + data + ')');
            if(data.error){
                alert(data.error);
                return
            }
            if(data.lnorde == 1){
                if($('#s_1').text().length == 0){

                    $('#s_1').html(data.name)
                }else{
                    $('#s_2').html(data.name)
                }
                Nu += 1;
            }else{
                if($('#s_1').text() == data.name){
                    $('#s_1').html('')
                }else{
                    $('#s_2').html('')
                }
                Nu -= 1;
            }
            long_connect(data.v)
        }
    })
    }
}
//长连接,接受游戏开始信号
function connect(){
    room_id = id();
    console.log('准备长连接');
    $.get('/game/long_connect',{'room_id':room_id},function(data){
        if(data.error){
            return
        }else{
            location.href = '/game/getpage?room_id='+data.room_id
        }
    },'json')
}
//动态生成按钮
function judge(){
    if(uname()!=$('#room_root').html()){
        var bu = $('#bu1');
        bu.html("<button id='connect'>"+"准备"+"</button>");
        bu.click(function(){
            connect()
        })
    }else{
        var bu = $('#bu1');
        bu.html("<button id='start'>"+"开始"+"</button>");
    }
}
//初始化
$(function(){
    get_data();
    judge();
    $('#signout').click(function(){
        signout()
    });
    $('#start').click(function(){
        start()
    });
    long_connect(v())
});