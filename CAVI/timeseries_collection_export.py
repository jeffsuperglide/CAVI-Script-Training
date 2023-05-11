"""
# Take a list of time series IDs and DSS file to create CSV file output
"""

import csv
import sys

import time
import itertools
from datetime import datetime

from hec.script.Constants import TRUE as true, FALSE as false
from hec.heclib.util import HecTime
from hec.heclib.dss import HecDss

# create a generator to format times from HEC int to Excel float
def datetime_excel(times):
    _t = HecTime()
    _t.showTimeAsBeginningOfDay(true)
    for t in times:
        _t.set(t)
        dt = datetime(_t.year(), _t.month(), _t.day(), _t.hour(), _t.minute())
        unixtime = time.mktime((dt.timetuple()))
        xltime = unixtime / 86400 + 25569
        yield xltime

def main(tsids, dsspath, output, tw=None):
    header = ["Date"]
    try:
        dss = HecDss.open(dsspath) if tw is None else HecDss.open(dsspath, tw)
        tsc_collection = [dss.get(tsid) for tsid in tsids]

        tsc_collection_times = [tsc.times for tsc in tsc_collection]
        collection_times_set = set(list(itertools.chain.from_iterable(tsc_collection_times)))
        collection_times_list = list(collection_times_set)
    except Exception as err:
        print(err)
        sys.exit()

    collection_values = []
    for tsc in tsc_collection:
        # get a dictionary for times and values in the TimeSeriesContainer
        tsc_dict = {tv[0]: tv[1] for tv in zip(tsc.times, tsc.values)}
        # append a value or None to the new list
        new_values = []
        for t in collection_times_list:
            val = tsc_dict[t] if t in tsc_dict else None
            new_values.append(val)

        header.append(tsc.fullName)
        collection_values.append(new_values)

    # Write out to CSV
    with open(output, "wb") as csvfile:
        csv_writer = csv.writer(csvfile, dialect="excel")
        csv_writer.writerow(header)
        tsc_collection_times = datetime_excel(collection_times_list)
        csv_writer.writerows(zip(tsc_collection_times, *collection_values))

if __name__=="__main__":
    dsspath = "C:\\Users\\u4rs9jsg\\CWMS\\models\\CWMS\\cwms-dev_3.2.3\\forecast\\2022.09.19-0500_GMT-0500\\LRH_Little_Sandy\\forecast.dss"
    output = "C:\\Users\\u4rs9jsg\\projects\\CAVI-Script-Training\\CAVI\\_out-put.csv"
    tsids = [
        "//LEON/ELEV//1HOUR/A0S0S0/",
        "//LEON/FLOW//1HOUR/A0S0S0/",
        "//LEON/FLOW-CUMLOC//1HOUR/A0S0S0/",
        "//LEON/FLOW-IN//1HOUR/A0S0S0/",
        "//LEON/FLOW-LOCAL//1HOUR/A0S0S0/",
        "//LEON/FLOW-UNREG//1HOUR/A0S0S0/",
    ]
    main(tsids=tsids, dsspath=dsspath, output=output)#, tw="25AUG2022 0000; 15SEP2022 0000")
