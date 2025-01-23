from flask import Flask, request, render_template, url_for,jsonify,send_from_directory
import waitress
from src.core.startup import StartUp
from src.core.dglab import ServerTread
from multiprocessing import Process,Manager,freeze_support,Queue
from src.core.process import logger_process,threaded_listen
import time
import json,os
import webbrowser


queue=Queue(-1)

processList=[]
app = Flask(__name__,static_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key' 

def rebootJob():
    global queue,params,listener_thread,startUp,sendClient,baseurl,headers
    queue.put({"text":"/reboot","level":"debug"})
    queue.put({"text":"sound process start to complete wait for 20s|| 程序开始重启 请等待20秒 ","level":"info"})
    params["running"] = False
    time.sleep(20)
    listener_thread = Process(target=threaded_listen,args=(baseurl,sendClient,startUp.config,headers,params,queue))
    listener_thread.start()
    params["running"] = True
    queue.put({"text":"sound process restart complete|| 程序完成重启","level":"info"})

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
 

# 处理表单提交
@app.route('/api/saveandreboot', methods=['post'])
def update_config():
    data=request.get_json(silent=True)
    if data is None: return jsonify({'text':'no data'}),400
    config=saveConfig()
    rebootJob() 
    return jsonify(config),200

 
# 示例函数
def open_web(host,port):
    webbrowser.open(f"http://{host}:{port}")
 

if __name__ == '__main__':
    freeze_support()
    try:
        

        logger_thread = Process(target=logger_process,daemon=True,args=(queue,))
        logger_thread.start()
        manager = Manager()
        params=manager.dict()
        queue_a=manager.Queue(-1)
        queue_b=manager.Queue(-1)

        queue.put({'text':r'''
------------------------------------------------------------------------
 __     __           __                      __        __            __        _______    ______   __         ______   _______  
/  |   /  |         /  |                    /  |      /  |          /  |      /       \  /      \ /  |       /      \ /       \ 
$$ |   $$ | ______  $$/   _______   ______  $$ |      $$/  _______  $$ |   __ $$$$$$$  |/$$$$$$  |$$ |      /$$$$$$  |$$$$$$$  |
$$ |   $$ |/      \ /  | /       | /      \ $$ |      /  |/       \ $$ |  /  |$$ |  $$ |$$ | _$$/ $$ |      $$ |__$$ |$$ |__$$ |
$$  \ /$$//$$$$$$  |$$ |/$$$$$$$/ /$$$$$$  |$$ |      $$ |$$$$$$$  |$$ |_/$$/ $$ |  $$ |$$ |/    |$$ |      $$    $$ |$$    $$< 
 $$  /$$/ $$ |  $$ |$$ |$$ |      $$    $$ |$$ |      $$ |$$ |  $$ |$$   $$<  $$ |  $$ |$$ |$$$$ |$$ |      $$$$$$$$ |$$$$$$$  |
  $$ $$/  $$ \__$$ |$$ |$$ \_____ $$$$$$$$/ $$ |_____ $$ |$$ |  $$ |$$$$$$  \ $$ |__$$ |$$ \__$$ |$$ |_____ $$ |  $$ |$$ |__$$ |
   $$$/   $$    $$/ $$ |$$       |$$       |$$       |$$ |$$ |  $$ |$$ | $$  |$$    $$/ $$    $$/ $$       |$$ |  $$ |$$    $$/ 
    $/     $$$$$$/  $$/  $$$$$$$/  $$$$$$$/ $$$$$$$$/ $$/ $$/   $$/ $$/   $$/ $$$$$$$/   $$$$$$/  $$$$$$$$/ $$/   $$/ $$$$$$$/  
                                                                                                                                
                                                                                                                                
                                                       
    
        》》》》                  《《《《
        》》》》请保持本窗口持续开启《《《《
        》》》》                  《《《《
    
        欢迎使用由VoiceLinkVR开发的VoiceLinkDGLAB
        本程序的开发这为boyqiu-001(boyqiu玻璃球)
        欢迎大家加入qq群1011986554获取最新资讯
        目前您使用的时公测账户,限制每日2000次请求
        如需获取更多资源请加群
------------------------------------------------------------------------
                    ''','level':'info'}
                    )

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
