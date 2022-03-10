function userLogin() {
    $.ajax({
        type: "POST",
        url: "/login/userLogin",
        data: {
            userId: $('#userId').val(),
            userPwd: $('#userPwd').val()
        },
        success: function (response) {
            console.log(response)
            if (response['result'] == 'success') {
                alert("로그인완료")
                $.cookie('mytoken', response['token'],{ path : '/'});
                window.location='/';
            } else {
                alert(response['msg']);
            }
        }
    })
}