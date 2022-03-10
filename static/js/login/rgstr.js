function userRgstr() {
    $.ajax({
        type: "POST",
        url: "/login/userRgstr",
        data: {
            userName: $('#userName').val(),
            userId: $('#userId').val(),
            userPwd: $('#userPwd').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login/login'
            } else {
                alert(response['msg'])
            }
        }
    })
}