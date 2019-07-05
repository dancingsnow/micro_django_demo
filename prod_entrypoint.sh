#!/usr/bin/env bash

cd /work

echo "starting ..."
#ls
#pwd

# 收集django框架静态文件到STATIC_ROOT目录
python manage.py collectstatic

if ["$DEBUG" == "true"]; then
    echo "use debug mode"
    echo "load data to db ... "
    # 生成表
    python manage.py makemigrations
    # 迁移表
    python manage.py migrate

    # 加载初始数据到db
    #python manage.py loaddata author_detail.json   # 先author_detail，再author（两者有一对一关联）
    #python manage.py loaddata author.json
    echo "load done!"
fi


exec "$@"
