# Installation
1. To run the application you're gonna need docker (CE version will be enough), 
you can download it here:
https://docs.docker.com/engine/installation/#supported-platforms

2. Start docker 

3. Once that's done run from the application's root directory this command: 
        ```
        docker build -f Dockerfile-web .
        ```

# Usage
## Config file setup
        File 'site_up_checker/validation_config.py' contains information about 
        which websites are going to be checked, what string do they need to contain,
        and what's should be the sampling period.
        The current file contains some dummy-checks (which you can obviously remove) 
        and you just need to follow this pattern to add your websites:
        ```
                REQUIREMENTS = {
                        "url1": list of required strings,
                        "url2": list of required strings,
                        ...
                }
        ```
        Set the sample period to any value in seconds.
## Starting the application
If the build step has finished successfully run this command to start the 
application:
        ```
        docker-compose up
        ```
Now you can access it in you web browser at '127.0.0.1:8070'

## Additional info
1. If you ran your application with the command above everytime you change the 
   config file you will need to rebuild the docker image and restart the app:
           ```
           docker-compose build --force-rm
           ```
   That's how it works in the production mode.
   However, you can also use the app in the development mode, then the app tracks 
   your changes and reloads everytime you change something - so you wouldn't need to 
   do anything after changing the config file, app would take care of everything 
   by itself.
   To run the app in development mode run:
           ```
           docker-compose -f docker-compose-dev.yml
           ```
2. Log file - you can access the log file by downloading it with the
   'Download log file'
