import os
# import uuid
# import base64
import logging
import tornado
import tornado.template
from tornado.options import define, options
from handlers.base import Customize404Handler
# import logconfig


# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))


# Command line options
define("port", default=8888, help="run on the given port", type=int)
define("address", default="127.0.0.1", help="run on the given address", type=str)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
define(
    "template",
    default="tornado",
    help="select template engine",
    type=str
)

tornado.options.parse_command_line()

# Deployment Configuration


# class DeploymentType:
#     PRODUCTION = "PRODUCTION"
#     DEV = "DEV"
#     SOLO = "SOLO"
#     STAGING = "STAGING"
#     dict = {
#         SOLO: 1,
#         PRODUCTION: 2,
#         DEV: 3,
#         STAGING: 4
#     }


# if 'DEPLOYMENT_TYPE' in os.environ:
#     DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
# else:
#     DEPLOYMENT = DeploymentType.SOLO


# App Settings
settings = dict()
# custom 404 page
settings['default_handler_class'] = Customize404Handler
settings['debug'] = options.debug
settings['static_path'] = path(ROOT, 'media')
#settings['cookie_secret'] = base64.b64encode(
#    uuid.uuid4().bytes+uuid.uuid4().bytes
#)
settings['cookie_secret'] = os.urandom(16)
settings['xsrf_cookies'] = True

# socket
settings['websocket_ping_interval'] = 1
settings['websocket_ping_timeout'] = 2
settings['websocket_max_message_size'] = 50

# Secret keys
settings['captcha_secret_key'] = 'KEY'
settings['captcha_site_key'] = 'KEY'
settings['neverbounce_key'] = 'KEY'
settings['email_sender'] = 'example@gmail.com'
settings['email_password'] = 'password'
# Select template engine
if options.template == 'tornado':
    settings['template_loader'] = tornado.template.Loader(path(ROOT, 'templates'))
elif options.template == 'jinja2':
    from tornado_jinja2 import Jinja2Loader
    import jinja2
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path(ROOT, 'template')),
        autoescape=False
    )
    jinja2_loader = Jinja2Loader(jinja2_env)
    settings['template_loader'] = jinja2_loader

# SYSLOG_TAG = "boilerplate"
# SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
# LOGGERS = {
#     'loggers': {
#         'boilerplate': {},
#     },
# }

# if settings['debug']:
#     LOG_LEVEL = logging.DEBUG
# else:
#     LOG_LEVEL = logging.INFO
# USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

# logconfig.initialize_logging(
#     SYSLOG_TAG,
#     SYSLOG_FACILITY,
#     LOGGERS,
#     LOG_LEVEL, 
#     USE_SYSLOG
# )

if options.config:
    tornado.options.parse_config_file(options.config)
