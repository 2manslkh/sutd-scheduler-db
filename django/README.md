## CI02 Group3 Scheduler Website 

### Pages/Features
**Accessible to all**
- Login (success/error)
- Logout
- Register (success/error)
- (optional) Profile (showing courses taken by an individual)
- Schedule calendar page (weekly view, ability to export to Google Calendar)
- Report problems to system manager

**For instructors**
- Soft constraints form page

**For course coordinators** 
- Admin backend -- able to change user roles 
- See inputs into scheduler (table format -- two tables, one hard one soft)
- Filter by course/venue
- Generate schedule 
- See errors in schedule 

### How to run
1. Download the `mysite` folder
2. cd inside the folder on your cmd/terminal 
3. run `python manage.py runserver` 
4. Go to localhost:8000 on your browser and you should see the website

### How to migrate databases (for website admins)
Make sure that you are in the folder with `manage.py`
1. `python manage.py makemigrations`
2. `python manage.py migrate`

### Requirements
- Python3 `pip install python3`
- Django `pip install django` **Note**: Ensure that you download v2.1.5 and up as there has been a bug fix.
- crispy_forms `pip install django-crispy-forms`
- multiselectfield `pip install django-multiselectfield`
- django_select2 `pip install django_select2`
