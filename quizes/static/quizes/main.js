const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startbtn = document.getElementById('start-button')
const url = window.location.href

modalBtns.forEach(modalBtns=>modalBtns.addEventListener('click',()=>{
    const pk = modalBtns.getAttribute('data-pk')
    const name = modalBtns.getAttribute('data-quiz')
    const numQuestions = modalBtns.getAttribute('data-questions')
    const difficulty = modalBtns.getAttribute('data-difficulty')
    const scoreToPass = modalBtns.getAttribute('data-pass')
    const time = modalBtns.getAttribute('data-time')

    modalBody.innerHTML=`
    <div class="h5 mb-3"> Are you ready to start the "<b> ${name} quiz</b>" ? </div>
    <div class="text-muted"> 
    <ul>
    <li>Difficulty: <b>${difficulty}</b></li>
    <li>Number of questions: <b>${numQuestions}</b></li>
    <li>Score to pass: <b>${scoreToPass}%</b></li>
    <li>The time: <b>${time} minute</b></li>
</ul>
</div>
`

startbtn.addEventListener('click',()=>{
    window.location.href = url+pk

})
}))
