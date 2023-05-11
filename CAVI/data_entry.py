#Use ListSelection to open manual data entry dialog and save to mydb.dss

from hec.dssgui import ListSelection
from hec.heclib.util import HecTime



mw = ListSelection.getMainWindow()
mw.setIsInteractive(1,0)  # Turn off popups
mw.open(r"C:\Users\u4rs9jsg\projects\CAVI-Script-Training\CAVI\LRH_Little_Sandy-usgs-data.dss")

time = HecTime()
time.setCurrent()
time.setTime("0800")
time.addDays(-5)

mw.timeSeriesDataEntry("//Little Sandy Blw Grayson Dam Nr Leon/STAGE//15Minute/OBS-USGS/", time.dateAndTime(4) )
