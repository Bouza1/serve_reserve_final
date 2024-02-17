import {Day} from './classes/user_day.js'
import {FormValidator} from './classes/formValidation.js'
import { Notification } from './classes/notification.js';
const notificaiton = new Notification()
let day;

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('date').valueAsDate = new Date();
    set_change_date_func()
    setupRadioButtons();
    day = new Day(document.querySelector(".btn-court-active").id, document.getElementById("date").value, returnUser())
    day.renderButtons();
    day.disableAllButtons()
    day.getTimes()
    day.setMinMaxDates('date')
    set_click_events();
    notificaiton.if_message_to_dsiplay();
});

function set_click_events(){
  for(let i = 0; i < day.buttons.length; i++)
  {
    day.buttons[i].button.addEventListener('click', function()
    {
      day.handleBooking(day.buttons[i].button.id, day.buttons[i].button.innerText)
    })
  }
}

function setupRadioButtons() {
  const radioButtons = document.querySelectorAll('.court_radio');
  radioButtons.forEach((radio) => {
    radio.addEventListener('change', (event) => {
      const labels = document.querySelectorAll('.btn-court-active');
      labels.forEach((label) => {
        label.classList.remove('btn-court-active');
        label.classList.add('btn-court')
      });
      const selectedLabel = event.target.parentElement;
      selectedLabel.classList.remove('btn-court');
      selectedLabel.classList.add('btn-court-active');
      day.disableAllButtons()
      day.court = event.target.id
      day.getTimes()
    });
  });
}

function returnUser(){
    let user = document.getElementById('hidden_u').innerText;
    return user
}

function set_change_date_func(){
    let date_inp = document.getElementById('date');
    date_inp.addEventListener("change", getday);
}

function getday(){
    day.day = document.getElementById("date").value;
    day.disableAllButtons()
    day.getTimes()
}

// Change Password Form
const change_p_form = new FormValidator('change_pword_btn')

let password_inp = document.getElementById('new_pword')
let confirm_pword = document.getElementById('confirm_pass_inp')
let change_btn = document.getElementById('change_pword_btn')

password_inp.addEventListener('input', function(){
  let bool = change_p_form.check_passw('new_pword', "password_instructions")
  if(bool === true)
  {
    change_p_form.enable_submit([change_p_form.check_passw('new_pword', "password_instructions"), change_p_form.check_confirm('new_pword', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

confirm_pword.addEventListener('input', function(){
  let bool = change_p_form.check_confirm('new_pword', 'confirm_pass_inp', "confirm_pword_instructions")
  if (bool === true)
  {
    change_p_form.enable_submit([change_p_form.check_passw('new_pword', "password_instructions"), change_p_form.check_confirm('new_pword', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

// Delete Account Form
const delete_acc_form = new FormValidator('final_delete_btn')
let del_acc_pword_inp = document.getElementById('delete_pword')
let confirm_del_acc_pword_inp = document.getElementById('confirm_delete_pword')

del_acc_pword_inp.addEventListener('input', function(){
  let bool = delete_acc_form.check_passw('delete_pword', "delete_warning")
  if(bool === true)
  {
    delete_acc_form.enable_submit([delete_acc_form.check_passw('delete_pword', 'delete_warning'), delete_acc_form.check_confirm('delete_pword', 'confirm_delete_pword', 'delete_warning')])
  }
})

confirm_del_acc_pword_inp.addEventListener('input', function(){
 let bool =  delete_acc_form.check_confirm('delete_pword', 'confirm_delete_pword', 'delete_warning')
 if(bool === true)
 {
   delete_acc_form.enable_submit([delete_acc_form.check_passw('delete_pword', 'delete_warning'), delete_acc_form.check_confirm('delete_pword', 'confirm_delete_pword', 'delete_warning')])
 }
})

const rows = document.querySelectorAll('.profile_row');
rows.forEach(row => {
  const tds = row.querySelectorAll('td');
  const editSvg = tds[2].querySelector('svg');
  tds.forEach(td => {
    td.addEventListener('mouseenter', () => {
      editSvg.style.visibility = 'visible';
    });
    td.addEventListener('mouseleave', () => {
      editSvg.style.visibility = 'hidden';
    });
  });
  rows.forEach(row => {
    const input = row.querySelector('input');
    row.addEventListener('click', () => {
      input.focus();
    });
  });
});
