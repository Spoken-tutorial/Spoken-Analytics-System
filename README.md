# Spoken-Analytics-System

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

* Switch to branch "arish"
```
git checkout arish
```

* Next, install the dependencies using pip:
```
pip install -r requirements-dev.txt 
```

* Change analytics_system/config.py-exp to analytics_system/config.py and change the configuration of database.

* Go to file in env/lib/python3.6/site-packages/djongo/models/fields.py and change the line no 91 to 
```
for field in self.model_container._meta._get_fields(reverse = False):
```
(mind the underscores)
This is to be done because there is bug in djongo (a library used in this project) in latest release.

* For testing purpose download the [database dump](https://drive.google.com/file/d/18TtQIrt_hUbsX8u21vpBYuQQsZNhL-CS/view?usp=sharing). Most of the test data is of date range 25-05-2020 to 02-06-2020.

* Restore the mongo dump
```
mongorestore --db logs --verbose \path\dump\<dumpfolder>
```

* Make migrations and migrate the database
```
python3 manage.py makemigraions
python3 manage.py migrate --database=default
```

* Finally, you’re ready to start the development server:
```
python manage.py runserver
```

Visit [Dashboard](http://127.0.0.1:8000/dashboard) in your browser to get to visualization page.




