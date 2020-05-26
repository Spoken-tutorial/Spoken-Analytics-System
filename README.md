# Spoken-Analytics-System


## Chart visualization added

## Setting up the project
* Create a virtual environment in recently created directory and activate it:
```
python3 -m venv env
source env/bin/activate ( for linux )
```

* Clone the repository and enter to the repository:
```
git clone https://github.com/Spoken-tutorial/Spoken-Analytics-System.git
cd Spoken-Analytics-System
```

* Switch to branch "arish" and go back to previous commit (3 commit ago) (some functionalities are not working in recent commits as they are in development)
```
git checkout arish
git checkout 65816a7c
```


* Next, install the dependencies using pip:
```
pip install -r requirements-dev.txt 
```

* Change analytics_system/config.py-exp to analytics_system/config.py and put the configuration of databases

* Restore the mongo dump
```
mongorestore --db logs --verbose \path\dump\<dumpfolder>
```

* Make migrations and migrate the database
```
python3 manage.py makemigraions
python3 manage.py migrate --database=default
```

* Go to file in env/lib/python3.6/site-packages/djongo/models/fields.py and change the line no 91 to
```
for field in self.model_container._meta._get_fields(reverse = False):
```
(mind the underscores)
This is to be done because there is bug in djongo in latest release.

* After that you have to run temp_daily, temp_weekly, temp_monthly, temp_yearly file in the shell so that stats can be calculated.

These files contain the same code as in logsUtil_* files but logsUtil_* files run from celery at regular intervals.

* You can only see the visualization of dashboard page till now, because date for other pages is not being calculated yet.

* To be able to see all pages you have to restore data from my database.

* Finally, you’re ready to start the development server:
```
python manage.py runserver
```

Visit http://127.0.0.1:8000/dashboard in your browser to get to visualization page.



