$(document).ready(function () {
    if(getCookie('role') !== 'root'){
        window.location.href= 'login.html';
    }else {
        $('.root-container').css('display','block')
    }
});