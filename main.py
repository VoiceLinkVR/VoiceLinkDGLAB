from flask import Flask, request, render_template, url_for,jsonify,send_from_directory
import waitress
from src.core.startup import StartUp
from src.core.dglab import ServerTread
from multiprocessing import Process,Manager,freeze_support,Queue
from src.core.process import logger_process,threaded_listen
import time
import json,os,io,base64
import webbrowser
import pyaudio

queue=Queue(-1)

processList=[]
app = Flask(__name__,static_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key' 

def rebootJob():
    global queue,params,listener_thread,startUp,queue_a,baseurl,headers,queue_b,server
    queue.put({"text":"/reboot","level":"debug"})
    queue.put({"text":"sound process start to complete wait for 20s|| 服务开始重启 请等待20秒 ","level":"info"})
    params["running"] = False
    time.sleep(20)
    params["running"] = True
    params["sourceLanguage"]=startUp.config.get("sourceLanguage")
    startUp.setThreads(queue_a,queue_b)
    listener_thread = Process(target=threaded_listen,args=(baseurl,startUp.config,startUp.patterns,headers,params,queue,queue_a,queue_b))
    listener_thread.start()
queue.put({"text":"sound process restart complete|| 服务完成重启","level":"info"})

@app.route('/api/saveConfig', methods=['post'])
def saveConfig():
    global queue,params,listener_thread,startUp,sendClient,baseurl,headers
    data=request.get_json()
    queue.put({"text":"/saveandreboot","level":"debug"})
    try:
        with open('client.json', 'r',encoding='utf8') as file, open('client-back.json', 'w', encoding="utf8") as f:
            f.write(file.read())
        startUp.config=data["config"]
        with open('client.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(startUp.config,ensure_ascii=False, indent=4))
    except Exception as e:
        queue.put({"text":f"config saved 配置保存异常:{e}","level":"warning"})
        return jsonify({"text":f"config saved 配置保存异常:{e}","level":"warning"}),401
    queue.put({"text":"config saved 配置保存完毕","level":"info"})
    return startUp.config

@app.route('/')
def ui():
    return render_template("index.html")

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/getQRcode', methods=['get'])
def get_image():

    global img
    
    # 保存图片为字节流
    byte_array = io.BytesIO()
    img.save(byte_array, format='PNG')
    byte_array = byte_array.getvalue()
    
    # 将字节流转换为Base64编码的字符串（可选，也可以直接发送字节流）
    base64_image = base64.b64encode(byte_array).decode('utf-8')
    
    # 发送Base64编码的图片字符串到前端（或者你可以使用send_file发送字节流）
    return jsonify({"image": base64_image})

@app.route('/api/getQRCodeURL', methods=['get'])
def getQRCodeURL():
    global wsurl
    queue.put({"text":"/getQRCodeURL","level":"debug"})
    return jsonify({"wsurl":wsurl}),200

# 处理表单提交
@app.route('/api/getConfig', methods=['get'])
def getConfig():
    global startUp,queue
    queue.put({"text":"/getConfig","level":"debug"})
    return jsonify(startUp.config),200


@app.route('/api/reboot', methods=['get'])
def reboot():
    rebootJob()
    return jsonify({'message':'sound process restart complete|| 程序完成重启'}),200

@app.route('/api/getMics', methods=['get'])
def getMics():
    global queue
    queue.put({"text":"/getMics","level":"debug"})
    # 创建 PyAudio 实例
    p = pyaudio.PyAudio()
    host_api_count=p.get_host_api_count()
    
    # 获取设备数量
    device_count = p.get_device_count()
 
    microphones = []
    hostapis=[]
    for j in range(host_api_count):
        hostapi=p.get_host_api_info_by_index(j)
        hostapis.append(hostapi["name"])
    for i in range(device_count):
        # 获取每个设备的详细信息
        dev_info = p.get_device_info_by_index(i)
        # 检查设备是否是输入设备（麦克风）
        if dev_info['maxInputChannels'] > 0:
            microphones.append( f"{hostapis[dev_info['hostApi']]} - {dev_info['name']}")
    
    # 关闭 PyAudio 实例
    p.terminate()
 
    return jsonify(microphones),200

# 处理表单提交
@app.route('/api/saveandreboot', methods=['post'])
def update_config():
    data=request.get_json(silent=True)
    if data is None: return jsonify({'text':'no data'}),400
    config=saveConfig()
    rebootJob() 
    return jsonify(config),200

# TODO 增加获取波形接口
@app.route('/api/getPatternName', methods=['get'])
def getPatternName():
    global startUp,queue
    queue.put({"text":"/getPatternName","level":"debug"})
    return jsonify(list(startUp.patterns.keys())),200
# 示例函数
def open_web(host,port):
    
    # 定义要打开的URL
    url = f"http://{host}:{port}"
    
    # 获取Edge浏览器的可执行文件路径
    # 不同的操作系统有不同的路径
    edge_path = None
    if os.name == 'nt':  # Windows系统
        edge_path = os.path.join(os.environ.get('ProgramFiles(x86)'), 'Microsoft', 'Edge', 'Application', 'msedge.exe')
    elif os.uname().sysname == 'Darwin':  # macOS系统（注意：macOS上默认可能没有安装Edge）
        # 通常需要用户手动指定Edge的路径，或者通过其他方式获取
        # 例如：edge_path = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
        pass  # 这里不做处理，因为路径需要用户指定
    elif os.uname().sysname == 'Linux':  # Linux系统
        # Linux上Edge的路径也可能需要用户手动指定
        # 例如：edge_path = '/opt/microsoft/edge/microsoft-edge'
        pass  # 这里不做处理，因为路径需要用户指定
    try:
        # 如果找到了Edge的路径，则使用它打开网页
        if edge_path:
            # 创建一个新的Edge控制器
            edge = webbrowser.get(using=edge_path)
            # 使用Edge控制器打开网页
            edge.open(url)
        else:
            # 如果没有找到Edge的路径，则使用默认浏览器打开网页
            webbrowser.open(url)
    except Exception :
        webbrowser.open(url)
    
 

if __name__ == '__main__':
    freeze_support()
    try:
        import logging
        # 获取 asyncio 的日志记录器
        asyncio_logger = logging.getLogger('asyncio')
        
        # 设置日志级别为 CRITICAL，这样只有严重错误才会被记录
        asyncio_logger.setLevel(logging.CRITICAL)

        logger_thread = Process(target=logger_process,daemon=True,args=(queue,))
        logger_thread.start()
        manager = Manager()
        params=manager.dict()
        queue_a=manager.Queue(-1)
        queue_b=manager.Queue(-1)



        params["running"] = True
        params['dgUnbinded']=True
        startUp=StartUp(queue,params)
        headers=startUp.run()
        server=startUp.setDglabServer()
        startUp.setThreads(queue_a,queue_b)
        baseurl=startUp.config.get("baseurl")
        client=server.client
        wsurl =client.get_qrcode(server.get_ws_url())
        img=server.create_qrcode(wsurl)
        img.save('qrcode.png')
        queue.put({'text':r'''
------------------------------------------------------------------------
     __     __           __                      __        __            __       
    /  |   /  |         /  |                    /  |      /  |          /  |      
    $$ |   $$ | ______  $$/   _______   ______  $$ |      $$/  _______  $$ |   __ 
    $$ |   $$ |/      \ /  | /       | /      \ $$ |      /  |/       \ $$ |  /  |
    $$  \ /$$//$$$$$$  |$$ |/$$$$$$$/ /$$$$$$  |$$ |      $$ |$$$$$$$  |$$ |_/$$/ 
     $$  /$$/ $$ |  $$ |$$ |$$ |      $$    $$ |$$ |      $$ |$$ |  $$ |$$   $$<  
      $$ $$/  $$ \__$$ |$$ |$$ \_____ $$$$$$$$/ $$ |_____ $$ |$$ |  $$ |$$$$$$  \ 
       $$$/   $$    $$/ $$ |$$       |$$       |$$       |$$ |$$ |  $$ |$$ | $$  |
        $/     $$$$$$/  $$/  $$$$$$$/  $$$$$$$/ $$$$$$$$/ $$/ $$/   $$/ $$/   $$/ 
                                                                                                                                
     _______    ______   __         ______   _______    
    /       \  /      \ /  |       /      \ /       \ 
    $$$$$$$  |/$$$$$$  |$$ |      /$$$$$$  |$$$$$$$  |
    $$ |  $$ |$$ | _$$/ $$ |      $$ |__$$ |$$ |__$$ |
    $$ |  $$ |$$ |/    |$$ |      $$    $$ |$$    $$< 
    $$ |  $$ |$$ |$$$$ |$$ |      $$$$$$$$ |$$$$$$$  |
    $$ |__$$ |$$ \__$$ |$$ |_____ $$ |  $$ |$$ |__$$ | 
    $$    $$/ $$    $$/ $$       |$$ |  $$ |$$    $$/ 
    $$$$$$$/   $$$$$$/  $$$$$$$$/ $$/   $$/ $$$$$$$/  
                   

        '''+f'webUI: http://{startUp.config['api-ip']}:{startUp.config['api-port']}'+r''' 
                                                
        》》》》                  《《《《            
        》》》》请保持本窗口持续开启《《《《          
        》》》》                  《《《《                                 
    
        欢迎使用由VoiceLinkVR开发的VRCLS 
        本程序的开发这为boyqiu-001(boyqiu玻璃球)
        欢迎大家加入qq群1011986554获取最新资讯
        目前您使用的时公测账户,限制每日2000次请求
        如需获取更多资源请加群
------------------------------------------------------------------------
                    ''','level':'info'}
                    )
        queue.put({"text":"请用 DG-Lab App 扫描二维码以连接",'level':'info'})

        params["sourceLanguage"]=startUp.sourceLanguage

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        # this is called from the background thread


        listener_thread = Process(target=threaded_listen,args=(baseurl,startUp.config,startUp.patterns,headers,params,queue,queue_a,queue_b))
        listener_thread.start()
        
        # time.sleep(10)

        # while True:time.sleep(1)
        # app.run(debug=True,)
        queue.put({'text':"api ok||api就绪",'level':'info'})
        open_web(startUp.config['api-ip'],startUp.config['api-port'])
        waitress.serve(app=app, host=startUp.config['api-ip'], port=startUp.config['api-port'])
    except Exception as e:
        print(f"Main thread encountered an error: {e}")
    finally:
        # 设置退出事件来通知所有子线程
        listener_thread.kill()
