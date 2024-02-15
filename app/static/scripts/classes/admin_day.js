import { Notification } from './notification.js';
const notify = new Notification()

export class AdminDay
{
    constructor(date)
    {
        this.courts = ['grass_one', 'grass_two', 'clay_one']
        this.day = date
        this.buttons = {'grass_one':[], 'grass_two':[], 'clay_one':[]}
    }

    // ============================== AI START ==============================
    getTimesPromise(court) 
    {
      // Asynchronously retrieves booked times for a specified court on selected date'.
        return new Promise(async (resolve, reject) => {
          try {
            const response = await fetch('/api/times_booked', {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ "date": this.day, "court": court })
            });
      
            if (response.ok) {
              let content = await response.json();
              resolve({"court":court,"times":content.times});
            } else {
              reject(new Error('Failed to get times'));
            }
          } catch (error) {
            reject(error);
          }
        });
    }
    // ============================== AI END ==============================
    
    returnAllTimes()
    {
      // Asynchronously retrieves booked times for a all 3 courts on selected date'.
      this.disableAllCourts()
        // ============================== AI END ==============================
        const promises = this.courts.map(court => this.getTimesPromise(court));
        Promise.all(promises)
            .then(resultsArray => {
              resultsArray.forEach(item => {
                this.populateCourts(item.court, item.times)
              })
            })
            .catch(error => {
                console.error('Error:', error);
            });
        // ============================== AI END ==============================
    }

    loadCourt(court_element, court)
    {
      // Loads a given court table with new timeslots
      const court_table_elements = document.getElementsByClassName(court_element)
      let j = 7;
      for(let i = 0; i < court_table_elements.length; i++)
      {
        let button = new AdminTimeSlot(j, court)
        court_table_elements[i].appendChild(button.button)
        this.buttons[court].push(button)
        j++
      }
    } 

    loadAllCourts()
    {
      // Loads all court tables with new timeslots
      this.loadCourt('grass_one_holder', 'grass_one')
      this.loadCourt('grass_two_holder', 'grass_two')
      this.loadCourt('clay_one_holder', 'clay_one')
    }


    populateCourts(court, data)
    {
      // Sets the state of all timeslots for a given court
      let buttons = this.buttons[court]
      for(let i = 0; i < buttons.length; i++)
      {
        buttons[i].setState(data[i+2], this.dayInHistory())
      }
    }

    disableCourt(court)
    {
      // Disables all timeslots of a given court
      for(let i = 0; i < this.buttons[court].length; i++)
      {
        this.buttons[court][i].button.disabled = true
      }
    }

    disableAllCourts()
    {
      // Disables all timeSlots
      for(let i = 0; i < this.courts.length; i++)
      {
        this.disableCourt(this.courts[i])
      }
    }

    setAllClickEvents()
    {
      // Set all click events
      let courtsArr = ['grass_one', 'grass_two', 'clay_one']
      for(let i = 0; i < courtsArr.length; i++)
      {
        this.setClickEvents(courtsArr[i])
      }

      let cancel_btn = document.querySelector('#cancel_booking_btn')
      cancel_btn.addEventListener('click', () => {
        this.handleBooking(document.querySelector('#view_booking_time').value, "Cancel", document.querySelector('#view_booking_court').value, document.querySelector('#view_booking_user').value)
      })

      let createBtn = document.querySelector('#create_booking_btn')
      createBtn.addEventListener('click', () => {
        this.handleBooking(document.querySelector('#new_booking_time').value, false, document.querySelector('#new_booking_court').value, document.querySelector('#new_booking_user').value)
      })
    }
    
    setClickEvents(court)
    {
      // Sets click events for all Timeslot Buttons
      for(let i = 0; i < this.buttons[court].length; i++)
      {
        this.buttons[court][i].button.addEventListener('click', () =>
        {
          if (this.buttons[court][i].button.innerText === 'View')
          {
            this.viewBooking(this.buttons[court][i].button.value, this.buttons[court][i].time, this.buttons[court][i].court)
          }
          else
          {
            this.openBookingModal(this.buttons[court][i].time, this.buttons[court][i].court)
          }

        })
      }
    }

    
    openBookingModal(id, court)
    {
      // Opens and populates the create booking 
      new bootstrap.Modal(document.querySelector("#create_booking_modal")).show();
      let dateTr = document.querySelector('#new_booking_date')
      let timeTr = document.querySelector('#new_booking_time')
      let courtTr = document.querySelector('#new_booking_court')
      let createBtn = document.querySelector('#create_booking_btn')
      dateTr.innerHTML = this.formatDate()
      dateTr.value = this.day
      let courts = {"grass_one":"Grass Court One", "grass_two":"Grass Court Two", "clay_one":"Clay Court"}
      courtTr.innerHTML = courts[court]
      courtTr.value = court
      timeTr.innerHTML = this.formatTimeString(id)
      timeTr.value = id
      createBtn.disabled = false
    }

    viewBooking(email, id, court)
    {
      // Opens and populates the view booking modal
      new bootstrap.Modal(document.querySelector("#view_booking_modal")).show();
      let dateTr = document.querySelector('#view_booking_date')
      let userTr = document.querySelector('#view_booking_user')
      let timeTr = document.querySelector('#view_booking_time')
      let courtTr = document.querySelector('#view_booking_court')
      let cancelBtn = document.querySelector('#cancel_booking_btn')
      let courts = {"grass_one":"Grass Court One", "grass_two":"Grass Court Two", "clay_one":"Clay Court"}
      dateTr.innerHTML = this.formatDate()
      dateTr.value = this.day
      courtTr.innerHTML = courts[court]
      courtTr.value = court
      userTr.innerHTML = email
      userTr.value = email
      timeTr.innerHTML = this.formatTimeString(id)
      timeTr.value = id
      if(this.dayInHistory())
      {
        cancelBtn.disabled = true;
      }
      else
      {
        cancelBtn.disabled = false;
      }
    }

    formatTimeString(time)
    {
      let startTime = time + ":00"
      let endTime = (time+1) + ":00"
      return startTime + " - " + endTime
    }

    // ======================================= AI START =======================================
    formatDate() 
    {
      const dateObject = new Date(this.day);
      // Get the day of the week
      const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const dayOfWeek = daysOfWeek[dateObject.getDay()];

      // Get the day with the correct ordinal suffix
      const day = dateObject.getDate();
      const suffix = (day >= 11 && day <= 13) || day % 10 !== 1 ? 'th' : day % 10 === 2 ? 'nd' : day % 10 === 3 ? 'rd' : 'th';

      // Get the month
      const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      const month = months[dateObject.getMonth()];

      // Format the date as "DayOfWeek DayOfMonthth MonthName"
      const formattedDate = `${dayOfWeek} ${day}${suffix} ${month}`;

      return formattedDate;
    }
    // ======================================= AI END =======================================
    
    dayInHistory() {
      // Checks if the day selected is in the past
      let today = new Date();
      today.setHours(0, 0, 0, 0);
      let compareDate = new Date(this.day);
      return compareDate < today;
    }

    async handleBooking(time, cancel, court, user) {
      // Sends a booking or cancellation request to the server and then updates the court table with the new court schedule.
      let bookingObj = this.createBookingObject(time, cancel, court, user);
      try {
        const response = await fetch('/api/handle_booking', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(bookingObj)
        });
    
        if (response.ok) {
          const content = await response.json();
          // ======================================= AI START =======================================
          // Use .then to execute code after the response has been fully received
          return Promise.resolve().then(() => {
            notify.showNotification(content);
            // Use the stored content instead of re-reading the response body
            // ======================================= AI END =======================================
            this.disableAllCourts();
            this.returnAllTimes();
          });
        } else {
          throw new Error('Failed to book slot');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }

    createBookingObject(time, cancel, court, user)
    // Formats a booking ready to send to server
    {
        let bookingObj = 
        {
            "date":this.day,
            "time":time,
            "court":court,
            "user":user
        }
        if(cancel === "Cancel")
        {
            bookingObj['cancel'] = true
        }
        else
        {
            bookingObj['cancel'] = false
        }
            
        return bookingObj
    }
  
}

