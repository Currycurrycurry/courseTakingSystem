$(document).ready(function () {
    alert(getCookie('role'));
    if(getCookie('role') !== 1){
        window.location.href= 'login.html';
    } else {
        $('.student-container').css('display','block')
    }

});