<template>
    <el-container>  
      <el-header>
        <h1>VoiceLinkDGLAB配置管理</h1>
      </el-header>
      <el-container>
        <el-aside width="10%">
            <sideInfo/>
        </el-aside>
        <el-main>
            <el-button-group style="margin-left:50%;margin-bottom: 20px;" >
                <el-button type="primary" @click="getconfig">获取配置</el-button>
                <el-button type="primary" @click="fetchImage">获取二维码</el-button>
                <el-button type="primary" @click="saveconfig">保存配置</el-button>
                <el-button type="primary" @click="saveAndBoot">保存配置并重启</el-button>
                <el-button type="primary" @click="reboot">重启服务</el-button>
            </el-button-group>
            <el-row :gutter="20">
                <el-col :span="8" >
                    <el-card style="height: 400px;">
                        <template #header>
                            <div class="card-header">
                            <span>程序配置</span>
                            </div>
                            
                        </template>
                        <el-form :model="data.config" label-width="auto">
                            <el-form-item label="服务器URL">
                                <el-input v-model="data.config.baseurl"></el-input>
                            </el-form-item>
                            <el-form-item label="郊狼服务端 IP">
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    content="修改该配置后，请关闭程序黑色窗口并重启程序"
                                    placement="right"
                                >
                                <el-input v-model="data.config['dglabServerIp']" placeholder="局域网中扫码异常时填写"></el-input>
                                </el-tooltip>
                            </el-form-item>
                            <el-form-item label="郊狼服务端 端口">
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    content="修改该配置后，请关闭程序黑色窗口并重启程序"
                                    placement="right"
                                >
                                <el-input type="number" v-model="data.config['dglabServerPort']"></el-input>
                                </el-tooltip>
                            </el-form-item>

                            <el-form-item label="程序退出文本">
                                <el-input v-model="data.config.exitText"></el-input>
                            </el-form-item>
                            <el-form-item label="识别语言">
                                <el-select v-model="data.config.sourceLanguage">
                                    <el-option label="阿非利堪斯语(Afrikaans)" value="af"></el-option>
                                    <el-option label="阿姆哈拉语(Amharic)" value="am"></el-option>
                                    <el-option label="阿拉伯语(Arabic)" value="ar"></el-option>
                                    <el-option label="阿萨姆语(Assamese)" value="as"></el-option>
                                    <el-option label="阿塞拜疆语(Azerbaijani)" value="az"></el-option>
                                    <el-option label="巴什基尔语(Bashkir)" value="ba"></el-option>
                                    <el-option label="白俄罗斯语(Belarusian)" value="be"></el-option>
                                    <el-option label="保加利亚语(Bulgarian)" value="bg"></el-option>
                                    <el-option label="孟加拉语(Bengali)" value="bn"></el-option>
                                    <el-option label="藏语(Tibetan)" value="bo"></el-option>
                                    <el-option label="布雷顿语(Breton)" value="br"></el-option>
                                    <el-option label="波斯尼亚语(Bosnian)" value="bs"></el-option>
                                    <el-option label="加泰罗尼亚语(Catalan)" value="ca"></el-option>
                                    <el-option label="捷克语(Czech)" value="cs"></el-option>
                                    <el-option label="威尔士语(Welsh)" value="cy"></el-option>
                                    <el-option label="丹麦语(Danish)" value="da"></el-option>
                                    <el-option label="德语(German)" value="de"></el-option>
                                    <el-option label="希腊语(Greek)" value="el"></el-option>
                                    <el-option label="英语(English)" value="en"></el-option>
                                    <el-option label="西班牙语(Spanish)" value="es"></el-option>
                                    <el-option label="爱沙尼亚语(Estonian)" value="et"></el-option>
                                    <el-option label="巴斯克语(Basque)" value="eu"></el-option>
                                    <el-option label="波斯语(Persian)" value="fa"></el-option>
                                    <el-option label="芬兰语(Finnish)" value="fi"></el-option>
                                    <el-option label="法罗语(Faroese)" value="fo"></el-option>
                                    <el-option label="法语(French)" value="fr"></el-option>
                                    <el-option label="加利西亚语(Galician)" value="gl"></el-option>
                                    <el-option label="古吉拉特语(Gujarati)" value="gu"></el-option>
                                    <el-option label="豪萨语(Hausa)" value="ha"></el-option>
                                    <el-option label="夏威夷语(Hawaiian)" value="haw"></el-option>
                                    <el-option label="希伯来语(Hebrew)" value="he"></el-option>
                                    <el-option label="印地语(Hindi)" value="hi"></el-option>
                                    <el-option label="克罗地亚语(Croatian)" value="hr"></el-option>
                                    <el-option label="海地克里奥尔语(Haitian Creole)" value="ht"></el-option>
                                    <el-option label="匈牙利语(Hungarian)" value="hu"></el-option>
                                    <el-option label="亚美尼亚语(Armenian)" value="hy"></el-option>
                                    <el-option label="印尼语(Indonesian)" value="id"></el-option>
                                    <el-option label="冰岛语(Icelandic)" value="is"></el-option>
                                    <el-option label="意大利语(Italian)" value="it"></el-option>
                                    <el-option label="日语(Japanese)" value="ja"></el-option>
                                    <el-option label="爪哇语(Javanese)" value="jw"></el-option>
                                    <el-option label="格鲁吉亚语(Georgian)" value="ka"></el-option>
                                    <el-option label="哈萨克语(Kazakh)" value="kk"></el-option>
                                    <el-option label="高棉语(Khmer)" value="km"></el-option>
                                    <el-option label="卡纳达语(Kannada)" value="kn"></el-option>
                                    <el-option label="韩语(Korean)" value="ko"></el-option>
                                    <el-option label="拉丁语(Latin)" value="la"></el-option>
                                    <el-option label="卢森堡语(Luxembourgish)" value="lb"></el-option>
                                    <el-option label="林加拉语(Lingala)" value="ln"></el-option>
                                    <el-option label="老挝语(Lao)" value="lo"></el-option>
                                    <el-option label="立陶宛语(Lithuanian)" value="lt"></el-option>
                                    <el-option label="拉脱维亚语(Latvian)" value="lv"></el-option>
                                    <el-option label="马达加斯加语(Malagasy)" value="mg"></el-option>
                                    <el-option label="毛利语(Maori)" value="mi"></el-option>
                                    <el-option label="马其顿语(Macedonian)" value="mk"></el-option>
                                    <el-option label="马拉雅拉姆语(Malayalam)" value="ml"></el-option>
                                    <el-option label="蒙古语(Mongolian)" value="mn"></el-option>
                                    <el-option label="马拉提语(Marathi)" value="mr"></el-option>
                                    <el-option label="马来语(Malay)" value="ms"></el-option>
                                    <el-option label="马耳他语(Maltese)" value="mt"></el-option>
                                    <el-option label="缅甸语(Burmese)" value="my"></el-option>
                                    <el-option label="尼泊尔语(Nepali)" value="ne"></el-option>
                                    <el-option label="荷兰语(Dutch)" value="nl"></el-option>
                                    <el-option label="尼诺尔斯克语(Nynorsk)" value="nn"></el-option>
                                    <el-option label="挪威语(Norwegian)" value="no"></el-option>
                                    <el-option label="奥克语(Occitan)" value="oc"></el-option>
                                    <el-option label="旁遮普语(Punjabi)" value="pa"></el-option>
                                    <el-option label="波兰语(Polish)" value="pl"></el-option>
                                    <el-option label="普什图语(Pashto)" value="ps"></el-option>
                                    <el-option label="葡萄牙语(Portuguese)" value="pt"></el-option>
                                    <el-option label="罗马尼亚语(Romanian)" value="ro"></el-option>
                                    <el-option label="俄语(Russian)" value="ru"></el-option>
                                    <el-option label="梵语(Sanskrit)" value="sa"></el-option>
                                    <el-option label="信德语(Sindhi)" value="sd"></el-option>
                                    <el-option label="僧伽罗语(Sinhala)" value="si"></el-option>
                                    <el-option label="斯洛伐克语(Slovak)" value="sk"></el-option>
                                    <el-option label="斯洛文尼亚语(Slovenian)" value="sl"></el-option>
                                    <el-option label="修纳语(Shona)" value="sn"></el-option>
                                    <el-option label="索马里语(Somali)" value="so"></el-option>
                                    <el-option label="阿尔巴尼亚语(Albanian)" value="sq"></el-option>
                                    <el-option label="塞尔维亚语(Serbian)" value="sr"></el-option>
                                    <el-option label="巽他语(Sundanese)" value="su"></el-option>
                                    <el-option label="瑞典语(Swedish)" value="sv"></el-option>
                                    <el-option label="斯瓦希里语(Swahili)" value="sw"></el-option>
                                    <el-option label="泰米尔语(Tamil)" value="ta"></el-option>
                                    <el-option label="泰卢固语(Telugu)" value="te"></el-option>
                                    <el-option label="塔吉克语(Tajik)" value="tg"></el-option>
                                    <el-option label="泰语(Thai)" value="th"></el-option>
                                    <el-option label="土库曼语(Turkmen)" value="tk"></el-option>
                                    <el-option label="他加禄语(Tagalog)" value="tl"></el-option>
                                    <el-option label="土耳其语(Turkish)" value="tr"></el-option>
                                    <el-option label="鞑靼语(Tatar)" value="tt"></el-option>
                                    <el-option label="乌克兰语(Ukrainian)" value="uk"></el-option>
                                    <el-option label="乌尔都语(Urdu)" value="ur"></el-option>
                                    <el-option label="乌兹别克语 (Uzbek)" value="uz"></el-option>
                                    <el-option label="越南语(Vietnamese)" value="vi"></el-option>
                                    <el-option label="依地语(Yiddish)" value="yi"></el-option>
                                    <el-option label="约鲁巴语(Yoruba)" value="yo"></el-option>
                                    <el-option label="粤语(Cantonese)" value="yue"></el-option>
                                    <el-option label="中文(Chinese)" value="zh"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-form>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card style="height: 400px;">
                        <template #header>
                            <div class="card-header">
                            <span>用户信息配置</span>
                            </div>
                            
                        </template>
                        <el-form :model="data.config" label-width="auto">
                            <el-form-item label="用户名">
                                <el-input v-model="data.config.userInfo.username"></el-input>
                            </el-form-item>
                            <el-form-item label="密码">
                                <el-input type="password" v-model="data.config.userInfo.password" show-password></el-input>
                            </el-form-item>
                        </el-form>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card style="height: 400px;">
                        <template #header>
                            <div class="card-header">
                            <span>郊狼二维码</span>
                            </div>
                            
                        </template>
                        <el-image :src="data.local.imageSrc" style="min-width: 200px;width: 70%; height: auto" v-if="data.local.imageSrc" fit="contain"/>

                    </el-card>
                </el-col>

            </el-row>
        <el-card style="margin-top: 20px;height: 620px;">
            <template #header>
                <span>自定义脚本配置</span>
            </template>
            <el-row  :gutter="5">
                <el-col  :span="6">
                    
                    <h5 class="mb-2">自定义脚本目录</h5>
                    <el-menu
                        default-active="1"
                        class="el-menu-vertical-demo"
                        @open="handleOpen"
                        @close="handleClose"
                    >
                    <el-scrollbar height="420px">
                        <el-menu-item v-for="(item, index) in data.config.scripts" :index="index" :key="index" @click="data.local.scriptClick=index">
                        <span>{{ item.action }}</span>
                        </el-menu-item>
                    </el-scrollbar>
                    </el-menu>
                    <el-button-group class="ml-4">
                            <el-button type="primary" @click="addScriptItem">添加脚本</el-button>

                            <el-button type="danger" @click="removeScriptItem" >删除选定脚本</el-button>
                        </el-button-group>


                </el-col>

                <el-col  :span="9">
                    <el-card style="height: 500px;">
                        <template #header>
                            <span>自定义脚本名称与关键词</span>
                        </template>

                        <el-form label-width="auto">
                        <el-form-item label="自定义脚本名称" >
                            <el-input v-model="data.config.scripts[data.local.scriptClick].action" placeholder="请输入名称"></el-input>
                        </el-form-item>

                        <el-button type="primary" @click="addCustomItem" style="margin-left: 70%;margin-bottom: 20px;">添加关键词</el-button>

                        <el-scrollbar height="320px">
                        <el-form-item v-for="(item, index) in data.config.scripts[data.local.scriptClick].text" :key="index" :label="'关键词' + (index + 1)">
                            <div>
                                <el-row :gutter="20">
                                    <el-col :span="18"><el-input v-model="data.config.scripts[data.local.scriptClick].text[index]"  placeholder="请输入文本"></el-input></el-col>
                                    <el-col :span="6"><el-button type="danger" :icon="Delete" circle @click="removeCustomItem(index)"/></el-col>
                                
                                
                                </el-row>
                            </div>

                        </el-form-item>
                        </el-scrollbar>
                    </el-form>
                    </el-card>

                </el-col>
                <el-col  :span="9">
                    <el-card style="height: 500px;">
                        <template #header>
                                <span>自定义脚本执行动作</span>
                        </template>
                        <el-scrollbar height="400px">
                            <el-descriptions
                                v-for="(item, index) in data.config.scripts[data.local.scriptClick].patterns"
                                class="margin-top"
                                :title="'波形' + (index + 1)"
                                :column="1"
                                border
                                :key="index"
                            >
                                <template #extra>
                                    <el-button-group class="ml-4">
                                        <el-button v-if="index==(data.config.scripts[data.local.scriptClick].patterns.length-1)" type="primary" :icon="Plus" @click="addActionItem"/>
                                        <el-button type="danger" :icon="Delete"  @click="removeActionItem(index)"/>
                                    </el-button-group>

                                </template>
                                <el-descriptions-item>
                                    <template #label>
                                        波形名称
                                    </template>
                                    <!-- <el-tooltip
                                        class="box-item"
                                        effect="dark"
                                        content="推荐从下方模型参数中复制参数路径"
                                        placement="right"
                                    > -->
                                    <el-select v-model="item.name">
                                        <el-option label="随机" value="random"/>
                                        <el-option v-for="(item, index) in data.local.patternName" :key="index"    :label="item" :value="item"/>
                                    </el-select>
                                    <!-- </el-tooltip> -->
                                </el-descriptions-item>
                                <el-descriptions-item>
                                    <template #label>
                                        通道
                                    </template>
                                    <el-select v-model="item.channel">
                                        <el-option label="随机" value="random"/>
                                        <el-option label="A通道" value="A"></el-option>
                                        <el-option label="B通道" value="B"></el-option>
                                    </el-select>
                                </el-descriptions-item>
                                <el-descriptions-item>
                                    <template #label>
                                        强度(%)
                                    </template>
                                    <el-slider v-model="item.intensity" show-input />
                                    <!-- <el-input v-model="item.intensity" placeholder="请输入强度值"/> -->
                                </el-descriptions-item>

                                <el-descriptions-item>
                                    <template #label>
                                        时长(s)
                                    </template>
                                    <el-slider v-model="item.time" :min="1" :max="5" :step="0.1" show-input />
                                </el-descriptions-item>
                            </el-descriptions>
                        </el-scrollbar>
                    </el-card>
                </el-col>
            </el-row>

   
    
    
            </el-card>

        </el-main>  
        <el-aside width="10%">
            <sideInfo/>
        </el-aside>
      </el-container>

    </el-container>
