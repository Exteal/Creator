import json

class ProFile:
    """manages kicad project (.kicad_pro) file"""
    def __init__(self):
        pass

    def write_kicad_pro_file(self, path, proData):
        """writes the .kicad_pro file"""
        with open(path, "w") as file:
            json.dump(proData,file,ensure_ascii=False, indent=2)

    def update_kicad_pro_file(self, path, data):
        """to update constraint data of the project"""
       
        with open(path) as file:
            kicad_pro_file = json.load(file)
            kicad_pro_file["board"]["design_settings"]["rules"] = data["rules"]

        with open(path, "w") as file:
            json.dump(kicad_pro_file, file, ensure_ascii=False, indent=2)