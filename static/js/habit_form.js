document.addEventListener('DOMContentLoaded', function() {
    const habitForm = document.getElementById('habit-form');
    const guidelinesSection = document.getElementById('guidelines-section');
    const stopSmokingFields = document.getElementById('stopSmokingFields');
    const wakeUpEarlyFields = document.getElementById('wakeUpEarlyFields');
    const eatHealthyFields = document.getElementById('eatHealthyFields');
    const customFieldsSection = document.getElementById('customFieldsSection');
    const customFieldsContainer = document.getElementById('customFieldsContainer');
    const addCustomFieldBtn = document.getElementById('addCustomField');

    function hideAllExtraFields() {
      [stopSmokingFields, wakeUpEarlyFields, eatHealthyFields, customFieldsSection].forEach(d => d.classList.add('d-none'));
      customFieldsContainer.innerHTML = '';
    }

    addCustomFieldBtn.addEventListener('click', () => {
      const fieldId = 'field-' + Date.now();

      const fieldHTML = `
        <div class="row mb-2 align-items-end custom-field" id="${fieldId}">
          <div class="col-md-3">
            <label class="form-label">Field Name <i class="bi bi-question-circle text-primary" data-bs-toggle="tooltip" title="Enter a descriptive label for your metric."></i></label>
            <input type="text" name="custom_field_key[]" class="form-control" placeholder="e.g., Snoozes">
          </div>
          <div class="col-md-3">
            <label class="form-label">Field Type <i class="bi bi-question-circle text-primary" data-bs-toggle="tooltip" title="Choose how you want to track data."></i></label>
            <select name="custom_field_type[]" class="form-select custom-field-type">
              <option value="text">Text</option>
              <option value="number">Number</option>
              <option value="date">Date</option>
              <option value="time">Time</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Default Value <i class="bi bi-question-circle text-primary" data-bs-toggle="tooltip" title="Optional starting value."></i></label>
            <input type="text" name="custom_field_value[]" class="form-control custom-field-value" placeholder="(optional)">
          </div>
          <div class="col-md-2 text-end">
            <button type="button" class="btn btn-outline-danger remove-field" data-field-id="${fieldId}">Remove</button>
          </div>
        </div>`;

      customFieldsContainer.insertAdjacentHTML('beforeend', fieldHTML);
      initTooltips();
    });

    document.addEventListener('change', e => {
      if (e.target.classList.contains('custom-field-type')) {
        const row = e.target.closest('.custom-field');
        const defaultValueInput = row.querySelector('.custom-field-value');
        defaultValueInput.type = e.target.value;
        defaultValueInput.value = '';
      }
    });

    document.addEventListener('click', e => {
      if (e.target.classList.contains('remove-field')) {
        const fieldId = e.target.getAttribute('data-field-id');
        const fieldRow = document.getElementById(fieldId);
        if (fieldRow) { fieldRow.remove(); }
      }
    });

    function initTooltips() {
      let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

      tooltipTriggerList.map(function(t) { return new bootstrap.Tooltip(t); });

    }
    initTooltips();

    document.querySelectorAll('.template-card').forEach(card => {
      card.addEventListener('click', () => {
        
        habitForm.classList.remove('d-none');
        habitForm.reset();
        guidelinesSection.classList.add('d-none');

        hideAllExtraFields();
        
        const tpl = card.dataset.template;

        if (tpl !== 'custom') {
          if (tpl === 'stop_smoking') { stopSmokingFields.classList.remove('d-none'); }
          else if (tpl === 'wake_up_early') { wakeUpEarlyFields.classList.remove('d-none'); }
          else if (tpl === 'eat_healthy') { eatHealthyFields.classList.remove('d-none'); }
        }

        customFieldsSection.classList.remove('d-none');
        guidelinesSection.classList.remove('d-none');
      });
    });
  });
  