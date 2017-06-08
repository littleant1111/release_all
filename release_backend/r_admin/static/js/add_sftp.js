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

    function ajax_submit() {
//        var item = $('input[name="item"]').val();
        var item = $('select[name="item"]').val();
        var value = $('input[name="value"]').val();
        var remark = $('input[name="remark"]').val();
        var project_id = $('input:radio[name="project_id"]:checked').val();
        var env_id = $('input:radio[name="env_id"]:checked').val();
//        alert('item:'+item + ' value:' +value+' remark:' +remark + ' project_id:'+project_id+' env_id:'+env_id);
        $.ajax({                             // 提交数据表单
            type:'POST',
            url : '/r_admin/addSftp/',
            data: {
                item : item,
                value : value,
                remark : remark,
                project_id : project_id,
                env_id : env_id,
            },
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                if (data != ''){
                    success('添加sftp信息成功！');
//                    location.href = '/r_admin/sftp_list/';
                }else{
                    error('添加sftp信息失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '添加sftp信息失败');
            },
            complete: function(XMLHttpRequest, textStatus) {
                waitDialog.close();
            },
        });
    }

//    $('#submit').click(function(e){
//    });


    $('#add_sftp_config').validate({
        rules:{
            item:{
                required : true,
            },
            value:{
                required : true,
            },
            remark:{
                required : true,
            },
            project_id:{
                required: true,
            },
            env_id:{
                required: true,
            },
        },
        messages:{
            item:{
                required : '请选择项目！',
            },
            value:{
                required : '请填写值！',
            },
            remark:{
                required : '请填写描述信息！',
            },
            project_id:{
                required : '请选择项目！',
            },
            env_id:{
                required : '请选择环境！',
            },
        },
        highlight: function(element, errorClass, validClass) {
            $(element).css({
                'border' : '2px solid red',
            }).removeClass('succ').addClass('my_error');
        },
        unhighlight: function(element, errorClass) {
            $(element).css({
                'border' : '1px solid #ccc',
            }).removeClass('my_error').addClass('succ');
        },
        submitHandler: function(form){
            ajax_submit();
        },
        errorContainer : '.my_errors',
        errorLabelContainer : '.my_errors',
        wrapper: 'li',

    });


});