</template>

<script setup>
import sideInfo from './side-info.vue'
import axios from 'axios';
import { ElMessage ,ElMessageBox} from 'element-plus'
import {
  Delete,Plus
} from '@element-plus/icons-vue'
import { onMounted, reactive } from 'vue';

let data=reactive({
    local:{
            imageSrc:null,
            scriptClick:0,
            patternName:[]
            },
    config:{
        "userInfo": {
            "username": "testuser",
            "password": "abc123!"
        },
        "baseurl": "https://whisper.boyqiu001.cn:7070",
        "api-ip":"127.0.0.1",
        "api-port":8980,
        "sourceLanguage": "zh",
        "dglabServerIp":"",
        "dglabServerPort":56742,
        "activateText":"",
        "exitText":"退出程序",
        "scripts": [
            {
                "action":"1",
                "text": ["测试","可以"],
                "patterns":[
                    {
                    "name":"呼吸",
                    "channel": "B",
                    "intensity": 10,
                    "time": 2
                    },
                    {
                    "name":"呼吸",
                    "channel": "A",
                    "intensity": 10,
                    "time": 3
                    }
                ]
            }
        ]
    }

})




onMounted(()=>{
    getconfig();
    fetchImage();
})
function getconfig() {
    axios.get('/api/getConfig').then(response => {
        data.config = response.data;
        ElMessage({
        message: '配置信息获取成功',
        type: 'success',
    })
    });
    axios.get('/api/getPatternName').then(response => {
        data.local.patternName = response.data;
        ElMessage({
        message: '波形名称获取成功',
        type: 'success',
    })
    });
}

