# Elasticsearch 使用说明
#### 1.导包
from elasticsearch import Elasticsearch, RequestsHttpConnection
#### 2.建立连接
```
es = Elasticsearch(
    [<host>],
    http_auth=('name', 'password'),
    port=9200, # 端口号 9200固定
    use_ssl=False  # 是否使用ssl
)
```
------------------------------------------------------------------------------------------------------------------------------------------
#### 3.映射参数
```
mappings = {
    "mappings": {
        "type_doc_test": {              # type_doc_test为doc_type  # 也就是文档名字
            "properties": {             # 内容-> 字段设置
                "id": {                 # 字段名称
                    "type": "long",     # 字段类型
                    "index": "true"     # 是否建立索引
                },
                "is_received": {
                    "type": "boolean",  
                    "index": "false"   
                },
            }
        }
    }
}
mapping 信息中指定了分词的字段，指定了字段的类型 type 为 text，字段属性里面需要添加（如果是 购买的阿里服务 不用考虑这点）：
分词器 analyzer 和 搜索分词器 search_analyzer 为 ik_max_word

[字段类型官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)

1.字符串类型
    text 、 keyword      # keyword不会进行分词,text会分词  （text模糊搜索[contains]，keyword精确搜索[==]）
2.数值类型
    long, integer, short, byte, double, float, half_float, scaled_float
3.日期类型
    date
4.布尔值类型
    boolean
5.二进制类型
    binary
6.范围类型
    integer_range, float_range, long_range, double_range, date_range
7.Array数据类型(Array不需要定义特殊类型)
    [ "one", "two" ]
    [ 1, 2 ]
    [{ "name": "Mary", "age": 12 },{ "name": "John", "age": 10}]
8.object数据类型 （json嵌套） # 注意必须小写
    { 
      "region": "US",
      "manager": { 
    "age":     30,
    "name": { 
      "first": "John",
      "last":  "Smith"
    }
      }
    }
9.地理数据类型
    Geo-point，Geo-Shape(比较复杂，参考官网文档，一般用Geo-point就可以了)
10.特殊数据类型
    ip(IPv4 and IPv6 addresses)
    completion(自动完成/搜索)
    token_count (数值类型，分析字符串，索引的数量)
    murmur3 (索引时计算字段值的散列并将它们存储在索引中的功能。 在高基数和大字符串字段上运行基数聚合时有很大帮助)
    join (同一索引的文档中创建父/子关系)        
```
#### 4.基本语法
```
1.创建索引
res = es.indices.create(index='datebeses', body=mappings)

index相当于数据库名称, body指定映射关系, 上述命令执行结果为：
创建一个名称为datebases的索引（数据库），创建第一张表名称为type_doc_test。
返回结果：{'acknowledged': True, 'shards_acknowledged': True}



------------------------------------------------------------------------------------------------------------------------------------------


2.插入单个数据
achtion = {
            'is_received': false,
            'id': 1,
        }
res = es.index(index="datebeses", doc_type="doc_type_test", body=action, id=1)


index 指定插入数据到哪个索引
doc_type 指定插入数据到哪个文档
bady 指定需要插入的数据（数据类型说明：python->dict ,  ohter->object）
id 非必传参数 建议传入手动输入 否则后续 get方法id不好指定， 不传id es会自动生成一个字符串id,不方便记录。
返回结果：
{'_id': '1', 
'result': 'created', 
'_index': 'index_test', 
'created': True, 
'_version': 1, 
'_type': 'doc_type_test', 
'_shards':{
            'failed': 0, 
            'successful': 2, 
            'total': 2
        }
}
2.1 多个数据插入

helpers.bulk(client=es,actions=actions)  # actions 列表
actions = [
    {
        "_index": "concrete_values",
        "_type": "concrete_values_list",
        "_id": 1,
        "_source": {
            "id": 1,
            "create_time": '2019-01-25',
            "update_time": '2019-01-25',
            "formset_concrete_id": 1,
            "case_id": 1,
            "company_id": 1,
            "biz_meta_id": 1,
            "value": {"value": "hello world!"},
            "content": "hello world",
            "name": "测试values", }},

]

------------------------------------------------------------------------------------------------------------------------------------------

3. 单个数据查询
res = es.get(index="index_test", doc_type="doc_type_test", id=1) # id参数必传

返回结果
{'_source': {'id': 1, 'is_received': True}, '_version': 1, '_index': 'index_test', 'found': True, '_type': 'doc_type_test', '_id': '1'}

```
------------------------------------------------------------------------------------------------------------------------------------------


