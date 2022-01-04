## APP 说明

> 目前仅支持，`获取资产组范围`,`获取资产组站点`,`添加站点标签` 三种方式

- ARL官方文档：https://github.com/TophantTechnology/ARL

## 动作列表

### 获取资产组范围

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **api**  | text | `是` | ARL服务api接口地址 |
| **token**  | text | `是` | ARL token|
| **search**  | text | `` | 查询语句 |

**返回值：**

```
# 正常
{'errcode': 0, 'errmsg': 'ok'}
```
### 获取资产组站点

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **api**  | text | `是` | ARL服务api接口地址 |
| **token**  | text | `是` | ARL token|
| **scope_id**  | text | `` | 资产组范围ID |
| **site**  | text | `` | 站点url |
| **search**  | text | `` | 通用查询 |

**返回值：**

```
# 正常
{'errcode': 0, 'errmsg': 'ok'}
```

### 添加站点标签

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **api**  | text | `是` | ARL服务api接口地址 |
| **token**  | text | `是` | ARL token|
| **_id**  | text | `是` | 站点id |
| **tag**  | text | `是` | 标签内容 |

**返回值：**

```
# 正常
{'errcode': 0, 'errmsg': 'ok'}
```
