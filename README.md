# Purpose
This project is made to provide some reference code to quickly deploy a new server which hosts multiple websites, runs scripts, host REST API's etc. It is assumed you have a Linux server, your repo is on GitLab and you want to use the CI/CD abilities of GitLab. Each website/script/API gets its own Docker container on the server. Furthermore, there is a nginx-proxy server (in its own Docker container) which routes domain names to the correct Docker container. You can find the GitHub project of this nginx-proxy server [here](https://github.com/jwilder/nginx-proxy).

# Required software
### Docker installation
_Follow the [Docker documentation](https://docs.docker.com/engine/install/debian/)._  
Please be aware you need to select the correct distro.

_Then follow parts of the [post-installation steps](https://docs.docker.com/compose/install/):_  
Automatically start Docker on boot:
```
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
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
_Follow the steps in in the [Docker documentation](https://docs.docker.com/compose/install/)._  

However, this didn't work for the Raspberry Pi specifically, the command couldn't be found. So I tried the following as an alternative, which did work (after installing python3 and pip3):
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

# Other server settings
## Connect to server with SSH keys
From your local pc, from a Linux terminal or WSL on Windows, run the following (your private key should be in the `.ssh` folder locally):
```
ssh-copy-id user@ip_address
```

If that doesn't work, try to follow [a few of these steps](https://superuser.com/questions/215504/permissions-on-private-key-in-ssh-folder):
- Home directory on the server should not be writable by others: `chmod go-w /home/$USER`
- SSH folder on the server needs 700 permissions: `chmod 700 /home/$USER/.ssh`
- Authorized_keys file needs 644 permissions: `chmod 644 /home/$USER/.ssh/authorized_keys`
- Make sure that user owns the files/folders and not root: `chown $USER:$USER authorized_keys` (or without the `$USER` after the colon) and `chown $USER:$USER /home/$USER/.ssh` (or without the `$USER` after the colon)
- Put the generated public key (from ssh-keygen) in the user's authorized_keys file on the server by running `ssh-copy-id user@ip_address` again locally

## Disable password authentication over SSH
Edit SSH config:
```
sudo nano /etc/ssh/sshd_config
```
And set the following:
```
PasswordAuthentication no
PubkeyAuthentication yes
PasswordAuthentication no
X11Forwarding no
```
Then restart the service:
```
service ssh restart
```

## Firewall
#### Allow IPv6
```
sudo nano /etc/default/ufw
```
And set the following:
```
IPV6=yes
```

#### Set policies
```
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

#### Allowing connections
Set the following:
```
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
```
Or the equivalent:
```
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
```
Set specific port ranges (setting tcp/udp is mandatory for port ranges):
```
sudo ufw allow 6000:6007/tcp
sudo ufw allow 6000:6007/udp
```
Finally enable:
```
sudo ufw enable
```

For more info, see [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04).

## Increase performance
You can increase the performance of the server by adding some swap memory in case the RAM memory is getting too full. Follow [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04) to set it up. 
