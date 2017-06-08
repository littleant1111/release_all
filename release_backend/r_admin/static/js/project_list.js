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

    $('input[name="refresh"]').click(function(e){
        window.location.reload(true);
    });

    // 加载网页时候调用
//    $.ajax({
//        type:'POST',
//        url : '/r_admin/getProjectList/',
//        data: {},
//        cache: false,
//        beforeSend:function(jqXR, settings){
//            waitDialog.show();
//        },
//        success:function(data){
//            waitDialog.close();
//            var obj = $('.tbody-content');
//            obj.find('*').remove();
//            if(data){
//                $(data).each(function(i){
//                    obj.append('<tr><td>'+ i +'</td><td>'+ data[i][1] +'</td><td>'+ data[i][2] +'</td><td class="action"><input class="input-admin" type="hidden" name="id" value="'+ data[i][0] +'"><input class="input-admin" type="button" name="edit" value="编辑"><input class="input-admin" type="button" name="delete" value="删除"></td></tr>');
//                });
//                loadedRun();
//            }
//        },
//        complete: function(XMLHttpRequest, textStatus) {
//            waitDialog.close();
//        },
//    });


//    function loadedRun(){          // 网页ajax 加载后运行

        $('input[name="edit"]').click(function(e){      // 编辑
            //error('功能开发中');
            var id = $(this).prev('input[name="id"]').val();
            location.href = '/r_admin/edit_project/?id=' + id;
        });

        $('input[name="delete"]').click(function(e){      // 删除按钮
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
                        url : '/r_admin/deleteProject/',
                        data: {
                            'id' : id,
                        },
                        beforeSend:function(jqXR, settings){
                            waitDialog.show();
                        },
                        success:function(data){
                            waitDialog.close();
                            if (parseInt(data) >= '0'){
                                success('删除项目成功！');
                                window.location.reload(true);
                            }else{
                                error('删除项目失败！');
                            }
                        },
                        error : function(XMLHttpRequest, textStatus, errorThrown) {
                            error('错误！' + errorThrown + '删除项目失败');
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

//    }

});