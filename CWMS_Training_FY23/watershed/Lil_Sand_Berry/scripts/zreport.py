"""
"""
import csv
import itertools
import os
import time
from datetime import datetime

from hec2.rts.ui.RtsTabType import FORECAST
from hec.heclib.dss import DSSPathname, HecDss
from hec.heclib.util import HecTime
from hec.script.Constants import FALSE as false
from hec.script.Constants import TRUE as true
from usace.cavi.script import CAVI

location = ["GRAYSONKY", "LEON"]    # B part
parameter = ["STAGE", "FLOW"]       # C part
version = ["OBS"]                   # F part in addition to key


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

def computeAlternative(currentAlternative, computeOptions):
	"""
	# Entry point into .py script
	Parameters
	----------
	currentAlternative : hec2.rts.plugins.standalone.impl.scripting.model.ScriptingPluginAlt
		Java Class
	computeOptions : hec2.rts.model.ComputeOptions
		Java Class
	"""
	# Check JavaDocs for additional methods
	currentAlternative.addComputeMessage("**** Start program order script ****")
	# Check JavaDocs for additional methods
	fparts = computeOptions.getFparts()
	# fpart = computeOptions.getFullFpart()
	# tz = computeOptions.getTimeZoneOffset()
	dssfilename = computeOptions.getDssFilename()
	# run_dir = computeOptions.getRunDirectory()
	run_tw = computeOptions.getRunTimeWindow()

	# Run code here resulting in an exit code or reference other methods
	# exit_status = function() # OR
	# exit_status = 1 (Pass) or 0 (Fail)

	exit_status = 0
	exit_status = report(run_tw, dssfilename, fparts[2])


	return exit_status

def report(tw, dssfile, fpart):
	header = ["Date"]
	# open the file, catalog (condensed), create dictionary of wants
	version.append(fpart)
	try:
		tsc_collection = []
		dss = HecDss.open(dssfile) if tw is None else HecDss.open(dssfile, tw.getLookbackTimeString(), tw.getEndTimeString())
		cat = dss.getCondensedCatalog()
		for tsid in cat:
			tsidString = tsid.toString()
			pathname = DSSPathname(tsidString)
			if pathname.bPart() in location and \
				pathname.cPart() in parameter and \
					pathname.fPart() in version:
						tsm = dss.read(tsidString)
						tsc_collection.append(tsm.getData())
		dss.close()
		
		tsc_collection_times = [tsc.times for tsc in tsc_collection]
		collection_times_set = set(list(itertools.chain.from_iterable(tsc_collection_times)))
		collection_times_list = list(collection_times_set)

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
		csvpath = os.path.dirname(dssfile)
		print(csvpath)
		csvpath = os.path.join(csvpath + "/../../../database/" + "post_process.csv")
		print(csvpath)
		csvpath = os.path.normpath(csvpath)
		print(csvpath)
		with open(csvpath, "wb") as csvfile:
			csv_writer = csv.writer(csvfile, dialect="excel")
			csv_writer.writerow(header)
			tsc_collection_times = datetime_excel(collection_times_list)
			csv_writer.writerows(zip(tsc_collection_times, *collection_values))

	except Exception as e:
		print(e)
		return 0

	return 1
