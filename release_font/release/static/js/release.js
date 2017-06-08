$(function(){

    var stage;                                          // 项目阶段
    var env;                                            // 环境类型
    var cu_text;                                        // 项目名称
    var cu_val;                                         // 项目编码
    var version;                                        // 项目版本
    var arrList;                                        // 应用列表



    // 加载中的对话框
    $( "#loadding" ).dialog({
        dialogClass: "no-close",
        autoOpen: false,
        width: 200,
        height:60,
        resizable:false,
        modal:true
    }).parent().find('.ui-widget-header').hide();// 隐藏标题

    // 错误时候的对话框
    $( "#error" ).dialog({
        dialogClass: "no-close",
        autoOpen: false,
        title : '错误提示',
        width: 600,
        height:300,
        resizable:false,
        modal:true,
    });

    // 错误时候的对话框
    $( "#error2" ).dialog({
        dialogClass: "no-close",
        autoOpen: false,
        title : '错误提示',
        width: 200,
        height:35,
        resizable:false,
        modal:false,
    }).parent().find('.ui-widget-header').hide();


    // 确认发布页面对话框
    $('#comfirm').dialog({
        dialogClass: "no-close",
        autoOpen: false,
        width: 600,
        height:400,
        title : '确认对话框',
        resizable:false,
        modal:true,
        closeText:'关闭',
        buttons: [
            {
                text: "确定",
                click: function() {
                    // ajax 检测配置文件信息
                    var data = {
                        'envtype':env,
                        'project':[{
                            'name' : cu_val,
                            'version': version,
                            'app' : arrList
                        }]
                    };
                    $.ajax({
                        type:'POST',
                        url : '/release/taskBegin/',
                        data: JSON.stringify(data),
                        dataType : 'json',
                        beforeSend:function(jqXR, settings){
                            $('#comfirm').dialog('close');
                            $('#loadding').dialog('open');
                        },
                        success:function(data){
                            $('#loadding').dialog('close');
                            if(data == 'true'){
                               location.href = '/release/detail/';   // 跳转到指定页面
                            }else {
                                $('#error').find('span')
                                    .text('错误信息,数据检查失败！').end().dialog('open');
                            }
                        },
                        error : function(XMLHttpRequest, textStatus, errorThrown){
                            $('#loadding').dialog('close');
                            $('#error').find('span')
                                .text('错误信息,textStatus:' + textStatus + 'errorThrown:' + errorThrown ).end().dialog('open');
                        },
                    });
                }
            },{
                text: "取消",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

    //  确认按钮点击事件
    setTimeout(function(){
        $('input[name="comfirm"]').click(function(){
            stage = $('input[name="stage"]:checked').val();
            // check stage
            var stageArr = ['sit', 'uat', 'pre', 'prd'];
            if($.inArray(stage, stageArr) == -1){
                $('#error2').dialog('open').html('未选择发布阶段！');
                $('.stage').find('li').css({'border' : '2px solid red'});
                setTimeout(function(){
                    $('#error2').dialog('close').html('...');
                    $('.stage').find('li').css({'border' : 'none'});
                }, 1000);
                return;
            }
            $('#stage').html(stage);                                  // 设置 阶段

            var release_env = $('input[name="envtype"]:checked').val();
            window.console.log(release_env);
            if (release_env == '0' || typeof(release_env) == 'undefined'){
                $('#error2').dialog('open').html('未选择发布环境！');
                $('.env').find('li').css({'border' : '2px solid red'});
                setTimeout(function(){
                    $('#error2').dialog('close').html('...');
                    $('.env').find('li').css({'border' : 'none'});
                }, 1000);
                return;
            }

            cu_val = $('select[name="project"]').val();               // 项目编码
            $('select[name="project"] option').each(function(i){
                if ($(this).val() == cu_val){
                    cu_text = $(this).text();                          // 项目名称
                }
            });

            // check project_name and project_code
            if (cu_val == '0' || typeof(cu_val) == 'undefined' || cu_text == '' || typeof(cu_text) == 'undefined'){
                $('#error2').dialog('open').html('未选择项目！');
                $('select[name="project"]').css({'border' : '2px solid red'});
                setTimeout(function(){
                    $('#error2').dialog('close').html('...');
                    $('select[name="project"]').css({'border' : '1px solid #ccc'});
                }, 1000);
                return;
            }

            $('#pro_name').text(cu_text);                            //  项目名称
            $('#pro_code').text(cu_val);                             //  项目编码

            version = $('select[name="version"]').val();             // 项目版本
            // check version
            if (version == '0' || typeof(version) == 'undefined'){
                $('#error2').dialog('open').html('未选择版本！');
                $('select[name="version"]').css({'border' : '2px solid red'});
                setTimeout(function(){
                    $('#error2').dialog('close').html('...');
                    $('select[name="version"]').css({'border' : '1px solid #ccc'});
                }, 1000);
                return;
            }

            $('#pro_version').text(version);
            //alert(stage + '|' + env + '|' + cu_text + '|' + cu_val + '|' + version );
            arrList = [];
            $('#apps').find('li').remove();
            $('input[name="app"]').each(function(i){
                if($(this).prop("checked")){
                    arrList.push($(this).val());
                }
            });
            // check arrList
            if (arrList.length == 0){
                $('#error2').dialog('open').html('未选择发布包！');
                $('.select_app').css({'border' : '2px solid red'});
                setTimeout(function(){
                    $('#error2').dialog('close').html('...');
                    $('.select_app').css({'border' : '1px solid #ccc'});
                }, 1000);
                return;

            }

            $(arrList).each(function(i){
                $('#apps').append('<li>' + arrList[i] + '&nbsp;&nbsp;</li>');
            });
            $('#comfirm').dialog('open');
        });
    },100);


    // 发布阶段点击
    $('input[name="stage"]').click(function(e){
        //alert($(this).val());
        stage = $(this).val();
        $.ajax({
            type:'POST',
            url : '/release/getEnvByStep/',
            data:{
                'env_step':stage,
            },
            success:function(data){
                if(data){
                    console.log(data);
                    var obj = $('.pro_main').find('li').remove().end().find('ul');
                    $(data).each(function(i){
                        obj.append('<li><label><input name="envtype" type="radio" value="'+ data[i] +'" />'+ data[i] +'</label></li>');
                    });
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown){
                alert('出现错误：' + errorThrown);
            }
        });

    });

    // 选择应用 全选
    $('input[name="all"]').click(function(){
        $('input[name="app"]').each(function(){
            if(!$(this).prop("checked")){
                $(this).prop("checked", true);
            }
        });
        $('input[name="notall"]').prop('checked', false);
    });
    // 选择应用 全不选
    $('input[name="notall"]').click(function(){
        $('input[name="app"]').each(function(){
            if($(this).prop("checked")){
                $(this).prop("checked", false);
            }
        });
        $('input[name="all"]').prop('checked', false);
    });



    //setTimeout(function(){
        //var stage = $('input[name="stage"]').val();
    $('.env ul').on('click', 'li', function(){                  // 动态绑定，将值赋值到对话框数据总
        env = $(this).find('input[name="envtype"]').val();

        $.ajax({
            type:'POST',
            url : '/release/getSystemInfo/',
            data:{
                'env':env,
            },
            success:function(data){
                if(data){
                    console.log(data);
                    var obj = $('select[name="project"]').find('option').remove().end();
                    $('select[name="project"]').append('<option value="0">--请选择--</option>');
                    $(data).each(function(i){
                        obj.append('<option value="'+ data[i][1] +'">'+ data[i][0] +'</option>');
                    });
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown){
                alert('出现错误：' + errorThrown);
            }
        });

        //alert(stage + '|' + env);
        $('#stage').html(stage);                                  // 设置 阶段
        $('#env').html(env);                                      // 设置 环境类型
    });
    //},100);

    //alert(cu_val + '|' + cu_text);
    // 项目名称下拉列表 点击事件
    $('select[name="project"]').bind('change', 'select', function(e){
        cu_val = $(this).val();
        cu_text = $(this).text()
        $.ajax({
            type:'POST',
            url : '/release/getVersionByEnvAndSysCode/',
            data:{
                'env':env,
                'code':cu_val,
            },
            success:function(data){
                if(data){
                    var obj = $('select[name="version"]').find('option').remove().end();
                    $('select[name="version"]').append('<option value="0">--请选择--</option>');
                    $(data).each(function(i){
                        obj.append('<option value="'+ data[i] +'">'+ data[i] +'</option>');
                    });
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown){
                alert('出现错误：' + errorThrown);
            }
        });
    });


    // 版本 下拉列表事件
    $('select[name="version"]').bind('change', 'select', function(){
        version = $(this).val();
        $.ajax({
            type:'POST',
            url : '/release/getPkgName/',
            data:{
                'env':env,
                'code':cu_val,
                'version':version,
            },
            success:function(data){
                if(data){
                    var obj = $('.select_app').find('label').remove().end();
                    $(data).each(function(i){
                        obj.append('<label><input name="app" type="checkbox" value="'+ data[i] +'" />'+ data[i] +'</label>');
                    });
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown){
                alert('出现错误：' + errorThrown);
            }
        });
    });


});
