document.addEventListener('DOMContentLoaded', () => {
  const customFieldsContainer = document.getElementById('customFieldsContainer');
  const addCustomFieldBtn = document.getElementById('addCustomField');

  document.querySelectorAll('.template-card').forEach(card => {
    card.addEventListener('click', () => {
      const selectedTemplate = card.getAttribute('data-template');
      window.location.href = `/habits/new/?template=${selectedTemplate}`;
    });
  });

  function createFieldRow() {
    const fieldId = 'field-' + Date.now();
    return `
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
        <div class="col-md-3">
          <label for="${fieldId}-importance" class="form-label">Importance</label>
          <select id="${fieldId}-importance" name="custom_field_required[]" class="form-select custom-field-required">
            <option value="optional">Optional</option>
            <option value="relevant">Relevant</option>
          </select>
        </div>
        <div class="col-md-2">
          <label for="${fieldId}-default" class="form-label">Default Value</label>
          <input type="text" id="${fieldId}-default" name="custom_field_value[]" class="form-control custom-field-value" placeholder="(optional)">
        </div>
        <div class="col-md-1 text-end">
          <button type="button" class="btn btn-outline-danger remove-field" data-field-id="${fieldId}">Remove</button>
        </div>
      </div>`;
  }

  if (addCustomFieldBtn) {
    addCustomFieldBtn.addEventListener('click', () => {
      const newFieldHTML = createFieldRow();
      customFieldsContainer.insertAdjacentHTML('beforeend', newFieldHTML);
    });
  }

  document.addEventListener('change', (e) => {
    if (e.target.classList.contains('custom-field-type')) {
      const row = e.target.closest('.custom-field');
      const defaultInput = row.querySelector('.custom-field-value');
      if (e.target.value === 'yesno') {
        defaultInput.style.display = 'none';
        defaultInput.value = '';
      } else {
        defaultInput.style.display = '';
      }
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
