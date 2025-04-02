document.addEventListener('DOMContentLoaded', () => {
  const customFieldsContainer = document.getElementById('customFieldsContainer');
  const addCustomFieldBtn = document.getElementById('addCustomField');

  document.querySelectorAll('.template-card').forEach(card => {
    card.addEventListener('click', () => {
      const selectedTemplate = card.getAttribute('data-template');
      window.location.href = `/habits/new/?template=${selectedTemplate}`;
    });
  });

  function applyFieldLogic(select) {
    const row = select.closest('.custom-field');
    const defaultInput = row.querySelector('.custom-field-value');
    const defaultWrapper = row.querySelector('.default-wrapper');
    const importanceWrapper = row.querySelector('.importance-wrapper');
    const importanceSelect = row.querySelector('.custom-field-required');
    const selectedType = select.value.toLowerCase();

    if (selectedType === 'yesno') {
      defaultWrapper.style.display = 'none';
      defaultInput.value = '';
      importanceWrapper.style.display = 'none';
    } else {
      defaultWrapper.style.display = '';
      importanceWrapper.style.display = '';

      if (selectedType === 'number') {
        defaultInput.type = 'number';
      } else if (selectedType === 'date') {
        defaultInput.type = 'date';
      } else if (selectedType === 'time') {
        defaultInput.type = 'time';
      } else {
        defaultInput.type = 'text';
      }

      importanceSelect.innerHTML = '';

      const optionOptional = document.createElement('option');
      optionOptional.value = 'optional';
      optionOptional.textContent = 'Optional';
      importanceSelect.appendChild(optionOptional);

      const optionRelevant = document.createElement('option');
      optionRelevant.value = 'relevant';
      optionRelevant.textContent = 'Relevant';
      importanceSelect.appendChild(optionRelevant);

      if (!['yesno', 'time'].includes(selectedType)) {
        const optionDisplay = document.createElement('option');
        optionDisplay.value = 'display';
        optionDisplay.textContent = 'Display';
        importanceSelect.appendChild(optionDisplay);
      }
    }
  }

  function createFieldRow() {
    const fieldId = 'field-' + Date.now();
    const html = `
      <div class="row mb-3 align-items-end custom-field" id="${fieldId}">
        <div class="col-md-3">
          <label for="${fieldId}-name" class="form-label">Field Name</label>
          <input type="text" id="${fieldId}-name" name="custom_field_key[]" class="form-control" placeholder="e.g. My Metric" />
        </div>
        <div class="col-md-3">
          <label for="${fieldId}-type" class="form-label">Field Type</label>
          <select id="${fieldId}-type" name="custom_field_type[]" class="form-select custom-field-type">
            <option value="text">Text</option>
            <option value="number">Number</option>
            <option value="date">Date</option>
            <option value="time">Time</option>
            <option value="yesno">Yes/No</option>
          </select>
        </div>
        <div class="col-md-3 importance-wrapper">
          <label class="form-label">Importance</label>
          <select name="custom_field_required[]" class="form-select custom-field-required"></select>
        </div>
        <div class="col-md-2 default-wrapper">
          <label class="form-label">Default Value</label>
          <input type="text" name="custom_field_value[]" class="form-control custom-field-value" placeholder="(optional)">
        </div>
        <div class="col-md-1 text-end mt-4">
          <button type="button" class="btn btn-outline-danger btn-sm mt-2 remove-field" data-field-id="${fieldId}">Remove</button>
        </div>
      </div>`;
    customFieldsContainer.insertAdjacentHTML('beforeend', html);
  
    const newRow = document.getElementById(fieldId);
    const select = newRow.querySelector('.custom-field-type');
    applyFieldLogic(select);
  }  

  if (addCustomFieldBtn) {
    addCustomFieldBtn.addEventListener('click', createFieldRow);
  }

  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-field')) {
      const fieldId = e.target.getAttribute('data-field-id');
      const fieldRow = document.getElementById(fieldId);
      if (fieldRow) {
        fieldRow.remove();
      }
    }
  });  

  document.querySelectorAll('.custom-field-type').forEach(applyFieldLogic);

  document.addEventListener('change', (e) => {
    if (e.target.classList.contains('custom-field-type')) {
      applyFieldLogic(e.target);
    }
  });

  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-field')) {
      const fieldId = e.target.getAttribute('data-field-id');
      const fieldRow = document.getElementById(fieldId);
      if (fieldRow) {
        fieldRow.remove();
      }
    }
  });
});