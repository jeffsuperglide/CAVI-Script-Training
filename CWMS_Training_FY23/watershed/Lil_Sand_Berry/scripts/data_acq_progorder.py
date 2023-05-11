"""Get USGS Data to DSS
"""

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
	# fparts = computeOptions.getFparts()
	# fpart = computeOptions.getFullFpart()
	# tz = computeOptions.getTimeZoneOffset()
	dssfilename = computeOptions.getDssFilename()
	# run_dir = computeOptions.getRunDirectory()
	run_tw = computeOptions.getRunTimeWindow()

	# Run code here resulting in an exit code or reference other methods
	# exit_status = function() # OR
	# exit_status = 1 or 0

	return 1
