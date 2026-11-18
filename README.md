 #########################################
#      Livestream Scheduler V1.5        #
#########################################

This project now comes in a Docker container. To run it use the following:
PLEASE NOTE: there are some required environment variables that need to be set. Please read more about these below

```shell
docker build -t livestream-scheduler:1.5 -f Dockerfile
docker run -d livestreamscheduler:1.5
```

## Planning Center
Planning Center creds can be generated using the Planning Center Developer Console:
https://api.planningcenteronline.com/oauth/applications
Note that the account used to generate these tokens will determine the access and permissions that the scheduler will have access too

Please enter the Service Type for the services you wish to schedule against 'PlanningCenterServiceTypeName'

The required environment variables are as below:
```shell
export PlanningCenterAppID='your-planning-center-app-id'
export PlanningCenterAppSecret='your-planning-center-app-secret'
export PlanningCenterServiceTypeName='your-service-type-name' #e.g. Sabbath Services
```

## Unsplash
Register with Unsplash as a developer using the following link: https://unsplash.com/developers
Enter the generated App Id against UnsplashAppID
```shell
export UnsplashAppID='your-unsplash-app-id'
```

## Google
To obtain the Google Cloud credentials:
On the Google API Console:
1. Create or select a project.
2. Enable the YouTube Data API v3 from the API Library.
3. On the Credentials panel, create an “OAuth client ID”. It may ask you to “Configure Consent Screen” first – continue with that if asked: The “User Type” can be External.
4. The next page will ask what you want the consent screen to look like – just fill out the essentials as this will only be seen by you to generate the initial token.
5.On the Scopes page, add the following scopes:
https://www.googleapis.com/auth/youtube
https://www.googleapis.com/auth/youtube.force-ssl
https://www.googleapis.com/auth/youtube.upload
6.On the test user page, you’ll want to add your own account, or the account that you want to create the YouTube videos in. This is important so that the OAuth login will work without being approved by Google.
7.Continuing with the Credential creation, for the Application Type, select “Desktop app”. The client ID and client secret will now be displayed. Download the JSON version]which will include the two required secrets.

The above steps were based on the guide here: https://dennistt.net/2022/01/24/youtube-live-stream-scheduler-part-2/ 

## Examples
![thumb](https://github.com/user-attachments/assets/a7d3d525-052f-44a2-83f8-939ca4422474)

This will generate a Livestream scheduled for 10:45 am 🕥 the next Saturday morning using the information provided in the user's Planning Center account.

![logo-full-color](https://github.com/user-attachments/assets/7ded16b1-4639-408c-860d-e5b8ab4e78bc)
You can schedule this python script to run once a week using Cron on Linux / MacOS and Task Scheduler on Windows machines see https://crontab.guru for help generating the cron string. You will need to curl the generate stream endpoint, which will look something like:
```shell
curl 'https://your-server-ip/createstream'
```

## To Do:
[ ] - Allow configuration of stream start time via the enviornment variables
[ ] - Support for uploading a custom thumbnail image to override the generated one
[ ] - Updating an already scheduled stream before the stream starts

## Completed:
[x] - Package app as a Docker / Podman container
[x] - Show error messages on admin page
[x] - Preview of the stream ad thumbnail added to the admin dashboard
[x] - Allow for title and preacher to be updated before scheduling the stream
[x] - Allow users to pass in authentication secrets via environment variables
[x] - Add button to re-authenticate bot with Google if it gets deauthenticatd