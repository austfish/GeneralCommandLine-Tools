import fire
import json
from app.main import run

# 加载应用参数
f = open('./app/app.json','rb') 
app = json.load(f) 
introduction = """
 ______                ___      
/\__  _\              /\_ \     
\/_/\ \/   ___     ___\//\ \    
   \ \ \  / __`\  / __`\\\ \ \     [{name}  --{version}]  
    \ \ \/\ \L\ \/\ \L\ \\\_\ \_
     \ \_\ \____/\ \____//\____\  
      \/_/\/___/  \/___/ \/____/
                                
                                                                         
Type:{type}

The tool is {description}
""".format(name=app['name'], version=app['version'], type=app['type'], description=app['description'])

app_funcs = {
    'name': app['name'],
    'version': app['version'],
    'type': app['type'],
    'description': app['description']
}


# 动态获取方法
for func in app['action']:
    func_name = func['name']
    func_class = func['func']
    func_action = getattr(run, func_class)
    # 手动转换为静态方法staticmethod
    app_funcs[func_class] = staticmethod(func_action)


# 动态生成类
Test = type(f"{app['name']}",(object,),app_funcs)


if __name__ == '__main__':
  print(introduction)
  fire.Fire(Test)