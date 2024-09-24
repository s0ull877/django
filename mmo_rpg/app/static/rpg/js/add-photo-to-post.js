let new_medias = document.querySelectorAll('.new-media')

var media_data = document.querySelector('.media-post-data')

new_medias.forEach((new_media) => {
  
  new_media.addEventListener('change', newMedia);

});

function newMedia(){

  file = this.querySelector('input');

  if (file.files[0].type.includes('image')) {

    src = URL.createObjectURL(file.files[0]);
  
    new_block = `<div class="media-item" style="position: static;" ><img src="${src}" alt="post-photo-2"></div>`
    media_data.innerHTML += new_block
  
    this.style.display = 'none'
  
    next_div=document.querySelector('.display-none');
    console.log(next_div)
    if (next_div) {
      next_div.classList.remove('display-none');
      next_div.style.position = 'static';
    }

  } else {
    file.files[0] = null
  }

};



