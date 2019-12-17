$(document).ready(function () {
    alert(getCookie('role'));
    if(getCookie('role') !== 2){
        window.location.href= 'login.html';
    } else {
        $('.instructor-container').css('display','block')
    }

});