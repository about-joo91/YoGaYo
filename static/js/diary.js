const diary_base_url = "http://192.168.45.104:8080/diary";


// 로딩이 완료 된 후, 데이터를 바로 가져옴
window.onload = async function get_acc() {

    const response = await fetch(diary_base_url + "/acc", {
        method: "GET",
    })

    const data = await response.json();
    let posts_acc = data['posts_acc'];

    // 여기가 차트
    new Chart(document.getElementById("myChart"), {
        type: 'line',
        data: {
            labels: ['오늘', '1일전', '2일전', '3일전', '4일전', '5일전'],
            datasets: [{
                label: '테스트 데이터셋',
                data: [
                    posts_acc[0],
                    posts_acc[1],
                    posts_acc[2],
                    posts_acc[3],
                    posts_acc[4],
                    posts_acc[5],
                ],
                borderColor: '#83ccc0',
                // backgroundColor: "rgba(24, 21, 14, 0.5)",
                fill: false,
                lineTension: 0.2
            }]
        },
        options: {
            legend: { display: false }, //얘가 있으면 그래프 지우기가 가능해서 뺌
            responsive: true,
            title: {
                display: false,
                text: '나의 요가자세 정확도'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: false,
                        labelString: '날짜별 정확도'
                    }
                }],
                yAxes: [{
                    display: false,
                    ticks: {
                        suggestedMin: 0,
                    },
                    scaleLabel: {
                        display: false,
                        labelString: 'X%'
                    }
                }]
            }
        }
    });
    console.log(posts_acc[0])
    const dr_fighting = document.getElementById("dr_fighting")
    let per = posts_acc[0] - posts_acc[1];
    if (per > 0) {
        dr_fighting.innerHTML = "Comment : 축하해요 어제보다" + per + "%만큼 잘하셨어요!!ㅎㅎ";
    }
    else {
        dr_fighting.innerHTML = "Comment : 어제보다 " + per + "%만큼 내려갔네요 ㅠㅠ 분발하셔요"
    }
    //여기는 today_post리스트 점수, 자세같은거 다루는 곳 

    // let today_acc = posts_acc[0];
    // const post_acc = document.querySelector('.dr_up_cd_pt_ac_acc');
    // const post_acc_check = document.querySelector('.dr_up_cd_pt_ac_check');

    // post_acc.innerHTML="정확도 (" + today_acc + "%)";
    //     if (today_acc > 90){
    //         post_acc_check.innerHTML="와 90퍼를 넘기셨네요!! 축하드려요 ㅎㅎ"
    //     }
    //     else if (today_acc >= 80){
    //         post_acc_check.innerHTML="80%면 잘한거쥬";
    //     }
    //     else if (today_acc >= 70){
    //         post_acc_check.innerHTML="70%면 잘한거쥬";
    //     }
    //     else if (today_acc >= 60){
    //         post_acc_check.innerHTML="60%대라고...?면 잘한거쥬";
    //     }
    //     else {
    //         post_acc_check.innerHTML="힘냅시다.";
    //     }
}
// 첫 번째 모달 여닫기
const modal_background = document.querySelector('.modal_background');
const small_modal = document.querySelector('.small_modal');

modal_background.addEventListener('click', function (e) {
    if (e.target.classList.contains('modal_background')) {
        close_modal()
    }
})

function open_modal(post_id) {
    const small_modal = document.getElementById('small_modal_' + post_id);
    document.getElementById('modal_background_' + post_id).style.display = "block";

    document.body.style.overflow = 'hidden';
    let modal_top_now = parseInt((window.innerHeight - small_modal.clientHeight) / 2)
    let modal_left_now = parseInt((window.innerWidth - small_modal.clientWidth) / 2)
    let small_modal_body = document.getElementById('small_modal_' + post_id);
    small_modal_body.style.left = modal_left_now + "px";
    small_modal_body.style.top = modal_top_now + "px";
    small_modal.style.display = 'flex';
    small_modal.style.justifycontent = 'center';
    small_modal.style.alignitems = "center";

}

function close_modal() {
    document.querySelector('.modal_background').style.display = "none"
    document.body.style.overflow = 'auto';
}
// 여기는 edit_modal
let edit_text = document.querySelector('.edit_text')

const edit_modal_background = document.querySelector('.edit_modal_background');
const edit_small_modal = document.querySelector('.edit_small_modal');

edit_modal_background.addEventListener('click', function (e) {
    if (e.target.classList.contains('edit_modal_background')) {
        close_edit_modal()
    }
})
function open_edit_modal(post_id) {
    const edit_modal_background = document.getElementById('edit_modal_background_' + post_id);
    const edit_small_modal = document.getElementById('edit_small_modal_' + post_id);

    edit_modal_background.style.display = "block";
    edit_small_modal.style.display = "flex";
    document.body.style.overflow = 'hidden';

    let edit_modal_top_now = parseInt((window.innerHeight - edit_small_modal.clientHeight) / 2);
    let edit_modal_left_now = parseInt((window.innerWidth - edit_small_modal.clientWidth) / 2);
    const edit_small_modal_body = document.querySelector('#edit_small_modal_' + post_id);
    edit_small_modal_body.style.left = edit_modal_left_now + "px";
    edit_small_modal_body.style.top = edit_modal_top_now + "px";
    edit_small_modal.style.justifycontent = 'center';
    edit_small_modal.style.alignitems = "center";

}
function close_edit_modal() {
    edit_modal_background.style.display = "none";
    document.body.style.overflow = 'fixed';

}

// 수정버튼을 눌렀을 시
async function edit_texts(post_id) {
    const edit_texts = document.getElementById("edit_text_" + post_id)
    const edit_post_id = post_id
    const edit_texts_Data = {
        edit_texts_give: edit_texts.value,
        post_id_give: edit_post_id,
    }
    console.log(edit_texts_Data)
    const response = await fetch(diary_base_url + "/edit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(edit_texts_Data)
    })
    const data = await response.json();
    alert(data['msg'])
    window.location.replace("/diary")
}
// 삭제 버튼을 눌렀을 시
async function delete_post(post_id) {
    const delete_post_id = post_id;
    const delete_texts_Data = {
        post_id_give: delete_post_id
    }

    const response = await fetch(diary_base_url+"/delete", {

        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(delete_texts_Data)
    })
    const data = await response.json();
    alert(data['msg'])
    window.location.replace("/diary")
}