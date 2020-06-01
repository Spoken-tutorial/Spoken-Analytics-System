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
from dashboard.models import Log, CameFromActivity, ExitLinkActivity, VisitorSpot
from dashboard.models import PageViewActivity, VisitorActivity, VisitorPath, VisitorInfo
from dashboard.models import BrowserStats, PlatformStats, OSStats, SourcesStats, CameFromStats, ExitLinkStats

num_rows = 10000 # number of rows to insert

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

page_titles = ["Watch Tutorial | spoken-tutorial.org", 
"CD Content Creation | spoken-tutorial.org", 
"Search Tutorials | spoken-tutorial.org", 
"Events & Happenings  | spoken-tutorial.org", 
"Login | spoken-tutorial.org", 
"Logout | spoken-tutorial.org", 
"Register | spoken-tutorial.org", 
"Software Training Dashboard | spoken-tutorial.org", 
"Software Training Planner | spoken-tutorial.org", 
"Software Training Student Batch | spoken-tutorial.org", 
"Software Training Select Participants | spoken-tutorial.org", 
"Software Training Resource Center | spoken-tutorial.org", 
"Participant/Student Login | spoken-tutorial.org", 
"India Map | spoken-tutorial.org",
"Workshop/Training Statistics  | spoken-tutorial.org", 
"PMMMNMTT Statistics  | spoken-tutorial.org",
"Tutorial Statistics  | spoken-tutorial.org",
"Online-Test Statistics  | spoken-tutorial.org", 
"Academic Centers  | spoken-tutorial.org", 
"Home | spoken-tutorial.org", 
"CD Image Download | spoken-tutorial.org",
"",
]

foss = ['Aakash+Business+Tool', 'Advance+C', 'Advanced+Cpp', 'Applications+of+GeoGebra', 
'Arduino', 'ASCEND', 'Avogadro', 'BASH', 'Biogas+Plant', 'Biopython', 'Blender', 'BOSS+Linux', 
'C', 'C+and+Cpp', 'CellDesigner', 'ChemCollective+Virtual+Labs', 'Cpp', 'Digital+Divide', 
'Digital+India', 'Drupal', 'DWSIM', 'eSim', 'ExpEYES', 'Filezilla', 'Firefox', 'FrontAccounting', 
'GChemPaint', 'gedit+Text+Editor', 'Geogebra', 'GeoGebra+for+Engineering+drawing', 'GIMP', 'Git', 
'GNS3', 'GNUKhata', 'GSchem', 'Inkscape', 'Introduction+to+Computers', 'Java', 
'Java+Business+Application', 'JChemPaint', 'Jmol+Application', 'Joomla', 'K3b', 'KiCad', 
'Koha+Library+Management+System', 'KTouch', 'KTurtle', 'LaTeX', 'LaTeX+Old+Version', 
'LibreOffice+Calc+on+BOSS+Linux', 'LibreOffice+Impress+on+BOSS+Linux', 'LibreOffice+Installation', 
'LibreOffice+Suite+Base', 'LibreOffice+Suite+Calc', 'LibreOffice+Suite+Draw', 'LibreOffice+Suite+Impress', 
'LibreOffice+Suite+Math', 'LibreOffice+Suite+Writer', 'LibreOffice+Writer+on+BOSS+Linux', 'Linux', 
'Moodle+Learning+Management+System', 'Netbeans', 'Ngspice', 'OpenFOAM', 'OpenModelica', 'OR+Tools', 
'Orca', 'Oscad', 'PERL', 'PhET', 'PHP+and+MySQL', 'Python', 'Python+3.4.3', 'Python+for+Biologists', 
'Python+Old+Version', 'QCad', 'R', 'RDBMS+PostgreSQL', 'Ruby', 'Scilab', 'Selenium', 'Showcase+Tutorials', 
'Single+Board+Heater+System', 'Skill+Development-+Fitter', 'Skill+Development-+InStore+Promoter', 
'Spoken+Tutorial+Technology', 'Step', 'Synfig', 'test', 'TEST+FOSS', 'Thunderbird', 
'Translation+and+Dubbing', 'Tux+Typing', 'UCSF+Chimera', 'Website+Information', 'What+is+Spoken+Tutorial', 'Xfig']

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
, "https://classroom.google.com/u/0/c/MTI1NTA0MDMzNzk3"
, "(No referring link)"]

