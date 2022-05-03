;

var user_edit_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".user_edit_wrap .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复提交~~");
                return;
            }

            var nickname_target = $(".user_edit_wrap input[name=nickname]");
            var nickname = nickname_target.val();

            var email_target = $(".user_edit_wrap input[name=email]");
            var email = email_target.val();

            var mobile_target = $(".user_edit_wrap input[name=mobile]");
            var mobile = mobile_target.val();

            var sex_target = $(".user_edit_wrap input[name=sex]");
            var sex = sex_target.val();

            if (!mobile || mobile.length < 2) {
                common_ops.tip("请输入符合规范的手机号~", mobile_target);
                return false;
            }

            var telReg = !!mobile.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/);
            //如果手机号码不能通过验证
            if(telReg == false){
                common_ops.tip("请输入符合规范的手机号~", mobile_target);
                return false;
            }

            if (!nickname || nickname.length < 2) {
                common_ops.tip("请输入符合规范的姓名~", nickname_target);
                return false;
            }

            if (!email || email.length < 2) {
                common_ops.tip("请输入符合规范的邮箱~", email_target);
                return false;
            }

            var emailReg = !!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/);
            //如果邮箱不能通过验证
            if(emailReg == false){
                common_ops.tip("请输入符合规范的邮箱~", email_target);
                return false;
            }



            btn_target.addClass("disabled");
            var data = {
                nickname: nickname,
                email: email,
                mobile: mobile,
                sex: sex
            }

            $.ajax({
                url: common_ops.buildUrl("/user/edit"),
                type: "POST",
                data: data,
                dataType: "json",
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })

        });
    }
};

$(document).ready(function () {
    user_edit_ops.init();
});