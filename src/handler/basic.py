from typing import Optional
from .base_handler import BaseHandler
from multiprocessing import Queue 
import winsound
import time
class BasicHandler(BaseHandler):
    def __init__(self,logger,config,pattern,params,pattern_a,pattern_b):
        self.config=config
        self.logger=logger
        self.pattern=pattern
        self.pattern_a:Queue=pattern_a
        self.pattern_b:Queue=pattern_b
    """聊天框处理器"""
        
    def handle(self, message: str):
        self.controlFunction(message)
    

    def action(self,script:dict):
        for pattern in script.get("patterns"):
            self.logger.put({'text':str(pattern),'level':'info'})
            channel=pattern.get("channel")
            if channel == 'A' or channel == 'a':self.pattern_a.put(pattern)
            elif channel == 'B' or channel =='b':self.pattern_b.put(pattern)
            

    def controlFunction(self,res):
        config=self.config
        logger=self.logger
        text=res['text']

        if config["activateText"] == "":
            logger.put({"text":"无头操作:"+text,"level":"info"})
            if text == config["exitText"]:
                exit(0)
            for script in config.get("scripts"):
                if any( command in text  for command in script.get("text")):
                    logger.put({"text":"执行操作:"+script["action"],"level":"info"})
                    #执行命令
                    self.action(script)
                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
        elif config["activateText"] in text:
            commandlist=text.split(config["activateText"])
            command=commandlist[-1]
            if (config["stopText"] in command) or config["stopText"] == "":
                if config["stopText"] != "":command=command.split(config["stopText"])[0]
                logger.put({"text":"有头操作:"+command,"level":"info"})
                if command == config["exitText"]:
                    exit(0)
                for script in config.get("scripts"):
                    if command in script.get("text"):
                        logger.put({"text":"执行操作:"+script.get("action"),"level":"info"})
                        for vrcaction in script["vrcActions"]:
                            type=vrcaction.get("vrcValueType")
                            #执行命令
                        winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)