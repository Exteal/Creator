"""
    @package
    Generate a Tab delimited list (csv file type).
    Components are sorted by ref and grouped by value with same footprint
    Fields are (if exist)
    'Ref', 'Qnty', 'Value', 'Cmp name', 'Footprint', 'Description', 'Vendor', 'Supplier Part Number'
 
    Command line:
    python "pathToFile/bom_csv_grouped_by_value_with_fp.py" "%I" "%O.csv"
"""

import kicad_netlist_reader
import csv
import sys

def generateCSV(netList, csvPath):

    try:
        f = open(csvPath, 'w')
        f.close()
    except IOError:
        e = "Can't open output file for writing: " + csvPath
        print(__file__, ":", e, sys.stderr)
        f = sys.stdout

    net = kicad_netlist_reader.netlist(netList)
 
    with open(csvPath, "w") as file:
        # Create a new csv writer object to use as the output formatter
        out = csv.writer(file, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
        
        # Output a set of rows for a header providing general information
        out.writerow(['Source:', net.getSource()])
        out.writerow(['Date:', net.getDate()])
        out.writerow(['Tool:', net.getTool()])
        out.writerow(['Generator:', "moi"] )
        out.writerow(['Component Count:', len(net.components)])
        out.writerow(['Ref', 'Qnty', 'Value', 'Footprint', 'Manufacturer', 'Manufacturer Part Number','Supplier','Supplier Part Number'])
        
        # Get all of the components in groups of matching parts + values
        # (see ky_generic_netlist_reader.py)
        grouped = net.groupComponents()
        
        # Output all of the component information
        for group in grouped:
            refs = ""
        
            # Add the reference of every component in the group and keep a reference
            # to the component so that the other data can be filled in once per group
            for component in group:
                refs += component.getRef() + ", "
                c = component
        
            # Fill in the component groups common data
            out.writerow([refs, len(group), c.getValue(), c.getFootprint(),c.getField("Manufacturer"), c.getField("Manufacturer Part Number"),c.getField("Supplier"),c.getField("Supplier Part Number")])
        # Import the KiCad python helper module and the csv formatter

        
        # Generate an instance of a generic netlist, and load the netlist tree from
        # the command line option. If the file doesn't exist, execution will stop

generateCSV(r"J:\Documentation_Stage\K25V1\Design\IDEFX_S_DaughterBoard.xml",r"J:\tests\BOMAJD.csv")