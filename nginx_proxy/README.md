# Installing and running the nginx-proxy
*The [Host multiple websites on one VPS with Docker and Nginx](https://blog.ssdnodes.com/blog/host-multiple-websites-docker-nginx/) tutorial was followed for this part*

Run
```
docker network create nginx-proxy
```

Then transfer the `docker-compose.yml` to the folder you want and run `docker-compose up -d` inside the folder. From here on out, for each website you want to add, you can make a container which is part of the `nginx-proxy` network and add the environment variable `VIRTUAL_HOST` which contains a list of all the domain names which need to be refered to this specific container. If you want to use Let's Encrypt for your domain names, you should add the environment variable `LETSENCRYPT_HOST` which contains a list of all the domain names as well.
