# Purpose
This project is made to quickly deploy a new server which hosts multiple websites. It is assumed your repo is on GitLab and you want to use the CI/CD abilities of GitLab for the hosting of (some of) the websites. Each website gets its own Docker container on the server. Furthermore, there is a nginx-proxy server (in its own Docker container) which routes you to the correct Docker container, based on the accessed domain name. You can find the GitHub project of this nginx-proxy server [here](https://github.com/jwilder/nginx-proxy).

# Docker installation
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

# Docker compose installation
First replace the version number with the current version in the script below, check the [release page](https://github.com/docker/compose/releases). Then run.
```
sudo -i
# curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
# chmod +x /usr/local/bin/docker-compose
```

# Installing and running the nginx-proxy
*The [Host multiple websites on one VPS with Docker and Nginx](https://blog.ssdnodes.com/blog/host-multiple-websites-docker-nginx/) tutorial was followed for this part*

Run
```
docker network create nginx-proxy
```

Then transfer the whole `nginx_proxy` to your home folder. Then run `docker-compose up -d` inside the folder.

# Installing and running LA(M)P server:
To host a website on the LA(M)P stack, use the `default_lamp` folder structure on the server. The `docker-compose.yml` file should be adjusted to the specific website accordingly, it is advised to add it to the project's own Git. The only thing that needs to be replaced with the website domain name, is `<something.nl/something.com>`.

# Installing and running Wordpress:
Use the `default_wordpress` structure on the server, and rename to the website its name. The `docker-compose.yml` file should be adjusted to the specific website accordingly. Again `<something.nl/something.com>` needs to be replaced plus the database and Wordpress need to be configured. FYI: The volume name made by docker compose takes the volume name defined in the `docker-compose.yml` file and prefixes it with the current folder name, or, with the foldername adjusted like described above, it will prefix the name with the domain name of the website.
