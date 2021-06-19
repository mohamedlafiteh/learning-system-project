const url = window.location.href
const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timertBox = document.getElementById('timer-box')



const activateTimer = (time) =>{
    if(time.toString().length <2){
         timertBox.innerHTML =`<p>0${time}:00</p>`
            }else {
           timertBox.innerHTML =`<b >${time}:00</b>`

            }
    let minutes = time -1
    let seconds = 60
    let displaySeconds
    let displayMintues
    const timer = setInterval(()=>{
        seconds --
        if(seconds <0) {
            seconds =59
            minutes--
        }
        if(minutes.toString().length <2) {
            displayMintues ='0' +minutes
        }else {
            displayMintues=minutes
        }

        if(seconds.toString().length <2) {
            displaySeconds='0'+seconds
        }else {
            displaySeconds =seconds
        }
        if(minutes ===0 && seconds ===0) {
            timertBox.innerHTML ="<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time finished')
                sendData()
            },500)

        }
        timertBox.innerHTML = `<b style="background-color:#FF0000; color: white">${displayMintues}:${displaySeconds}</b>`
    },1000)



}

$.ajax({
type:'GET',
    url:`${url}/data`,
    success:function (response){
        const data = response.data
        data.forEach(e =>{
            for(const [question,answers] of Object.entries(e)) {
               quizBox.innerHTML += `
                <hr>
                <div class="mb-2">
                  <b>${question}</b>
                </div>
               `
                answers.forEach(answer =>{
                    quizBox.innerHTML+= `
                     <div>
                       <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                       <label for="${question}">${answer}</label>
                     </div>
                    `
                })
            }
        })
        activateTimer(response.time)
    },
    error:function (error){
    console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = ()=> {
    const elements = [...document.getElementsByClassName('ans')]

    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(e=>{
        if(e.checked) {
            data[e.name]=e.value
        }else {
            if(!data[e.name]) {
                data[e.name] =null
            }
        }
    })
    $.ajax({
       type: 'POST',
       url:` ${url}/save/`,
        data:data,
        success:function (response){
            const results = response.results
            console.log(results)
            quizForm.classList.add('not-visible')

            scoreBox.innerHTML = `${response.passed ? 'Well done you passed!': 'Sorry, it is fail: ( '} your result is ${response.score.toFixed(2)} %`

            results.forEach(r =>{
                const resDiv = document.createElement("div")
                for(const [question,resp] of Object.entries(r)){
                    resDiv.innerHTML+=question
                    const cls = ['container','p-3','text-light','h6']
                    resDiv.classList.add(...cls)
                    if(resp =='not answered'){
                        resDiv.innerHTML+='-not answered'
                        resDiv.classList.add('bg-danger')
                    }else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']
                        if(answer ==correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML+=`answered: ${answer}`
                        }else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML+=`| correct answer : ${correct}`
                            resDiv.innerHTML+=`| answered : ${answer}`

                        }
                    }
                }
                // const body = document.getElementsByTagName('BODY')[0]
                resultBox.append(resDiv)

            })
        },
        error:function (error){
           console.log(error)
        }
    })

}
quizForm.addEventListener('submit',e=>{
    e.preventDefault()
    sendData()
})