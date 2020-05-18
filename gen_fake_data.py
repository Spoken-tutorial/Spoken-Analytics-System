"""
This file can generate fake data for database.
change num_rows to desired number of rows to be inserted.
excute this file in python shell.
>> exec(open("gen_fake_data.py").read())
"""

import datetime
import random
import dateutil.parser

from dateutil import tz
from django_populate import Faker
from dashboard.models import Log, CameFromActivity

num_rows = 1000 # number of rows to insert

india_tz = tz.gettz('Asia/Kolkata')

# Creating populator object
populator = Faker.getPopulator()

event_names = ["event.video.watch", "event.cdcontent.download", "event.tutorial.search", "event.news", "event.login", 
"event.logout", "event.register", "event.software.training", "event.software.training.planner", 
"event.software.training.student.batch", "event.software.training.select.participants", 
"event.software.training.resource.center", "event.participant.login", "event.statistics", 
"event.statistics.training", "event.statistics.fdp.training", "event.statistics.tutorial.content", 
"event.statistics.online.test", "event.statistics.academic.center", "event.home.view"]

paths = ["/watch/", "/cdcontent/", "/tutorial-search/", "/news/", "/accounts/login/", "/accounts/logout/", 
"/accounts/register/", "/software-training/", "/software-training/training-planner/", "/software-training/student-batch/", 
"/software-training/select-participants/", "/software-training/resource-center/", "/participant/login/", "/statistics/", 
"/statistics/training/", "/statistics/pmmmnmtt/fdp/", "/statistics/tutorial-content/", "/statistics/online-test/", 
"/statistics/academic-center/", "/home/"]

foss = ["Aakash Business Tool", "Advance C", "Advanced Cpp", "Applications of GeoGebra", "Arduino", "ASCEND", 
"Avogadro", "BASH", "Biogas Plant", "Biopython", "Blender", "BOSS Linux", "C", "C and Cpp", "CellDesigner", 
"ChemCollective Virtual Labs", "Cpp", "Digital Divide", "Digital India", "Drupal", "DWSIM", "eSim", "ExpEYES", 
"Filezilla", "Firefox", "FrontAccounting", "GChemPaint", "gedit Text Editor", "Geogebra", 
"GeoGebra for Engineering drawing", "GIMP", "Git", "GNS3", "GNUKhata", "GSchem", "Inkscape", 
"Introduction to Computers", "Java", "Java Business Application", "JChemPaint", "Jmol Application", "Joomla", 
"K3b", "KiCad", "Koha Library Management System", "KTouch", "KTurtle", "LaTeX", "LaTeX Old Version", 
"LibreOffice Calc on BOSS Linux", "LibreOffice Impress on BOSS Linux", "LibreOffice Installation", 
"LibreOffice Suite Base", "LibreOffice Suite Calc", "LibreOffice Suite Draw", "LibreOffice Suite Impress", 
"LibreOffice Suite Math", "LibreOffice Suite Writer", "LibreOffice Writer on BOSS Linux", "Linux", 
"Moodle Learning Management System", "Netbeans", "Ngspice", "OpenFOAM", "OpenModelica", "OR Tools", "Orca", "Oscad", 
"PERL", "PhET", "PHP and MySQL", "Python", "Python 3.4.3", "Python for Biologists", "Python Old Version", "QCad", 
"R", "RDBMS PostgreSQL", "Ruby", "Scilab", "Selenium", "Showcase Tutorials", "Single Board Heater System", 
"Skill Development- Fitter", "Skill Development- InStore Promoter", "Spoken Tutorial Technology", "Step", 
"Synfig", "test", "TEST FOSS", "Thunderbird", "Translation and Dubbing", "Tux Typing", "UCSF Chimera", 
"Website Information", "What is Spoken Tutorial", "Xfig"]

tutorials = ["Tutorial 1", "Tutorial 2", "Tutorial 3", "Tutorial 4", "Tutorial 5", "Tutorial 6", "Tutorial 7", "Tutorial 8"]

