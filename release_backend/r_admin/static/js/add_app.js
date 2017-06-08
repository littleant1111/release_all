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

    function success2(data){
        $('.king-success').click(function (){
            $topBar({
                text:data,
                setClass:'bg-success'
            });
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

    function error2(data,the_time){                //  错误时候提示信息
        var animation = $(this).attr('data-animation');
        toastr.remove();
        toastr.error('<br>'+ data,'提示',{
            timeOut:the_time,
            showMethod :animation
        });
    }


    $('input[name="refresh"]').click(function(e){   // 刷新
        window.location.reload(true);
    });


    function ajax_submit(){
        var name = $('input[name="name"]').val();
        var user = $('input[name="user"]').val();
        var pkgname = $('input[name="pkgname"]').val();
        var dir = $('input[name="dir"]').val();
        var port = $('input[name="port"]').val();
        var seqence = $('input[name="seqence"]').val();
        var project_id = $('input:radio[name="project_id"]:checked').val();
        var machine_id = $('input:radio[name="machine_id"]:checked').val();
//        alert('name:'+name + 'env:' +env);
        var laststr = dir.substr(dir.length-1,1);
        if (laststr != '/'){
            var dir = dir + '/';
        }

        $.ajax({                             // 提交数据表单
            type:'POST',
            url : '/r_admin/addApp/',
            data: {
                name : name,
                user : user,
                pkgname : pkgname,
                dir : dir,
                port : port,
                seqence : seqence,
                project_id : project_id,
                machine_id : machine_id,
            },
            beforeSend:function(jqXR, settings){
                waitDialog.show();
            },
            success:function(data){
                waitDialog.close();
                if (data != ''){
                    success('添加应用成功！');
                }else{
                    error('添加应用失败！');
                }
            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
                error('错误！' + errorThrown + '添加应用失败');
            },
            complete: function(XMLHttpRequest, textStatus) {
                waitDialog.close();
            },
        });
    }



//    $('#submit').click(function(e){                // 提交
//    });

    $('#add_app').validate({
        rules:{
            name:{
                required : true,
                minlength : 2,
            },
            user:{
                required : true,
                minlength : 2,
            },
            pkgname:{
                required : true,
                minlength : 2,
                remote : {
                    type:"POST",
                    url:"/r_admin/checkAppName/",
                    data:{
                        appname:function(){return $("#name").val();},
                        pkgname:function(){return $("#pkgname").val();}
                    },
//                    success:function(data){
//                        waitDialog.close();
//                        if (data != true){
//                            $('#name').css('border','2px solid red');
//                            error2('应用名和包名 与 数据库中应用名和包名 不一致！', 3000);
//                        }
//                    },
                },
            },
            dir:{
                required: true,
            },
            port:{
                required: true,
            },
            seqence:{
                required: true,
            },
            project_id:{
                required: true,
            },
            machine_id:{
                required: true,
            },
        },
        messages:{
            name:{
                required : '请填写应用名称',
                minlength : '不得小于{0}位！',
            },
            user:{
                required : '请填写安装用户',
                minlength : '不得小于{0}位！',
            },
            pkgname:{
                required : '请填写ip地址',
                minlength : '不得小于{0}位！',
                remote : '填入的包名和应用名 与 数据库中包名应用名不一致！',
            },
            dir:{
                required : '必填',
            },
            port:{
                required : '必填',
            },
            seqence:{
                required: '必填',
            },
            project_id:{
                required: '必选',
            },
            machine_id:{
                required: '必选',
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
        }

    });



});