let like_buttons = document.querySelectorAll('.post-like');

function LikeButtonClick() {

  like_count_span=this.querySelector('span')
  
  var token = this.querySelector('input[name="csrfmiddlewaretoken"]').value

  if (this.classList.contains('liked')) {

    this.classList.remove('liked');
    var value = false;
    like_count_span.innerText--;

  } else {

    this.classList.add('liked');
    var value = true;
    like_count_span.innerText++;

  };

  change_url=$(this).attr('change_url')
  
  $.ajax({
    type: "POST",
    url: change_url,
    data: {
      value: value,
      csrfmiddlewaretoken: token,
      },
  }

);
}

like_buttons.forEach((button) => {
  button.addEventListener('click', LikeButtonClick);
});