import {set_page_height} from './main.js';
import {FormValidator} from './classes/formValidation.js'
import { Notification } from './classes/notification.js';



const notificaiton = new Notification()

document.addEventListener("DOMContentLoaded", function() {
  set_page_height();
  set_terms_cond_btns();
  notificaiton.if_message_to_dsiplay();
});

// Register Account Form
const form = new FormValidator('register_btn')

let fname_inp = document.getElementById('fname_inp')
let lname_inp = document.getElementById('lname_inp')
let email_inp = document.getElementById('email_inp')
let password_inp = document.getElementById('password_inp')
let confirm_pword = document.getElementById('confirm_pass_inp')

fname_inp.addEventListener('blur', function(){
  let x = form.check_name('fname_inp', "name_instructions")
  if(x === true)
  {
    form.display_popup('terms_conditions', [form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_passw("password_inp", "password_instructions"), form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

lname_inp.addEventListener('blur', function(){
  let y = form.check_name('lname_inp', "name_instructions")
  if(y === true)
  {
    form.display_popup('terms_conditions', [form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_passw("password_inp", "password_instructions"), form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

email_inp.addEventListener('blur', function(){
  let z = form.check_email('email_inp', "email_instructions")
  if(z === true)
  {
    form.display_popup('terms_conditions', [form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_passw("password_inp", "password_instructions"), form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

password_inp.addEventListener('blur', function(){
  let b = form.check_passw("password_inp", "password_instructions")
  if(b === true)
  {
    form.display_popup('terms_conditions', [form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_passw("password_inp", "password_instructions"), form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

confirm_pword.addEventListener('input', function(){
  let c = form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")
  if(c === true)
  {
    form.display_popup('terms_conditions', [form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_passw("password_inp", "password_instructions"), form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

function set_terms_cond_btns(){
  let buttons = document.getElementsByClassName('dis-agree-btn')
  for(let i = 0; i < buttons.length; i++)
  {
    buttons[i].addEventListener('click', function()
    {
      if(this.value === "agree")
      {
        form.enable_submit([true]);
      } 
      else 
      {
        form.disable_submit();
      }
    })
  }
}

