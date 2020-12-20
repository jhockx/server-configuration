# Installing and running Wordpress:
To host an OctoberCMS website, use this folder structure on the server. The `docker-compose.yml` file should be adjusted to the specific website accordingly. Configure `VIRTUAL_HOST` and `container_name`. The environment variable `CMS_LINK_POLICY: secure` is needed to indicate resources are loaded over https instead of http.

### Note
The CI/CD for Gitlab has not been setup yet for OctoberCMS websites. Please check the other folders for inspiration in case you wish to do so.
