document.addEventListener('DOMContentLoaded', ()=>{
  let urlInput = document.getElementById("url-input");
  let submitBtn = document.getElementById("submit-url");
  if (urlInput.value !== null){
    submitBtn.disabled = false;
  }
})

document.addEventListener('DOMContentLoaded', ()=>{
  let videoOnlyRowElements = document.querySelectorAll('.video-only-rows')
  videoOnlyRowElements.forEach(hideElement)
  let audioOnlyRowElements = document.querySelectorAll('.audio-only-rows')
  audioOnlyRowElements.forEach(hideElement)
  let selectOption = document.querySelector('#downloadType')
  selectOption.selectIndex = 1;
})

function checkInput() {
    let urlInput = document.getElementById("url-input");
    let submitBtn = document.getElementById("submit-url");
    let youtubeUrlRegex = /^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+/i;
  
    if (youtubeUrlRegex.test(urlInput.value)) {
      submitBtn.disabled = false;
    } else {
      submitBtn.disabled = true;
    }
  }

function hideElement(el){
  el.style.display = 'none';
}

function showElement(el){
  el.style.display = '';
}

function viewSelectedFormat(){
  let selectedOption = document.querySelector('#downloadType').value

  let videoWithAudioRowElements = document.querySelectorAll('.video-with-audio-rows')
  videoWithAudioRowElements.forEach(hideElement)
  let videoOnlyRowElements = document.querySelectorAll('.video-only-rows')
  videoOnlyRowElements.forEach(hideElement)
  let audioOnlyRowElements = document.querySelectorAll('.audio-only-rows')
  audioOnlyRowElements.forEach(hideElement)

  if (selectedOption === 'video_with_audio') {
    videoWithAudioRowElements.forEach(showElement)
  } else if (selectedOption === 'video_only') {
    videoOnlyRowElements.forEach(showElement)
  } else if (selectedOption === 'audio_only') {
    audioOnlyRowElements.forEach(showElement)
  } else if (selectedOption === 'all_formats')  {
    videoWithAudioRowElements.forEach(showElement)
    videoOnlyRowElements.forEach(showElement)
    audioOnlyRowElements.forEach(showElement)
  }
}