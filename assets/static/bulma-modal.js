document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.card.workshop').forEach(function ($el) {
    $el.addEventListener('click', function () {
      document.getElementById($el.dataset.target).classList.add('is-active');
    });
  });

  document.querySelectorAll('.modal-close').forEach(function ($el) {
    $el.addEventListener('click', function () {
      document.querySelectorAll('.modal.is-active').forEach(function ($modal) {
        $modal.classList.remove('is-active');
      });
    });
  });
});
