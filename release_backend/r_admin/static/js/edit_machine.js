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
        var host = $('#host').val();
        var ip = $('#ip').val();
        var vm = $('input:radio[name="vm"]:checked').val();
        var cpu = $('#cpu').val();
        var memory = $('#memory').val();
        var env = $('input:radio[name="env"]:checked').val();
//        alert('vm' + vm + 'env' + env);
//        return
        $.ajax({                             // 提交数据表单
            type:'POST',
            url : '/r_admin/editMachine/',
            data: {
                id : id,
                name : name,
                host : host,
                ip : ip,
                vm : vm,
                cpu : cpu,
                memory : memory,
                env : env
            },
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                window.console.log(data);
                if (data == 'true'){
                    success('保存机器成功！');
                }else{
                    error('保存机器失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '保存机器失败');
            },
        });
    });

});