download_links = ["https://spoken-tutorial.org/media/videos/85/Arduino-Brochure-English.pdf", 
"https://spoken-tutorial.org/media/videos/85/Arduino-Brochure-English.pdf",
"https://spoken-tutorial.org/media/videos/14/1373/resources/Numbering-Equations-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/14/1373/resources/Numbering-Equations-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/50/1254/resources/Lists-and-its-Operations-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/50/1254/resources/Lists-and-its-Operations-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/97/965/resources/Admin-dashboard-Slides.zip",
"https://spoken-tutorial.org/media/videos/97/965/resources/Admin-dashboard-Slides.zip",
"https://process.spoken-tutorial.org/images/9/95/Test_Instruction_for_Participants.pdf",
"https://process.spoken-tutorial.org/images/9/95/Test_Instruction_for_Participants.pdf",
"https://spoken-tutorial.org/media/videos/29/24/resources/Conditional-Branching-Slides.zip",
"https://spoken-tutorial.org/media/videos/29/24/resources/Conditional-Branching-Slides.zip",
"https://spoken-tutorial.org/media/videos/14/11/resources/Equations-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/14/11/resources/Equations-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/50/1253/resources/Data-types-and-Factors-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/50/1253/resources/Data-types-and-Factors-Assignment.pdf",
"https://process.spoken-tutorial.org/images/9/95/Test_Instruction_for_Participants.pdf",
"https://process.spoken-tutorial.org/images/9/95/Test_Instruction_for_Participants.pdf",
"https://spoken-tutorial.org/media/videos/97/983/resources/Categories-in-Moodle-Assignment.txt",
"https://spoken-tutorial.org/media/videos/50/1252/resources/Merging-and-Importing-Data-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/50/1252/resources/Merging-and-Importing-Data-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/97/983/resources/Categories-in-Moodle-Assignment.txt",
"https://spoken-tutorial.org/media/videos/25/64/resources/If-Statement-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/25/64/resources/If-Statement-Codefiles.zip",
"https://process.spoken-tutorial.org/images/9/95/Test_Instruction_for_Participants.pdf",
"https://process.spoken-tutorial.org/images/9/95/Test_Instruction_for_Participants.pdf",
"https://spoken-tutorial.org/media/videos/14/1410/resources/Writing-Style-Files-in-LaTeX-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/14/1410/resources/Writing-Style-Files-in-LaTeX-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/14/11/resources/Equations-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/14/11/resources/Equations-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/50/1251/resources/Operations-on-Matrices-and-Data-Frames-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/50/1251/resources/Operations-on-Matrices-and-Data-Frames-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/21/19/resources/File-System-Slides.zip",
"https://spoken-tutorial.org/media/videos/21/19/resources/File-System-Slides.zip",
"https://spoken-tutorial.org/media/videos/89/Python-3.4.3-Instruction-Sheet-English.pdf",
"https://spoken-tutorial.org/media/videos/89/Python-3.4.3-Instruction-Sheet-English.pdf",
"https://spoken-tutorial.org/media/videos/50/1250/resources/Creating-Matrices-using-Data-Frames-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/50/1250/resources/Creating-Matrices-using-Data-Frames-Assignment.pdf",
"https://spoken-tutorial.org/media/videos/29/15/resources/Matrix-Operations-Slides.zip",
"https://spoken-tutorial.org/media/videos/29/15/resources/Matrix-Operations-Slides.zip",
"https://spoken-tutorial.org/media/videos/14/1411/resources/Indic-Language-Typesetting-in-LaTeX-Codefiles.zip",
"https://spoken-tutorial.org/media/videos/14/1411/resources/Indic-Language-Typesetting-in-LaTeX-Codefiles.zip"]

