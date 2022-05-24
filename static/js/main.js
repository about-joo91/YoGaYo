// function posting() {     let title = $('#title').val()     let file =
// $('#file')[0].files[0]     let form_data = new FormData()
// form_data.append("title_give", title)     form_data.append("file_give", file)
// $.ajax({         type: "POST",         url: "/fileupload",         data:
// form_data,         cache: false,         contentType: false,
// processData: false,         success: function (response) {
// alert(response["result"])             window.location.reload()         }
// });   }
const base_url = "http://192.168.0.17:8080"

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
    alert("123");
    // .then((response) => alert(response["result"]))
    // .then((data) => window.location.reload());
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
})

const closeBtn = modal.querySelector(".close-area")
closeBtn.addEventListener("click", e => {
    modal.style.display = "none"
})

modal.addEventListener("click", e => {
    const evTarget = e.target
    console.log(evTarget)
    if (evTarget.classList.contains("upload_modal_wrapper")) {
        modal.style.display = "none"
    }
})
