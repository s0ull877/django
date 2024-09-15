let like_buttons = document.querySelectorAll('.post-like');

function LikeButtonClick(button) {
  if (this.classList.contains('liked')) {
    this.classList.remove('liked');
  } else {
    this.classList.add('liked');
  };
};

like_buttons.forEach((button) => {
  button.addEventListener('click', LikeButtonClick);
});