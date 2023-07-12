from plugins.web import *
from plugins.weather import *
from plugins.markmap import *
from plugins.SD import *
from plugins.date import *
from plugins.upload import *

log("Loading plugins", "EVENT")

from plugins.utils import *

import plugins.web as web
import plugins.weather as weather
import plugins.markmap as markmap
import plugins.SD as SD
import plugins.date as date
import plugins.upload as upload

log("Plugins loaded", "EVENT")