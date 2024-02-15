# Serve Reserve Tennis Booking Application

## To Run:
- Fork Repository
- Terminal:
  - ``` py -m venv venv ```
  - ``` venv/Scripts/activate ```
  - ``` pip install -r requirements.txt ```
  - ``` py run.py ```

## Testing:
Tests Do Not Run In The Command Line! Could Not Resolve The Issue
- ALL 60 Tests Pass 

To Run Tests:
- Enable Discovery of Python unittest tests within your IDE
- When prompted for directory select 'tests'
- when prompted for the pattern to identify tests select "Python files containing the word 'test'"
- You may have to close and restart the virtual environemnt to discover the tests if they are not found
- View Appendix U for picture demonstration in Visual Studio Code

## Dependencies:
- annotated-types==0.6.0
- bcrypt==4.0.1
- blinker==1.6.3
- cffi==1.16.0
- click==8.1.7
- colorama==0.4.6
- cryptography==41.0.4
- Flask==3.0.0
- Flask-Bcrypt==1.0.1
- Flask-Mail==0.9.1
- itsdangerous==2.1.2
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- psycopg2==2.9.9
- pycparser==2.21
- pydantic==2.4.2
- pydantic_core==2.10.1
- python-dotenv==1.0.0
- typing_extensions==4.8.0
- Werkzeug==3.0.0


## AI Generated
- All code with AI commented at the end been generated using Chat-GPT 3.5 architecure, example below.

  ``` x = 5 #AI ```

  ``` let x = 5 //AI ```

- All Code Between AI START and AI END is also generated using Chat-GPT 3.5 architecure, example below
```
  // ======================================= AI START =======================================
  let today = new Date();
  let thirtyDaysFromNow = new Date();
  thirtyDaysFromNow.setDate(today.getDate() + 30);
  let formattedToday = today.toISOString().split('T')[0];
  let formattedThirtyDaysFromNow = thirtyDaysFromNow.toISOString().split('T')[0];
  // ======================================= AI END ======================================= 
```