export class AdminTimeSlot 
{
  // Stores and manages the physical TimeSlot Buttons
  constructor(time, court) 
  {
    this.time = time;
    this.court = court;
    this.button = this.createButton(court);
  }

  createButton(court)
  {
    // Creates and returns the physical TimeSlot Button
    const timeslot = document.createElement('button');
    timeslot.classList.add('btn', 'w-100', 'shadow', court, 'btn-purp', 'book-btn') 
    timeslot.innerText = this.returnTimeString() 
    timeslot.value = 0;
    timeslot.id = this.time
    return timeslot;
  }

  setState(state, dayInHistory)
  {
    // Sets the state of TimeSlot Button
      if(state === "0")
      {
        if(dayInHistory)
        {

          this.button.disabled = true;
        }
        else
        {
          this.button.disabled = false;
        }
        this.button.innerText = this.returnTimeString()
        this.button.classList = ('')
        this.button.classList.add('btn', 'btn-available', 'w-100', 'shadow', 'book-btn')
      } 
      else 
      {
        this.button.disabled = false;
        this.button.innerText = "View";
        this.button.value = state
        this.button.classList.add('btn', 'btn-cancel', 'shadow', 'w-100', 'book-btn')
      }
  }
  
  returnTimeString() 
  {
    return this.time + ":00";
  }

}


