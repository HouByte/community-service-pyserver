;
var member_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });
        $(".remove").click(function () {
            that.ops("remove", $(this).attr("data"));
        });
        $(".lock").click(function () {
            that.ops("lock", $(this).attr("data"));
        });
        $(".recover").click(function () {
            that.ops("recover", $(this).attr("data"));
        });
    },
    ops: function (act, id) {
        var callback = {
            "ok": function () {
                $.ajax({
                    url: common_ops.buildUrl("/member/ops"),
                    type: "POST",
                    data: {
                        act: act,
                        id: id
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        if (res.code == 200) {
                            callback = function () {
                                window.location.href = window.location.href;
                            }
                        }
                        common_ops.alert(res.msg, callback);
                    },
                    error:common_ops.errorHandle
                });
            },
            "cancel": null
        };
        var tip = ''
        switch (act) {
            case 'remove':
                tip = '确定删除？'
                break
            case 'recover':
                tip = '确定恢复？'
                break
            case 'lock':
                tip = '确定冻结？'
                break
        }
        common_ops.confirm(tip, callback);
    }
};

$(document).ready(function () {
    member_index_ops.init();
});