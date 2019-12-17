$(document).ready(function () {
    if(getCookie('role') !== 'instructor'){
        window.location.href= 'login.html';
    } else {
        $('.instructor-container').css('display','block')
    }

});