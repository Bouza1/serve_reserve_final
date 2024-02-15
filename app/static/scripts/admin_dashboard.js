// import {set_page_height, if_message_to_dsiplay} from './main.js';
import {FormValidator} from './classes/formValidation.js'
import {AdminDay} from './classes/admin_day.js'
import { AdminUserSearch } from './classes/admin_day.js'
import { Notification } from './classes/notification.js';

const notificaiton = new Notification()

let search;
let day;

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('date').valueAsDate = new Date();
    day = new AdminDay(document.getElementById("date").value)
    day.loadAllCourts()
    day.setAllClickEvents()
    day.returnAllTimes()
    search = new AdminUserSearch()
    search.setUserDropDowns()
    search.setSearchFunction()
    setChangeDate()
    notificaiton.if_message_to_dsiplay();
});

function setChangeDate()
{
    let date_inp = document.getElementById('date');
    date_inp.addEventListener("change", getDay);
}

function getDay()
{
  day.day = document.getElementById('date').value
  day.returnAllTimes()
}

// Create User Account Form
const form = new FormValidator('create_user_btn')
let fname_inp = document.getElementById('fname_inp')
let lname_inp = document.getElementById('lname_inp')
let email_inp = document.getElementById('email_inp')
let email_confirm_inp = document.getElementById('email_confirm_inp')

fname_inp.addEventListener('blur', function(){
  let x = form.check_name('fname_inp', "name_instructions")
  if(x === true)
  {
    form.enable_submit([form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_confirm('email_inp', 'email_confirm_inp', "email_instructions")])
  }
})

lname_inp.addEventListener('blur', function(){
  let y = form.check_name('lname_inp', "name_instructions")
  if(y === true)
  {
    form.enable_submit([form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_confirm('email_inp', 'email_confirm_inp', "email_instructions")])
  }
})

email_inp.addEventListener('blur', function(){
  let z = form.check_email('email_inp', "email_instructions")
  if(z === true)
  {
    form.enable_submit([form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_confirm('email_inp', 'email_confirm_inp', "email_instructions")])
  }
})

email_confirm_inp.addEventListener('input', function(){
  let c = form.check_confirm('email_inp', 'email_confirm_inp', "email_instructions")
  if(c === true)
  {
    form.enable_submit([form.check_name('fname_inp', "name_instructions"), form.check_name('lname_inp', "name_instructions"), form.check_email('email_inp', "email_instructions"), form.check_confirm('email_inp', 'email_confirm_inp', "email_instructions")])
  }
})

let openUsersProfile = document.getElementById('open-users-profile')
openUsersProfile.addEventListener('click', function() {
  search.openUsersProfile()
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

let deleteUserBtn = document.getElementById('delete-users-profile')
deleteUserBtn.addEventListener('click', function() {
  let userChosen = document.getElementById('usersearch')

  let p_user_display = document.getElementById("users_email")
  p_user_display.innerText = userChosen.value  

  let hidden_inp = document.getElementById("email_delete")
  hidden_inp.value = userChosen.value

  var deleteAccountModal = new bootstrap.Modal(document.getElementById('delete_modal'));
  deleteAccountModal.show();

})


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