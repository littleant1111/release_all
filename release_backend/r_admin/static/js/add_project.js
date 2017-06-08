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

//    $.ajax({           // 加载网页时候调用
//        type:'POST',
//        url : '/r_admin/getEnvInfo/',
//        data: {},
//        beforeSend:function(jqXR, settings){
//            waitDialog.show();
//        },
//        success:function(data){
//            waitDialog.close();
//            var obj = $('.env');
//            obj.find('*').remove();
//            if(data){
//                $(data).each(function(i){
//                    obj.append('<label class="mr10"><input type="checkbox" name="env"  class="bk-top5" value="'+ data[i][0] +'"><span class="bk-lh30">'+ data[i][1] +'</span></label>');                });
//            }
//        },
//        complete: function(XMLHttpRequest, textStatus) {
//            waitDialog.close();
//        },
//    });

    function ajax_submit(){
        var name = $('#name').val();
        var remark = $('#remark').val();
        var env_arr = [];
        $('input[name="env"]:checked').each(function(){
            env_arr.push($(this).val());
        });
        window.console.log(env_arr);
//        alert('arr:' + arr);
//        return;

        $.ajax({                             // 提交数据表单
            type:'POST',
            url : '/r_admin/addProject/',
            data : JSON.stringify({
                name : name,
                remark : remark,
                env : env_arr
            }),
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                if (data != ''){
                    success('添加项目成功！');
                }else{
                    error('添加项目失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '添加项目失败');
            },
            complete: function(XMLHttpRequest, textStatus) {
                waitDialog.close();
            },
        });
    }


//    $('#submit').click(function(e){
//    });

    $('#add_project').validate({
        rules:{
            name:{
                required : true,
                minlength : 3,
                remote : {
                    type:"POST",
                    url:"/r_admin/checkProjectCode/",
                    data:{
                        pro_code:function(){return $("#name").val();}
                    }
                },
            },
            remark:{
                required : true,
                minlength : 2,
            },
            env : {
                required : true,
            },
        },
        messages:{
            name:{
                required : '请填写机器名称',
                minlength : '不得小于{0}位！',
                remote : '项目编码已经存在！',
            },
            remark:{
                required : '请填写主机名称',
                minlength : '不得小于{0}位！',
            },
            env : {
                required : '必选环境类型',
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
        errorLabelContainer : '.my_errors',
        wrapper: 'li',

    });


});
