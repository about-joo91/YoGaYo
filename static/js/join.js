const user_email = document.querySelector('#user_email');
const nick_name = document.querySelector('#nick_name');
const user_password = document.querySelector('#user_password');

// 자기 주소 작성할 것
const back_url = 'http://192.168.0.23:8080';

async function sign_up() {
    let user_email_value = user_email.value;
    let nick_name_value = nick_name.value;
    let user_password_value = user_password.value;

    if (user_email_value == "") {
        alert("이메일 주소를 입력하셔요")
        user_email.focus();
        return;
    }
 
    if (nick_name_value == "") {
        alert("닉네임을 입력하셔요")
        nick_name.focus()
        return;
    }
    
    if (user_password_value == "") {
        alert("비밀번호를 입력하셔요")
        user_password.focus()
        return;
    }

    const request_body = {
        user_email_give : user_email_value,
        user_password_give : user_password_value,
        nick_name_give : nick_name_value
    }

    const response = await fetch(back_url+'/sign_up',{
        method:'POST',
        body: JSON.stringify(request_body),
    });

    const data = await response.json();

    alert(data['msg']);
}

const join_button = document.querySelector('#join_button');

join_button.addEventListener('click',sign_up)