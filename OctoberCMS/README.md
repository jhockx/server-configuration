# Installing and running OctoberCMS:

To host an OctoberCMS website, use this folder structure on the server. The `docker-compose.yml` file should be adjusted
to the specific website accordingly. Configure `VIRTUAL_HOST` and `container_name`. The environment
variable `CMS_LINK_POLICY: secure` is needed to indicate resources are loaded over https instead of http.

### Documentation

Checkout [the full documentation](https://github.com/aspendigital/docker-octobercms) for all the OctoberCMS-in-Docker
settings.
