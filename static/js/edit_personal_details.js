document.addEventListener("DOMContentLoaded", function () {
    const modalEl = document.getElementById('editInfoModal');
    if (!modalEl) return;
  
    const step1 = document.getElementById('step1');
    const step2Old = document.getElementById('step2Old');
    const step2Sec = document.getElementById('step2Sec');
    const step3 = document.getElementById('step3');
    const progress = document.getElementById('wizardProgress');
    const btnUseOld = document.getElementById('btnUseOld');
    const btnForgotPw = document.getElementById('btnForgotPw');
    const backToStep1 = document.getElementById('backToStep1');
    const backToStep1b = document.getElementById('backToStep1b');
    const verifyOldBtn = document.getElementById('verifyOldBtn');
    const verifySecBtn = document.getElementById('verifySecBtn');
    const backStep3 = document.getElementById('backStep3');
    const btnUpdatePw = document.getElementById('btnUpdatePw');
    const oldPassword = document.getElementById('oldPassword');
    const oldPwError = document.getElementById('oldPwError');
    const secError = document.getElementById('secError');
    const newPassErrors = document.getElementById('newPassErrors');
  
    let method = null;
    let verifiedOldPassword = "";
  
    btnUseOld?.addEventListener('click', () => {
      method = "old";
      step1.classList.add('d-none');
      step2Old.classList.remove('d-none');
      progress.style.width = '66%';
    });
  
    btnForgotPw?.addEventListener('click', () => {
      method = "forgot";
      step1.classList.add('d-none');
      step2Sec.classList.remove('d-none');
      progress.style.width = '66%';
    });
  
    backToStep1?.addEventListener('click', () => {
      step2Old.classList.add('d-none');
      step1.classList.remove('d-none');
      oldPwError.textContent = '';
      oldPassword.value = '';
      progress.style.width = '33%';
    });
  
    backToStep1b?.addEventListener('click', () => {
      step2Sec.classList.add('d-none');
      step1.classList.remove('d-none');
      secError.textContent = '';
      document.querySelectorAll('.secAnswer').forEach(el => el.value = '');
      progress.style.width = '33%';
    });
  
    verifyOldBtn?.addEventListener('click', () => {
      oldPwError.textContent = '';
      fetch(CHANGE_PASSWORD_URL, {
        method: 'POST',
        headers: {
          'X-CSRFToken': CSRF_TOKEN,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ old_password: oldPassword.value, new_password1: '', new_password2: '' })
      })
        .then(res => res.json())
        .then(data => {
          if (data.ok) {
            verifiedOldPassword = oldPassword.value;
            step2Old.classList.add('d-none');
            step3.classList.remove('d-none');
            progress.style.width = '100%';
          } else {
            oldPwError.textContent = data.errors.old_password
              ? data.errors.old_password.join(', ')
              : 'Incorrect password.';
          }
        })
        .catch(() => {
          oldPwError.textContent = 'Server error. Please try again.';
        });
    });
  
    verifySecBtn?.addEventListener('click', () => {
      secError.textContent = '';
      let answers = {};
      document.querySelectorAll('.secAnswer').forEach(el => {
        answers[el.dataset.question] = el.value.trim();
      });
      fetch(VERIFY_SECURITY_URL, {
        method: 'POST',
        headers: {
          'X-CSRFToken': CSRF_TOKEN,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(answers)
      })
        .then(res => res.json())
        .then(data => {
          if (data.valid) {
            step2Sec.classList.add('d-none');
            step3.classList.remove('d-none');
            progress.style.width = '100%';
          } else {
            secError.textContent = 'Security answers didn’t match.';
          }
        })
        .catch(() => {
          secError.textContent = 'Server error. Please try again.';
        });
    });
  
    btnUpdatePw?.addEventListener('click', () => {
      newPassErrors.textContent = '';
      const pw1 = document.querySelector('[name="new_password1"]').value;
      const pw2 = document.querySelector('[name="new_password2"]').value;
      let payload = { new_password1: pw1, new_password2: pw2 };
      if (method === 'old') {
        payload.old_password = verifiedOldPassword;
      } else {
        payload.verify = '1';
      }
      fetch(CHANGE_PASSWORD_URL, {
        method: 'POST',
        headers: {
          'X-CSRFToken': CSRF_TOKEN,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
        .then(res => res.json())
        .then(data => {
          if (data.ok) {
            alert('Password updated successfully!');
            location.reload();
          } else {
            let errMsg = '';
            for (let field in data.errors) {
              errMsg += `${field}: ${data.errors[field].join(', ')}\n`;
            }
            newPassErrors.textContent = errMsg || 'Error updating password.';
          }
        })
        .catch(() => {
          newPassErrors.textContent = 'Server error updating password.';
        });
    });
  });
  