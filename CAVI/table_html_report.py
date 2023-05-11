"""
# Generate HTML report and open
"""

import java
from hec.heclib.dss import HecDss
from hec.script import Tabulate, TableExportOptions, Plot

 
def main():
    # open the dss file
    # get the data
    # create a table
    # export as html
    dss = HecDss.open(r"C:\Users\u4rs9jsg\projects\CAVI-Script-Training\CAVI\LRH_Little_Sandy-usgs-data.dss")
    
    stage = dss.read("//Little Sandy River At Grayson/STAGE//15Minute/OBS-USGS/")
    stage_day_avg = stage.transformTimeSeries("1DAY", "", "AVE")
    tbl = Tabulate.newTable()
    tbl.addData(stage_day_avg.getData())
    opts = TableExportOptions()# get new export options
    opts.delimiter = ","# delimit with commas
    opts.title = "My Table"# set the title
    
    # fileName = r"C:\Users\u4rs9jsg\projects\CAVI-Script-Training\CAVI\LRH_Little_Sandy-usgs-data.txt"# set the output file name

    # Handle the known Java issue
    try:
        tbl.exportAsHTML(r"C:\Users\u4rs9jsg\projects\CAVI-Script-Training\CAVI\LRH_Little_Sandy.html", "Little Sandy", "\t")
    except java.lang.NullPointerException as npe:
        print(npe)

    plt = Plot.newPlot()
    plt.addData(stage_day_avg.getData())
    plt.setLocation(-1000,-1000)
    plt.showPlot()
    plt.saveToJpeg(r"C:\Users\u4rs9jsg\projects\CAVI-Script-Training\CAVI\LRH_Little_Sandy.jpeg")


    tbl.close()
    plt.close()
    dss.close()



if __name__=="__main__":
    main()
