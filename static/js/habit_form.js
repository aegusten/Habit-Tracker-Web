document.addEventListener('DOMContentLoaded', function(){
  const habitForm = document.getElementById('habit-form')
  const guidelinesSection = document.getElementById('guidelines-section')
  const stopSmokingFields = document.getElementById('stopSmokingFields')
  const wakeUpEarlyFields = document.getElementById('wakeUpEarlyFields')
  const eatHealthyFields = document.getElementById('eatHealthyFields')
  const customFieldsSection = document.getElementById('customFieldsSection')
  const customFieldsContainer = document.getElementById('customFieldsContainer')
  const addCustomFieldBtn = document.getElementById('addCustomField')
  const confirmPresetBtn = document.getElementById('confirmPresetBtn')
  const confirmCustomBtn = document.getElementById('confirmCustomBtn')
  function hideAllExtraFields(){
    if(stopSmokingFields) stopSmokingFields.classList.add('d-none')
    if(wakeUpEarlyFields) wakeUpEarlyFields.classList.add('d-none')
    if(eatHealthyFields) eatHealthyFields.classList.add('d-none')
    if(customFieldsSection) customFieldsSection.classList.add('d-none')
    if(customFieldsContainer) customFieldsContainer.innerHTML = ''
  }
  function initTooltips(){
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function(t){ return new bootstrap.Tooltip(t) })
  }
  if(addCustomFieldBtn){
    addCustomFieldBtn.addEventListener('click', () => {
      const fieldId = 'field-' + Date.now()
      const fieldHTML = `
        <div class="row mb-2 align-items-end custom-field" id="${fieldId}">
          <div class="col-md-3">
            <label class="form-label">Field Name</label>
            <input type="text" name="custom_field_key[]" class="form-control" placeholder="e.g., Snoozes">
          </div>
          <div class="col-md-3">
            <label class="form-label">Field Type</label>
            <select name="custom_field_type[]" class="form-select custom-field-type">
              <option value="text">Text</option>
              <option value="number">Number</option>
              <option value="date">Date</option>
              <option value="time">Time</option>
              <option value="yesno">Yes/No</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Default Value</label>
            <input type="text" name="custom_field_value[]" class="form-control custom-field-value" placeholder="(optional)">
          </div>
          <div class="col-md-2 text-end">
            <button type="button" class="btn btn-outline-danger remove-field" data-field-id="${fieldId}">Remove</button>
          </div>
        </div>`
      customFieldsContainer.insertAdjacentHTML('beforeend', fieldHTML)
      initTooltips()
    })
  }
  document.addEventListener('change', e => {
    if(e.target.classList.contains('custom-field-type')){
      const row = e.target.closest('.custom-field')
      const defaultValueInput = row.querySelector('.custom-field-value')
      defaultValueInput.type = e.target.value === 'yesno' ? 'checkbox' : e.target.value
      defaultValueInput.value = ''
    }
  })
  document.addEventListener('click', e => {
    if(e.target.classList.contains('remove-field')){
      const fieldId = e.target.getAttribute('data-field-id')
      const fieldRow = document.getElementById(fieldId)
      if(fieldRow) fieldRow.remove()
    }
  })
  initTooltips()
  if(confirmPresetBtn) confirmPresetBtn.classList.add('d-none')
  if(confirmCustomBtn) confirmCustomBtn.classList.add('d-none')
  const templateCards = document.querySelectorAll('.template-card')
  templateCards.forEach(card => {
    card.addEventListener('click', () => {
      if(habitForm){
        habitForm.classList.remove('d-none')
        habitForm.reset()
      }
      if(guidelinesSection) guidelinesSection.classList.add('d-none')
      hideAllExtraFields()
      if(confirmPresetBtn) confirmPresetBtn.classList.add('d-none')
      if(confirmCustomBtn) confirmCustomBtn.classList.add('d-none')
      const tpl = card.dataset.template
      if(tpl !== 'custom'){
        if(tpl === 'stop_smoking' && stopSmokingFields) stopSmokingFields.classList.remove('d-none')
        else if(tpl === 'wake_up_early' && wakeUpEarlyFields) wakeUpEarlyFields.classList.remove('d-none')
        else if(tpl === 'eat_healthy' && eatHealthyFields) eatHealthyFields.classList.remove('d-none')
        if(confirmPresetBtn) confirmPresetBtn.classList.remove('d-none')
      } else {
        if(confirmCustomBtn) confirmCustomBtn.classList.remove('d-none')
      }
      if(customFieldsSection) customFieldsSection.classList.remove('d-none')
      if(guidelinesSection) guidelinesSection.classList.remove('d-none')
    })
  })
})
