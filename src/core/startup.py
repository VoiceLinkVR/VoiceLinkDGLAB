import json
from .defaultConfig import defaultConfig,defaultpatterns
from .dglab import DGLabServerTread,ServerTread
import requests
import time

class StartUp:
    def __init__(self,logger,params):
        self.logger=logger
        self.params=params
        self.tragetTranslateLanguage="en"
        logger.put({"text":f"server start","level":"info"})
        try:            
            with open('patterns.json', 'r', encoding="utf8") as f:
                self.patterns = json.load(f)
        except FileNotFoundError:
            with open('patterns.json', 'w+', encoding="utf8") as f:
                logger.put({"text":'正在创建波形文件',"level":"info"})
                f.write(json.dumps(defaultpatterns,ensure_ascii=False, indent=4))
                self.patterns = defaultpatterns

        try:
            with open('client.json', 'r',encoding='utf-8') as file:
                self.config:dict = json.load(file)
        except FileNotFoundError:
            with open('client.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(defaultConfig,ensure_ascii=False, indent=4))
                self.config=defaultConfig
        except requests.exceptions.JSONDecodeError as e:
            self.logger.put({'text':"配置文件异常,详情："+str(e.strerror),"level":"error"})
            time.sleep(10)
            exit(0)

    def setDglabServer(self):
        self.dglabServer=DGLabServerTread(self.config,self.logger,self.params)
        self.dglabServer.run()
        time.sleep(5)
        return self.dglabServer
    def setThreads(self,queue_a,queue_b):
        self.AThread=ServerTread(self.logger,self.dglabServer.client,self.patterns,self.params,queue_a,"A")
        self.AThread.run()
        self.BThread=ServerTread(self.logger,self.dglabServer.client,self.patterns,self.params,queue_b,"B")
        self.BThread.run()
    def run(self):
        self.configCheck()
        res= self.checkAccount()
        return res
    def configCheck(self):
        try:
            with open('client.json', 'r',encoding='utf-8') as file:
                self.config:dict = json.load(file)
                configDiff=list(set(defaultConfig.keys())-set(self.config.keys()))
            if configDiff != []:
                self.logger.put({'text':"配置文件更新,增加条目："+str(configDiff),"level":"info"})
                for newConfig in configDiff:
                    self.config[newConfig]=defaultConfig[newConfig]
                with open('client.json', 'w', encoding="utf8") as file:
                    file.write(json.dumps(self.config,ensure_ascii=False, indent=4))
            # configDefaultScripts=[script["action"] for script in self.config["defaultScripts"]]
            # defaultScriptsDiff=[script for script in defaultConfig["defaultScripts"] if script["action"] not in configDefaultScripts]
            # if defaultScriptsDiff != []:
            #     self.logger.put({'text':"配置文件更新,增加默认指令条目："+str(defaultScriptsDiff),"level":"info"})
            #     for newConfig in defaultScriptsDiff:
            #         self.config["defaultScripts"].append(newConfig)
            #     with open('client.json', 'w', encoding="utf8") as file:
            #         file.write(json.dumps(self.config,ensure_ascii=False, indent=4))
        except requests.exceptions.JSONDecodeError as e:
            self.logger.put({'text':"配置文件异常,详情："+str(e.strerror),"level":"warning"})
            time.sleep(10)
            exit(0)
        whisperSupportedLanguageList=["af","am","ar","as","az","ba","be","bg","bn","bo","br","bs","ca","cs","cy","da","de","el","en","es"
                                    ,"et","eu","fa","fi","fo","fr","gl","gu","ha","haw","he","hi","hr","ht","hu","hy","id","is","it",
                                    "ja","jw","ka","kk","km","kn","ko","la","lb","ln","lo","lt","lv","mg","mi","mk","ml","mn","mr","ms",
                                    "mt","my","ne","nl","nn","no","oc","pa","pl","ps","pt","ro","ru","sa","sd","si","sk","sl","sn","so","sq",
                                    "sr", "su", "sv","sw","ta", "te","tg","th","tk","tl","tr","tt","uk","ur","uz","vi","yi","yo","yue","zh"]
        self.sourceLanguage="zh" if self.config["sourceLanguage"] =="" else self.config["sourceLanguage"]
        if  self.sourceLanguage not in whisperSupportedLanguageList:
            self.logger.put({'text':'please check your sourceLanguage in config,please choose one in following list\n 请检查sourceLanguage配置是否正确 请从下方语言列表中选择一个(中文是 zh)\n list:'+str(whisperSupportedLanguageList),"level":"warning"})
            input("press any key to exit||按下任意键退出...")
            exit(0)
    def checkAccount(self):


        while True:
            time.sleep(0.1)
            if self.config["userInfo"]["username"] == "" or self.config["userInfo"]["password"] == "" or self.config["userInfo"]["username"] is None or self.config["userInfo"]["password"] is None:
                self.logger.put({'text':"userinfo empty , please enter again||无用户信息请重新输入","level":"warning"})
                self.config["userInfo"]["username"] = input("请输入用户名: ")
                self.config["userInfo"]["password"] = input("请输入密码: ")
                continue
            baseurl=self.config["baseurl"]
            response = requests.post(baseurl+"/login",json=self.config["userInfo"])
            if response.status_code != 200: 
                self.logger.put({'text':response.text,"level":"debug"})
                self.logger.put({'text':"password or account error , please enter again||账户或密码错误,请重新输入","level":"warning"})
                self.config["userInfo"]["username"] = input("请输入用户名: ")
                self.config["userInfo"]["password"] = input("请输入密码: ")
                continue
            with open('client.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(self.config,ensure_ascii=False, indent=4))
            break

        res=response.json()
        return {'Authorization': 'Bearer '+res["access_token"]}