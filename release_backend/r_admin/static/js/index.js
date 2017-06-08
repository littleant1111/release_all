$(function(){

    // 默认显示添加主机页面
    $('.main').find('*').remove().end().append($('#add-machine').html());

    $('#c_add_machine').click(function(e){            // 添加机器按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#add-machine').html());
        //$('#add-machine').show();
    });
    $('#c_machine_list').click(function(e){         // 机器列表按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#machine_list').html());
    });


    $('#c_add_project').click(function(e){         // 添加项目 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#add_project').html());
    });
    $('#c_project_list').click(function(e){         // 项目列表 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#project_list').html());
    });


    $('#c_add_env').click(function(e){         // 添加环境 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#add_env').html());
    });
    $('#c_env_list').click(function(e){         // 环境列表 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#env_list').html());
    });

    $('#c_add_app').click(function(e){         // 添加应用 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#add_app').html());
    });
    $('#c_app_list').click(function(e){         // 应用列表 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#app_list').html());
    });

    $('#c_add_sftp_config').click(function(e){         // 添加 sftp配置 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#add_sftp_config').html());
    });
    $('#c_sftp_config_list').click(function(e){         // sftp配置列表 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#sftp_config_list').html());
    });


    $('#c_add_user').click(function(e){         // 添加 用户 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#add_user').html());
    });
    $('#c_user_list').click(function(e){         // 用户列表 按钮点击
        $('.main').find('*').remove().end().text('');
        $('.main').append($('#user_list').html());
    });
});