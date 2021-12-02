 #配置logging的基本信息，level=logging.INFO，记录INFO及以上的日志
import logging; logging.basicConfig(level=logging.INFO)
import asyncio,json,os,time
from datetime import datetime
from aiohttp import web

#部署一个web服务器首先要创建一个请求处理器，请求处理器可以是普通方法，也可以是一个协程方法，
# 它只有一个用于接受Request实例对象的参数，之后返回Response实例对象
def index(request):
    return web.Response(body=b"<h1>Awesome<h1>",headers={'content-type':'text/html'})


async def init(loop):
    #搭建WebApp的核心
    app = web.Application()
    #添加路由
    app.router.add_route('GET', '/', index)
    # 构造AppRunner对象
    apprunner = web.AppRunner(app)
     # 调用setup()方法，注意因为源码中这个方法被async修饰，此方法是一个corotine(协程)，所以前面要加上await，否则报错 
    await apprunner.setup()
    #创建服务器，将apprunner的server属性传递进去
    srv = await loop.create_server(apprunner.server, '127.0.0.1', 9000)
    #打印日志
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

#从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行
loop = asyncio.get_event_loop()
#把init协程放到loop中执行
loop.run_until_complete(init(loop))
loop.run_forever()