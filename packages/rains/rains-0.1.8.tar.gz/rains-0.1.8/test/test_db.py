
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.common.rains_server import RainsServer
rains_server = RainsServer()
rains_server.running()
