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

    function ajax_submit(){
        var name = $('input[name="name"]').val();
        var env = $('input:radio[name="env"]:checked').val();
//        alert('name:'+name + 'env:' +env);
        $.ajax({                             // 提交数据表单
            type:'POST',
            url : '/r_admin/addEnv/',
            data: {
                name : name,
                env : env,
            },
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                if (data != ''){
                    success('添加环境成功！');
                }else{
                    error('添加环境失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '添加环境失败');
            },
            complete: function(XMLHttpRequest, textStatus) {
                waitDialog.close();
            },
        });
    }

//    $('#submit').click(function(e){
//    });

    $('#add_env').validate({
        rules:{
            name:{
                required : true,
                minlength : 2,
            },
            env:{
                required : true,
            },
        },
        messages:{
            name:{
                required : '请填写环境名称！',
                minlength : '不得小于{0}位！',
            },
            env:{
                required : '请选择发布阶段',
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