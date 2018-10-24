document.addEventListener('DOMContentLoaded', function () {
  function activateModal() {
    document.getElementById(this.dataset.target).classList.add('is-active');
  }

  function deactivateAllModals() {
    activeModals = document.querySelectorAll('.modal.is-active')
    for (i = 0; i < activeModals.length; i++) {
      activeModals[i].classList.remove('is-active')
    }
  }

  workshopCards = document.querySelectorAll('.card.workshop')
  for (i = 0; i < workshopCards.length; i++) {
    workshopCards[i].addEventListener('click', activateModal)
  }

  closeButtons = document.querySelectorAll('.modal-close')
  for (i = 0; i < closeButtons.length; i++) {
    closeButtons[i].addEventListener('click', deactivateAllModals)
  }
});
