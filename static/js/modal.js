
const upload_modal = document.querySelector('.upload_modal');
const preview_image = document.getElementById('um_preview_image_box')
const um_p_ib_wrapper = document.getElementById('um_p_ib_wrapper')
const um_desc = document.querySelector('.um_desc');
const um_header_next_btn = document.querySelector('.um_header_next_btn')
const um_header_upload_btn = document.querySelector('.um_header_upload_btn');
const um_comment_page = document.querySelector('.um_comment_page');
const mh_i_square = document.querySelector('.mh_i_square')
const upload_modal_wrapper = document.querySelector('.upload_modal_wrapper')
const ul_bb_prev = document.querySelector('.ul_bb_prev')
const ul_bb_next = document.querySelector('.ul_bb_next')
const um_preview_images = document.querySelector('.um_preview_images')

function isValid(data) {
    if (data.types.indexOf('Files') < 0)
        return false;
    if (data.files[0].type.indexOf('image') < 0) {
        alert('이미지 파일만 업로드 가능합니다.')
        return false;
    }
    if (data.files[0].size >= 1024 * 1024 * 50) {
        alert('50MB 이상인 파일은 업로드 할 수 없습니다.')
    }
    return true;
}
upload_modal.addEventListener('dragover', function (e) {
    e.preventDefault();
    um_desc.style.transition = 500 + 'ms'
    um_desc.style.color = 'rgb(65, 147, 239)'
});
upload_modal.addEventListener('dragleave', function (e) {
    e.preventDefault();
    um_desc.style.transition = 500 + 'ms'
    um_desc.style.color = 'black'
});

const formData = new FormData();
let file_length = 0
upload_modal.addEventListener('drop', function (e) {
    e.preventDefault();
    const data = e.dataTransfer;
    if (!isValid(data)) return;
    um_p_ib_wrapper.style.width = 400 * data.files.length + "px"
    file_length = data.files.length
    for (let i = 0; i < data.files.length; i++) {
        formData.append(data.files[i].name, data.files[i])
        const reader = new FileReader();
        reader.onload = () => {
            um_p_ib_wrapper.innerHTML +=
                `
            <img class="um_preview_images" src="${reader.result}">
            `
        }
        reader.readAsDataURL(data.files[i])
    }
    preview_image.style.display = 'block'
    um_desc.style.display = 'none'
    um_header_next_btn.style.display = 'flex'
    if (data.files.length > 1) {
        ul_bb_next.style.visibility = 'visible'
    }

});
ul_bb_cur_idx = 0
ul_bb_next.addEventListener('click', function () {
    ul_bb_prev.style.visibility = 'visible'
    if (++ul_bb_cur_idx == file_length - 1) {
        ul_bb_next.style.visibility = 'hidden'
    }
    um_p_ib_wrapper.style.transition = 500 + 'ms'
    um_p_ib_wrapper.style.transform = "translate3d(-" + (400 * ul_bb_cur_idx) + "px,0px,0px)"
})
ul_bb_prev.addEventListener('click', function () {
    if (--ul_bb_cur_idx == 0) {
        ul_bb_prev.style.visibility = 'hidden'
    }
    um_p_ib_wrapper.style.transform = "translate3d(-" + (400 * ul_bb_cur_idx) + "px, 0px, 0px)"
    ul_bb_next.style.visibility = 'visible'
    um_p_ib_wrapper.style.transition = 500 + 'ms'

})
um_header_next_btn.addEventListener('click', function () {
    um_header_next_btn.style.display = 'none'
    upload_modal.style.transition = 500 + "ms"
    upload_modal.style.width = 800 + "px"

    setTimeout(() => {
        um_header_upload_btn.style.display = 'flex'
        um_comment_page.style.display = 'block'
        um_preview_images.style.borderRadius = "0px 0px 0px 0px";
    }, 500)
})
um_header_upload_btn.addEventListener('click', () => {
    let content_give = $('#um_cp_ma_f_input').val()
    formData.append('content', content_give)
    $.ajax({
        type: "POST",
        url: "/posts",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        },

    })

})
(function() {
            
    var $file = document.getElementById("file")
    var dropZone = document.querySelector(".um_cp_dropzone")

    var toggleClass = function(className) {
        
        console.log("current event: " + className)

        var list = ["dragenter", "dragleave", "dragover", "drop"]

        for (var i = 0; i < list.length; i++) {
            if (className === list[i]) {
                dropZone.classList.add("um_cp_dropzone-" + list[i])
            } else {
                dropZone.classList.remove("um_cp_dropzone-" + list[i])
            }
        }
    }
    
    var showFiles = function(files) {
        dropZone.innerHTML = ""
        for(var i = 0, len = files.length; i < len; i++) {
            dropZone.innerHTML += "<p>" + files[i].name + "</p>"
        }
    }

    var selectFile = function(files) {
        // input file 영역에 드랍된 파일들로 대체
        $file.files = files
        showFiles($file.files)
        
    }
    
    $file.addEventListener("change", function(e) {
        showFiles(e.target.files)
    })

    // 드래그한 파일이 최초로 진입했을 때
    dropZone.addEventListener("dragenter", function(e) {
        e.stopPropagation()
        e.preventDefault()

        toggleClass("dragenter")

    })

    // 드래그한 파일이 dropZone 영역을 벗어났을 때
    dropZone.addEventListener("dragleave", function(e) {
        e.stopPropagation()
        e.preventDefault()

        toggleClass("dragleave")

    })

    // 드래그한 파일이 dropZone 영역에 머물러 있을 때
    dropZone.addEventListener("dragover", function(e) {
        e.stopPropagation()
        e.preventDefault()

        toggleClass("dragover")

    })

    // 드래그한 파일이 드랍되었을 때
    dropZone.addEventListener("drop", function(e) {
        e.preventDefault()

        toggleClass("drop")

        var files = e.dataTransfer && e.dataTransfer.files
        console.log(files)

        if (files != null) {
            if (files.length < 1) {
                alert("폴더 업로드 불가")
                return
            }
            selectFile(files)
        } else {
            alert("ERROR")
        }

    })

})();

function upload_modal_in() {
    upload_modal_wrapper.style.display = 'flex';
}
function upload_modal_out() {
    upload_modal_wrapper.style.display = 'none'
}
mh_i_square.addEventListener('click', upload_modal_in)
upload_modal_wrapper.addEventListener('click', function (e) {
    if (e.target.classList.contains('upload_modal_wrapper')) {
        upload_modal_out()
    }
})