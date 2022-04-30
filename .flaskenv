# flask配置
FLASK_APP=app.py
FLASK_ENV=development
#FLASK_ENV=production
FLASK_RUN_HOST = 127.0.0.1
FLASK_RUN_PORT = 5000

# flask配置
SYSTEM_NAME = 社区服务

# 数据库配置信息
DATABASE_TYPE=mysql
DATABASE_HOST=127.0.0.1
# DATABASE_HOST=dbserver
DATABASE_PORT=3306
DATABASE=mysql
DATABASE_USERNAME=root
DATABASE_PASSWORD=root

# Redis 配置
# REDIS_HOST=127.0.0.1
# REDIS_PORT=6379

# 密钥配置(记得改)
SECRET_KEY='pear-admin-flask'

# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USERNAME='123@qq.com'
MAIL_PASSWORD='XXXXX' # 生成的授权码