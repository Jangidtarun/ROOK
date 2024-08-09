console.log('Quiz app is loading');

let progressbar = document.getElementById('progress-bar');
function updateprogressbar(progress){
  progressbar.style.width = `${progress}%`;
}

async function goberdas(url){
  try{
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response error: ${response.status}`);
      }

      const jsonData = await response.json();
      const questions = jsonData['questions'];

      let totaltime = 0;
      questions.forEach(q => {
        totaltime += q.time_limit;
      });

      let progress = 0;
      const timerid = setInterval(() => {
        progress += 0.1;
        tmp = (progress/totaltime) * 100;
        updateprogressbar(tmp);
        if(progress >= totaltime){
          clearInterval(timerid);
          console.log('time is over');
        }
      }, 100);
      
    } catch(err){
    console.error('err: ', err);
  }
}

window.addEventListener('load', function() {
  const quiz_id = document.getElementById('quiz_id').value;
  const url = `/load_quiz_data/${quiz_id}/`;

  goberdas(url);
})