clicked_from = ["https://spoken-tutorial.org/tutorial-search/?search_foss=Arduino&search_language=English", 
"https://spoken-tutorial.org/tutorial-search/?search_foss=Arduino&search_language=English", 
"https://spoken-tutorial.org/watch/LaTeX/Numbering Equations/English/", 
"https://spoken-tutorial.org/watch/LaTeX/Numbering Equations/English/", 
"https://spoken-tutorial.org/watch/R/Lists and its Operations/English/", 
"https://spoken-tutorial.org/watch/R/Lists and its Operations/English/", 
"https://spoken-tutorial.org/watch/Moodle Learning Management System/Admin dashboard/English/", 
"https://spoken-tutorial.org/watch/Moodle Learning Management System/Admin dashboard/English/", 
"https://spoken-tutorial.org/testimonials/media/", 
"https://spoken-tutorial.org/testimonials/media/", 
"https://spoken-tutorial.org/watch/Scilab/Conditional Branching/English/", 
"https://spoken-tutorial.org/watch/Scilab/Conditional Branching/English/", 
"https://spoken-tutorial.org/watch/LaTeX/Equations/English/", 
"https://spoken-tutorial.org/watch/LaTeX/Equations/English/", 
"https://spoken-tutorial.org/watch/R/Data types and Factors/English/", 
"https://spoken-tutorial.org/watch/R/Data types and Factors/English/", 
"https://spoken-tutorial.org/participant/index/?category=2", 
"https://spoken-tutorial.org/participant/index/?category=2", 
"https://spoken-tutorial.org/watch/Moodle Learning Management System/Categories in Moodle/English/", 
"https://spoken-tutorial.org/watch/R/Merging and Importing Data/English/", 
"https://spoken-tutorial.org/watch/R/Merging and Importing Data/English/", 
"https://spoken-tutorial.org/watch/Moodle Learning Management System/Categories in Moodle/English/"
]

exit_links = ["https://statcounter.com/p5528933/?guest=1", 
"https://googleresearch.blogspot.in/2015/03/announcing-google-mooc-focused-research.html", 
"https://googleresearch.blogspot.in/2015/03/announcing-google-mooc-focused-research.html", 
"https://www.youtube.com/user/SpokenTutorialIITB/", 
"https://www.youtube.com/user/SpokenTutorialIITB/", 
"mailto:contact@spoken-tutorial.org", 
"mailto:contact@spoken-tutorial.org", 
"https://fossee.in/fellowship/2020", 
"https://fossee.in/fellowship/2020", 
"https://fossee.in/fellowship/2020", 
"https://fossee.in/fellowship/2020", 
"http://application.reimagine-education.com/the-winners-individual/2015/132/2193b0ae3841f24da1464d4b6b70ee0f/Indian Institute of Technology Bombay", 
"http://application.reimagine-education.com/the-winners-individual/2015/132/2193b0ae3841f24da1464d4b6b70ee0f/Indian Institute of Technology Bombay", 
"https://statcounter.com/p5528933/?guest=1", 
"https://python.fossee.in/", 
"https://python.fossee.in/", 
"https://creativecommons.org/licenses/by-sa/4.0/", 
"https://googleresearch.blogspot.in/2015/03/announcing-google-mooc-focused-research.html"]

pages = ["https://spoken-tutorial.org/cdcontent/", 
"https://spoken-tutorial.org/", 
"https://spoken-tutorial.org/software-training/test/verify-test-certificate/", 
"https://spoken-tutorial.org/stfellowship2020/", 
"https://spoken-tutorial.org/keyword-search/", 
"https://spoken-tutorial.org/cdcontent/", 
"https://spoken-tutorial.org/participant/index/?category=2"]

browsers = ["Firefox", "Chrome for Android", "Chrome", "Samsung Internet", "Opera"]

browser_versions = ["76.0", "83.0", "81.0", "11.2", "68.0"]

os = ["Linux", "Android", "Windows", "Mac"]

os_versions = ["7", "8", "8.1"]

