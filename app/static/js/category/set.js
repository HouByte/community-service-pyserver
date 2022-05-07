;
var account_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_account_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复提交~~");
                return;
            }

            var name_target = $(".wrap_account_set input[name=name]");
            var name = name_target.val();

            var weight_target = $(".wrap_account_set input[name=weight]");
            var weight = weight_target.val();

            var id = $(".wrap_account_set input[name=id]").val()
            if (id.trim () === ''){
                id = undefined
            }

            if (name.trim () === ''){
                name_target = undefined
            }

            if (name.length < 1) {
                common_ops.tip("请输入符合规范的类名~", name_target);
                return false;
            }

            //btn_target.addClass("disabled");

            var data = {
                name: name,
                weight: weight,
                id: id
            };

            $.ajax({
                url: common_ops.buildUrl("/category/set"),
                type: "POST",
                data: data,
                dataType: "json",
                success: function (res) {
                    //btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/category/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                },
                error:common_ops.errorHandle
            })

        });
    }
};

$(document).ready(function () {
    account_set_ops.init();
});