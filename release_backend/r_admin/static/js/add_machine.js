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


    // 加载网页时候调用
    $.ajax({
        type:'POST',
        url : '/r_admin/getEnvInfo/',
        data: {},
        beforeSend:function(jqXR, settings){
            waitDialog.show();
        },
        success:function(data){
            waitDialog.close();
            var obj = $('.env');
            obj.find('*').remove();
            if(data){
                $(data).each(function(i){
                    obj.append('<label class="mr10"><input type="radio" name="env"  class="bk-top5" value="'+ data[i][0] +'"><span class="bk-lh30">'+ data[i][1] +'</span></label>');
                });
            }
        },
        complete: function(XMLHttpRequest, textStatus) {
            waitDialog.close();
        },
    });

    function ajax_submit(){
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
            url : '/r_admin/addMachine/',
            data: {
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
                if (data != ''){
                    success('添加机器成功！');
                }else{
                    error('添加机器失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '添加机器失败');
            },
            complete: function(XMLHttpRequest, textStatus) {
                waitDialog.close();
            },
        });

    }

    //  保存按钮点击
//    $('#submit').click(function(e){
//    });


    $('#add-machine').validate({
        rules:{
            name:{
                required : true,
                minlength : 2,
            },
            host:{
                required : true,
                minlength : 2,
            },
            ip:{
                required : true,
                minlength : 2,
                remote : {
                    type:"POST",
                    url:"/r_admin/checkip/",
                    data:{
                        ip:function(){return $("#ip").val();}
                    }
                },
            },
            vm:{
                required: true,
            },
            env:{
                required: true,
            },
            cpu:{
                required: true,
            },
            memory:{
                required: true,
            },
        },
        messages:{
            name:{
                required : '请填写机器名称',
                minlength : '不得小于{0}位！',
            },
            host:{
                required : '请填写主机名称',
                minlength : '不得小于{0}位！',
            },
            ip:{
                required : '请填写ip地址',
                minlength : '不得小于{0}位！',
                remote : '机器IP已经录入！',
            },
            vm:{
                required : '必选是否是虚拟机',
            },
            env:{
                required : '必选环境类型',
            },
            cpu:{
                required: '必填cpu信息',
            },
            memory:{
                required: '必填内存信息',
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
        //errorContainer : '.my_errors',
        errorLabelContainer : '.my_errors',
        wrapper: 'li',
    });

});