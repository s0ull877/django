var textarea = document.querySelector('.comment-text')

function autosize(){
  var el = this;
  setTimeout(function(){
    el.style.cssText = 'height:auto; padding:0';
    el.style.cssText = 'height:' + el.scrollHeight + 'px';
  },0);
};

if (textarea) {
  textarea.addEventListener('keydown', autosize);
};
