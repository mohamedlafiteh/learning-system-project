let qTag = document.getElementById('qu-tag')
let scoTag = document.getElementById('sc-tag')
let rTag = document.getElementById('re-tag')
let tTag = document.getElementById('ti-tag')
let lbuttonTag = document.getElementById('l-button-l')
let llbuttonTag = document.getElementById('l-button-ll')


let is_answered = false

const startTimer = (t) =>{
    if(t.toString().length <2){
         tTag.innerHTML =`<p>0${t}:00</p>`
            }else {
           tTag.innerHTML =`<b >${t}:00</b>`

            }
    let min = t -1
    let sec = 60
    let showSec
    let showMin
    const timer = setInterval(()=>{
        sec --
        if(sec <0) {
            sec =59
            min--
        }
        if(min.toString().length <2) {
            showMin ='0' +min
        }else {
            showMin=min
        }

        if(sec.toString().length <2) {
            showSec='0'+sec
        }else {
            showSec =sec
        }
        if(min ===0 && sec ===0) {
            tTag.innerHTML ="<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time finished')
                if(!is_answered){
                    postFormData()
                }

            },500)

        }
        tTag.innerHTML = `<b style="background-color:#FF0000; color: white">${showMin}:${showSec}</b>`
    },1000)
}

$.ajax({
type:'GET',
    url:data_url,
    success:function (response){
        const allData = response.data
        allData.forEach(e =>{
            for(const [ques,ans] of Object.entries(e)) {
               qTag.innerHTML += `
                <hr>
                <div class="mb-2 font-italic">
                  <b>${ques}</b>
                </div>
               `
                ans.forEach(answer =>{
                    qTag.innerHTML+= `
                     <div>
                       <input type="radio" class="ans" id="${ques}-${answer}" name="${ques}" value="${answer}">
                       <label for="${ques}">${answer}</label>
                     </div>
                    `
                })
            }
        })

            startTimer(response.time)

    },
    error:function (error){
    console.log(error)
    }
})

let quizForm = document.getElementById('quizz-form')
let csrf = document.getElementsByName('csrfmiddlewaretoken')

const postFormData = ()=> {
    let elements = [...document.getElementsByClassName('ans')]

    let allData = {}
    allData['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(e=>{
        if(e.checked) {
            allData[e.name]=e.value
        }else {
            if(!allData[e.name]) {
                allData[e.name] =null
            }
        }
    })
    $.ajax({
       type: 'POST',
       url:result_url,
        data:allData,
        success:function (response){
            const quizResults = response.results
            const sco = response.score
            quizForm.classList.add('not-visible')
            is_answered=true
            console.log(response.passed)
            scoTag.innerHTML = `${response.passed ? 'Well done you passed! You can start learning maths from the first or second lecture': 'It is not success, you can start learning maths from the first lecture '} your result is ${response.score.toFixed(2)} %`

            quizResults.forEach(r =>{
                let resultsTag = document.createElement("div")
                for(let [ques,resp] of Object.entries(r)){
                    resultsTag.innerHTML+=ques
                    let cls = ['container','p-3','text-light','h6']
                    resultsTag.classList.add(...cls)
                    if(resp =='not answered'){
                        resultsTag.innerHTML+=' Not answered'
                        resultsTag.classList.add('bg-danger')
                    }else {
                        let answer = resp['answered']
                        let correct = resp['correct_answer']
                        if(answer ==correct) {
                            resultsTag.classList.add('bg-success')
                            resultsTag.innerHTML+=` Answered: ${answer}`
                        }else {
                            resultsTag.classList.add('bg-danger')
                            resultsTag.innerHTML+=` | Correct answer : ${correct}`
                            resultsTag.innerHTML+=` | Answered : ${answer}`

                        }
                    }
                }

                if(sco){
                   lbuttonTag.classList.remove("not-visible")
                }else {
                     llbuttonTag.classList.remove("not-visible")
                }

                rTag.append(resultsTag)


            })
        },
        error:function (error){
           console.log(error)
        }
    })

}
quizForm.addEventListener('submit',e=>{
    e.preventDefault()
    postFormData()
})