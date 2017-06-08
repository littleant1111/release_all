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

    $('input[name="refresh"]').click(function(e){    // 刷新 点击按钮
        window.location.reload(true);
    });

//    $('input[name="edit"]').click(function(e){      //
//        error('此项不能编辑，只能删除！');
//    });

    $('input[name="delete"]').click(function(e){
        var id = $(this).parent().find('input[name="id"]').val();
        //        alert('id:'+id);
        var d = dialog({
            width: 300,
            title: '提示',
            quickClose: true,
            content: '确定要删除吗！',
            ok: function() {
                $.ajax({                             // 提交数据表单
                    type:'POST',
                    url : '/r_admin/deleteSftp/',
                    data: {
                        'id' : id,
                    },
                    beforeSend:function(jqXR, settings){
                        waitDialog.show();
                    },
                    success:function(data){
                        waitDialog.close();
                        window.console.log('ssssssssssssssssssss'+ data);
                        if (parseInt(data) >= '0'){
                            success('删除sftp配置项成功！');
                            window.location.reload(true);
                        }else{
                            error('删除sftp配置项失败！');
                        }
                    },
                    error : function(XMLHttpRequest, textStatus, errorThrown) {
                        error('错误！' + errorThrown + '删除sftp配置项失败');
                    },
                    complete: function(XMLHttpRequest, textStatus) {
                        waitDialog.close();
                    },
                });
            },
            cancelValue: '取消',
            cancel: function() {
            },
            onshow: function() {
            }
        });
        d.show();
    });

});