function saveconfig(){
    axios.post('/api/saveConfig',{'config':data.config},{headers: {
    'Content-Type': 'application/json'
  }}).then(        ElMessage({
        message: '配置信息保存成功',
        type: 'success',
    }))
}
function saveAndBoot(){
    saveconfig()
    reboot()
}
function reboot(){
    axios.get('/api/reboot')
}

function  addCustomItem() {
    data.config.scripts[data.local.scriptClick].text.push('');
}

function removeCustomItem(index) {
    data.config.scripts[data.local.scriptClick].text.splice(index, 1);
}
function addActionItem(){
    data.config.scripts[data.local.scriptClick].patterns.push({
                    "name":"呼吸",
                    "channel": "A",
                    "intensity": 0,
                    "time": 2
                    })
}

function removeActionItem(index){
    data.config.scripts[data.local.scriptClick].patterns.splice(index, 1);
}
function addScriptItem(){
    data.config.scripts.push({
                "action":"脚本",
                "text": [""],
                "patterns":[
                    {
                    "name":"呼吸",
                    "channel": "A",
                    "intensity": 0,
                    "time": 2
                    }
                ]
            })
}
function removeScriptItem(){
    const index=data.local.scriptClick
    ElMessageBox.confirm(
    '请确认是否删除自定义脚本:'+ data.config.scripts[index]['action'],
    'Warning',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
        if(index==0 && data.config.scripts.length==1){
        data.config.scripts[0]={
            "action": "脚本",
            "text": [""],
            "vrcActions": [{
                    "vrcPath": "",
                    "vrcValueType": "bool",
                    "vrcValue": 0,
                    "sleeptime": 0.1
                }]
        }

        return
    }
    else{
        data.local.scriptClick=index==0?0:index-1
        data.config.scripts.splice(index, 1);
    }

    ElMessage({
        type: 'success',
        message: '删除成功',
        })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      })
    })
    
}
function fetchImage() {
      try {
        axios.get('/api/getQRcode').then(response=>{
            const base64Image = response.data.image;
            // 将Base64字符串转换为data URL
            data.local.imageSrc = `data:image/png;base64,${base64Image}`;
        });

      } catch (error) {
        console.error('Error fetching image:', error);
      }
    }

</script>

<style scoped>
.info-container {
  padding: 20px;
  font-size: 14px; /* 可以根据需要调整字体大小 */
  line-height: 1.5; /* 调整行高以增加可读性 */
}
 
.info-container p {
  margin: 10px 0; /* 调整段落之间的间距 */
}
</style>

