function showMessage(message, type = 2, time=1000, wait=0) {
    let ele = $("#myModal .modal-body p");
    $(ele).html(message);
    let color;
    if(type===2) {
        color = "#31708f"; // 提示
    } else if(type === 1 ) {
        color = "#3c763d"; //成功
    } else {
        color = "#8a6d3b"; // 警告
    }
    $(ele).css("color",color);
    $("#myModal").modal('show');
    if(!wait){ // 不等待
        setTimeout(function () {
            $("#myModal").modal('hide');
        },time)
    }
}