# iot feature 文档
添加自定义功能
原型链接：https://iot.console.aliyun.com/product
## 功能类型
1.属性
2.服务
3.事件
## 参数结构
### 属性服务时
#### IoTFeature
|参数名称|参数类型|是否必填|说明|
|---|---|---|---|
product_id|string|是|产品id
category_id|string|是|产品所属分类id
required|int|是|标准还是自定义(0:自定义\|1:标准)
standard|int|否(当required为1时,需要此字段)|标准还是自定义(0:可选\|1:必选)
func_type|stirng|是|功能类型：Attr\|Service\|Event 三选一,暂时只考虑Attr
func_name|string|是|功能名称,不超过32个字符
data_name|string|是|标识符,不超过32个字符
data_type|int|是|数据类型,共9种(0-8)
function|Rule_|是|规则
description|stirng|否|功能描述，不超过256个字符

#### Rule_int32
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|0|是|代表int32(整数型)
min|int||是|最小值
max|int||是|最大值
step|int||是|步长
data_unit|int||否|单位
writeable|int||是|是否可读写(0:只读;1:读写),默认只读
#### Rule_float
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|1|是|代表float
min|int||是|最小值
max|int||是|最大值
step|int||是|步长
data_unit|int||否|单位
writeable|int||是|是否可读写(0:只读;1:读写),默认只读
#### Rule_double
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|2|是|代表double
min|int||是|最小值
max|int||是|最大值
step|int||是|步长
data_unit|int||否|单位
writeable|int||是|是否可读写(0:只读;1:读写),默认只读
#### Rule_enum
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|3|是|代表enum(枚举)，枚举项至少有一项
param_len|int||是|参数列表长度
param0|string||是|参数值
param_desc0|string||是|参数描述
param1|string||否|参数值
param_desc1|string||否|参数描述
writeable|int||是|是否可读写(0:只读;1:读写),默认只读


#### Rule_bool
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|4|是|代表bool
desc0|string||是|作用描述
desc1|string||是|作用描述
writeable|int||是|是否可读写(0:只读;1:读写),默认只读
#### Rule_text
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|5|是|代表text(字符串)
len|int||是|字节长度
writeable|int||是|是否可读写(0:只读;1:读写),默认只读
#### Rule_date
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|6|是|代表date(时间型)
format|string|"UTC"|是|固定为"UTC"(毫秒)
writeable|int||是|是否可读写(0:只读;1:读写),默认只读
#### Rule_struct
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|7|是|代表struct(结构体)
param|Common(string)||是|参考上面通用数据类型,JSON字符串格式
writeable|int||是|是否可读写(0:只读;1:读写),默认只读

#### Rule_array
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
data_type|int|8|是|代表array
elem_type|int||是|元素类型(0:int32|1:float|2:double|3:text|4:struct)
param|Common(string)||否|当elem_type为4时展示
writeable|int||是|是否可读写(0:只读;1:读写),默认只读
#### Common
参数名称|参数类型|值|是否必填|说明
---|---|---|---|--
func_name|string||是|功能名称,不超过32个字符
data_name|string||是|标识符,不超过32个字符
data_type|int||是|数据类型,共7种(0-6)
function|Rule_||是|规则
description|stirng||否|功能描述，不超过256个字符
注：当data_type为Rule_struct时，参数rule里的无writeable字段


#### rule_struct function示例

[
    {
        "func_name": "test",
        "data_name": ":demo",
        "data_type": 0,
        "function": {
            "min": 1,
            "max": 30,
            "step": 2,
            "data_unit": ""
        },
        "description": ""
    }
]


[
    {
        "func_name": "test",
        "data_name": "demo",
        "data_type": 3,
        "function": {
            "param_len": 1,
            "params": [
                {
                    "param0": 1,
                    "param_desc0": "描述1"
                }
            ]
        },
        "description": ""
    }
]



