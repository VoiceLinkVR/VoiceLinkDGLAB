
import asyncio
import threading
from multiprocessing import Queue
from pydglab_ws import FeedbackButton,  RetCode,StrengthData,DGLabLocalClient,DGLabWSServer,Channel,StrengthOperationType
import qrcode
import socket
import time
class DGLabServerTread:
    def __init__(self,config,logger,params) -> None:
        self.config=config
        self.strengthData:StrengthData=None
        self.client:DGLabLocalClient=None
        self.loop=None
        self.params=params
        self.logger=logger

    def run(self):
        thread = threading.Thread(target=self.run_asyncio_loop,daemon=True)
        thread.start()
        return thread
    
    def run_asyncio_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.serverStart())
        except Exception as e:
            self.wirte_log("DGLabServerTread Error:"+str(e),"error")
        finally:
            self.wirte_log("DGLabServerTread Exit","info")
        
    def create_qrcode(self,data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        
        return img
    
    def get_local_ip(self):
        try:
            # 创建一个socket对象
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 利用UDP协议的特性，尝试发送无需实际传输的数据
            s.connect(('10.255.255.255', 1))
            local_ip = s.getsockname()[0]
        except Exception as e:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        return local_ip
    
    def get_ws_url(self):
        port=self.config["dglabServerPort"] 
        return f"ws://{str(self.get_local_ip())}:{port}"
    
    def print_qrcode(self,data: str):
        """输出二维码到终端界面"""
        image=self.create_qrcode(data)
        image.save('qrcode.png')

    def wirte_log(self,text:str,level:str|None):
        self.logger.put({"text":text,"level":"info"if level==None else level})


    async def serverStart(self):

        port=self.config["dglabServerPort"]
        if self.config["dglabServerIp"]=="":ip=str(self.get_local_ip())
        else: ip=self.config["dglabServerIp"]
        async with DGLabWSServer(ip,port,60) as server:
            self.client = server.new_local_client()
            client=self.client

            # 等待绑定
            await client.bind()
            self.params['dgUnbinded']=False
            self.wirte_log(f"已与 App {self.client.target_id} 成功绑定","info")

            async for data in client.data_generator(FeedbackButton, RetCode,StrengthData):

                if isinstance(data,StrengthData):
                    self.strengthData=data
                    if self.strengthData.a_limit != self.strengthData.a:
                        await self.client.set_strength(Channel.A,StrengthOperationType.SET_TO,self.strengthData.a_limit)
                    if self.strengthData.b_limit != self.strengthData.b:
                        await self.client.set_strength(Channel.B,StrengthOperationType.SET_TO,self.strengthData.b_limit)
                
                # 接收 心跳 / App 断开通知
                elif data == RetCode.CLIENT_DISCONNECTED:
                    self.wirte_log("App 已断开连接，你可以尝试重新扫码进行连接绑定","info")
                    self.params['dgUnbinded']=True
                    await client.rebind()
                    self.wirte_log("重新绑定成功","info")
                    self.params['dgUnbinded']=False
                if self.params.get('running')==False:return



class ServerTread:
    def __init__(self,logger,client,patterns,params,queue,channel) -> None:
        super().__init__()
        self.logger=logger
        self.client:DGLabLocalClient=client
        self.patterns=patterns
        self.params=params
        self.queue:Queue=queue
        self.channel=channel

        

    def run(self):
        thread = threading.Thread(target=self.run_asyncio_loop,daemon=True)
        thread.start()
        return thread
    
    def run_asyncio_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.webSocketstart())
        except Exception as e:
            self.writeLog("ServerTread Error:"+str(e),"error")
        finally:
            self.writeLog("info","ServerTread Exit")

                
    async def webSocketstart(self):
        while self.params.get('running'):
            if self.params.get("dgUnbinded"): 
                if self.channel=="A": self.writeLog("info","waiting for dgserver bind 等待dglab socket扫码绑定")
                time.sleep(3)
                continue
            
            try:
                data:dict=self.queue.get() 
                name=data.get("name")
                intensity= data.get("intensity")
                takeTime=float(data.get("time"))
                tickstime=await self.sendMessage(name,takeTime,intensity)
                await asyncio.sleep(tickstime/10-0.5)  
            except TimeoutError:  
                self.writeLog("warning","Timeout,Sever cannot connect to APP,please check APP||连接超时,无法连接至APP请检查APP是否处于运行状态")
                await asyncio.sleep(1)  
            except ConnectionRefusedError:
                self.writeLog("warning","ConnectionRefused,Server cannot to APP,please check APP||无法连接致手机APP,请检查手机APP是否开启")
                await asyncio.sleep(1)  
            except  Exception as e:
                self.writeLog("error",f"unexcepted error:{e}|type:{type(e)}")
                await asyncio.sleep(1)  
                continue



    async def sendMessage(self,pattern_name,time,intensity):
        pattern=self.patterns[pattern_name]
        intensity= 100 if intensity >100 else intensity
        pattern = [(a, tuple(int(b_i * intensity / 100 ) for b_i in b)) for a, b in pattern]

        looptime=self.getPatternLoopTime(pattern_name,time*10)

        await self.client.add_pulses(self.getChannel(self.channel),*(pattern*looptime))
        self.writeLog("info",f"Sent|channel:{self.channel}|name:{pattern_name}|intensity:{intensity}|ticks:{time*10}|time:{len(pattern)/10*looptime} s")
        return len(pattern)*looptime
    
    def writeLog(self,level,text):
        self.logger.put({'text':text,'level':level})

    def getChannel(self,value):
        if value=='A' or value=='a':return Channel.A
        if value=='B' or value=='b':return Channel.B
        self.writeLog("error",f"unexpected json 参数错误 channel error ") 


    
    def getPatternLoopTime(self,pattern_name,ticks)->int:
        one_round_tick=len(self.patterns[pattern_name])
        num=int(ticks/one_round_tick)
        return num+1
    

if __name__ == "__main__":
    import time
    try:

        logger=Queue(-1)
        server=DGLabServerTread({"dglabServerPort":5678,"dglabServerIp":"0.0.0.0"},logger,None)
        thread=server.run()
        time.sleep(5)

        url =server.client.get_qrcode(server.get_ws_url())
        img=server.create_qrcode(url)
        print(img)
        img.save('qrcode.png')
        # self.wirte_log("请用 DG-Lab App 扫描二维码以连接","info")
        print(123)

        while True:
            print(1)
            time.sleep(1)
    except:
        server.stop=True