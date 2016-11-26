/* web/module/console/main.js */
$(function(){
    $('.nav').click(function(event){
        $i = $(this).children('i');
        if ($i.hasClass('triangle-r')) {            
            $i.removeClass().addClass('triangle-b');
            /* 获取子菜单列表，第一项 */
            if ($(this).hasClass('host')) {
                $.getJSON('/monitor/api/getHostGroupList/', function(data) {
                    console.log(data);
                });                
            } else if ($(this).hasClass('trigger')) {
                console.log('trigger');
            } else if ($(this).hasClass('config')) {
                console.log('config');
            }
        } else {
            $i.removeClass().addClass('triangle-r');
        }
    });
});

