import {set_page_height } from './main.js';
import {FormValidator} from './classes/formValidation.js'
import { Notification } from './classes/notification.js';

const notificaiton = new Notification()


document.addEventListener("DOMContentLoaded", function() {
  set_page_height();
  notificaiton.if_message_to_dsiplay();
  
});

// Login Form
const form = new FormValidator('login-btn')

let username_inp = document.getElementById('username')
username_inp.addEventListener('blur', function(){
  let x = form.check_email('username', "email_instructions")
  if(x === true)
  {
    form.enable_submit([form.check_email('username', "email_instructions"), form.check_passw("password", "password_instructions")])
  }
  else
  {
    form.disable_submit()
  }
})

let password_inp = document.getElementById('password')
password_inp.addEventListener('input', function(){
  let y = form.check_passw("password", "password_instructions")
  if(y === true)
  {
    form.enable_submit([form.check_email('username', "email_instructions"), form.check_passw("password", "password_instructions")])
  }
  else
  {
    form.disable_submit()
  }
})

// Reset Form
const resetForm = new FormValidator ('reset_email_btn')

let reset_email_inp = document.getElementById('username_reset')
reset_email_inp.addEventListener('blur', function(){
  let x = resetForm.check_email('username_reset', "reset_email_instructions")
  if(x === true)
  {
    resetForm.enable_submit([form.check_email('username_reset', "reset_email_instructions")])
  }
  else
  {
    resetForm.disable_submit()
  }
})