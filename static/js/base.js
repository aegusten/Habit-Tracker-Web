document.addEventListener('DOMContentLoaded', function() {
  if (localStorage.getItem('theme') === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    var themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
    }
  }
  var themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      if (document.documentElement.getAttribute('data-theme') === 'dark') {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        this.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        this.innerHTML = '<i class="bi bi-sun-fill"></i>';
      }
    });
  }
  document.querySelectorAll('.tab-link').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.tab-link').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var todaySection = document.getElementById('today-section');
      var archiveSection = document.getElementById('archive-section');
      if (todaySection && archiveSection) {
        todaySection.classList.toggle('d-none', btn.dataset.target !== '#today-section');
        archiveSection.classList.toggle('d-none', btn.dataset.target !== '#archive-section');
      }
    });
  });
});
