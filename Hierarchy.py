import os

class Hierarchy:
    """creates a directory and file hierarchy, based on the HIERARCHY_SCHEME data structure :
    
    dictionnaries values become dirs(named after key)
    strings values become files(named after value)
    other values such as None or ints will be ignored"""

    HIERARCHY_SCHEME = {
                        "Design" : {
                            "Components" : {} ,
                            "Reports" : {},
                            "Sch" : None,
                            "Pcb" : None,
                            "Pro" : None
                        },

                        "Doc" : {
                            "Board" :{"Full" : None, "3D" : None},
                            "Schematic" : {"Schematic" : None},
                            "Meca" : {},
                            "User" : "User.txt"
                        }, 

                        "Fab" : {
                            "Assembly" : {
                                "Equipement": None,
                                "FabMaster" : "fabmaster.cad",
                                "Bom" : None,
                                "NetList" : None,
                                "Spec" : "spec.txt",
                                "XY Position": None
                            },
                            "PCB" : {
                                "Gerber" : {
                                    "Decoupage Percage" : None,
                                    "Art Aper" : None
                                },
                                "Stackup" : {"Stackup" : "stackup.txt"}
                            },
                            "FabSpec" : "fabSpec.txt"
                        }, 

                        "Log" : "log.txt"
                    }

    def hierarchyCreation(self, boardNumber):
        os.mkdir(boardNumber)
        self.recursiveHierarchyCreation(Hierarchy.HIERARCHY_SCHEME, boardNumber + "/")


    def recursiveHierarchyCreation(self, object, path):
        if (type(object) == dict):
            for key, value in object.items():
                if type(value) == dict:
                    os.mkdir(path + key)
                    if path == "":
                        self.recursiveHierarchyCreation(value, key+ "/")
                    else :
                        self.recursiveHierarchyCreation(value, path + "/" + key+ "/")
                elif(type(value) == str):
                    open( path + value,"x")
        elif (type(object) == str):
            open(path + object,"x")

    
    def get_path_to_dir(self, dirName):
        path = self.recursive_path_to_dir(dirName, Hierarchy.HIERARCHY_SCHEME, "")
        return path

    def recursive_path_to_dir(self, dirName, object, path):
        if type(object) == dict:
            for key, value in object.items():
                if type(value) == dict:
                    if key == dirName:
                        return path
                    else:
                        finalpath = self.recursive_path_to_dir(dirName, value, path + "/" + key)
                        if finalpath is not None:
                            return finalpath

        

    