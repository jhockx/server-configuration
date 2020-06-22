# Purpose
This project is made to quickly deploy a new server which hosts multiple websites. It is assumed you have a Linux server, your repo is on GitLab and you want to use the CI/CD abilities of GitLab for the hosting of (some of) the websites. Each website gets its own Docker container on the server. Furthermore, there is a nginx-proxy server (in its own Docker container) which routes you to the correct Docker container, based on the accessed domain name. You can find the GitHub project of this nginx-proxy server [here](https://github.com/jwilder/nginx-proxy).

# Required software
### Docker installation
*The [Getting started with Docker on your VPS](https://blog.ssdnodes.com/blog/getting-started-docker-vps/) tutorial was followed for this part*

First, Docker and Docker-compose need to be installed on the server:
```
sudo curl -sS https://get.docker.com/ | sh
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
First replace the version number with the current version in the script below, check the [release page](https://github.com/docker/compose/releases). Then run.
```
sudo -i
# curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
# chmod +x /usr/local/bin/docker-compose
```

### Nginx reverse proxy
See the README in the `nginx_proxy` folder.

# Add websites
To add websites, follow the instructions in the `README.md` in the folder of the specific architecture you want to use for your website. For instance, if you want to host a Wordpress website, look in the `Wordpress` folder.

# Add CI/CD by configuring a GitLab Runner
[Install the GitLab Runner](https://docs.gitlab.com/runner/install/linux-repository.html). After installation, go to `Settings > Ci/CD > Runners (Expand)` in your project/subgroup/group in GitLab and follow the instructions to setup your GitLab Runner. Just to make sure, restart you GitLab Runner by running `gitlab-runner restart` on your server. Run `gitlab-runner verify` to instantly let the Runner connect to your repo. If you want this runner to be available for multiple projects, go to the Runner on GitLab and un-check "Lock to current projects".  

We want each job of the GitLab Runner to run in a Docker container. For this, do the following:
- Add the gitlab-runner to the docker group: `sudo usermod -aG docker gitlab-runner`.
- In the configuration of the Runner (`/etc/gitlab-runner/config.toml`), you need to add `"/var/run/docker.sock:/var/run/docker.sock"` to the volumes. This lets the runner create new Docker containers through the Unix socket that the Docker daemon listens to. HTTP requests are send to this socket to create new containers.
- Optionally, you can set `disable_cache` to `true`. This will remove all disabled containers, which can be nice if you do not have a lot of space on the host or if you want less cluttering in Portainer. It can slow down jobs of course.
- Restart the runner: `gitlab-runner restart`.
