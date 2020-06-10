# Website log storage API

- Run the Django server on port 8001, as specified in the repo's README ~ ```python manage.py runserver 127.0.0.1:8001```
- Ensure the Redis server is running and configured correctly. Then run monitor_queue.py ~ ```python monitor_queue.py```
- **Note:** If you need to change the IP address/port on which the server runs, you will also need to change the LOGS_API_URL value in the settings.py of spoken-website.

# Tutorial progress logs API

- The views defined in *logs_api/views.py* define the API methods for tutorial progress logs.

# Celery beats for cron jobs

Run ```celery -A analytics_system beat -l INFO```  
This will send the cron jobs defined in settings.py to Celery. So Celery has to be running to processes these tasks.

# Miscellaneous

## [Documentation Report](https://docs.google.com/document/d/1YXwQmeMuMrX0YKncGss35xBPszmqwgO2zt37Oj0-0Vk/edit)

## Presentation Video - yet to add.

## Using Logstash to sync MongoDB and Elasticsearch

- Download the driver [here](https://dbschema.com/jdbc-driver/MongoDb.html)
- Extract the zip contents
- Ensure you have Elasticsearch, MongoDB and Logstash installed, and that Elasticsearch is running.
- Download the configuration file [mongo-es-logstash.conf](../Misc/mongo-es-logstash.conf) present in this repo, and change the configurations as required (you will definitely need to change the value of jdbc_driver_library).
- Run logstash with
> sudo /path/to/logstash -f /path/to/mongo-es-logstash.conf    
  
For example,    
  
> sudo /usr/share/logstash/bin/logstash -f /home/krithik/Desktop/Git/Spoken-Analytics-System/Misc/mongo-es-logstash.conf    

## GeoIP

- Creating a cron job to update GeoLite2 database periodically - [Link](https://mauteam.org/mautic/mautic-admins/solved-maxmind-geolite2-database-not-updating/)
- Check https://dev.maxmind.com/geoip/geoip2/geolite2/ for attribution and credits details.