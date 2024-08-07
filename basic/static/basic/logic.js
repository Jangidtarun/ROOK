console.log('Quiz app is loading');

// DOM element references
const takeQuizBtn = document.getElementById('take-quiz-btn');
const questionPaperDiv = document.getElementById('question-paper');
const progressbarContainer = document.querySelector('.progress-bar-container');
const progressBar = document.querySelector('.progress-bar');



// Load quiz data
async function loadData() {
  const quizId = document.getElementById('quiz-id').value;
  const url = `/take_quiz/${quizId}/`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response error: ${response.status}`);
    }

    const jsonData = await response.json();
    const questions = jsonData['questions'];

    const currq = document.getElementById('curr-question-text');
    
    let current_time_limit = questions[0].time_limit * 1000; 
    
    async function myTimer(delay, iteration_limit) {
        let index = 0;
        // progressbarContainer.style.width = `${delay/10}px`;

        const timer = async () => {
            
            let timerid;
            if (index < iteration_limit) {
                console.log('curr-delay: ', delay);
                console.log(questions[index]);

                // do all the shit here
                currq.innerHTML = questions[index].text;
                // show options
                let options_ = [];

                for(let i=0;i<4;i++){
                    const id = `option-${i+1}`;
                    console.log('id: ', id);
                    const tmp = document.getElementById(id);
                    console.log(tmp);
                    tmp.innerHTML = questions[index].options[i].text;
                    options_.push(tmp);
                }

                let selected_answers = []

                options_.forEach(element => {
                    element.addEventListener('click', () => {
                        console.log("select option: ", element.innerHTML);
                        selected_answers.push(element.innerHTML);
                        // change to next answer
                    })
                });

                // const option1 = document.getElementById('option-1');
                // option1.innerHTML = questions[index].options[0].text;

                // const option2 = document.getElementById('option-2');
                // option2.innerHTML = questions[index].options[1].text;

                // const option3 = document.getElementById('option-3');
                // option3.innerHTML = questions[index].options[2].text;

                // const option4 = document.getElementById('option-4');
                // option4.innerHTML = questions[index].options[3].text;


                let elapsed_time = 0;
                const timerprogressbar = async () => {
                    let timerprogressbar_id;
                    if(elapsed_time < delay){
                        
                        const progress = (elapsed_time / delay) * 98.5;
                        progressBar.style.width = `${progress}px`;
                        
                        elapsed_time += 10;
                        timerprogressbar_id = setTimeout(timerprogressbar, 10);
                    } else{
                        elapsed_time = 0;
                        clearTimeout(timerprogressbar_id);
                        console.log("this one's over");
                    }
                }
                await timerprogressbar();
                
                
                timerid = setTimeout(timer, delay);
                index++;
                if(index < iteration_limit){
                    delay = questions[index].time_limit * 1000;
                }
            } else{
                clearTimeout(timerid);
                console.log('stopped!');
                console.log('time to move to the results page.');
                // move to the results page.
            }
        };
        await timer();
    }

    await myTimer(current_time_limit, questions.length);

    console.log("time's up");

  } catch (error) {
    console.error('Error fetching quiz data:', error.message);
  }

  takeQuizBtn.style.display = 'none';
  questionPaperDiv.style.display = 'block';
}




// Event listeners
takeQuizBtn.addEventListener('click', loadData);


// Removed commented-out code related to preventing page reload (consider server-side solution)
