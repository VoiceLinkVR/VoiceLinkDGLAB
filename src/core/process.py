from .logger import MyLogger
from ..handler.basic import BasicHandler
import speech_recognition as sr
import requests
from multiprocessing import Process,Queue
import winsound
from .dglab import DGLabServerTread,ServerTread
import threading
import asyncio

def once(audio:sr.AudioData,baseurl,config,pattern,headers,params,logger,pattern_a,pattern_b):
    sourceLanguage=params["sourceLanguage"]
    basicHandler=BasicHandler(logger,config,pattern,params,pattern_a,pattern_b)
    try:

        logger.put({"text":"音频输出完毕","level":"info"})

        url=baseurl+"/whisper/multitranscription"
    
        logger.put({"text":f"url:{url}","level":"debug"})
        files = {'file': ('filename', audio.get_wav_data(), 'audio/wav')}
        data = { 'sourceLanguage': sourceLanguage}
        response = requests.post(url, files=files, data=data, headers=headers)
        # 检查响应状态码
        if response.status_code != 200:
            logger.put({"text":f"数据接收异常:{response.text}","level":"warning"})
            return
        # 解析JSON响应
        res = response.json()
        logger.put({"text":"你说的是: " + res["text"],"level":"info"})
        if res["text"] =="":
            logger.put({"text":"返回值过滤","level":"debug"})
            return
        # 执行操作
        basicHandler.handle(res)
        

    except requests.JSONDecodeError:
        logger.put({"text":"json解析异常,code:"+str(response.status_code)+" info:"+response.text,"level":"warning"})
        return
    except Exception as e:
        logger.put({"text":e,"level":"warning"})
        return
def threaded_listen(baseurl,config,pattern,headers,params,logger,pattern_a,pattern_b):
    # logger=MyLogger().logger
    r = sr.Recognizer()
    m = sr.Microphone(device_index=None if config.get("micIndex")== -1 else config.get("micIndex"))
    logger.put({"text":"开始音量测试","level":"info"})
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    logger.put({"text":"结束音量测试","level":"info"})
    logger.put({"text":"sound process started complete||音频进程启动完毕","level":"info"})
    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
    with m as s:
        while params["running"]:
            try:  # listen for 1 second, then check again if the stop function has been called
                audio = r.listen(s, 10)
            except sr.WaitTimeoutError:  # listening timed out, just try again
                pass
            else:
                if params["running"]:
                    p = Process(target=once,daemon=True, args=(audio,baseurl,config,pattern,headers,params,logger,pattern_a,pattern_b))
                    p.start()

    logger.put({"text":"sound process exited complete||音频进程退出完毕","level":"info"})
def logger_process(queue:Queue):
    logger=MyLogger().logger
    while True:
        text=queue.get()
        if text['level']=="debug":logger.debug(text['text'])
        elif text['level']=="info":logger.info(text['text'])
        elif text['level']=="warning":logger.warning(text['text'])
        elif text['level']=="error":logger.error(text['text'])
        else :logger.warning(text)

