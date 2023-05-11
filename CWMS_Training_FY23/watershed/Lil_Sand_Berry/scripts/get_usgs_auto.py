"""Get USGS Data to DSS
"""

import os

from rtsutils.cavi.jython import status
from rtsutils.usgs import USGSDataRetrieve

from hec.script import MessageBox

# set start time and end time relative to now()
from hec.heclib.util import HecTime
st = HecTime()
et = HecTime()
et.setCurrent()
st.setCurrent()
st.subtractHours(2)


rts_dss = os.path.join(
    status.get_database_directory(),
    "{}-usgs-data.dss".format(status.get_watershed().getName()),
)
retrieve = USGSDataRetrieve()
retrieve.set_dssfilename(rts_dss)
retrieve.set_begin_date(st.dateAndTime())
retrieve.set_end_date(et.dateAndTime())
retrieve.set_timezone("GMT")
retrieve.set_tzdss("GMT")
loc_file = os.path.join(status.get_shared_directory(), "usgs_locations.csv")
retrieve.set_locations_file(loc_file)
retrieve.run()
#MessageBox.showInformation("Script Done", "Script Done")