#### 4.1 简单查询
```
doc = {
    "query": {  # 查询集
         "match": {  # 查询器
             # 字段名 以及 值  查询的字段type在建立索引的时候如果设置的为text才可以分词查询 其他 都为 ==
             "id": 50000}
         },
    "sort": {"id": {"order": "desc"}},  # 排序   字段  排序方式
    "from": 0,  # 从第几个数据查询
    "size": 1  # 每页的数据数量
}
```

#### 4.2 搜索所有数据
```
es.search(index="my_index",doc_type="test_type")
# 或者
body = {
    "query":{
        "match_all":{}
    }
}
es.search(index="my_index",doc_type="test_type",body=body)
```


#### 4.3 term与terms 
```
# term
body = {
    "query":{
        "term":{
            "name":"python"
        }
    }
}
# 查询name="python"的所有数据
es.search(index="my_index",doc_type="test_type",body=body)

# terms
body = {
    "query":{
        "terms":{
            "name":[
                "python","android"
            ]
        }
    }
}
# 搜索出name="python"或name="android"的所有数据
es.search(index="my_index",doc_type="test_type",body=body)
```


#### 4.4 match与multi_match  单字段或多个字段查询
```
# match:匹配name包含python关键字的数据
body = {
    "query":{
        "match":{
            "name":"python"
        }
    }
}
# 查询name包含python关键字的数据
es.search(index="my_index",doc_type="test_type",body=body)
 
# multi_match:在name和addr里匹配包含深圳关键字的数据
body = {
    "query":{
        "multi_match":{
            "query":"深圳",
            "fields":["name","addr"]
        }
    }
}
# 查询name和addr包含"深圳"关键字的数据
es.search(index="my_index",doc_type="test_type",body=body)
```

#### 4.5 ids 多个ID查询
```
body = {
    "query":{
        "ids":{
            "type":"test_type",
            "values":[
                "1","2"
            ]
        }
    }
}
# 搜索出id为1或2d的所有数据
es.search(index="my_index",doc_type="test_type",body=body)
```

#### 4.6 复合查询
```
body = {
    "query":{
        "bool":{
            "must":[
                {
                    "term":{
                        "name":"python"
                    }
                },
                {
                    "term":{
                        "age":18
                    }
                }
            ]
        }
    }
}
# 获取name="python"并且age=18的所有数据
es.search(index="my_index",doc_type="test_type",body=body)

```

#### 4.7 切片式查询
```
# 可以用作分页
body = {
    "query":{
        "match_all":{}
    }
    "from":2    # 从第二条数据开始
    "size":4    # 获取4条数据
}
# 从第2条数据开始，获取4条数据
es.search(index="my_index",doc_type="test_type",body=body)

```