export class AdminUserSearch
{
  constructor() 
  {
    this.searchBars = []
  }

  async getUserEmail(email) 
  {
    // Returns a users details for a given email address.
    try 
      {
        const response = await fetch('/api/search_user_email', {
        method: 'POST',
        headers: 
        {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "user": email})
        });
        if (response.ok) 
        {
        let content = await response.json();
        this.populateUserDetails(content.user)
        } 
      } 
      catch(error) 
      {
        console.error('Error:', error);
    }
  }
  
  populateDropDowns(emails)
  {
    // Populates the Select inputs for user search bars
    let searchBars = document.getElementsByClassName('user_selects')
    for(let i = 0; i < searchBars.length; i ++)
    {
      for(let j = 0; j < emails.length; j++)
      {
        let opt = document.createElement('option')
        opt.value = emails[j]
        opt.innerText = emails[j]
        searchBars[i].appendChild(opt)
      }
    }
  }

  async setUserDropDowns()
  {
    // Returns all user email addresses within the database
    fetch('/api/return_users', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(content => {
      this.populateDropDowns(content['emails'])
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  setSearchFunction()
  {
    // Sets the input triggers for the select inputs (user search bars)
    let searchBox = document.getElementById('usersearch')
    searchBox.addEventListener('input', () => {
      this.getUserEmail(searchBox.value)
    })
  }

  populateUserDetails(user)
  {
    // Populates the User Details Sections with a users details
    let usersEmail = document.getElementById('usersearch')
    usersEmail.value = user.username
    let firstNameDiv = document.getElementById('search_firstname')
    let lastnameDiv = document.getElementById('search_lastname')
    let roleDiv = document.getElementById('search_role')
    let emailDiv = document.getElementById('search_email')
    let phoneDiv = document.getElementById('search_phone')
    firstNameDiv.innerHTML = user.firstname
    lastnameDiv.innerHTML = user.lastname
    roleDiv.innerHTML = user.role
    emailDiv.innerHTML = user.username
    phoneDiv.innerHTML = user.phonenumber

  }

  async openUsersProfile()
  {
    // Returns a users details when opening up the profile modal
    let usersEmail = document.getElementById('usersearch')
    try 
    {
      const response = await fetch('/api/search_user_email', {
      method: 'POST',
      headers: 
      {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "user": usersEmail.value})
      });
      if (response.ok) 
      {
      let content = await response.json();
      this.populateUserProfile(content.user)
      } 
    } 
    catch(error) 
    {
      console.error('Error:', error);
    }
  }

  populateUserProfile(user)
  {
    // Populates the profile sections with a users details
    let profileFirstname = document.getElementById('firstname')
    let profileLastname = document.getElementById('lastname')
    let profileHousenum = document.getElementById('housenum')
    let profileStreet = document.getElementById('street')
    let profileTown = document.getElementById('town')
    let profilePostcode = document.getElementById('postcode')
    let profileEmail = document.getElementById('email')
    let profileHiddenEmail = document.getElementById('hidden_email')
    let profilePhoneNum = document.getElementById('phonenum')
    profileFirstname.value = user.firstname
    profileLastname.value = user.lastname
    profileHousenum.value = user.housenum
    profileStreet.value = user.street
    profileTown.value = user.town
    profilePostcode.value = user.postcode
    profileEmail.value = user.username
    profileHiddenEmail.value = user.username
    profilePhoneNum.value = user.phonenumber
    var profileModal = new bootstrap.Modal(document.getElementById('profile_modal'));
    profileModal.show();

  }

}