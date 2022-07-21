import os
import datetime
import platform
from sanic import Sanic
from img2img_color_api import getImg
from sanic.response import json, text
app = Sanic("MyHelloWorldApp")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7788)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.post("/picture")
async def hello_world(request):
    req = request.json["imgParam"]
    print(req)
    now_time = str(datetime.datetime.now())
    specialChars = "-:. "
    for specialChar in specialChars:
        now_time = now_time.replace(specialChar, '_')
    path = os.path.split(os.path.realpath(__file__))[0]
    host_os = platform.system()
    if "Windows" == host_os:
        req["output"] = os.path.split(os.path.realpath(__file__))[
            0]+'\\data\\' + req['background']+'_'+req['language']+'_' + str(req['num_cols'])+'_' + now_time + '_' + 'hello.png'
    else:
        req["output"] = os.path.split(os.path.realpath(__file__))[
            0]+'/data/' + req['background']+'_'+req['language']+'_' + str(req['num_cols'])+'_' + now_time + '_' + 'hello.png'
    getImg(req)
    return json({"received": True, "message": req['output']})
