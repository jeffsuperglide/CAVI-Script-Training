"""
# Export time series data to csv with excel as the dialec
"""


import csv
import time
from datetime import datetime

from hec.script.Constants import TRUE as true, FALSE as false
from hec.heclib.dss import HecDss, HecTimeSeries
from hec.heclib.util import HecTime
from hec.io import TimeSeriesCollectionContainer, TimeSeriesContainerAligner

# create a generator to format times from int to string
def datetime_excel(times):
    _t = HecTime()
    _t.showTimeAsBeginningOfDay(true)
    for t in times:
        _t.set(t)
        dt = datetime(_t.year(), _t.month(), _t.day(), _t.hour(), _t.minute())
        unixtime = time.mktime((dt.timetuple()))
        xltime = unixtime / 86400 + 25569
        yield xltime


def main():
    dss = HecDss.open(r"C:\Users\u4rs9jsg\projects\CAVI-Script-Training\CAVI\LRH_Little_Sandy-usgs-data.dss")

    # Time Series Container
    tsids = [
        "//Little Sandy River At Grayson/STAGE//15Minute/OBS-USGS-DUP/",
        "//Little Sandy River At Grayson/FLOW//15Minute/OBS-USGS-DUP/"
    ]
    ts_collection = TimeSeriesCollectionContainer()
    for tsid in tsids:
        tsc = dss.get(tsid)
        ts_collection.add(tsc)

    ts_collection.finishedAdding()
    

    print(ts_collection.getSequences())
    
    # tsc_aligner = TimeSeriesContainerAligner(ts_collection.get())
    # while tsc_aligner.hasNext():
    #     tsc_aligner.alignNext()


    
    # for tsc in ts_collection.get():
    #     print(tsc.parameter)
    #     with open("C:\\Users\\u4rs9jsg\\projects\\CAVI-Script-Training\\CAVI\\%s.csv" % tsc.parameter, "wb") as csvfile:
    #         csv_writer = csv.writer(csvfile, dialect="excel")
    #         csv_writer.writerows(zip(datetime_excel(tsc.times), tsc.values))

    #     all_times = stage_tsc.times + flow_tsc.times
    #     set_times = list(set(all_times))


    #     write_row_val = []
    #     for ti in set_times:
    #         write_row_val.append([ti, stage_time_val[ti], flow_time_val[ti]])


    #     csv_writer.writerow(["", "Minimum", stage_tsm.min(), flow_tsm.min()])
    #     csv_writer.writerow(["", "Maximum", stage_tsm.max(), flow_tsm.max()])
    #     csv_writer.writerow(["", "Mean", stage_tsm.mean(), flow_tsm.mean()])
    #     # write data
    #     # csv_writer.writerows(zip(datetime_excel(stage_tsc.times), stage_tsc.values))
    #     csv_writer.writerows(write_row_val)



    dss.close()

if __name__=="__main__":
    main()
