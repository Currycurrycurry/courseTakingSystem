$(document).ready(function () {
    initResource();
    bindEvents();
});

function bindEvents() {
    $("#login-btn").click(function () {
        if (checkData()) {
            let username = $("#inputUsername").val();
            let pwd = $("#inputPassword").val();
            let data = {'username': username, 'pwd': pwd};
            $.when(login(data))
                .done(function () {
                    showMessage("登录成功，即将跳转。",1);
                    setTimeout(function () {
                        window.location.href = goBack($(".login-body").attr("id"));
                    },500);
                }).fail(function () {
                showMessage("登录失败，请检查用户名或密码是否正确。",2);
            })
        }
    });
}
function checkData() {
    let legal = true;
    let name = $("#inputUsername").val();
    let pwd = $("#inputPassword").val();
    if(name == '') {
        $("#name_info").css('visibility','visible');
        legal = false;
    }
    if(pwd == '') {
        $("#pwd_info").css('visibility','visible');
        legal = false;
    }
    setTimeout(function () {
        $(".info").css('visibility','hidden');
    },1500);
    return legal;
}


function initResource() {

}