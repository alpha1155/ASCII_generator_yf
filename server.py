from sanic import Sanic
from sanic.response import json, text
from img2img_color_api import getImg
app = Sanic("MyHelloWorldApp")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7788)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.get("/picture")
async def hello_world(request):
    imgParam = {"input": ".\\data\\jinx.png",
                "output": ".\\data\\jinx_Ascii_black.jpg",
                'language': 'chinese',
                "mode": "standard",
                "background": "black",
                "num_cols": 1100,
                "scale": 2}
    getImg(imgParam)
    return json({"ddd": "jhhlhph."})
