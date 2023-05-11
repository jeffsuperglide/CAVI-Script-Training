"""CWMS Radar Data to DSS
"""

import os

from rtsutils.cavi.jython import status
from rtsutils.cwmsradar import CwmsRADAR

from hec.heclib.util import HecTime
from hec.script import MessageBox

# set start time and end time relative to now()
from hec.heclib.util import HecTime
st = HecTime()
et = HecTime()
et.setCurrent()
st.setCurrent()
st.subtractHours(2)

cwmsdat = CwmsRADAR()
cwmsdat.begintime = cwmsdat.format_datetime(st)
cwmsdat.endtime = cwmsdat.format_datetime(et)
cwmsdat.dssfile = os.path.join(
    status.get_database_directory(),
    "{}.dss".format(status.get_watershed().getName()),
)
cwmsdat.read_config(os.path.join(status.get_shared_directory(), "template_cwms_radar.config"))
# Reading the configutation file defines the lists but they still need to be set
cwmsdat.set_tsids()
cwmsdat.run()
MessageBox.showInformation("Script Done", "Script Done")
