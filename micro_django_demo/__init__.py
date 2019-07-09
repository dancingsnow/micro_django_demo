import pymysql
pymysql.install_as_MySQLdb()
# 应对 django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3 的报错
pymysql.version_info = version_info = (1, 3, 13, "final", 0)


from django.db.backends.mysql import operations

# 针对django中MySQLdb对Python2的操作
class MyDatabaseOperations(operations.DatabaseOperations):
    def last_executed_query(self, cursor, sql, params):
        # With MySQLdb, cursor objects have an (undocumented) "_executed"
        # attribute where the exact query sent to the database is saved.
        # See MySQLdb/cursors.py in the source distribution.
        query = getattr(cursor, '_executed', None)
        # if query is not None:
        #     query = query.decode(errors='replace')
        return query

setattr(operations, "DatabaseOperations", MyDatabaseOperations)