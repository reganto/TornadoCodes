import os
import tornado
import tornado.template

from tornado.options import define, options

import environment

# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
define("template", default="tornado", 
        help="select template engine", 
        type=str
      )

tornado.options.parse_command_line()

MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')

# Deployment Configuration


class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }


if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

settings = dict()
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = MEDIA_ROOT
settings['cookie_secret'] = "your-cookie-secret"
settings['xsrf_cookies'] = True

# Select template engine
if options.template == 'tornado':
    settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)
elif options.template == 'jinja2':
    from tornado_jinja2 import Jinja2Loader
    import jinja2

    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_ROOT), autoescape=False)
    jinja2_loader = Jinja2Loader(jinja2_env)

    settings['template_loader'] = jinja2_loader

SYSLOG_TAG = "boilerplate"

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
   'loggers': {
        'boilerplate': {},
    },
}

if settings['debug']:
    #LOG_LEVEL = logging.DEBUG
    pass
else:
    LOG_LEVEL = logging.INFO
USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

#logconfig.initialize_logging(SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS,
#                             LOG_LEVEL, USE_SYSLOG)

if options.config:
    tornado.options.parse_config_file(options.config)
