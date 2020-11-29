# Installing and running LA(M)P server:
To host a website on the LA(M)P stack, use this folder structure on the server. The `docker-compose.yml` file should be adjusted to the specific website accordingly. The only thing that needs to be replaced is the `VIRTUAL_HOST` and the `container_name`.

### Instructions for static website development
* [Download npm](https://nodejs.org/en/download/) (~40MB)
* `npm install http-server -g`
* `http-server ./[yourfolder] -c-1 -p 1337` (for more info, [see the documentation](https://www.npmjs.com/package/http-server))
* Go to http://localhost:1337/