#### 4.8 范围查询
```
body = {
    "query":{
        "range":{
            "age":{
                "gte":18,       # >=18
                "lte":30        # <=30
            }
        }
    }
}
# 查询18<=age<=30的所有数据
es.search(index="my_index",doc_type="test_type",body=body)

```
#### 4.9 前缀查询
```
body = {
    "query":{
        "prefix":{
            "name":"p"
        }
    }
}
# 查询前缀为"p"的所有数据
es.search(index="my_index",doc_type="test_type",body=body)

```
#### 4.10 通配符查询
```
body = {
    "query":{
        "wildcard":{
            "name":"*id"
        }
    }
}
# 查询name以id为后缀的所有数据
es.search(index="my_index",doc_type="test_type",body=body)

```
#### 4.11 排序
```
body = {
    "query":{
        "match_all":{}
    }
    "sort":{
        "age":{                 # 根据age字段升序排序
            "order":"asc"       # asc升序，desc降序
        }
    }
}

```
#### 4.12 响应过滤
```
# 只需要获取_id数据,多个条件用逗号隔开
es.search(index="my_index",doc_type="test_type",filter_path=["hits.hits._id"])
 
# 获取所有数据
es.search(index="my_index",doc_type="test_type",filter_path=["hits.hits._*"])

```
#### 4.13 count
```
# 获取数据量
es.count(index="my_index",doc_type="test_type")

```
#### 4.14 聚合查询
**· 4.14.1 获取最小值**
```
body = {
    "query":{
        "match_all":{}
    },
    "aggs":{                        # 聚合查询
        "min_age":{                 # 最小值的key
            "min":{                 # 最小
                "field":"age"       # 查询"age"的最小值
            }
        }
    }
}
# 搜索所有数据，并获取age最小的值
es.search(index="my_index",doc_type="test_type",body=body)
```
**· 4.14.2 获取最大值**
```
body = {
    "query":{
        "match_all":{}
    },
    "aggs":{                        # 聚合查询
        "max_age":{                 # 最大值的key
            "max":{                 # 最大
                "field":"age"       # 查询"age"的最大值
            }
        }
    }
}
# 搜索所有数据，并获取age最大的值
es.search(index="my_index",doc_type="test_type",body=body)
```
**· 4.14.3 获取和**
```

body = {
    "query":{
        "match_all":{}
    },
    "aggs":{                        # 聚合查询
        "sum_age":{                 # 和的key
            "sum":{                 # 和
                "field":"age"       # 获取所有age的和
            }
        }
    }
}
# 搜索所有数据，并获取所有age的和
es.search(index="my_index",doc_type="test_type",body=body)

```
**· 4.14.4 获取平均值**
```
body = {
    "query":{
        "match_all":{}
    },
    "aggs":{                        # 聚合查询
        "avg_age":{                 # 平均值的key
            "sum":{                 # 平均值
                "field":"age"       # 获取所有age的平均值
            }
        }
    }
}
# 搜索所有数据，获取所有age的平均值
es.search(index="my_index",doc_type="test_type",body=body)

```
------------------------------------------------------------------------------------------------------------------------------------------
#### 5 查询数据数量
```
res = es.search(index="index_test", doc_type="doc_type_test", filter_path=["hits.total"])
{'hits': {'total': 1}} # total是该doc里面所有的数量 可以用来与from size 做分页

res = es.count(index="index_test",doc_type="doc_type_test")
{'_shards': {'total': 5, 'successful': 5, 'failed': 0}, 'count': 1}
```
#### 6 删除一条数据
```
res = es.delete(index="index_test", doc_type="doc_type_test", id=1， ignore=[400, 404])
# 失败 返回结果  如果 没有ignore 找不到记录会报异常
{'_id': '2', '_index': 'index_test', '_type': 'doc_type_test', '_version': 2, 'found': False, '_shards': {'successful': 2, 'total': 2, 'failed': 0}, 'result': 'not_found'}
# 成功返回结果
{'_shards': {'failed': 0, 'total': 2, 'successful': 2}, 'result': 'deleted', '_index': 'index_test', '_type': 'doc_type_test', 'found': True, '_version': 2, '_id': '1'}
```
#### 7更新数据
```
#更新的主要点： 
#1. 需要指定 id 
#2. body={"doc": <xxxx>} , 这个doc是必须的
es.update(index="index_test",doc_type="doc_type_test",id=1,body={"doc":{"id":"python1","is_received":False}})
```
#### 7.1 条件删除，更新
```
# 删除
delete_by_query：删除满足条件的所有数据，查询条件必须符合DLS格式

query = {'query': {'match': {'sex': 'famale'}}}# 删除性别为女性的所有文档

query = {'query': {'range': {'age': {'lt': 11}}}}# 删除年龄小于11的所有文档

es.delete_by_query(index='indexName', body=query, doc_type='typeName')


# 更新
update_by_query：更新满足条件的所有数据，写法同上删除和查询
```

##### 8 删除索引  慎用！
```
result = es.indices.delete(index='index_test', ignore=[400, 404])

```