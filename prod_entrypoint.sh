#!/usr/bin/env bash

cd /work

echo "starting script ..."

# 收集django框架静态文件到STATIC_ROOT目录
python manage.py collectstatic

# 初始化数据库
if ["$INIT_DB" == "true"]; then
    echo "Initialize DB table ... "
    # 生成表
    python manage.py makemigrations
    # 迁移表
    python manage.py migrate

    # 加载初始数据到db
    echo "load data to DB table ... "
    python manage.py loaddata author_detail.json   # 先author_detail，再author（两者有一对一关联）
    python manage.py loaddata author.json
    echo "load done!"
fi

echo "finish script!"

exec "$@"
