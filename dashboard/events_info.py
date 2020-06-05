"""
This file contains name of events of which logs are being logged.

Currently this file is being used only to find the titles of page using event name.
The logs stored using middleware do not contain title of page.
So the function get_title_of_event() is used to get the page title.
This file is only used in the calculation of event stats.
"""

# List of tuples containing event names and page titles
events_titles = [
    ("event.video.watch", "Watch Tutorial | spoken-tutorial.org"), 
    ("event.cdcontent.download", "CD Content Creation | spoken-tutorial.org"), 
    ("event.tutorial.search", "Search Tutorials | spoken-tutorial.org"), 
    ("event.news", "Events & Happenings  | spoken-tutorial.org"), 
    ("event.login", "Login | spoken-tutorial.org"), 
    ("event.logout", "Logout | spoken-tutorial.org"), 
    ("event.register", "Register | spoken-tutorial.org"), 
    ("event.software.training", "Software Training Dashboard | spoken-tutorial.org"), 
    ("event.software.training.planner", "Software Training Planner | spoken-tutorial.org"), 
    ("event.software.training.student.batch", "Software Training Student Batch | spoken-tutorial.org"), 
    ("event.software.training.select.participants", "Software Training Select Participants | spoken-tutorial.org"), 
    ("event.software.training.resource.center", "Software Training Resource Center | spoken-tutorial.org"), 
    ("event.participant.login", "Participant/Student Login | spoken-tutorial.org"), 
    ("event.statistics", "India Map | spoken-tutorial.org"), 
    ("event.statistics.training", "Workshop/Training Statistics  | spoken-tutorial.org"), 
    ("event.statistics.fdp.training", "PMMMNMTT Statistics  | spoken-tutorial.org"), 
    ("event.statistics.tutorial.content", "Tutorial Statistics  | spoken-tutorial.org"), 
    ("event.statistics.online.test", "Online-Test Statistics  | spoken-tutorial.org"), 
    ("event.statistics.academic.center", "Academic Centers  | spoken-tutorial.org"), 
    ("event.home.view" , "Home | spoken-tutorial.org"), 
    ("event.media.cdimage", "CD Image Download | spoken-tutorial.org")
]

# Function to get page title of particular event
def get_title_of_event(event_name):
    for i in range(len(events_titles)):
        if events_titles[i][0] == event_name:
            return events_titles[i][1]
    return ""