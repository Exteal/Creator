class Schematic:
    pass

def write_schematic_file(path, data): 

    optional =  """(kicad_sch
    (version 20211014)                                             
    (generator eeschema)                                         

    )""".format(data["version"])

    with open(path, "w") as file:
        file.write(optional)