document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#submit-form').addEventListener('click', function(ev) {
    ev.preventDefault();

    var form = document.querySelector('form#workshop-application');
    var params = new URLSearchParams(new FormData(form)).toString();
    var url = '{{ this.submit_url }}' + '?' + params;

    var request = new XMLHttpRequest();
    request.open('GET', url, true);

    request.onload = function() {
      if (request.status >= 200 && request.status < 400) {
        alert('Başvurunuz alındı.');
      } else {
        alert('Bir sorun oluştu, lütfen yeniden deneyiniz.');
      }
    };

    request.onerror = function() {
      alert('Bir sorun oluştu, lütfen yeniden deneyiniz.');
    };

    request.send();
  });
});
