document.addEventListener("DOMContentLoaded", function(){
  var fpStep1 = document.getElementById('fpStep1');
  var fpStep2Old = document.getElementById('fpStep2Old');
  var fpStep2Sec = document.getElementById('fpStep2Sec');
  var fpStep3 = document.getElementById('fpStep3');
  var fpIdNumber = document.getElementById('fpIdNumber');
  var fpOldPassword = document.getElementById('fpOldPassword');
  var fpError1 = document.getElementById('fpError1');
  var fpError2 = document.getElementById('fpError2');
  var fpErrorSec = document.getElementById('fpErrorSec');
  var fpError3 = document.getElementById('fpError3');
  var fpOldPwBtn = document.getElementById('fpOldPwBtn');
  var fpSecBtn = document.getElementById('fpSecBtn');
  var fpBack1 = document.getElementById('fpBack1');
  var fpBack1b = document.getElementById('fpBack1b');
  var fpVerifyOldBtn = document.getElementById('fpVerifyOldBtn');
  var fpVerifySecBtn = document.getElementById('fpVerifySecBtn');
  var fpBack2 = document.getElementById('fpBack2');
  var fpUpdatePwBtn = document.getElementById('fpUpdatePwBtn');
  var fpQuestionsContainer = document.getElementById('fpQuestionsContainer');
  var fpMethod = null;
  fpOldPwBtn.onclick = function() {
    fpMethod = "old";
    if(!fpIdNumber.value.trim()){
      fpError1.textContent = "Please enter ID Number first.";
      return;
    }
    fpError1.textContent = "";
    fpStep1.classList.add('d-none');
    fpStep2Old.classList.remove('d-none');
  };
  fpSecBtn.onclick = function() {
    fpMethod = "forgot";
    if(!fpIdNumber.value.trim()){
      fpError1.textContent = "Please enter ID Number first.";
      return;
    }
    fpError1.textContent = "";
    fpStep1.classList.add('d-none');
    fpStep2Sec.classList.remove('d-none');
    fpQuestionsContainer.innerHTML = '\n      <div class="mb-3">\n        <label class="form-label">What was your first pet’s name?</label>\n        <input type="text" class="form-control fpSecAnswer" data-q="What was your first pet’s name?">\n      </div>\n      <div class="mb-3">\n        <label class="form-label">What city were you born in?</label>\n        <input type="text" class="form-control fpSecAnswer" data-q="What city were you born in?">\n      </div>\n      <div class="mb-3">\n        <label class="form-label">What was your childhood nickname?</label>\n        <input type="text" class="form-control fpSecAnswer" data-q="What was your childhood nickname?">\n      </div>';
  };
  fpBack1.onclick = function() {
    fpStep2Old.classList.add('d-none');
    fpStep1.classList.remove('d-none');
    fpOldPassword.value = "";
    fpError2.textContent = "";
  };
  fpBack1b.onclick = function() {
    fpStep2Sec.classList.add('d-none');
    fpStep1.classList.remove('d-none');
    fpQuestionsContainer.innerHTML = "";
    fpErrorSec.textContent = "";
  };
  fpVerifyOldBtn.onclick = function() {
    fpError2.textContent = "";
    var pl = {
      "id_number": fpIdNumber.value.trim(),
      "old_password": fpOldPassword.value.trim(),
      "new_password1": "",
      "new_password2": ""
    };
    fetch("{% url 'accounts:public_forgot_password_view' %}", {
      method: "POST",
      headers: {'X-CSRFToken':'{{ csrf_token }}','Content-Type':'application/json'},
      body: JSON.stringify(pl)
    }).then(function(r) { return r.json(); }).then(function(data) {
      if(data.ok){
        fpStep2Old.classList.add('d-none');
        fpStep3.classList.remove('d-none');
      } else {
        fpError2.textContent = data.errors.old_password ? data.errors.old_password.join(", ") : "Incorrect password.";
      }
    }).catch(function() { fpError2.textContent = "Server error. Please try again."; });
  };
  fpVerifySecBtn.onclick = function() {
    fpErrorSec.textContent = "";
    var answers = {};
    document.querySelectorAll('.fpSecAnswer').forEach(function(el) {
      answers[el.dataset.q] = el.value.trim();
    });
    answers["id_number"] = fpIdNumber.value.trim();
    fetch("{% url 'accounts:public_verify_security_answers' %}", {
      method: "POST",
      headers: {'X-CSRFToken':'{{ csrf_token }}','Content-Type':'application/json'},
      body: JSON.stringify(answers)
    }).then(function(r) { return r.json(); }).then(function(d) {
      if(d.valid){
        fpStep2Sec.classList.add('d-none');
        fpStep3.classList.remove('d-none');
      } else {
        fpErrorSec.textContent = "Security answers didn’t match. Please try again.";
      }
    }).catch(function() { fpErrorSec.textContent = "Server error. Please try again."; });
  };
  fpBack2.onclick = function() {
    fpStep3.classList.add('d-none');
    if(fpMethod === "old"){
      fpStep2Old.classList.remove('d-none');
    } else {
      fpStep2Sec.classList.remove('d-none');
    }
    fpError3.textContent = "";
  };
  fpUpdatePwBtn.onclick = function() {
    fpError3.textContent = "";
    var pw1 = document.getElementById('fpNewPw1').value.trim();
    var pw2 = document.getElementById('fpNewPw2').value.trim();
    var payload = {
      "id_number": fpIdNumber.value.trim(),
      "new_password1": pw1,
      "new_password2": pw2
    };
    if(fpMethod === "old"){
      payload["old_password"] = fpOldPassword.value.trim();
    } else {
      payload["verify"] = "1";
    }
    fetch("{% url 'accounts:public_forgot_password_view' %}", {
      method: "POST",
      headers: {'X-CSRFToken':'{{ csrf_token }}','Content-Type':'application/json'},
      body: JSON.stringify(payload)
    }).then(function(r) { return r.json(); }).then(function(data) {
      if(data.ok){
        alert("Password updated successfully!");
        location.reload();
      } else {
        var err = "";
        for(var f in data.errors){
          err += f + ": " + data.errors[f].join(", ") + "\n";
        }
        fpError3.textContent = err || "Error updating password.";
      }
    }).catch(function() { fpError3.textContent = "Server error updating password."; });
  };
});
