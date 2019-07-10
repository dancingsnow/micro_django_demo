# django-demo

## 操作顺序

- 1.创建网络
    - `docker network create django_demo_net`
- 2.启动数据库
    - `cd dev/` 执行`dev/`下的`compose`文件
    - `docker-compose up`
- 3.启动程序
    - DEBUG打开会初始化数据库，及其数据等，其他不会进行此操作
    - 执行`docker-compose up`



## Tips:
1. sqlite中的 admin superuser account:
    - username: admin
    - password: admin123456 

2. drf_yasg就是为了生成swagger-ui以及对应的可视化文档,实现api操作，靠的还是rest_framework框架的序列化操作
4. 后续的app名称可以都设为controllers，便于管理
5. 返回值使用rest-frame的Response进行封装，
```python
from rest_framework.response import Response  # 推荐
from django.http.response import JsonResponse, HttpResponse # 可以序列化成功，但是日志中间件会报错
```
6. 静态文件的服务器，切勿频繁请求


