# Installing and running the nginx-proxy
### Reverse proxy
*The [Host multiple websites on one VPS with Docker and Nginx](https://blog.ssdnodes.com/blog/host-multiple-websites-docker-nginx/) tutorial was followed for this part*

Run
```
docker network create nginx-proxy
```

Then transfer the `docker-compose.yml` to the folder you want and run `docker-compose up -d` inside the folder. From here on out, for each website you want to add, you can make a container which is part of the `nginx-proxy` network and add the environment variable `VIRTUAL_HOST` which contains a list of all the domain names which need to be refered to this specific container (for more info, [see the documentation](https://github.com/nginx-proxy/nginx-proxy)). 

### Let's Encrypt
If you want to use Let's Encrypt for your domain names, you should add the environment variable `LETSENCRYPT_HOST` which contains a list of all the domain names as well (for more info, [see the documentation](https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion)).

### Basic authentication
The `docker-compose.yml` is setup for basic authentication if you want to use that (for more info, [see the documentation](https://github.com/nginx-proxy/nginx-proxy#basic-authentication-support)). To add users and passwords, you need to use the `htpasswd` command. Install by running:
```sudo apt install apache2-utils```
Then add passwords in the correct volume (check the `docker-compose.yml` where `/etc/nginx/htpasswd` is mapped to on the host machine):
```
htpasswd <something.nl> <user name>
htpasswd <www.something.nl> <user name>
```
This will prompt the password to save for each user. It will then save it in files called `<something.nl>` and `<www.something.nl>`. If these files do not exist yet, add the `-c` flag to the command (for more info, [see the documentation](http://httpd.apache.org/docs/2.2/programs/htpasswd.html) on `htpasswd`).
