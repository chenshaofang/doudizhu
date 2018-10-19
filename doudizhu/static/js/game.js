$(function(){
    select_puke();
    appear_puke();
    get_puke_accept(appear(),appear(),'');
});
//长连接，接收扑克
function get_puke_accept(appear,myappear,puke){
    d = {
        'room_id':room_id(),
        'appear':appear,
        'puke':puke
    };
    $.get('/game/get_puke_accept',d,function(data){
        if(data.appear == '0' && data.appear != myappear){
           for(var i=1;i<=data.puke_len;i++){
                 $('[name="0"]>li').last().remove();
            }
        }else if(data.appear == '1' && data.appear != myappear){
           for(var i=1;i<=data.puke_len;i++){
                 $('[name="1"]>li').last().remove();
            }
        }else if(data.appear == '2' && data.appear != myappear){
           for(var i=1;i<=data.puke_len;i++){
                 $('[name="2"]>li').last().remove();
            }
        }
        $('#puke').html(data.puke);
        if(data.game_over){
            $('#game_over').html("<button id='b_game_over'>"+"结束"+"</button>");
            $('#b_game_over').click(function(){
                $.get('/game/game_over',{'room_id':room_id()},function(){},'json');
                location.href = '/room/getroom?id='+data.game_over;
            });
            return
        }
        get_puke_accept(data.appear,myappear,data.puke)
    },'json')
}
//要出的牌的列表
var puke_list = [];
//要删除元素的列表
var element = [];
//选牌
function select_puke(){
    $('#wj1').click(function(e){
        var ht = $(e.target);
        for(var i=0;i<=puke_list.length;i++){
            if(ht.html()==puke_list[i]){
                var index = puke_list.indexOf(ht.html());
                puke_list.splice(index,1);
                element.splice(index,1);
                return
            }
        }
        puke_list[puke_list.length] = ht.html();
        element[element.length] = ht;
    })
}
// 出牌
function appear_puke(){
    $('#appear_puke').click(function(){
        for(var i=0;i<element.length;i++){
            element[i].remove();
        }
        console.log(puke_list);
        var d = {
            'puke':String(puke_list),
            'appear':appear(),
            'room_id':room_id(),
            'puke_len':puke_list.length
        };
        $.get('/game/appear_puke',d,function(){
        },'json');
        puke_list.splice(0,puke_list.length);
    })
}
