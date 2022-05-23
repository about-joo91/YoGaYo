const user_email = document.querySelector('#user_email');
const nick_name = document.querySelector('#nick_name');
const user_password = document.querySelector('#user_password');

async function sign_up() {
    let user_email_give = user_email.value;
    let nick_name_give = nick_name.value;
    let user_password_give = user_password.value;

    if (user_email_give == "") {
        alert("email 주소가 비어있으셔요.")
        user_email.focus();
        return;
    }

    if (nick_name_give == "") {
        alert("nick_name 칸이 비어있으셔요.")
        nick_name.focus()
        return;
    }

    if (user_password_give == "") {
        alert("비밀번호 칸이 비어있으셔요.")
        user_password.focus()
        return;
    }


    const request_body = {
        user_email_give: user_email_give,
        user_password_give: user_password_give,
        nick_name_give: nick_name_give
    }

    const response = await fetch('http:127.0.0.1:5000/login/sign_up', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify(request_body),

    })


}
// $.ajax({
//     type: "POST",
//     url: "/login/sign_up",
//     data: {
//         user_email_give : user_email_give,
//         user_password_give : user_password_give,
//         nick_name_give : nick_name_give,
//     },
//     success: function (response) {
//         alert(response['msg'])
//         window.location.replace(response['url'])
//     }
// });

const join_button = document.querySelector('#join_button');

join_button.addEventListener('click', sign_up)