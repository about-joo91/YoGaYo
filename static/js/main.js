// function posting() {     let title = $('#title').val()     let file =
// $('#file')[0].files[0]     let form_data = new FormData()
// form_data.append("title_give", title)     form_data.append("file_give", file)
// $.ajax({         type: "POST",         url: "/fileupload",         data:
// form_data,         cache: false,         contentType: false,
// processData: false,         success: function (response) {
// alert(response["result"])             window.location.reload()         }
// });   }
const base_url = "http://192.168.45.104:8080"
const file_input = document.getElementById('file');
const preview_img_box = document.querySelector('.preview_img_box')
file_input.addEventListener('change', function () {
    const file_list = this.files
    let file = file_list[0]
    const reader = new FileReader();
    reader.onload = () => {
        preview_img_box.innerHTML += `
        <img class ='um_preview_image' src= "${reader.result}">
        `
    }
    reader.readAsDataURL(file)
})


function posting() {
    let title = document.getElementById('title').value
    let file = document.getElementById('file').files[0]
    console.log(file)
    let form_data = new FormData()

    form_data.append("title_give", title)
    form_data.append("file_give", file)

    fetch(base_url + "/fileupload", {
        method: "POST",
        body: form_data
    })
    alert("다이어리에서 당신의 정확도를 확인하세요!!");
}
function find_img() {
    // $('#find_title').val() 퓨어 자바스크립트 변환
    let title = document
        .getElementById('find_title')
        .value
    document
        .getElementById('link')
        .href = '/fileshow/' + title
}

// 모달 
const modal = document.getElementById("modal")
const btnModal = document.getElementById("modal_button")
btnModal.addEventListener("click", e => {
    modal.style.display = "flex"
    modal.style.position = "fixed";
    document.body.style.overflow = 'hidden';
})

const closeBtn = modal.querySelector(".close-area")
closeBtn.addEventListener("click", e => {
    modal.style.display = "none"
    document.body.style.overflow = "auto";
})

modal.addEventListener("click", e => {
    const evTarget = e.target
    if (evTarget.classList.contains("upload_modal_wrapper")) {
        modal.style.display = "none"
        document.body.style.overflow = "auto";
    }
})
const pop_up_modal_wrapper = document.querySelector('.pop_up_modal_wrapper');
const pum_x_btn = document.querySelector('.pum_x_btn');
pum_x_btn.addEventListener('click', function () {
    pop_up_modal_wrapper.style.display = 'none'
})
const pum_r_btn = document.querySelector('.pum_r_btn');
pum_r_btn.addEventListener('click', function () {
    pop_up_modal_wrapper.style.display = 'none'
    modal.style.display = 'flex'
    document.body.style.overflow = 'hidden';
})