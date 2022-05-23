// function posting() {     let title = $('#title').val()     let file =
// $('#file')[0].files[0]     let form_data = new FormData()
// form_data.append("title_give", title)     form_data.append("file_give", file)
// $.ajax({         type: "POST",         url: "/fileupload",         data:
// form_data,         cache: false,         contentType: false,
// processData: false,         success: function (response) {
// alert(response["result"])             window.location.reload()         }
// });   }
const base_url = "http://192.168.0.23:8080"

function posting() {
    let title = $('#title').val()
    let file = $('#file')[0].files[0]
    let form_data = new FormData()

    form_data.append("title_give", title)
    form_data.append("file_give", file)

    fetch(base_url + "/fileupload", {
        method: "POST",
        body: form_data
    })
    .then((response) => alert(response["result"]), window.location.reload())
    .then((data) => window.location.reload());
}
function find_img() {
    // $('#find_title').val() 퓨어 자바스크립트 변환
    let title = document
        .getElementById('find_title')
        .val()
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
    if(evTarget.classList.contains("upload_modal_wrapper")) {
        modal.style.display = "none"
    }
})

// // 이미지 드래그 앤 드롭
// var sec9 = document.querySelector('#drag');
// // var btnUpload = sec9.querySelector('.btn-upload');
// var inputFile = sec9.querySelector('input[type="file"]');
// var uploadBox = sec9.querySelector('.upload-box');

// /* 박스 안에 Drag 들어왔을 때 */
// uploadBox.addEventListener('dragenter', function(e) {
//     console.log('dragenter');
// });

// /* 박스 안에 Drag를 하고 있을 때 */
// uploadBox.addEventListener('dragover', function(e) {
//     e.preventDefault();

//     var vaild = e.dataTransfer.types.indexOf('Files') >= 0;

//     if(!vaild){
//         this.style.backgroundColor = 'red';
//     }
//     else{
//         this.style.backgroundColor = 'green';
//     }
    
// });

// /* 박스 밖으로 Drag가 나갈 때 */
// uploadBox.addEventListener('dragleave', function(e) {
//     console.log('dragleave');

//     this.style.backgroundColor = 'white';
// });

// /* 박스 안에서 Drag를 Drop했을 때 */
// uploadBox.addEventListener('drop', function(e) {
//     e.preventDefault();

//     console.log('drop');
//     this.style.backgroundColor = 'white';

//     console.dir(e.dataTransfer);

//     var data = e.dataTransfer.files[0];
//     console.dir(data);       
// });