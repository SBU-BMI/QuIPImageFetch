import requests
import json
import argparse
import xml.dom.minidom

# Option Configuration.
parser = argparse.ArgumentParser(description='Download a specific tile from the tile server.')
parser.add_argument('--pid', metavar='PATHDB_ID', required=True, help='PathDB ID of the image.')
parser.add_argument('-m', '--meta', action='store_true', default=False, help='Show metadata for this image.')
parser.add_argument('-o', '--outdir', dest="outdir", help='Give an output directory the saved image.')
parser.add_argument('-l', '--level', dest='level', default=10, help='Zoom level of the tile.')
parser.add_argument('-x', dest='x_pos', default=0, help='X position of the tile.')
parser.add_argument('-y', dest='y_pos', default=0, help='Y position of the tile.')

args = parser.parse_args()

# variables
login_url = 'https://quip.bmi.stonybrook.edu/user/login?_format=json'
jwt_url = 'https://quip.bmi.stonybrook.edu/jwt/token'
headers = { 'Content-Type': 'application/json' }
body = { 'name': 'jbalsamo', 'pass': 'H8tha1dr' }

session = requests.Session()  # create a Session object
resp = session.post(login_url, json=body,headers=headers)
out = resp.json()
fout = json.dumps(out,indent=4)

print("--------------------------------")
name = out['current_user']['name']
print("  Logged in as " + name)
print("--------------------------------")

token = session.get(jwt_url)
tout = token.json()
pt = json.dumps(tout,indent=4)
user_token = tout["token"]
#print("Token: ",user_token)

# setup formatted URLs
meta_url = "https://quip.bmi.stonybrook.edu/caMicroscope/img/IIP/raw/?token={}&DeepZoom=pathdb*{}.dzi".format(user_token,args.pid)
tile_url = "https://quip.bmi.stonybrook.edu/caMicroscope/img/IIP/raw/?token={}&DeepZoom=pathdb*{}_files/{}/{}_{}.jpg".format(user_token, args.pid,args.level,args.x_pos,args.y_pos)

results = session.get(tile_url)
if results.status_code == 200:
    img_data = results.content
    if args.outdir != None:
        dout = args.outdir
    else:
        dout = ""
    filename = dout + args.pid + "_" + str(args.level) + "_" + str(args.x_pos) + "_" + str(args.y_pos) + ".jpg"
    print("    Saving image - " + filename)
    with open(filename, 'wb') as handler:
        handler.write(img_data)
        print("\n    Image saved successfully")

print("--------------------------------")

if args.meta:
    metadata = session.get(meta_url)
    OriginalXml = metadata.text
    temp = xml.dom.minidom.parseString(OriginalXml)
    meta_output = temp.toprettyxml()
    print("Metadata (Status: {}):\n{}".format(metadata.status_code,meta_output))
    print("--------------------------------")
