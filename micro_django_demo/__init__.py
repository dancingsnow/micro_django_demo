import pymysql
pymysql.install_as_MySQLdb()
# 应对 django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3 的报错
pymysql.version_info = version_info = (1, 3, 13, "final", 0)