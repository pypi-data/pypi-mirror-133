# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpel_captcha']

package_data = \
{'': ['*'], 'simpel_captcha': ['font/*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0']

setup_kwargs = {
    'name': 'simpel-captcha',
    'version': '0.1.2',
    'description': 'FastAPI or starlette 生成验证码(图片/文字)',
    'long_description': '# simpel_captcha\n> 提供分别生成图片验证码和文本验证码的方法，可结合 [FastAPI](https://fastapi.tiangolo.com/) 或者 [starlette](https://www.starlette.io/) 中的`StreamingResponse`返回图片验证码\n\n# API\n## captcha\n> 生成文字验证码，接受一个num参数，关系到生成的验证码位数\n\n```python\nfrom simpel_captcha import captcha\n\nprint(f\'验证码: {captcha(6)}\')\n```\noutput:\n```shell\n验证码: TjXP\n```\n## img_captcha\n> 生成图片验证码, 返回数据为元组 `(Image| BytesIO, captcha)`\n\n```python\nfrom simpel_captcha import img_captcha\n\nimage, text = img_captcha()\n\nprint(f\'图片对象: {image}\')\nprint(f\'验证码: {text}\')\n```\noutput:\n```shell\n图片对象: <PIL.Image.Image image mode=RGB size=100x30 at 0x1C7A0CAA7C0>\n验证码: TjXP\n```\n# [FastAPI](https://fastapi.tiangolo.com/)\n```python\nfrom fastapi import FastAPI\nfrom fastapi.responses import StreamingResponse\n\nfrom simpel_captcha import img_captcha\n\napp = FastAPI()\n\n\n@app.get("/captcha", summary=\'图片验证码\')\ndef image_captcha():\n    image, text = img_captcha(byte_stream=True)\n    # todo 将验证码缓存到Redis中 \n    return StreamingResponse(content=image, media_type=\'image/jpeg\')\n```\n# [starlette](https://www.starlette.io/)\n```python\nfrom starlette.applications import Starlette\nfrom starlette.responses import StreamingResponse\nfrom starlette.routing import Route\n\nfrom simpel_captcha import img_captcha\n\n\nasync def captcha(request):\n    image, text = img_captcha(byte_stream=True)\n    # todo 将验证码缓存到Redis中 \n    return StreamingResponse(content=image, media_type=\'image/jpeg\')\n\n\napp = Starlette(debug=True, routes=[\n    Route(\'/captcha\', captcha)\n])\n```\noutput:\n![Postman请求](example/image/postman.png)  \n![浏览器F12](example/image/fastapi.png)\n\n# LICENSE\n```text\nMIT License\n\nCopyright (c) 2022 柒意\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n```',
    'author': '柒意',
    'author_email': '396667207@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitee.com/zy7y/simpel_captcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