languages = ["Arabic", "Assamese""Bengali", "Bhojpuri", "Bodo", "Dogri", "English", "English-USA", "Gujarati", 
"Hindi", "Kannada", "Kashmiri", "Khasi", "Khmer", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", 
"Nepali", "Oriya", "Persian", "Punjabi", "Rajasthani", "Sanskrit", "Santhali", "Sindhi", "Spanish", "Tamil", 
"Telugu", "Thai", "Urdu",]

states_uts = [ "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
 "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
 "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttarakhand", "Uttar Pradesh", "West Bengal", 
 "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman & Diu", "The Government of NCT of Delhi",
 "Jammu & Kashmir", "Ladakh", "Lakshadweep", "Puducherry"]

cities = ["Mumbai", "Delhi", "Bengaluru", "Ahmedabad", "Hyderabad", "Chennai", "Kolkata", "Pune", "Jaipur", "Surat", "Lucknow", 
"Kanpur", "Nagpur", "Patna", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Vadodara", "Firozabad", "Ludhiana", "Rajkot", "Agra", 
"Siliguri", "Nashik", "Faridabad", "Patiala", "Meerut", "Kalyan-Dombivali", "Vasai-Virar", "Varanasi", "Srinagar", "Dhanbad", 
"Jodhpur", "Amritsar", "Raipur", "Allahabad", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Madurai", "Guwahati", 
"Chandigarh", "Hubli-Dharwad", "Amroha", "Moradabad", "Gurgaon", "Aligarh", "Solapur"]

referrer = ["android-app://com.google.android.gm"
, "https://classroom.google.com/c/MTI0OTg2NTkwOTA0/p/MTAzMzY0NDEyNjkw/details"
, "https://www.rediffmail.com/cgi-bin/red.cgi?red=https://spoken-tutorial.org/accounts/confirm/KfEBaC9oE8pPAprokOTcmPasTpSR2fnnr/kp.poongodi&isImage=0&BlockImage=0&rediffng=0&rdf=UXQFaAJqXzRTaVJpCzwKNwcLA28KMFgtU3sAZA==&rogue=557fc65d8f3a43d67cd809d8f7d8b60d4b446fc5"
, "https://classroom.google.com/u/1/c/MTAyNzM2MzQ2NjY0"
, "https://storage.googleapis.com/uniquecourses/online.html"
, "android-app://com.google.android.googlequicksearchbox/"
, "http://etcm.ticollege.org/cms1/course/view.php?id=9"
, "https://classroom.google.com/c/MTI0OTg2NTkwOTA0/p/MTAzMzY0NDEyNjk2/details"
, "android-app://com.google.android.gm/"
, "https://mail.google.com/mail/u/0/"
, "https://classroom.google.com/u/0/c/MTI1NTA0MDMzNzk3"]

# def randomData():
#     visited_by = lambda x: populator.generator.user_name() if random.randint(0, 1) == 1 else ""
#     method = lambda x: random.choice(["GET", "POST"])
#     city = lambda x: random.choice(cities)
#     region = lambda x: random.choice(states_uts)
#     country = lambda x: populator.generator.country()
#     ip_address = lambda x: "230.124." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255))
#     event_name = lambda x: random.choice(event_names)
#     path_info = lambda x: "/watch/" + random.choice(foss) + "/" + random.choice(tutorials) + "/" + random.choice(languages) if random.choice(paths) == "/watch/" else random.choice(paths)
#     data = {
#         'path_info': path_info,
#         'visited_by': visited_by,
#         'browser_info' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
#         'request_data' : '{data: request_data}',
#         'method': method,
#         'event_name': event_name,
#         'city': city,
#         'region': region,
#         'country': country,
#         'ip_address':  ip_address,
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2y', end_date='+16d', tzinfo=india_tz),
#     }
#     return data

def randomData():
    data = {
        'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+6d', tzinfo=india_tz),
        'referrer': lambda x: random.choice(referrer),
        'entry_page': lambda x: random.choice(paths)
    }
    return data

# Adding data to populator object
populator.addEntity(CameFromActivity, num_rows, randomData())

# Inserting data to database
populator.execute()