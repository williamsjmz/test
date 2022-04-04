document.addEventListener('DOMContentLoaded', () => {

  const upload_changes = document.querySelector('#upload-changes-link');
  upload_changes.addEventListener('click', () => {

    const container = document.querySelector('#alerts-container');
    container.innerHTML = ``;

    fetch(`upload_changes/`, { method: "POST", })
    .then(response => response.json())
    .then(data => {
      if (data['message'] === 'success') {
        
        const my_alert = document.createElement('div');
        my_alert.classList.add('alert');
        my_alert.classList.add('alert-success');
        my_alert.innerHTML = `Portal updated successfully.`;

        const container = document.querySelector('#alerts-container');
        container.append(my_alert);

      }else {

        const my_alert = document.createElement('div');
        my_alert.classList.add('alert');
        my_alert.classList.add('alert-danger');
        my_alert.innerHTML = `${data['message']}`;

        const container = document.querySelector('#alerts-container');
        container.append(my_alert);

      }
    })

  })

})