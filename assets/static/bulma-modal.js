function activate() {
  document.querySelector('#modal-'+ this.id).classList.add('is-active');
}

function deactivate() {
  ms = document.querySelectorAll('.modal.is-active')
  for (i = 0; i < ms.length; i++) {
    ms[i].classList.remove('is-active')
  }
}

ws = document.querySelectorAll('.card.workshop')
for (i = 0; i < ws.length; i++) {
  ws[i].addEventListener('click', activate)
}

xs = document.querySelectorAll('.modal-close')
for (i = 0; i < xs.length; i++) {
  xs[i].addEventListener('click', deactivate)
}
