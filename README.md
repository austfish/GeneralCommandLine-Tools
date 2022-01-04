# GeneralCommandLine-Tools
通用命令行工具，快速编写命令行工具
# 0x00 背景
安全测试过程中，有很多脚本工具，在进行编写的时候，难以复用、集成等问题。在快速调用过程中，需要重新写命令行调用工具，效率低下。
所以通过通用的命令行启动脚本，使得在工具开发的过程中，关注工具的功能、参数即可，调用逻辑将统一，在批量调用多个工具时、更容易适配。
应用结构参考[W5 SOAR](https://github.com/w5teams/w5)应用格式，可以无缝衔接使用，上传至W5即可实现Web页面调用应用，实现页面使用、命令行使用两种方式。
# 0x01 安装使用
## 1.1 下载项目
`git clone git@github.com:austfish/GeneralCommandLine-Tools.git`
**安装依赖**
`pip install -r requirements.txt`
## 1.2 定制应用

1. **app**目录下编写应用文档
1. **app.json** 配置文件更改脚本名称、类型、参数、函数名称、参数配置
1. **main.py** 文件编写功能函数

​

**1.3 使用工具**
`python start.py -h`
`python start.py get_asset_scope 127.0.0.1:5003 123456`
# 0x02 脚本应用开发
## 2.1 开发规范
### 2.1.1 基本规范

- APP 参数不能用 result ，此为系统变量
- app.json 必须包含 identification
- APP 开发文件只能有一个脚本 run.py
- 请用 async , await 开启异步，提升性能
- HTTP 请求库，推荐使用 requests
### 2.1.3 try except
为了保证 APP 的稳定性，请使用 try except 语法
```python
try:
    pass
except:
    pass
else:
    pass
finally:
    pass
```
### 2.1.4 导入第三方模块
防止用户没安装第三方模块，为了达到友好的提示，请在函数里 import 库
```python
#!/usr/bin/env python
# encoding:utf-8
from loguru import logger

async def hello_world(name):
    try:
        import nmap
    except:
        logger.info("[Hello World] 导入 nmap 模块失败, 请输入命令 pip install nmap")
        return {"status":2,"result":"导入 nmap 失败"}

    logger.info("[Hello World] 该 APP 执行参数为: {name}", name=name)
    return {"status":0,"result":"Hello," + name}
```
### 2.1.5 返回值说明
返回数据结构为：字典
```python
// 列：
{
    "status":0,
    "result":"执行成功",
    "html":"<span style='color:#333;'>执行成功</span>"
}
```
#### 参数说明
| **key** | **是否必写** | **说明** |
| --- | --- | --- |
| **status** | 是 | 执行状态 |
| **result** | 是 | 执行结果，原始数据 |
| **html** | 否 | 可视化报告用，筛选过的数据，支持 HTML+CSS 语法 ，此项不写默认为 result 数据 |

| **状态码** | **说明** |
| --- | --- |
| 0 | 正常 |
| 1 | 警告 |
| 2 | 异常 |
| 3 | 威胁 |

## 2.2 HelloWord Demo
### 2.2.1 创建项目格式
```python
├── helloworld       # APP 目录名
│   ├── app.json    # APP 配置文件
│   ├── icon.png    # APP 图标
│   ├── main       # APP 代码
|   |   └── run.py  # APP 入口文件
│   └── readme.md   # APP 说明文件
```
### 2.2.2 编写代码
```python
#!/usr/bin/env python
# encoding:utf-8
from loguru import logger # 导入日记库，没有请先安装 pip install loguru

# 为了保证性能，使用了 async await 开启异步携程，Python 3.7+ 的特性
async def hello_world(name):
    # 输出日记，生产环境会输出到指定目录
    logger.info("[Hello World] 该 APP 执行参数为: {name}", name=name)
    # 返回值，格式为： 状态码，返回内容
    return {"status": 0, "result": "Hello," + name}
```
**async** , **await** 使用 Demo
```python
#!/usr/bin/env python
# encoding:utf-8
from loguru import logger

async def hello_world(name):
    try:
        import requests
    except:
        logger.info("[Hello World] 导入 requests 模块失败, 请输入命令 pip install requests")
        return 2, "缺少 requests 模块"

    # 使用 await
    r = await requests.get(url="https://w5.io")
    print(r)

    logger.info("[Hello World] 该 APP 执行参数为: {name}", name=name)
    return {"status":0,"result":"Hello," + name,"html": '''<span style="color:red">{name}</span>'''.format(name="Hello," + name)}
```
### 2.2.3 APP 测试
使用 **asyncio** 运行测试，正式发布后请删除 **main** 入口函数
```python
#!/usr/bin/env python
# encoding:utf-8
from loguru import logger  # 导入日记库，没有请先安装 pip install loguru


# 为了保证性能，使用了 async await 开启异步，Python 3.7+ 的特性
async def hello_world(name):
    # 输出日记，生产环境会输出到指定目录
    logger.info("[Hello World] 该 APP 执行参数为: {name}", name=name)
    # 返回值，格式为： 状态码，返回内容
    return {"status": 0, "result": "Hello," + name}


if __name__ == '__main__':
    # 导入异步库
    import asyncio


    # 测试函数
    async def test():
        result = await hello_world("W5")
        print(result)


    # 加入异步队列
    async def main(): await asyncio.gather(test())


    # 启动执行
    asyncio.run(main())
```
## 2.3 APP配置文件
**注意：**

- 不能有 result 的参数，默认为 APP 结果变量
- 动作参数顺序，要保证和函数的参数顺序一致
### 2.3.1 app.json
APP配置文件
```json
{
  "identification": "w5soar",               // w5soar 签名，无需更改，必须存在
  "is_public": true,                        // 是否为公开 APP，设置 false 为私有 APP
  "name": "Hello World",                     // APP 名称
  "version": "0.1",                         // APP 版本
  "description": "W5 SOAR - Hello World",    // APP 描述
  "type": "基本应用",                        // APP 分类
  "action": [                               // APP 动作列表
    {
      "name": "HelloWorld",                  // APP 动作名称
      "func": "hello_world"                  // 动作对应的函数名
    }
  ],
  "args": {                                 // 动作参数
    "hello_world": [                         // 动作对应的函数名
      {
        "key": "name",                      // 动作参数名
        "type": "text",                     // 动作参数类型
        "required": true                    // 是否是必填项
      }
    ]
  }
}
```
### 2.3.2 多个动作
修改 action 字段
```json
  "action": [                              // APP 动作列表
    {
      "name": "HelloWorld",                 // APP 动作名称
      "func": "hello_world"                 // 动作对应的函数名
    },
    {
      "name": "test",                      // APP 动作名称
      "func": "app_test"                   // 动作对应的函数名
    },
    {
      "name": "demo",                      // APP 动作名称
      "func": "app_demo"                   // 动作对应的函数名
    }
  ],
```
### 2.3.3 动作参数
```json
 "args": {                                 // 动作参数
    "hello_world": [                         // 动作对应的函数名
      {
        "key": "name",                      // 动作参数名
        "type": "text",                     // 动作参数类型
        "required": true                    // 是否是必填项
      }
    ],
    "app_test": [                           // 动作对应的函数名
      {
        "key": "name",                      // 动作参数名
        "type": "text",                     // 动作参数类型
        "required": true                    // 是否是必填项
      },
      {
        "key": "sex",                       // 动作参数名
        "type": "text",                     // 动作参数类型
        "required": true                    // 是否是必填项
      }
    ],
    "app_demo": [                           // 动作对应的函数名
      {
        "key": "name",                      // 动作参数名
        "type": "text",                     // 动作参数类型
        "required": true                    // 是否是必填项
      },
      {
        "key": "age",                       // 动作参数名
        "type": "text",                     // 动作参数类型
        "required": false                   // 是否是必填项
      },
      {
        "key": "test",                      // 动作参数名
        "type": "text",                     // 动作参数类型
        "required": false                   // 是否是必填项
      }
    ]
  }
```
### 2.3.4 参数类型
为了提高用户体验，可以设置参数类型
```json
  "args": {                                 // 动作参数
    "app_demo": [                           // 动作对应的函数名
      {
        "key": "name",                      // 动作参数名
        "type": "text",                     // 动作参数类型
        "default": "W5",                    // 参数默认值，不写默认为空
        "required": true                    // 是否是必填项
      },
      {
        "key": "age",                       // 动作参数名
        "type": "number",                   // 动作参数类型
        "default": 18,                      // 参数默认值，不写默认为空
        "required": true                    // 是否是必填项
      },
      {
        "key": "desc",                      // 动作参数名
        "type": "textarea",                 // 动作参数类型
        "required": true                    // 是否是必填项
      },
      {
        "key": "type",                      // 动作参数名
        "type": "select",                   // 动作参数类型
        "default": "test",                  // 参数默认值，不写默认不选择
        "data": [                           // 下拉列表
          "test",
          "test2",
          "test3",
          "test4"
        ],
        "required": true                    // 是否是必填项
      }
    ]
  }
```
**目前支持 5 种类型**

| **类型** | **说明** |
| --- | --- |
| **text** | 文本输入框 |
| **password** | 密码输入框 |
| **textarea** | 多行文本输入框 |
| **number** | 数字输入框 |
| **select** | 下拉选择框 |

## 2.4 其他配置
### 2.4.1 icon.png
图标名称 icon.png 不可改变
图标大小 200 x 200
### 2.4.2 readme.md
APP 使用文档，下面为文档 Demo
```markdown
## APP 说明

> W5 SOAR Hello World

## 动作列表

### HellWorld

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **name**  | string | `是` | 名字 |

**返回值：**

Hello,{{name}} !"
```
# 0x03 通用启动工具
将启动脚本放入应用同级目录下，即可实现调用。
本项目下的APP应用是[灯塔资产](https://github.com/TophantTechnology/ARL)API调用工具
### 3.1 启动Banner
![image.png](https://cdn.nlark.com/yuque/0/2022/png/10388730/1641267103304-e7929164-4792-447c-81a4-ec544cdf713e.png#clientId=ua30bc171-ba60-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=254&id=uf7a16609&margin=%5Bobject%20Object%5D&name=image.png&originHeight=254&originWidth=522&originalType=binary&ratio=1&rotation=0&showTitle=false&size=11428&status=done&style=none&taskId=uf2b18a84-31dd-46cc-bbe2-e3f7b2187cc&title=&width=522)
### 3.2 帮助信息
![image.png](https://cdn.nlark.com/yuque/0/2022/png/10388730/1641267156613-ea242592-5008-4710-a6de-a0862945c15e.png#clientId=ua30bc171-ba60-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=433&id=u7bd20b18&margin=%5Bobject%20Object%5D&name=image.png&originHeight=433&originWidth=316&originalType=binary&ratio=1&rotation=0&showTitle=false&size=14525&status=done&style=none&taskId=u0ec6d95d-a703-4468-9d97-96ec15203c3&title=&width=316)
Help帮助信息，展示该应用支持的COMMANDS

- add_site_tag
- get_asset_scope
- get_asset_scope_site
### 3.3 使用演示
![image.png](https://cdn.nlark.com/yuque/0/2022/png/10388730/1641267324428-07341981-2910-4b68-b985-8078f98bd13a.png#clientId=ua30bc171-ba60-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=450&id=u1e9d9847&margin=%5Bobject%20Object%5D&name=image.png&originHeight=450&originWidth=1541&originalType=binary&ratio=1&rotation=0&showTitle=false&size=76225&status=done&style=none&taskId=ua0322d26-bd60-4747-bad9-0d6d7c03f23&title=&width=1541)
# 0x04 Web自动化调用工具
## 4.1 基于W5
W5 是一个面向企业安全与运维设计的 **低代码** 自动化平台，可以让团队降低 人工成本，提升 工作效率。可以把代码 图形化、可视化、可编排。让不同的系统，不同的组件通过 APP 进行封装形成平台能力，通过剧本画出你想要的逻辑过程，利用多种 Trigger 去实现自动化执行。
W5 适应用于多个方向，例：Devops、安全运营、自动化渗透、工作流程等
[参考文档](https://w5soar.com/help/#w5-%E4%BB%8B%E7%BB%8D)
## 4.2 使用演示
### 4.2.1 WEB 上传
应用中心 - 》 导入 APP
![image.png](https://cdn.nlark.com/yuque/0/2022/png/10388730/1641274458795-02079644-07d1-4212-abf2-cea6d86c64e3.png#clientId=ua30bc171-ba60-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=ua7852ab4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1594&originWidth=2874&originalType=url&ratio=1&rotation=0&showTitle=false&size=531836&status=done&style=none&taskId=u5f75ee0c-b0b3-4cc2-87b5-10bb8cdf246&title=)

- 必须进入 **私有APP** 目录下进行压缩，文件层级要符合规范
- **APPS** 下的目录，根据压缩包的名字创建，所以命名不能重复，必须唯一
- 必须包含 icon.png， readme.md 等文件
### 4.2.2 灯塔应用使用
![image.png](https://cdn.nlark.com/yuque/0/2022/png/10388730/1641274506530-0c06d306-e511-4959-92af-2f58739b9f93.png#clientId=ua30bc171-ba60-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=394&id=u8cdf5d06&margin=%5Bobject%20Object%5D&name=image.png&originHeight=394&originWidth=746&originalType=binary&ratio=1&rotation=0&showTitle=false&size=46392&status=done&style=none&taskId=u012943a1-9771-4e85-bdab-da2ef461aa2&title=&width=746)
# 0x05 参考
## 5.1 参考项目
[ARL(Asset Reconnaissance Lighthouse)资产侦察灯塔系统](https://github.com/TophantTechnology/ARL)
[W5 SOAR 使用文档](https://w5soar.com/help/)
## 5.2 参考文档
[python动态加载模块、类、函数](https://cloud.tencent.com/developer/article/1568138)
[python fire使用指南](https://blog.csdn.net/qq_17550379/article/details/79943740)
[Python动态类和动态方法的创建和调用](https://blog.51cto.com/u_14246112/3141757)
[[Python]解决python3中关于import的疑难杂症](https://segmentfault.com/a/1190000039773026)
