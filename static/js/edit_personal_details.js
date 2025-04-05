document.addEventListener("DOMContentLoaded", function () {
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

  btnUseOld.onclick = () => {
    method = "old";
    step1.classList.add('d-none');
    step2Old.classList.remove('d-none');
    progress.style.width = '66%';
  };

  btnForgotPw.onclick = () => {
    method = "forgot";
    step1.classList.add('d-none');
    step2Sec.classList.remove('d-none');
    progress.style.width = '66%';

    const idNumber = document.getElementById('userIdNumber')?.value;
    if (!idNumber) return;
  
    fetch(GET_SECURITY_QUESTIONS_URL, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id_number: document.getElementById('userIdNumber').value })
    })
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('securityQuestionsContainer');
      container.innerHTML = '';
      data.questions.forEach(q => {
        const qDiv = document.createElement('div');
        qDiv.className = 'mb-3';
        qDiv.innerHTML = `
          <label class="form-label">${q.text}</label>
          <input type="text" class="form-control secAnswer" data-id="${q.id}" placeholder="Your answer">
        `;
        container.appendChild(qDiv);
      });
    })
    .catch(err => {
      console.error("Error fetching questions:", err);
      secError.textContent = 'Failed to load security questions.';
    });
  };

  backToStep1.onclick = () => {
    step2Old.classList.add('d-none');
    step1.classList.remove('d-none');
    oldPwError.textContent = '';
    oldPassword.value = '';
    progress.style.width = '33%';
  };

  backToStep1b.onclick = () => {
    step2Sec.classList.add('d-none');
    step1.classList.remove('d-none');
    secError.textContent = '';
    document.querySelectorAll('.secAnswer').forEach(el => el.value = '');
    progress.style.width = '33%';
  };

  verifyOldBtn.onclick = () => {
    oldPwError.textContent = '';
    fetch(CHANGE_PASSWORD_URL, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        old_password: oldPassword.value,
        new_password1: '',
        new_password2: ''
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.ok) {
          verifiedOldPassword = oldPassword.value;
          step2Old.classList.add('d-none');
          step3.classList.remove('d-none');
          progress.style.width = '100%';
        } else {
          oldPwError.textContent = data.errors?.old_password?.join(', ') || 'Incorrect password.';
        }
      })
      .catch(() => {
        oldPwError.textContent = 'Server error. Please try again.';
      });
  };

  verifySecBtn.onclick = () => {
    secError.textContent = '';
    const idNumber = document.getElementById('userIdNumber')?.value;
    if (!idNumber) {
      secError.textContent = "Missing user ID.";
      return;
    }
  
    const answers = { id_number: idNumber };
    document.querySelectorAll('.secAnswer').forEach(el => {
      const id = el.dataset.id;
      answers[id] = el.value.trim();
    });
  
    fetch(VERIFY_SECURITY_URL, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(answers)
    })
      .then(response => response.json())
      .then(data => {
        if (data.valid) {
          step2Sec.classList.add('d-none');
          step3.classList.remove('d-none');
          progress.style.width = '100%';
        } else {
          secError.textContent = 'Security answers didn’t match. Please try again.';
        }
      })
      .catch(() => {
        secError.textContent = 'Server error. Please try again.';
      });
  };

  btnUpdatePw.onclick = () => {
    newPassErrors.textContent = '';
    const pw1 = document.querySelector('[name="new_password1"]').value;
    const pw2 = document.querySelector('[name="new_password2"]').value;

    const payload = {
      new_password1: pw1,
      new_password2: pw2
    };

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
      .then(response => response.json())
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
  };
});