# For Logs Model
def randomData():
    data = {
        'path_info': lambda x: "/watch/" + random.choice(foss) + "/" + random.choice(tutorials) + "/" + random.choice(languages) if random.choice(paths) == "/watch/" else random.choice(paths),
        'event_name': lambda x: random.choice(event_names),
        'page_title': lambda x: random.choice(page_titles),
        'visited_by': lambda x: populator.generator.user_name() if random.randint(0, 1) == 1 else "anonymous",
        'ip_address':  lambda x: "230.124.0." + str(random.randint(0, 255)),
        'datetime': lambda x: populator.generator.date_time_between(start_date='-10d', end_date='+2d', tzinfo=india_tz),
        'referrer': lambda x: random.choice(referrer),
        'browser_family': lambda x: random.choice(browsers),
        'browser_version': lambda x: random.choice(browser_versions),
        'os_family': lambda x: random.choice(os),
        'os_version': lambda x: random.choice(os_versions),
        'device_family': lambda x: random.choice(["Lenovo K8 Note", "Realme XT", "Realme X2", "Samasung M31S", "Samsung M40"]),
        'device_type': lambda x: random.choice(["Mobile", "PC"]),
        'latitude': lambda x: populator.generator.local_latlng(country_code='IN', coords_only=True)[0],
        'longitude': lambda x: populator.generator.local_latlng(country_code='IN', coords_only=True)[1],
        'city': lambda x: random.choice(cities),
        'region': lambda x: random.choice(states_uts),
        'country': 'India',
    }
    return data

# For CameFromActivity Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+6d', tzinfo=india_tz),
#         'referrer': lambda x: random.choice(referrer),
#         'entry_page': lambda x: random.choice(paths)
#     }
#     return data

# For DownloadActivity Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'download_link': lambda x: random.choice(download_links),
#         'clicked_from': lambda x: random.choice(clicked_from)
#     }
#     return data

# For ExitLinkActivity Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'exit_link_clicked': lambda x: random.choice(exit_links),
#         'exit_link_page': lambda x: random.choice(pages)
#     }
#     return data

# For VisitorSpot Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'ip_address': lambda x: "230.124." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)),
#         'geom': lambda x: {'type': 'Point','coordinates': [float(i) for i in populator.generator.local_latlng(country_code='IN', coords_only=True)][::-1] }
#     }
#     return data

# For PageViewActivity Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'browser': lambda x: random.choice(browsers),
#         'os': lambda x: random.choice(os),
#         'screen_res': lambda x: random.choice(resolutions),
#         'city': lambda x: random.choice(cities),
#         'region': lambda x: random.choice(states_uts),
#         'country': 'India',
#         'language': lambda x: random.choice(languages),
#         'ip_address': lambda x: "230.124." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)),
#         'isp': lambda x: random.choice(isp),
#         'page_url': lambda x: random.choice(pages),
#         'referrer': lambda x: random.choice(referrer),
#     }
#     return data

# For PageViewActivity Model
# def randomData():
#     data = {
#         'page_views': lambda x: random.randint(1, 10),
#         'total_visits':  lambda x: random.randint(1, 40),
#         'latest_page_view': lambda x: populator.generator.date_time_between(start_date='-1d', end_date='+1d', tzinfo=india_tz),
#         'city': lambda x: random.choice(cities),
#         'region': lambda x: random.choice(states_uts),
#         'country': 'India',
#         'visit_length_sec': lambda x: random.randint(1, 500),
#         'ip_address': lambda x: "230.124." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)),
#         'isp': lambda x: random.choice(isp),
#         'screen_res': lambda x: random.choice(resolutions),
#         'referrer': lambda x: random.choice(referrer),
#         'browser': lambda x: random.choice(browsers),
#         'os': lambda x: random.choice(os),
#         'entry_page': lambda x: random.choice(pages),
#         'latest_page': lambda x: random.choice(pages),
#         'visit_page': lambda x: random.choice(pages),
#     }
#     return data

