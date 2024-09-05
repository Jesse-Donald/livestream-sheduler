#########################################
#      Livestream Scheduler V1.0        #
#########################################

Please replace the placeholder information found in the config.json file to set up the application.

Planning Center creds can be generated using the Planning Center Developer Console:
https://api.planningcenteronline.com/oauth/applications
Note that the account used to generate these tokens will determine the access and permissions that the scheduler will have access too

Please enter the Service Type for the services you wish to schedule against 'PlanningCenterServiceTypeName'

Register with Unsplash as a developer using the following link: https://unsplash.com/developers
Enter the generated App Id against UnsplashAppID

To obtain the Google Cloud credentials follow the guide here: https://dennistt.net/2022/01/24/youtube-live-stream-scheduler-part-2/ to obtain the credentials.json file
run the googleAuth.py file to ensure that the application has been correclty authorized and linked to your account. These are the only credentials that are not inclided in the config.json file

![thumb](https://github.com/user-attachments/assets/a7d3d525-052f-44a2-83f8-939ca4422474)

This will generate a Livestream scheduled for 10:45 am 🕥 the next Saturday morning using the information provided in the user's Planning Center account
![logo-full-color](https://github.com/user-attachments/assets/7ded16b1-4639-408c-860d-e5b8ab4e78bc)
You can schedule this python script to run once a week using Cron on Linux / MacOS and Task Scheduler on Windows machines see https://crontab.guru for help generating the cron string
