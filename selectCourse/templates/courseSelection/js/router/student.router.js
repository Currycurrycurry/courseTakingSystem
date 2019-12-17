$(document).ready(function () {
    if(getCookie('role') !== 'student'){
        window.location.href= 'login.html';
    } else {
        $('.student-container').css('display','block')
    }

});