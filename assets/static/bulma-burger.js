document.addEventListener('DOMContentLoaded', function () {
  function navbarToggle() {
    this.classList.toggle('is-active');
    document.getElementById(this.dataset.target).classList.toggle('is-active');
  }

  navbarBurgers = document.querySelectorAll('.navbar-burger')
  for (i = 0; i < navbarBurgers.length; i++) {
    navbarBurgers[i].addEventListener('click', navbarToggle)
  }
});
