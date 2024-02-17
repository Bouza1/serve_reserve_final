import { Notification } from './notification.js';
const notify = new Notification()

export class Day
{
    constructor(court, date, user)
    {
        this.court = court;
        this.day = date;
        this.user = user;
        this.buttons = []
    }
    
    renderButtons()
    {
      // Loads new TimeSlots
        let parentDiv = document.getElementById("button-container");
        for(let i=7; i < 19; i++)
        {
            const button = new TimeSlot(i);
            this.buttons.push(button)
            parentDiv.appendChild(button.button);
        }
    }

    async getTimes() 
    {
      // Asynchronously retrieves booked times for a specified court on a selected date'.
        try 
        {
            const response = await fetch('/api/times_booked', {
            method: 'PUT',
            headers: 
            {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "date": this.day, "court":this.court})
            });
            if (response.ok) 
            {
            let content = await response.json();
            for(let i = 0; i < this.buttons.length; i++){
                this.buttons[i].setState(content.times[i+2], this.user, this.buttons[i].button);
            }
            } 
            else 
            {
            throw new Error('Failed to get times');
            }
        } 
        catch(error) 
        {
            console.error('Error:', error);
        }
    }

    async handleBooking(time, cancel)
    {
    // Sends a booking or cancellation request to the server and then updates the court table with the new court schedule.
      let bookingObj = this.createBookingObject(time, cancel);
      this.disableAllButtons()
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
          notify.showNotification(content) 
          this.getTimes()
        } else {
          throw new Error('Failed to book slot');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }

    createBookingObject(time, cancel)
    {
      // Formats a booking ready to send to server
        let bookingObj = 
        {
            "date":this.day,
            "time":time,
            "court":this.court,
            "user":this.user
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


    disableAllButtons()
    {
      // Disables all TimeSlots
        for (let i=0; i < this.buttons.length; i ++)
        {
            this.buttons[i].button.disabled = true;
        }
    }

    setMinMaxDates(element)
    {
      // Sets the min and max dates of the calender dorp down
      let date_inp = document.getElementById(element)
      let today = new Date();
      let thirtyDaysFromNow = new Date();
      thirtyDaysFromNow.setDate(today.getDate() + 30);
      let formattedToday = today.toISOString().split('T')[0];
      let formattedThirtyDaysFromNow = thirtyDaysFromNow.toISOString().split('T')[0];
      date_inp.min = formattedToday;
      date_inp.max = formattedThirtyDaysFromNow;
    }
      
}

export class TimeSlot 
{
    constructor(time)
    {
        this.time = time;
        this.button = this.createButton();
    }

    createButton() 
    {
      // Creates and returns the physical TimeSlot Button
        const timeslot = document.createElement('button'); 
        timeslot.classList.add('btn', 'btn-sm', 'btn-available', 'shadow', 'w-100', 'book-btn'); 
        timeslot.innerText = this.returnTimeString(); 
        timeslot.value = 0;
        timeslot.id = this.time
        return timeslot;
    }

    returnTimeString() 
    {
        return this.time + ":00";
    }

    setState(state, user, button)
    {
      // Sets Stats of TimeSlot Button
        if(state === "0")
        {
          button.disabled = false;
          button.innerText = this.returnTimeString()
          button.classList = ('')
          button.classList.add('btn', 'btn-sm', 'btn-available', 'shadow', 'w-100', 'book-btn')
        } 
        else if(state === user)
        {
          button.disabled = false;
          button.innerText = "Cancel";
          button.classList = ('')
          button.classList.add('btn', 'btn-sm', 'btn-cancel', 'shadow', 'w-100', 'book-btn')
          // button.setAttribute('class', 'btn btn-sm btn-warning text-light shadow w-100 book-btn');
        } 
        else 
        {
          button.disabled = true;
          button.innerText = "Not Available";
          button.setAttribute('class', 'btn btn-unavailable btn-sm btn-un text-light shadow w-100 book-btn');
        }
    }
}
