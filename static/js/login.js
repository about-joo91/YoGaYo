const user_email = document.querySelector('#user_email');
const user_password = document.querySelector('#user_password');

async function login() {
    let user_email_give = user_email.value;
    let user_password_give = user_password.value;

    if (user_email_give == "") {
        alert("email 주소가 비어있으셔요.")
        user_email.focus();
        return;
    }

    if (user_password_give == "") {
        alert("비밀번호 칸이 비어있으셔요.")
        user_password.focus();
        return;
    }

    const request_body = {
        user_email_give : user_email_give,
        user_password_give : user_password_give
    }

    const response = await fetch('http:127.0.0.1:8080/login',{
        method:'POST',
        body:request_body
    })
}

const login_button = document.querySelector('#login_button');

login_button.addEventListener('click',login)






// function sign_in() {
//     user_email = document.getElementById('user_email');
//     user_password = document.getElementById('user_password');

//     $.ajax({
//         type: 'POST',
//         url: '/login',
//         data: {
//             user_email_give: user_email,
//             user_password_give: user_password
//         },
//         success: function (response) {
//             if (response['result'] == 'success') {
//                 $.cookie('mytoken', response['token'], { path: '/' });
//                 window.location.replace('/main')
//             } else {
//                 alert(response['msg'])
//             }
//         }
//     });
// }