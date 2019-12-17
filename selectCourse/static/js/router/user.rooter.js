$(document).ready(function () {
    removeCookie('role');
    if(getCookie('role') === null){
        window.location.href= 'login.html';
    }else {
        $('.index-container').css('display','block');
        switch (getCookie('role')) {
            case 'root':
                $('#root-menu').css('display','block');break;
            case 'instructor':
                $('#instructor-menu').css('display','block');break;
            case 'student':
                $('#student-menu').css('display','block');break;
        }
    }
});