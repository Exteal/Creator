from abc import ABC, abstractmethod


def get_substring_inbetween(string: str, str_start: str, str_end: str):
    """return the part between 2 substrings in a string
    substring can be a single char

    @param string : the string
    @param str_start : the start substring
    @param str_end : the end substring"""
    return string.partition(str_start)[2].partition(str_end)[0]


def is_top_layer(layer):
    """return True if this layer is a Top Layer, False otherwise"""
    return "Top" in layer


class StackupReader(ABC):
    """Since some KiCad SWIG object are automatically generated,
    the best actual way to get stackup data is to directly read the .kicad_pcb file

    This abstract class implements an algorithm that reads and retrieve stackup information,
    inherit this class if KiCad's pcb file structure changes"""

    def __init__(self):
        pass

    def read_stackup(self, path):
        """Reads a .kicad_pcb file and returns data needed to write stackup file"""

        with open(path) as file:
            lines = file.readlines()
            board_thickness = self.get_board_thickness(lines)

            board_stackup = self.get_stackup(lines)
            stack = []
            silk_screen_layers = []
            solder_mask_layers = []

            for line in board_stackup:
                if self.is_layer(line):
                    if self.is_thick_layer(line):
                        stack.append(self.separate(line))
                        if self.is_solder_mask_layer(line):
                            solder_mask_layers.append(line)
                    elif self.is_silk_screen_layer(line):
                        silk_screen_layers.append(line)
                if self.is_copper_finish_line(line):
                    finish = self.get_copper_finish(line)

            stackup = {}

            for idx, layer in enumerate(stack):
                stackup[str(idx)] = {}
                for cat in layer:
                    cat = cat.replace("\"", "")
                    split = cat.split(" ", 1)
                    stackup[str(idx)][split[0]] = split[1].strip()

            data = {
                "stackup": stackup,
                "finish": finish,
                "board_thickness": board_thickness,
                "silkscreen": self.get_stackup_presence(silk_screen_layers),
                "solder_mask": self.get_stackup_presence(solder_mask_layers),
            }

            return data

    def get_stackup_presence(self, layers):
        """Used to determine the sides that contain silkscreen and solder mask

        @param layers : the list of layers"""
        if len(layers) == 2:
            return "Both"
        elif len(layers) == 1:
            if is_top_layer(layers[0]):
                return "Top"
            else:
                return "Bottom"
        else:
            return "None"

    @abstractmethod
    def separate(self, line):
        pass

    @abstractmethod
    def is_copper_finish_line(self):
        pass

    @abstractmethod
    def is_solder_mask_layer(self):
        pass

    @abstractmethod
    def is_silk_screen_layer(self):
        pass

    @abstractmethod
    def is_thick_layer(self):
        pass

    @abstractmethod
    def get_copper_finish(self):
        pass

    @abstractmethod
    def get_stackup(self):
        pass

    @abstractmethod
    def is_layer(self, line):
        pass

    @abstractmethod
    def get_board_thickness(self, lines):
        pass


class StackupReader_6_0_4(StackupReader):
    """The KiCad 6.0.4 (28/06/22) implementation of StackupReader class"""

    def __init__(self):
        super().__init__()

    def separate(self, line: str):
        """separates properties of a layer in a list

        @param line : the layer line taken from the file
        @return tab : a list of properties (names + values)"""
        tab = []
        index = line.find("(")
        index += 1
        current = ""

        for char in line[index:]:
            if char != ")" and char != "(":
                current += char
                index += 1
            else:
                if char == "(":
                    if current:
                        tab.append(current)
                        current = ""
                else:
                    if current:
                        tab.append(current)
                        current = ""

        for idx, string in enumerate(tab):
            if not string.strip():
                tab.pop(idx)

        return tab

    def is_general_board_line(self, line):
        return "  (general" in line

    def is_thickness_line(self, line):
        return "    (thickness" in line

    def get_board_thickness(self, lines):
        thickness = None
        for idx, line in enumerate(lines):
            j = 1
            if self.is_general_board_line(line):
                while not lines[idx + j].startswith("  )"):
                    if self.is_thickness_line(lines[idx + j]):
                        thickness = self.get_thickness(lines[idx + j])
                        break
                    j = j + 1
        return float(thickness)

    def get_stackup(self, lines):
        stackup = []
        for idx, line in enumerate(lines):
            if line.startswith("    (stackup"):
                j = 1
                while not lines[idx + j].startswith("    )"):
                    stackup.append(lines[idx + j])
                    j = j + 1
        return stackup

    def is_thick_layer(self, layer: str):
        return not ("Silk" in layer or "Paste" in layer)

    def is_copper_finish_line(self, line: str):
        return "(copper_finish " in line

    def get_copper_finish(self, line: str):
        return get_substring_inbetween(line, "\"", "\"")

    def is_layer(self, line):
        return "(layer " in line

    def is_silk_screen_layer(self, line):
        return "Silk" in line

    def is_solder_mask_layer(self, line):
        return "Mask" in line

    def get_thickness(self, layer):
        return get_substring_inbetween(layer, "thickness ", ")")