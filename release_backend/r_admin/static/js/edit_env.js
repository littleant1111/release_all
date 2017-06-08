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
        var name = $('#name').val();
        var step_id = $('input[name="env"]:checked').val();
        $.ajax({                                          // 提交数据表单
            type:'POST',
            url : '/r_admin/editEnv/',
            data: JSON.stringify({
                id : id,
                name : name,
                step_id : step_id
            }),
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                window.console.log(data);
                if (data){
                    success('保存环境成功！');
                    location.href = '/r_admin/env_list/';
                }else{
                    error('保存环境失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '保存环境失败');
            },
        });
    });

});