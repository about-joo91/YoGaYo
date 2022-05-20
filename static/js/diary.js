// 모달
const modal_background = document.querySelector('.modal_background');
const small_modal = document.querySelector('.small_modal');

modal_background.addEventListener('click', function (e) {
if (e.target.classList.contains('modal_background')) {
    close_modal()
}
})
function open_modal(){
    document.querySelector('.modal_background').style.display="block"
    document.body.style.overflow = 'hidden';
    let modal_top_now = parseInt((window.innerHeight - 380) / 2)
    let modal_left_now = parseInt((window.innerWidth - 380) / 2)
    let small_modal_body = document.querySelector('.small_modal');
    small_modal_body.style.left = modal_left_now + "px";
    small_modal_body.style.top = modal_top_now + "px";
    small_modal.style.display = 'flex';
    small_modal.style.justifycontent = 'center';
    small_modal.style.alignitems = "center"; 

}

 function close_modal(){
    document.querySelector('.modal_background').style.display="none"
    document.querySelector('.small_modal').style.display="none"
    document.body.style.overflow = 'auto';
}
    // myChart
// 여기부터 차트
let today = 80.2;
let one_ago = 72.4;
let two_ago = 69.2;
let three_ago = 73.2;
let four_ago = 57.2;
let five_ago = 72.2;
acc=[
    today,one_ago,two_ago,three_ago,four_ago,five_ago
]
new Chart(document.getElementById("myChart"), {
    type: 'line',
    data: {
        labels: ['오늘', '1일전', '2일전', '3일전', '4일전', '5일전'],
        datasets: [{
            label: '테스트 데이터셋',
            data: [
                acc[0],
                acc[1],
                acc[2],
                acc[3],
                acc[4],
                acc[5],
            ],
            borderColor: 'green',
            // backgroundColor: "rgba(24, 21, 14, 0.5)",
            fill: false,
            lineTension: 0
        }]
    },
    options: {
        legend: { display: false }, //얘가 있으면 그래프 지우기가 가능해서 뺌
        responsive: true,
        title: {
            display: true,
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
                    display: true,
                    labelString: '날짜별 정확도'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0,
                },
                scaleLabel: {
                    display: true,
                    labelString: 'X%'
                }
            }]
        }
    }
});

if (acc[0] > acc[1]){
    let per = acc[0] - acc[1]
    document.getElementById("dr_fighting").innerHTML = "축하해요 어제보다" + per + "%만큼 잘하셨어요!!ㅎㅎ";

 //여기는 today_post리스트 점수, 자세같은거 다루는 곳 
let today_acc = 80;  //today_acc는 오늘 날짜의 acc를 가져온다.
document.querySelector('.dr_up_cd_pt_ac_acc').innerHTML="정확도" + today_acc + "%";
    if (today_acc >= 80){
        document.querySelector('.dr_up_cd_pt_ac_check').innerHTML="80%면 잘한거쥬";
    }

}
