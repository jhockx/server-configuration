# Running scheduled Python scripts:
Take a look at the `Dockerfile`, when building the image, it simply copies the files and installs all the needed packages. If you want to run scripts on a Raspberry Pi (ARM architecture), take a look at the `Dockerfile-RaspberryPi`, it is specifically designed to be able to run Python and Pip on the Raspberry Pi or Home Assistant (Debian based). Remove `-RaspberryPi` from the name before using it.

The `.gitlab-ci.yml` has two stages:
- The `build` stage which has a single job to build the Docker Image. Because this can sometimes be a slow process (especially installing Pandas on the Raspberry Pi for instance), the build stage will only be executed when the Dockerfile has been changed.
- The `run` stage contains a `deploy` job which starts the container and adds a volume for logging. This volume can then be accessed on the server to read the logs. Then another job is ran to execute a Python script inside the running container (in this case it is called `some-script`). Rename this job and run your own script. Your script should write log results to the `/logs` folder, because the contents of this folder will be the artifacts for each Gitlab job. In the `.gitlab-ci.yml` this job is triggered manually, so change this where necessary. To run multiple scripts, just copy this job, change the job name and run another script.
- The `cleanup` stage stops and removes the Docker container, as it isn't needed anymore after running the script(s).

To run a scheduled job, simply add a schedule through the Gitlab website.
