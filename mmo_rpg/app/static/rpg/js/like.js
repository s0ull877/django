let like_buttons = document.querySelectorAll('.post-like');

function LikeButtonClick() {

    like_count_span=this.querySelector('span')
    
    var token = this.querySelector('input[name="csrfmiddlewaretoken"]').value

    // убрать или поставить лайк
    if (this.classList.contains('liked')) {
        var value = false;
    } else {
        var value = true;
    };

    change_url=$(this).attr('change_url')

    var button = this
    
    $.ajax({

        type: "POST",
        url: change_url,
        data: {
            value: value,
            csrfmiddlewaretoken: token,
            },

        success: function (data) {

          if (value) {

              button.classList.add('liked');
              like_count_span.innerText++;

          } else {

              button.classList.remove('liked');
              like_count_span.innerText--;
            }
        }
      });
}

like_buttons.forEach((button) => {
    button.addEventListener('click', LikeButtonClick);
});