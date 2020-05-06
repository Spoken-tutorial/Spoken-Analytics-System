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

* Switch to branch "arish"
```
git checkout arish
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

* Genereate fake data
excute gen_fake_data.py file in python shell.
```
>> exec(open("gen_fake_data.py").read())
```

* Finally, you’re ready to start the development server:
```
python manage.py runserver
```

Visit http://127.0.0.1:8000/dashboard in your browser to get to visualization page.


