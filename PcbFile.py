class PcbFile:
  def __init__(self):
    pass

  def write_pcb_file(self, path, data):
    """writes a kicad_pcb file"""


    str = """(kicad_pcb (version 20211014) (generator Gen)
  (general
    (thickness {})
  )

  (paper A4)
  (layers
    (0 F.Cu signal)\n""".format(data['Thickness'])
    
    for layerId in range(1,data["Layers"]-1):
      str+= f"    ({layerId} Inner{layerId}.Cu signal)\n" 

    str +="""    (31 B.Cu signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)"""
    for layer in get_optional_layers(data):
      str+=layer
  
    str+="  )\n"
  
    str+="""
  (setup
    
    (stackup\n"""
  
    str +="      (layer F.Cu (thickness {copper_outer_thickness}))\n".format(copper_outer_thickness=data["copper_outer_thickness"])
    str +="      (layer B.Cu (thickness {copper_outer_thickness}))\n".format(copper_outer_thickness=data["copper_outer_thickness"])

    for dielectric in range(1,data["Layers"]):
      str +="      (layer dielectric{dielectric} (thickness {dielectric_thickness}))\n".format(dielectric = dielectric, dielectric_thickness=data["dielectric_thickness"])
    
    for layer in range(1,data["Layers"]-1):
      str +="      (layer Inner{layer}.Cu (thickness {copper_inner_thickness}))\n".format(layer=layer, copper_inner_thickness=data["copper_inner_thickness"])

    str += """      (layer "F.Paste" (type "Top Solder Paste"))
      (layer "B.Paste" (type "Bottom Solder Paste"))"""

    
    str += get_silkcreen_stackup(data["silkscreen"])

    str+= get_solder_mask_stackup(data["solder_mask"])

    str+="""      (copper_finish "{finish}")
  
    )
    (via_drill {via_drill})
    (via_size {via_size})""".format(via_drill = data["Via_drill_diameter"],
    via_size=data["Via_diameter"], finish=data["finish"])

    if(data["UVias"]):
      str+="""    
      (uvia_size {uvia_size})
      (uvia_drill {uvia_drill_size})""".format(uvia_size = data["uvia_diameter"],
      uvia_drill_size=data["uvia_drill_diameter"])

    str +="""
  )
)"""
    with open(path, "w") as file:
        file.write(str)

def isAllowed(bool):
  """booleans in kicads format"""
  if bool:
    return "yes"
  return "no"

def get_optional_layers(data):
  """returns a list containing optional layers definition"""
  layers = []
  layers.append(get_silkscreen_layers(data["silkscreen"]))
  layers.append(get_solder_mask_layers(data["solder_mask"]))
  return layers


def get_lines(data, line_top, line_bottom):
  """returns kicad_pcb file lines """
  if data == "Both":
    return "\n" + line_top + "\n" + line_bottom + "\n"
  elif data == "Top" :
    return "\n" + line_top + "\n"
  elif data == "Bottom" :
    return "\n" + line_bottom + "\n"
  elif data == "None" :
    return ""
  else :
    return ""

def get_silkscreen_layers(data):
  silkscreen_top = '    (36 "F.SilkS" user "F.Silkscreen")'
  silkscreen_bottom = '    (37 "B.SilkS" user "B.Silkscreen")'

  return get_lines(data, silkscreen_top, silkscreen_bottom)

def get_silkcreen_stackup(data):
  silk_top = '      (layer "F.SilkS" (type "Top Silk Screen"))'
  silk_bottom = '      (layer "B.SilkS" (type "Bottom Silk Screen"))'

  return get_lines(data, silk_top, silk_bottom)

def get_solder_mask_layers(data):
  mask_top = '    (38 "F.Mask" user "F.SolderMask")'
  mask_bottom = '    (37 "B.Mask" user "B.SolderMask")'

  return get_lines(data, mask_top, mask_bottom)

def get_solder_mask_stackup(data):
  mask_top = '      (layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))'
  mask_bottom = '      (layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))'

  return get_lines(data, mask_top, mask_bottom) 