# For VisitorPath Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'city': lambda x: random.choice(cities),
#         'region': lambda x: random.choice(states_uts),
#         'country': 'India',
#         'ip_address': lambda x: "230.124." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)),
#         'isp': lambda x: random.choice(isp),
#         'visit_num':  lambda x: random.randint(1, 10),
#         'screen_res': lambda x: random.choice(resolutions),
#         'browser': lambda x: random.choice(browsers),
#         'os': lambda x: random.choice(os),
#         'path': lambda x: [{'datetime': populator.generator.date_time_between(start_date='-2d', end_date='now', tzinfo=india_tz), 'referrer': random.choice(referrer), 'page_url': random.choice(pages)} for i in range(random.randint(1, 10))]
#     }
#     return data

# For KeywordActivity Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'name': lambda x: random.choice(['www.google.com', 'www.google.co.in', 'google.com']),
#         'search_query': '(Keywords Unavailable)',
#         'entry_page': lambda x: random.choice(paths)
#     }
#     return data

# For VisitorInfo Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'referrer': lambda x: random.choice(referrer),
#         'browser': lambda x: random.choice(browsers),
#         'ip_address': lambda x: "230.124." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)),
#         'os': lambda x: random.choice(os),
#         'city': lambda x: random.choice(cities),
#         'region': lambda x: random.choice(states_uts),
#         'country': 'India',
#         'screen_res': lambda x: random.choice(resolutions),
#         'returning_visits': lambda x: random.randint(1, 10),
#         'javascript': lambda x: random.randint(0, 1),
#         'visit_length_sec': lambda x: random.randint(1, 500),
#         'isp': lambda x: random.choice(isp),
#         'path': lambda x: [{'datetime': populator.generator.date_time_between(start_date='-2d', end_date='now', tzinfo=india_tz), 'referrer': random.choice(referrer), 'page_url': random.choice(pages)} for i in range(random.randint(1, 10))]
#     }
#     return data

# For ISPStats Model
# def randomData():
#     data = {
#         'isp': lambda x: random.choice(isp),
#         'path': lambda x: [{'datetime': populator.generator.date_time_between(start_date='-2d', end_date='now', tzinfo=india_tz), 'referrer': random.choice(referrer), 'page_url': random.choice(pages)} for i in range(random.randint(1, 10))]
#     }
#     return data

# For BrowserStats Model
# def randomData():
    # data = {
    #     'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
    #     'browser_type': lambda x: random.choice(['Mobile Browsers', 'Chrome', 'Firefox', 'Edge', 'Opera', 'Other']),
    #     'name': lambda x: random.choice(browsers),
    #     'page_views': lambda x: random.randint(0, 1000),
    # }
    # return data

# For PlatformStats Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'platform': lambda x: random.choice(['Desktop', 'Mobile', 'Tablet']),
#         'page_views': lambda x: random.randint(1, 1000),
#     }
#     return data

# For OSStats Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-2d', end_date='+1d', tzinfo=india_tz),
#         'os': lambda x: random.choice(['Android', 'iOS', 'Win10', 'Win7', 'Win8.1', 'OSX']),
#         'page_views': lambda x: random.randint(1, 1000),
#     }
#     return data

# For SourcesStats Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-10d', end_date='+1d', tzinfo=india_tz),
#         'referrer_page_views': lambda x: random.randint(1, 1000),
#         'search_page_views': lambda x: random.randint(1, 1000),
#         'direct_page_views': lambda x: random.randint(1, 1000),
#         'total_page_views': lambda x: random.randint(1, 3000),
#     }
#     return data

# For CameFromStats Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-10d', end_date='+1d', tzinfo=india_tz),
#         'referrer': lambda x: random.choice(referrer),
#         'page_views': lambda x: random.randint(1, 1000),
#     }
#     return data

# For ExitLinkStats Model
# def randomData():
#     data = {
#         'datetime': lambda x: populator.generator.date_time_between(start_date='-10d', end_date='+1d', tzinfo=india_tz),
#         'exit_link': lambda x: random.choice(exit_links),
#         'page_views': lambda x: random.randint(1, 1000),
#     }
#     return data

# Adding data to populator object
populator.addEntity(Log, num_rows, randomData())

# Inserting data to database
populator.execute()