class StackupFile:        
    def write_stackup_file(self, data, path):

        copper_layers = {}

        for idx, (key, value) in (enumerate(data["stackup"].items())):
            if "Cu" in value["layer"]:
                copper_layers[value["layer"]] = data["stackup"][str(idx)]

        content = """Stackup
 ========

 Board .. : {board}
 Date ... : {date}

 Nbr  Type     Dielectric[Cts]             Thickness     Class    Via    Layer
 ~~~  ~~~~~~~  ~~~~~~~~~~~~~~~~~~~~~~~~~~  ~~~~~~~~~    ~~~~~~    ~~~    
""".format(board=data["board"], date= data["date"])
        
        for j in copper_layers:   
            content+="""   {nbr}  {type}  ==========================         {thickness}mm     class      -+-      {side}
""".format(nbr=j, type = parse_type(copper_layers[j]), thickness = copper_layers[j]["thickness"],
side = parse_side(copper_layers[j]["side"]))



        content+="""
 Dimension ............ : {width} mm x {height} mm
 Thickness ............. : {thick} mm
 Class ................ : c
 Finish ............... : {finish}
 Solder Mask .......... : {solder_mask}
 Silkscreen ........... : {silkscreen}
 Electrical Test ...... : e""".format(
  thick=data["board_thickness"],
  finish=data["finish"], solder_mask=data["solder_mask"],
  silkscreen=data["silkscreen"],
  width = data["width"], height = data["height"])

        with open(path,"w") as file:
            file.write(content)

def parse_type(layer: dict):
    externs = ["F", "B"]
    if any(x in layer["layer"] for x in externs):
        return "EXTERN"
    return "INTERN"

def parse_side(bool):
    if bool:
        return "TOP"
    return "BOTTTOM"
