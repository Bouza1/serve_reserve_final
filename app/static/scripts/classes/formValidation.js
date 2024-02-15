export class FormValidator {
    // Provides unfiromed validation to all forms.
    constructor(submit_button) 
    {
        this.submit = document.getElementById(submit_button)
        this.instructionsFlag = {}
    }
    
    check_passw(element, instructions_element)
    {
        // Checks inputted passwords conform to the requirements and applys styling/ shows intructions depenedent on result
        let password_inp = document.getElementById(element)
        let instructions = document.getElementById(instructions_element)
        let password_value = password_inp.value
        let pword_reg_x = /^(?=.*[A-Z])(?=.*\d).{8,}$/
        if(password_value.match(pword_reg_x)){
            this.applyCorrectStyling(password_inp)
            instructions.style.display = "none";
            this.instructionsFlag[instructions_element] = 0
            return true;
        } else {
            this.applyWrongStyling(password_inp)
            if(!Object.values(this.instructionsFlag).includes(1))
            {
                instructions.style.display = "block";
                this.instructionsFlag[instructions_element] = 1
            }
            return false;
        }
    }

    check_confirm(og_element, confirm_element, instructions_element)
    {
        // Checks confirm inputs conform to the requirements and applys styling / shows intructions depenedent on result
        let og_input = document.getElementById(og_element)
        let confirm_input = document.getElementById(confirm_element)
        let instructions = document.getElementById(instructions_element)
        if(og_input.value === confirm_input.value && confirm_input.value.length > 7)
        {
            this.applyCorrectStyling(confirm_input)
            instructions.style.display = "none";
            this.instructionsFlag[instructions_element] = 0
            return true;
        } 
        else 
        {
            this.applyWrongStyling(confirm_input)
            if(!Object.values(this.instructionsFlag).includes(1))
            {
                instructions.style.display = "block";
                this.instructionsFlag[instructions_element] = 1
            }
            return false;
        }
    }

    enable_submit(arr)
    {
        // Checks all inputs and enables/disables submit button dependent on results
        for(let i = 0; i < arr.length; i++)
        {
            if(arr[i] === false)
            {
                this.submit.disabled = true;
            }
            else
            {
                this.submit.disabled = false;
            }
        }
    }

    disable_submit()
    {
        // Disables the submit button of the form 
        this.submit.disabled = true;
    }

    clear_all_inputs(arr)
    {
        // Clears all inputs
        arr.forEach(element =>{
            let inp = document.getElementById(element)
            inp.value = ""
            inp.innerText = ""
        })
    }
    
    check_email(element, instructions_element)
    {
        // Checks inputted emails conform to the requirements and applys styling/ shows intructions depenedent on result
        let uname = document.getElementById(element)
        let instructions = document.getElementById(instructions_element)
        let email_value = uname.value
        let mail_reg_x = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if(email_value.match(mail_reg_x))
        {
            this.applyCorrectStyling(uname)
            instructions.style.display = "none";
            this.instructionsFlag[instructions_element] = 0
            return true;
        }
        else
        {
            this.applyWrongStyling(uname)
            if(!Object.values(this.instructionsFlag).includes(1))
            {
                instructions.style.display = "block";
                this.instructionsFlag[instructions_element] = 1
            }
            return false;
        }
    }

    check_name(element, instructions_element)
    {
        // Checks inputted names conform to the requirements and applys styling/ shows intructions depenedent on result
        let name_inp = document.getElementById(element)
        let instructions = document.getElementById(instructions_element)
        let name_value = name_inp.value
        if((name_value.length >= 3) && (/^[a-zA-Z]+$/.test(name_value)))
        {
            this.applyCorrectStyling(name_inp)
            instructions.style.display = "none";
            this.instructionsFlag[instructions_element] = 0
            return true;
        } 
        else 
        {
            this.applyWrongStyling(name_inp)
            if(!Object.values(this.instructionsFlag).includes(1))
            {
                instructions.style.display = "block";
                this.instructionsFlag[instructions_element] = 1
            }
            return false;
        }
    }

    display_popup(element, arr)
    {
        // Checks all inputs and displays popup dependent on results
        let popup = document.getElementById(element)
        for(let i = 0; i < arr.length; i++)
        {
            if(arr[i] === false)
            {
                popup.style.display = "none";
            }
            else
            {
                if(!Object.values(this.instructionsFlag).includes(1))
                {
                    popup.style.display = "block";
                }
            }
        }
    }

    applyCorrectStyling(element)
    {
        // Applies styling to an element which is validated
        element.style.border = "3px solid #9F9DFF";
    }

    applyWrongStyling(element)
    {
        // Applies styling to an element which is invalid
        element.style.border = "3px solid #FDC5C5";
    }

}
  
