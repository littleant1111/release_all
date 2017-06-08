/**
 * Created by wangzi on 2017/3/7.
 */
$(function () {

    //table2_demo4_js_start
    //表格(DataTables)-4，综合示例
    var language = {
        search: '搜索：',
        lengthMenu: "每页显示 _MENU_ 记录",
        zeroRecords: "没找到相应的数据！",

        info: "分页 _PAGE_ / _PAGES_",
        infoEmpty: "暂无数据！",
        infoFiltered: "(从 _MAX_ 条数据中搜索)",
        paginate: {
            first: '首页',
            last: '尾页',
            previous: '上一页',
            next: '下一页',
        }
    };
    // refreshdatatable(selectsystem);
    //
    // function refreshdatatable(selectsystem) {
    //        $("#table2_demo5").dataTable({
    //
    //     autoWidth: false,
    //     lengthChange: true, //不允许用户改变表格每页显示的记录数
    //     pageLength: 100, //每页显示几条数据
    //     lengthMenu: [5, 10, 20], //每页显示选项
    //     pagingType: 'full_numbers',
    //     ajax: '/release/getbsdetail/',
    //     ordering: true,
    //     // "scrollX": true,
    //                   queryParams: {
    //             selectsystem: selectsystem,
    //         },
    //
    //     columns: [
    //         {data: "envchild_name"},
    //         {data: "project_name"},
    //         {data: "app_name"},
    //         {data: "ip"},
    //         {data: "user"},
    //         {data: "appdir"},
    //         // {
    //         //     data: null,
    //         //     orderable: false,
    //         //     // render: function (data, type, row, meta) {
    //         //     //     return '<a class="king-btn king-default del">发布详情</a>';
    //         //     // }
    //         // }
    //     ],
    //     language: language,
    // });
    // }




    // var t = $("#table2_demo4").DataTable();//获取datatables对象
    // // 删除按钮绑定事件
    // $("#table2_demo4 tbody").on('click', 'a.del', function () {
    //     var row = t.row($(this).parents('tr')),//获取按钮所在的行
    //         data = row.data();
    //     window.console.log(data);
    //
    //     str = data['apps'];
    //     var strs = new Array(); //定义一数组
    //     var strswar = new Array(); //定义一数组
    //
    //     strs = str.split(","); //字符分割
    //     for (var i = 0; i < strs.length; i++) {
    //         strswar[i] = strswar[i] + '.war';
    //     }
    //     var projectdata = {
    //         'project': [{'app': strswar, 'version': data['version'], 'name': data['project_code']}],
    //         'envtype': data['env'],
    //         'taskid': data['id'],
    //         'apps': strs,
    //
    //     };
    //     $.ajax({
    //         type: 'POST',
    //         url: '/release/taskBegin/',
    //         data: JSON.stringify(projectdata),
    //         dataType: 'json',
    //         beforeSend: function (jqXR, settings) {
    //             $('#comfirm').dialog('close');
    //             $('#loadding').dialog('open');
    //         },
    //         success: function (projectdata) {
    //             $('#loadding').dialog('close');
    //             if (projectdata == 'true') {
    //                 location.href = '/release/detail/';   // 跳转到指定页面
    //             } else {
    //                 alert('error');
    //             }
    //         },
    //         error: function (XMLHttpRequest, textStatus, errorThrown) {
    //             $('#loadding').dialog('close');
    //             $('#error').find('span')
    //                 .text('错误信息,textStatus:' + textStatus + 'errorThrown:' + errorThrown).end().dialog('open');
    //         },
    //     });
    //
    //     // if(confirm('确定要删除'+data.name+' ?')){
    //     //   row.remove().draw();
    //     // }
    //
    // });
    // //table2_demo4_js_end
});