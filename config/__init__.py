from oslo_config import cfg
from oslo_log import log as logging
from os.path import join, dirname


conf = cfg.CONF
log = logging.getLogger(__name__)
logging.register_options(conf)

# common
default_opts = [
    cfg.IntOpt(name="port", default=8888),
]

conf.register_opts(default_opts)

# sqlalchemy
sqlalchemy = cfg.OptGroup(name='sqlalchemy', title="ORM 相关配置")
conf.register_group(sqlalchemy)
conf.register_cli_opts([
    cfg.BoolOpt('echo', default=True),
    cfg.BoolOpt('autoflush', default=True),
    cfg.IntOpt('pool_size', 10),
    cfg.IntOpt('pool_recycle', 3600)
], sqlalchemy)

# mysql
mysql = cfg.OptGroup(name='mysql', title="MySQL 配置")
conf.register_group(mysql)
conf.register_cli_opts([
    cfg.StrOpt('unitymob', default='localhost'),
], mysql)

# redis
redis = cfg.OptGroup(name='redis', title="Redis 相关配置")
conf.register_group(redis)
conf.register_cli_opts([
    cfg.StrOpt('host', default='127.0.0.1'),
    cfg.IntOpt('port', default=6379),
    cfg.IntOpt('db', default=0),
    cfg.StrOpt('password', default='123456'),
], redis)


conf(default_config_files=[join(dirname(__file__), '.'.join(['config', 'ini']))])

logging.setup(conf, "unitymob")