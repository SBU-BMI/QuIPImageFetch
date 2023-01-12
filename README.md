# QuIPImageFetch

The script "quipfetch.py" will fetch an image tile from your
Quip Server Instance.

To use the script use the following command and options.

```
usage: quipfetch.py [-h] -b YOUR_QUIP_URL -u USERNAME -p PASSWORD --pid PATHDB_ID [-m] [-o OUTDIR] [-l LEVEL] [-x X_POS] [-y Y_POS]

Download a specific tile from the tile server.

options:
-h, --help show this help message and exit
-b YOUR_QUIP_URL, --base-url YOUR_QUIP_URL
Give the base URL or your quip instance.
-u USERNAME, --username USERNAME
Your Quip username.
-p PASSWORD, --password PASSWORD
Your Quip password.
--pid PATHDB_ID PathDB ID of the image.
-m, --meta Show metadata for this image.
-o OUTDIR, --outdir OUTDIR
Give an output directory the saved image.(Use trailing slashes)
-l LEVEL, --level LEVEL
Zoom level of the tile.
-x X_POS X position of the tile.
-y Y_POS Y position of the tile.
```

The script is based on the following instructions:

1. Authenticate First
   Send POST request to <https://your_quip_server_url/user/login?\_format=json>
   with a JSON body of:
   {"name":"username", "pass": "password"}
   This will create a session with a cookie that will allow you to get a JWT Access Token. You must use a session to retrieve the needed cookies for the next steps.

2. Retrieve a valid JWT token
   Do a GET to <https://your_quip_server_url/jwt/token>
   which will retrieve a JWT token similar to the following:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhsdwwwiJ9.eyJpYXQiOjE2NzExMTg2MjMsImV4cCI6MTY3MTEyMjIyMywiZHJ1cGFsIjp7InVpZCI6IjE1In19.W0CnEtFnEEAJWnvIZKff3wxOu5ESpw2WdapKVbeTvzdsWix2WCHWRQ0L2317-zuZUoYAID61v-8v3tUkkv3bjT2ViplT84_YAjd3G6KkC6fc5CbCdW9zMKNXJoeN289otpI-blb0AKKOetdAbC6hxf0D7ew4_9y4Y7EjVjGbLXfh8POHi7VF9_wIXd2AXNlFg9iZ6yZwbK4_9rfkOlf9BD1TR4P70GIIfCQgt0gNtNEoAWI3f6I3YG3m_37zhZNJxbyR6zq40OimPyEFJbJQ3D4X7ulgd06rbwDOtt5qgHeusYpl1lQpd-qBliCaSlaUlbGZ_OA0jynjhr4VNxDDxw"
}
```

3. Now access your image with a HTTP GET the DeepZoom API:
   **Image Retrieval**
   The following parameters are required: your_JWT_TOKEN_VALUE, pathdbid, level, x, y

   The following url used in a get request will return an image:
   <https://your*quip_server_url/caMicroscope/img/IIP/raw/?token={your_JWT_TOKEN_VALUE}&DeepZoom=pathdb\*{pathdbid}\_files/{level}/{x}*{y}.jpg>

   Example with most fields filled in:
   <https://your_quip_server_url/caMicroscope/img/IIP/raw/?token={your_JWT_TOKEN_VALUE}&DeepZoom=pathdb\*1688_files/10/0_0.jpg>

   **Metadata Retrieval**
   The following url is used for getting metadata on image (height,width,tile size). The data will be returned as xml:
   <https://your_quip_server_url/caMicroscope/img/IIP/raw/?token={your_JWT_TOKEN_VALUE}&DeepZoom=pathdb\*1688.dzi>

   The XML returned looks like this:

   ```xml
       <Image TileSize="256" Overlap="0" Format="jpg">
           <Size Width="101184" Height="74432"/>
       </Image>
   ```
