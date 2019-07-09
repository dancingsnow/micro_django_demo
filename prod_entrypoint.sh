#!/usr/bin/env bash

cd /work

if [ "$DEBUG" == "true" ]; then
    echo "use debug mode"
    python setup.py develop
else
    echo "use product mode"
	python setup.py install

fi

echo "starting script ..."
# 初始化
if [ "$INIT_BUILD" == "true" ]; then

    # 收集django框架静态文件到STATIC_ROOT目录
    python manage.py collectstatic --clear
#    python manage.py collectstatic --dry-run

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
