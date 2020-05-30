# for load testing with LocustIO

from locust import HttpLocust, TaskSet, between

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/watch/BASH/Introduction+to+BASH+Shell+Scripting/English/")

class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 5}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = 0