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

    function ajax_submit(){
        var user = $('input[name="user"]').val();
        var password = $('input[name="password"]').val();
        var homedir = $('input[name="homedir"]').val();
        var sshport = $('input[name="sshport"]').val();
        var machine_id = $('input:radio[name="machine_id"]:checked').val();
        $.ajax({                             // 提交数据表单
            type:'POST',
            url : '/r_admin/addUser/',
            data: {
                user : user,
                password : password,
                homedir : homedir,
                sshport : sshport,
                machine_id : machine_id,
            },
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                if (data != ''){
                    success('添加用户成功！');
                }else{
                    error('添加用户失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '添加用户失败');
            },
            complete: function(XMLHttpRequest, textStatus) {
                waitDialog.close();
            },
        });
    }

//    $('#submit').click(function(e){
//    });

    $('#add_user').validate({
        rules:{
            user:{
                required : true,
                minlength : 2,
            },
            password:{
                required : true,
                minlength : 4,
            },
            homedir:{
                required : true,
                minlength : 2,
            },
            sshport:{
                required: true,
            },
            machine_id:{
                required: true,
                remote : {
                    type:"POST",
                    url:"/r_admin/checkUserMachineExists/",
                    data:{
                        user:function(){return $('input[name="user"]').val();},
                        machine_id:function(){return $('input:radio[name="machine_id"]:checked').val();}
                    }
                }
            },
        },
        messages:{
            user:{
                required : '请填写用户名称',
                minlength : '不得小于{0}位！',
            },
            password:{
                required : '请填写用户密码',
                minlength : '不得小于{0}位！',
            },
            homedir:{
                required : '请填写用户家目录',
                minlength : '不得小于{0}位！',
            },
            sshport:{
                required : 'ssh端口必填',
            },
            machine_id:{
                required : '机器必选',
                remote : '此用户在此机器上已经存在！',
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
        errorContainer : '.my_errors',
        errorLabelContainer : '.my_errors',
        wrapper: 'li',

        submitHandler: function(form){
            ajax_submit();
        }

    });



});