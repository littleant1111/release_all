$(function(){
    var taskid = $('input[name="taskid"]').val();
    var project_code = $('select[name="project"]').val();
    var h_handle = '';

    // 错误时候的对话框
    $( "#error" ).dialog({
        dialogClass: "no-close",
        autoOpen: false,
        width: 200,
        height:42,
        resizable:false,
        modal:false
    }).parent().find('.ui-widget-header').hide();// 隐藏标题


    // 获取任务状态
    function getTaskInfo(){
        $.ajax({
        　　type : 'POST',
        　　url : '/release/getTaskInfo/',
            data:{
                'taskid': taskid,
            },
        　　success:function(data){
                if(data){
                    if(data.log != ''){
                        $('#log_content').html(data.log).scrollTop(30000);
                    }
                    $('.step_info').find('li').removeClass('selected');
                    $(data.task).each(function(i){
                        var dom_li = $('.step_info').find('li');
                        dom_li.each(function(j){
                            var c_step_id = $(this).find('input[name="step_id"]').val();
                            if (c_step_id == data.task[i].id) {
                                $(this).find('.right').remove();
                                if (data.task[i].status == '1'){
                                    $(this).append('<img class="right" src="/static/img/loadding2.gif">');
                                    $(this).addClass('selected');
                                    $('.step_remark_content').text($(this).find('input[name="comments"]').val());
                                }else if (data.task[i].status == '2'){
                                    $(this).append('<img class="right" src="/static/img/right.png">');
                                }else if (data.task[i].status == '-1'){
                                    $(this).append('<img class="right" src="/static/img/error.png">');
                                }else{
                                    $(this).find('span').text('');
                                }
                            }
                        });
                    });
                }
        　　},
        });
    }


    // 红绿点击事件
    $('.step_info').find('.left').bind('click', 'img', function(){
        var _this = $(this);
        var is_stop = $('input[name="is_stoped"]').val();
        $.ajax({
        　　type : 'POST',
        　　url : '/release/clickRedGreen/',
        　　data:{
                'is_stop': is_stop,
                'stepid' : _this.next('input[name="step_id"]').val()
            },
        　　dataType : 'json',
        　　success:function(data){
                if(data == '1'){
                    $('input[name="is_stoped"]').val('1');
                    _this.attr('src', '/static/img/red_yuan.png');
                }else{
                    $('input[name="is_stoped"]').val('0');
                    _this.attr('src', '/static/img/green_yuan.png');
                }
        　　},
        });
    });

    // 根据应用名 获取 ip列表
    $('select[name="app"]').on('change', function(){
        var app = $('select[name="app"]').val();
        if (app == '0'){
            return
        }
        $('select[name="host"]').find('option').remove();
        $.ajax({
        　　type : 'POST',
        　　url : '/release/getIpaddresses/',
        　　data:{
                'app': app
            },
        　　success:function(data){
                if(data){
                    $(data).each(function(i){
                        $('select[name="host"]').append('<option value="'+ data[i] +'">'+ data[i] +'</option>');
                    });
                }
        　　},
        });
    });

    // 日志获取按钮点击
    $('input[name="getlog"]').on('click', function(e){
        var app = $('select[name="app"]').val();
        var ip = $('select[name="host"]').val();
        if (app == '0' || typeof(app) == 'undefined'){
            $( "#error" ).dialog('open').html('请选择应用...');
            $('select[name="app"]').css({
                    'border' : '2px solid red'
            });
            setTimeout(function(){
                $('select[name="app"]').css({
                    'border' : '1px solid #ccc'
                });
                $( "#error" ).dialog('close').html('...');
            }, 1500);
            return;
        }
        if (ip == '0' || typeof(ip) == 'undefined'){
            $( "#error" ).dialog('open').html('请选择主机...');
            $('select[name="app"]').css({
                    'border' : '1px solid #ccc'
            });
            setTimeout(function(){
                $('select[name="app"]').css({
                    'border' : '2px solid red'
                });
                $( "#error" ).dialog('close').html('...');
            }, 1500);
            return;
        }

        var step_id = $('.step_info').find('.selected').find('input[name="step_id"]').val();
        if (typeof(step_id) == 'undefined'){
            $( "#error" ).dialog('open').html('请选择对应步骤日志...');
            $('.step_info').find('li').css({
                    'border' : '2px solid red'
            });
            setTimeout(function(){
                $('.step_info').find('li').css({
                    'border' : 'none'
                });
                $( "#error" ).dialog('close').html('...');
            }, 1500);
            return;
        }
        $.ajax({
        　　type : 'POST',
        　　url : '/release/getRemoteLog/',
        　　data:{
                'taskid': taskid,
                'project_code' : project_code,
                'app' : app,
                'ip' : ip,
                'step_id' : step_id
            },
            beforeSend:function(jqXR, settings){
                $('#log_content').text('日志加载中 。。。');
            },
        　　success:function(data){
                if(data){
                    $('#log_content').text(data);
                }
        　　},
        });
    });


    //动态绑定左边链接的点击事件
    $('.step_link').click(function(){
        $('.step_info').find('li').removeClass('selected');
        $(this).parent().addClass('selected');
    });

    // 执行步骤按钮点击
    $('input[name="exec"]').click(function(e){
        var app = $('select[name="app"]').val();
        var ip = $('select[name="host"]').val();
        var dom_selected = $('.step_info').find('.selected')
        var step_name = dom_selected.find('input[name="step_name"]').val();
        var step_id = dom_selected.find('input[name="step_id"]').val();
        window.console.log(step_id);
        if (typeof(step_id) == "undefined"){
            $( "#error" ).dialog('open').html('请选择操作步骤...');
            $('.step_info').find('li').css({
                    'border' : '2px solid red'
            });
            setTimeout(function(){
                $( "#error" ).dialog('close').html('...');
                $('.step_info').find('li').css({
                    'border' : 'none'
                });
            }, 1500);
            return;
        }
        $.ajax({
        　　type : 'POST',
        　　url : '/release/clickCommand/',
            data:{
                'taskid': taskid,
                'project_code' : project_code,
                'app' : app,
                'ip' : ip,
                'step_name' : step_name,
                'step_id' : step_id
            },
            beforeSend:function(jqXR, settings){
                $('input[name="exec"]').css({
                    'background': '#d2d2d2',
                }).attr('disabled', 'true').val('执行中');
                dom_selected.find('.right').remove();
                dom_selected.append('<img class="right" src="/static/img/loadding2.gif">');
            },
        　　success:function(data){
                if (data.msg) {
                    $('#log_content').text($('#log_content').text() + '\n' + data.msg);
                }
//                if(data.result == 'false'){}
        　　},
            complete: function(XMLHttpRequest, textStatus) {
                $('input[name="exec"]').css({
                    'background': 'gold',
                }).removeAttr('disabled').val('执行');
                clearInterval(h_handle);
                h_handle = '';
                setTimeout(function(){
                    getTaskInfo();
                }, 3000);
            },
        });

//        if(h_handle != ''){
            h_handle = setInterval(function(){
                getTaskInfo();
            }, 3000);
//        }

    });

   $(window).load(function(){
    window.console.log('asfdfsadfsd');
      setTimeout(function(){
                    getTaskInfo();
                }, 1000);}
);

});
