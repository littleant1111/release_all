$(function(){

    var waitDialog = dialog({   // 加载对话框
            width: 200,
            content: '<img class="mr5" src="https://magicbox.bkclouds.cc/static_api/v3/components/loading1/images/loading_2_16x16.gif">请稍后，加载中...'
        });

    function success(data){     // 提交成功提示信息
        var animation = $(this).attr('data-animation');
        toastr.remove();
        toastr.success('<br>'+ data,'提示',{
            timeOut:1500,
            showMethod :animation
        });
    }

    function error(data){          //  错误时候提示信息
        var animation = $(this).attr('data-animation');
        toastr.remove();
        toastr.error('<br>'+ data,'提示',{
            timeOut:1500,
            showMethod :animation
        });
    }

//    function ajax_submit(){
//    }

    //  保存按钮点击
    $('#submit').click(function(e){
        var id = $('#id').val();
        var user = $('#user').val();
        var password = $('#password').val();
        var homedir = $('#homedir').val();
        var sshport = $('#sshport').val();
        var machine_id = $('input[name="machine_id"]:checked').val();
        $.ajax({                                          // 提交数据表单
            type:'POST',
            url : '/r_admin/editUser/',
            data: JSON.stringify({
                id : id,
                name : user,
                password : password,
                home_dir : homedir,
                sshport : sshport,
                machine_id : machine_id,
            }),
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                window.console.log(data);
                if (data == '1'){
                    success('保存用户成功！');
                    location.href = '/r_admin/user_list/';
                }else{
                    error('保存用户失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '保存用户失败');
            },
        });
    });

});