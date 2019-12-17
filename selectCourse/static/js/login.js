$(document).ready(function () {
    initResource();
    bindEvents();
});

function bindEvents() {
    $("#login-btn").click(function () {
        if (checkData()) {
            let username = $("#inputUsername").val();
            let pwd = $("#inputPassword").val();
            let data = {'user_id': username, 'password': pwd};
            $.ajax({
                url:"/selectCourse/login/",
                type:"post",
                datatype:"json",
                data: data,
                async: false,
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                success: function(response) {
                    if(response['code'] == 1){
                        showMessage("登录成功，即将跳转。",1);
                        setTimeout(function () {
                        // window.location.href = goBack($(".login-body").attr("id"));
                        window.location.href="/selectCourse/index.html";
                    },500);
                    }
                    if (response['code'] == -1){
                        showMessage("登录失败，请检查用户名或密码是否正确。",2);
                    }
                    
                }
            });

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