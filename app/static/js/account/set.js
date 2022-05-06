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

            var nickname_target = $(".wrap_account_set input[name=nickname]");
            var nickname = nickname_target.val();

            var mobile_target = $(".wrap_account_set input[name=mobile]");
            var mobile = mobile_target.val();

            var email_target = $(".wrap_account_set input[name=email]");
            var email = email_target.val();

            var login_name_target = $(".wrap_account_set input[name=login_name]");
            var login_name = login_name_target.val();

            var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
            var login_pwd = login_pwd_target.val();

            var sex_target = $(".wrap_account_set input[name=sex]:checked");
            var sex = sex_target.val();

            var id = $(".wrap_account_set input[name=id]").val()
            if (id.trim () === ''){
                id = undefined
            }

            if (login_pwd.trim () === ''){
                login_pwd = undefined
            }

            if (nickname.length < 1) {
                common_ops.tip("请输入符合规范的姓名~", nickname_target);
                return false;
            }

             if (mobile.length < 1) {
                common_ops.tip("请输入符合规范的手机号码~", mobile_target);
                return false;
            }

            var telReg = !!mobile.match(/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/);
            //如果手机号码不能通过验证
            if(telReg == false){
                common_ops.tip("请输入符合规范的手机号~", mobile_target);
                return false;
            }

            if (email.length < 1) {
                common_ops.tip("请输入符合规范的邮箱~", email_target);
                return false;
            }
            var emailReg = !!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/);
            //如果邮箱不能通过验证
            if(emailReg == false){
                common_ops.tip("请输入符合规范的邮箱~", email_target);
                return false;
            }

            if (login_name.length < 1) {
                common_ops.tip("请输入符合规范的登录用户名~", login_name_target);
                return false;
            }

            //4到16位，字母数字下划线，减号
            var loginNameReg = !!login_name.match( /^[-_a-zA-Z0-9]{4,16}$/);
            //如果用户名不能通过验证
            if(loginNameReg == false){
                common_ops.tip("请输入符合规范的登录用户名(4到16位，字母数字下划线，减号 )~", login_name_target);
                return false;
            }

            if (login_pwd === undefined && id === undefined){
                 common_ops.tip("请输入符合规范的登录密码~", login_pwd_target);
                 return false;
            }

            if (login_pwd !== undefined){
                if (login_pwd.length < 6) {
                    common_ops.tip("请输入符合规范的登录密码~", login_pwd_target);
                    return false;
                }

                //至少6-16个字符，至少1个大写字母，1个小写字母和1个数字
                var loginPwdReg = !!login_pwd.match( /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{6,16}$/);
                //如果登录密码不能通过验证
                if(loginPwdReg == false){
                    common_ops.tip("请输入符合规范的登录密码~", login_pwd_target);
                    return false;
                }
            }





            //btn_target.addClass("disabled");

            var data = {
                nickname: nickname,
                mobile: mobile,
                email: email,
                login_name: login_name,
                login_pwd: login_pwd,
                sex: sex,
                id: id
            };

            $.ajax({
                url: common_ops.buildUrl("/account/set"),
                type: "POST",
                data: data,
                dataType: "json",
                success: function (res) {
                    //btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/account/index");
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