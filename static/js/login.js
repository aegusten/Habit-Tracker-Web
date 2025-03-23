document.addEventListener("DOMContentLoaded", function(){
  const fpStep1 = document.getElementById('fpStep1');
  const fpStep2Old = document.getElementById('fpStep2Old');
  const fpStep2Sec = document.getElementById('fpStep2Sec');
  const fpStep3 = document.getElementById('fpStep3');
  const fpIdNumber = document.getElementById('fpIdNumber');
  const fpOldPassword = document.getElementById('fpOldPassword');
  const fpError1 = document.getElementById('fpError1');
  const fpError2 = document.getElementById('fpError2');
  const fpErrorSec = document.getElementById('fpErrorSec');
  const fpError3 = document.getElementById('fpError3');
  const fpOldPwBtn = document.getElementById('fpOldPwBtn');
  const fpSecBtn = document.getElementById('fpSecBtn');
  const fpBack1 = document.getElementById('fpBack1');
  const fpBack1b = document.getElementById('fpBack1b');
  const fpVerifyOldBtn = document.getElementById('fpVerifyOldBtn');
  const fpVerifySecBtn = document.getElementById('fpVerifySecBtn');
  const fpBack2 = document.getElementById('fpBack2');
  const fpUpdatePwBtn = document.getElementById('fpUpdatePwBtn');
  const fpQuestionsContainer = document.getElementById('fpQuestionsContainer');
  let fpMethod = null;

  fpOldPwBtn.onclick = () => {
    fpMethod = "old";
    if(!fpIdNumber.value.trim()){
      fpError1.textContent = "Please enter ID Number first.";
      return;
    }
    fpError1.textContent = "";
    fpStep1.classList.add('d-none');
    fpStep2Old.classList.remove('d-none');
  };

  fpSecBtn.onclick = () => {
    fpMethod = "forgot";
    if(!fpIdNumber.value.trim()){
      fpError1.textContent = "Please enter ID Number first.";
      return;
    }
    fpError1.textContent = "";
    fpStep1.classList.add('d-none');
    fpStep2Sec.classList.remove('d-none');
    fpQuestionsContainer.innerHTML = `
      <div class="mb-3">
        <label class="form-label">What was your first pet’s name?</label>
        <input type="text" class="form-control fpSecAnswer" data-q="What was your first pet’s name?">
      </div>
      <div class="mb-3">
        <label class="form-label">What city were you born in?</label>
        <input type="text" class="form-control fpSecAnswer" data-q="What city were you born in?">
      </div>
      <div class="mb-3">
        <label class="form-label">What was your childhood nickname?</label>
        <input type="text" class="form-control fpSecAnswer" data-q="What was your childhood nickname?">
      </div>`;
  };

  fpBack1.onclick = () => {
    fpStep2Old.classList.add('d-none');
    fpStep1.classList.remove('d-none');
    fpOldPassword.value = "";
    fpError2.textContent = "";
  };

  fpBack1b.onclick = () => {
    fpStep2Sec.classList.add('d-none');
    fpStep1.classList.remove('d-none');
    fpQuestionsContainer.innerHTML = "";
    fpErrorSec.textContent = "";
  };

  fpVerifyOldBtn.onclick = () => {
    fpError2.textContent = "";
    let pl = {
      "id_number": fpIdNumber.value.trim(),
      "old_password": fpOldPassword.value.trim(),
      "new_password1": "",
      "new_password2": ""
    };

    fetch("{% url 'accounts:public_forgot_password_view' %}", {
      method: "POST",
      headers: {'X-CSRFToken':'{{ csrf_token }}','Content-Type':'application/json'},
      body: JSON.stringify(pl)
    }).then(r => r.json()).then(data => {
      if(data.ok){
        fpStep2Old.classList.add('d-none');
        fpStep3.classList.remove('d-none');
      } else {
        fpError2.textContent = data.errors.old_password ? data.errors.old_password.join(", ") : "Incorrect password.";
      }
    }).catch(() => { fpError2.textContent = "Server error. Please try again."; });
  };

  fpVerifySecBtn.onclick = () => {
    fpErrorSec.textContent = "";
    let answers = {};
    document.querySelectorAll('.fpSecAnswer').forEach(el => {
      answers[el.dataset.q] = el.value.trim();
    });

    answers["id_number"] = fpIdNumber.value.trim();
    fetch("{% url 'accounts:public_verify_security_answers' %}", {
      method: "POST",
      headers: {'X-CSRFToken':'{{ csrf_token }}','Content-Type':'application/json'},
      body: JSON.stringify(answers)
    }).then(r => r.json()).then(d => {
      if(d.valid){
        fpStep2Sec.classList.add('d-none');
        fpStep3.classList.remove('d-none');
      } else {
        fpErrorSec.textContent = "Security answers didn’t match. Please try again.";
      }
    }).catch(() => { fpErrorSec.textContent = "Server error. Please try again."; });
  };

  fpBack2.onclick = () => {
    fpStep3.classList.add('d-none');
    if(fpMethod === "old"){
      fpStep2Old.classList.remove('d-none');
    } else {
      fpStep2Sec.classList.remove('d-none');
    }
    fpError3.textContent = "";
  };

  fpUpdatePwBtn.onclick = () => {
    fpError3.textContent = "";
    let pw1 = document.getElementById('fpNewPw1').value.trim();
    let pw2 = document.getElementById('fpNewPw2').value.trim();
    let payload = {
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
    }).then(r => r.json()).then(data => {
      if(data.ok){
        alert("Password updated successfully!");
        location.reload();
      } else {
        let err = "";
        for(let f in data.errors){
          err += f+": "+data.errors[f].join(", ")+"\n";
        }
        fpError3.textContent = err || "Error updating password.";
      }
    }).catch(() => { fpError3.textContent = "Server error updating password."; });
  };
});