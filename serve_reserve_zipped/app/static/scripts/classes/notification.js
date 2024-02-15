export class Notification {
  constructor() 
  {
  
  }

  if_message_to_dsiplay() 
  {
    // Checks if there is a message to display, if so displays it
      try {
          let message = document.getElementById('message').innerText;
          let message_object = JSON.parse(message);
          this.showNotification(message_object);
      } catch (error) {
          console.log(error);
      }
  }

  showNotification(message) 
  {
    // Formats a message to the notificationa and displays it
      let toastDiv = document.createElement('div');
      let toast_type = "notify_" + message['type'];
      toastDiv.setAttribute('id', 'liveToast');
      toastDiv.classList.add('toast', 'hide', 'notifcation-styl', 'my-3');
      toastDiv.setAttribute('role', 'alert');
      toastDiv.setAttribute('aria-live', 'assertive');
      toastDiv.setAttribute('aria-atomic', 'true');
    

      let toastHeader = document.createElement('div');
      toastHeader.classList.add('toast-header', 'bg-purp', 'notifcation_head', toast_type);

      let toastTitle = document.createElement('strong');
      toastTitle.classList.add('me-auto');
      toastTitle.setAttribute('id', 'toast-title');
      toastTitle.innerText = message['title'];

      let toastTime = document.createElement('small');
      toastTime.textContent = 'Just Now';

      let closeButton = document.createElement('button');
      closeButton.setAttribute('type', 'button');
      closeButton.classList.add('btn-close');
      closeButton.setAttribute('data-bs-dismiss', 'toast');
      closeButton.setAttribute('aria-label', 'Close');
      closeButton.addEventListener('click', () => {
          this.destroyNotification(); 
      });


      let toastBody = document.createElement('div');
      toastBody.classList.add('toast-body');
      toastBody.setAttribute('id', 'toast-body');
      let p_tag = document.createElement('p');

      p_tag.innerText = message['message'];
      toastBody.appendChild(p_tag);

      toastHeader.appendChild(toastTitle);
      toastHeader.appendChild(toastTime);
      toastHeader.appendChild(closeButton);
      toastDiv.appendChild(toastHeader);
      toastDiv.appendChild(toastBody);

      let toastContainer = document.getElementById('toast_div');
      toastContainer.appendChild(toastDiv);

      const myToast = new bootstrap.Toast(toastDiv);
      myToast.show();
  }

  destroyNotification() 
  {
    // Destorys the notifcaiton when called upon
      let toastContainer = document.getElementById('toast_div');
      while (toastContainer.firstChild) 
      {
          toastContainer.removeChild(toastContainer.firstChild);
      }
  }

}
