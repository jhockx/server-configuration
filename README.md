# Purpose
This project is made to provide some reference code to quickly deploy a new server which hosts multiple websites, runs scripts, host REST API's etc. It is assumed you have a Linux server, your repo is on GitLab and you want to use the CI/CD abilities of GitLab. Each website/script/API gets its own Docker container on the server. Furthermore, there is a nginx-proxy server (in its own Docker container) which routes domain names to the correct Docker container. You can find the GitHub project of this nginx-proxy server [here](https://github.com/jwilder/nginx-proxy).

# Required software
### Docker installation
*The [Getting started with Docker on your VPS](https://blog.ssdnodes.com/blog/getting-started-docker-vps/) tutorial was followed for this part.  
Also see the [Docker documentation](https://docs.docker.com/engine/install/debian/).*

First, Docker and Docker-compose need to be installed on the server:
```
curl -fsSL https://get.docker.com -o get-docker.sh
```

Test the installation:
```
sudo docker run hello-world
```

Automatically start Docker on boot:
```
sudo systemctl enable docker
```

To not write `sudo` in front of each Docker command all the time, we can add the Docker group to the current user:
```
sudo groupadd docker
sudo usermod -aG docker $USER
```

Now logout and log back in. You should now be able to run Docker without `sudo`:
```
docker run hello-world
```

### Docker compose installation
Follow the steps in in the [Docker documentation](https://docs.docker.com/compose/install/). However, this didn't work for the Raspberry Pi specifically, the command couldn't be found. So I tried the following as an alternative, which did work (after installing python3 and pip3):
```
sudo pip3 install docker-compose
```

### Nginx reverse proxy
See the README in the `nginx_proxy` folder.

# Add websites, run scripts, host REST API's
To add websites, follow the instructions in the `README.md` in the folder of the specific architecture you want to use for your website. For instance, if you want to host a Wordpress website, look in the `Wordpress` folder or if you want to run a scheduled Python script look in the python_script folder.

# Add CI/CD by configuring a GitLab Runner
[Install the GitLab Runner](https://docs.gitlab.com/runner/install/linux-repository.html). After installation, go to `Settings > CI/CD > Runners (Expand)` in your project/subgroup/group in GitLab and follow the instructions to setup your GitLab Runner. One of the things you need to answer is which executor you want to use. Pick `Docker` and as image use `alpine:latest`. Just to make sure, restart you GitLab Runner by running `gitlab-runner restart` on your server. Run `gitlab-runner verify` to instantly let the Runner connect to your repo. If you want this runner to be available for multiple projects, go to the Runner on GitLab and un-check "Lock to current projects".  

We want each job of the GitLab Runner to run in a Docker container. For this, do the following:
- Add the gitlab-runner to the docker group: `sudo usermod -aG docker gitlab-runner`.
- In the configuration of the Runner (`/etc/gitlab-runner/config.toml`), you need to add `"/var/run/docker.sock:/var/run/docker.sock"` to the volumes. This lets the runner create new Docker containers through the Unix socket that the Docker daemon listens to. HTTP requests are send to this socket to create new containers.
- Optionally, you can set `disable_cache` to `true`. This will remove all disabled containers, which can be nice if you do not have a lot of space on the host or if you want less cluttering in Portainer. It can slow down jobs of course.
- Restart the runner: `gitlab-runner restart`.

Now your `config.toml` file should look something like this:
```
[[runners]]
  name = "RUNNER_NAME"
  url = "https://gitlab.com/"
  token = "SOME_GENERATED_TOKEN_DURING_REGISTRATION_OF_THE_RUNNER_(THIS_IS_NOT_THE_REGISTRATION_TOKEN!)"
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
    shm_size = 0
```

To use CI/CD, you need a `gitlab-ci.yml` file in the root of your project. This file can be found in some of the folders and used to auto deploy on the host. If you want to use Docker-in-Docker (dind), you can add the following right after the image definition:
```
services:
  - name: docker:dind
```

If that doesn't work, try the following:
```
services:
  - name: docker:19.03.0-dind
    entrypoint: ["env", "-u", "DOCKER_HOST"]
    command: ["dockerd-entrypoint.sh"]
variables:
  DOCKER_HOST: tcp://docker:2375/
  DOCKER_DRIVER: overlay2
  # See https://github.com/docker-library/docker/pull/166
  DOCKER_TLS_CERTDIR: ""
```
