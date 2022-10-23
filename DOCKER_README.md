### lizardbyte/retroarcher

#### Using docker run
Create and run the container (substitute your `<values>`):

```bash
docker run -d \
  --name=retroarcher \
  --restart=unless-stopped
  -v <path to data>:/config \
  -e PUID=<uid> \
  -e PGID=<gid> \
  -e TZ=<timezone> \
  -p 9696:9696 \
  lizardbyte/retroarcher
```

To update the container it must be removed and recreated:

```bash
# Stop the container
docker stop retroarcher
# Remove the container
docker rm retroarcher
# Pull the latest update
docker pull lizardbyte/retroarcher
# Run the container with the same parameters as before
docker run -d ...
```

#### Using docker-compose

Create a `docker-compose.yml` file with the following contents (substitute your `<values>`):

```yaml
version: '3'
services:
  retroarcher:
    image: lizardbyte/retroarcher
    container_name: retroarcher
    restart: unless-stopped
    volumes:
      - <path to data>:/config
    environment:
      - PUID=<uid>
      - PGID=<gid>
      - TZ=<timezone>
    ports:
      - 9696:9696
```

Create and start the container (run the command from the same folder as your `docker-compose.yml` file):

```bash
docker-compose up -d
```

To update the container:
```bash
# Pull the latest update
docker-compose pull
# Update and restart the container
docker-compose up -d
```

#### Parameters
You must substitute the `<values>` with your own settings.

Parameters are split into two halves separated by a colon. The left side represents the host and the right side the
container.

**Example:** `-p external:internal` - This shows the port mapping from internal to external of the container.
Therefore `-p 9696:9696` would expose port `9696` from inside the container to be accessible from the host's IP on port
`9696` (e.g. `http://<host_ip>:9696`). The internal port must be `9696`, but the external port may be changed
(e.g. `-p 8080:9696`).


| Parameter                   | Function                                                                             | Example Value       | Required |
|-----------------------------|--------------------------------------------------------------------------------------|---------------------|:--------:|
| `-p <port>:9696`            | Web UI Port                                                                          | `9696`              |   True   |
| `-v <path to data>:/config` | Volume mapping                                                                       | `/home/retroarcher` |   True   |
| `-e PUID=<uid>`             | User ID                                                                              | `1001`              |  False   |
| `-e PGID=<gid>`             | Group ID                                                                             | `1001`              |  False   |
| `-e TZ=<timezone>`          | Lookup TZ value [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) | `America/New_York`  |   True   |

#### User / Group Identifiers:

When using data volumes (-v flags) permissions issues can arise between the host OS and the container. To avoid this
issue you can specify the user PUID and group PGID. Ensure the data volume directory on the host is owned by the same
user you specify.

In this instance `PUID=1001` and `PGID=1001`. To find yours use id user as below:

```bash
$ id dockeruser
uid=1001(dockeruser) gid=1001(dockergroup) groups=1001(dockergroup)
```
