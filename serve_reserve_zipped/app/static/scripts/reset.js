import {set_page_height} from './main.js';
import {FormValidator} from './classes/formValidation.js'

document.addEventListener("DOMContentLoaded", function() {
  set_page_height();
});


const form = new FormValidator('reset_btn')

let password_inp = document.getElementById('password_inp')
let confirm_pword = document.getElementById('confirm_pass_inp')

password_inp.addEventListener('blur', function(){
  let b = form.check_passw("password_inp", "password_instructions")
  if(b === true)
  {
    form.enable_submit([form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})

confirm_pword.addEventListener('input', function(){
  let c = form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")
  if(c === true)
  {
    form.enable_submit([form.check_confirm('password_inp', 'confirm_pass_inp', "confirm_pword_instructions")])
  }
})
