"""
# Plot time series base interval and hourly average
"""
from hec.script import Plot, Tabulate
from hec.script.Constants import TRUE as true, FALSE as false
from hec.heclib.dss import HecDss, DSSPathname

try:
    from rtsutils.cavi.jython import status
except ImportError as err:
    print(err)

def main():
    """
    #
    """
    # Get CAVI status to determine watershed, time window, database dir, etc
    # Take the lowest interval and convert to hourly average
    # Show the plot
    # Optionally save averages to DSS

    # Get a catalog of pathnames
    dss = HecDss.open(r"C:\Users\u4rs9jsg\projects\CAVI-Script-Training\CAVI\LRH_Little_Sandy-usgs-data.dss")
    cat = dss.getCondensedCatalog()

    # Iterate through the pathnames and create plots based on parameters
    plot = Plot.newPlot()
    table = Tabulate.newTable()
    for dss_path in cat:
        dsspathname = DSSPathname(dss_path.toString())
        dsspathname.setDPart("")
        
        tsm = dss.read(dsspathname.toString())

        tsm_interp = tsm.interpolateDataAtRegularInterval("1HOUR", "")
        tsm_forward_avg = tsm.forwardMovingAverage(4)
        
        plot.addData(tsm.getContainer())
        plot.addData(tsm_forward_avg.getContainer())
        # plot.addData(tsm_interp.getContainer())
        
        table.addData(tsm.getContainer())
        table.addData(tsm_forward_avg.getContainer())
        # table.addData(tsm_interp.getContainer())
    # plot.showPlot()
    table.showTable()

    if dss: dss.close()

if __name__=="__main__":
    main()
