# -*- coding: utf-8 -*-

import subprocess
import wx
import json
import os
import pcbnew
import re
import locale
from datetime import date, datetime
import shutil


##
#GUI lines : 
#import os
#(wx.Bitmap(os.path.join(os.path.dirname(__file__) + "./Pictures/select_path_icon.png"), wx.BITMAP_TYPE_ANY))
##

from . import FabDialog
from . import Hierarchy
from . import ExcelPcbStandards
from . import PcbFile
from . import ProFile
from . import Archive
from . import PositionFile
from . import StackupFile
from . import SchemaFile
from . import StackupReader
from . import LogFile

LAYER_CATEGORY_TOP = "TOP"
LAYER_CATEGORY_BOTTOM = "BOTTOM"
LAYER_CATEGORY_COMMON = "COMMON"
CARD_NUMBER_PATTERN = "K[0-9]+V[0-9]*"

card_number_validator = re.compile(CARD_NUMBER_PATTERN)


def write_kicad_schematic_file(pathToArchive, schData):
    path_to_sch_file = "/Design/{}.kicad_sch".format(schData["fileName"])
    SchemaFile.write_schematic_file(pathToArchive + path_to_sch_file, schData)

def write_library_file(path, lib_name):
    str = """(fp_lib_table
  (lib (name "{name}")(type "KiCad")(uri "${{KIPRJMOD}}/Components/{name}.pretty")(options "")(descr ""))
)""".format(name = lib_name)
    
    with open(path, "w") as file:
        file.write(str)

def navigate(self, page):
    self.Close()
    window = page(None)
    window.Show()

def display_message(message):
    wx.LogMessage(message)

def is_valid_card_number(number):
    if (re.fullmatch(card_number_validator, number)):
       return
    raise Exception("invalid card number format") 

def get_kicad_format_version():
    """get KICADs build date, and formats it to write project files"""
    strDate = pcbnew.GetBuildDate()
    locale.setlocale(locale.LC_ALL, "en_GB")
    date = datetime.strptime(strDate,"%b %d %Y %H:%M:%S")
    version = datetime.strftime(date,"%Y%m%d")
    locale.setlocale(locale.LC_ALL, "")
    return version

def calculate_dielectric_thickness(thickness, copperExtThc, copperInnThc, nbLayer):
    diel = ((thickness) - (2*copperExtThc) - (nbLayer-2)*copperInnThc)/(nbLayer-1)
    return diel

def parse_boolean(string):
    return string == "True"

class HomeLogic(FabDialog.HomeFrame):
    def __init__(self, parent):
        super(HomeLogic, self).__init__(parent)
    
    def nav_hierarchy(self, event):
        window = HierarchyLogic(None)
        self.Close()
        window.Show()
        

    def nav_archiver(self, event):
        window = ArchiveLogic(None)
        self.Close()
        window.Show()

class ArchiveLogic(FabDialog.ArchiveFrame):
    def __init__(self, parent):
        super(ArchiveLogic, self).__init__(parent)
        with open(os.path.join(os.path.dirname(__file__) + "./Utils/UserData.json")) as file: 
            self.user_data = json.load(file)
       
        for key, value in self.user_data.items():
            self.user_data[key] = self.user_data[key].replace("\\","\\\\")

        self.hierarchy_handler = Hierarchy.Hierarchy()
        self.stackup_handler = StackupFile.StackupFile()
        self.stackup_reader = StackupReader.StackupReader_6_0_4()

    def displayProgress(self, percent):
        self.progressBarArchive.SetValue(percent)  

    def toggleProgressBarArchive(self):
        self.pushButtonArchivePcb.Show(not self.pushButtonArchivePcb.IsShown())
        self.progressBarArchive.Show(not self.progressBarArchive.IsShown())
        self.Layout()

    def archive_pcb(self, event):
        """update archive file and generates production files for current board"""
        path = self.lineEditArchiverPath.GetValue()
        board = pcbnew.GetBoard()

        project_path = self.get_project_path(board)
        card_number = os.path.basename(project_path)

        #st = pcbnew.GetSettingsManager()
        #pro = st.Prj()
        #pro.GetProjectPath()

        if not path or path == project_path:
            path = project_path
        else:
            path = path + "/" + os.path.basename(project_path)+ "_Archive"
            shutil.copytree(project_path, path)

        today = date.today()
        formatedDate = today.strftime("%Y%m%d")

        self.toggleProgressBarArchive()
        self.displayProgress(0)

        #update archive file
        self.update_archive_file(card_number, formatedDate) 
        self.displayProgress(5)


        #create drill files
        self.write_drill_files(path, board)
        self.displayProgress(10)

        #create gerber files
        self.write_gerber_files(path, board)
        self.displayProgress(20)

        #create meca file

        self.write_meca_files(board, path)
        self.displayProgress(30)

        #create equipment file
        self.write_equipment_files(board, path)
        self.displayProgress(50)


        #create DRC report
        version = pcbnew.GetBuildVersion()
        release, major, minor = version.split(".")

        if int(major) >0:
            pcbnew.WriteDRCReport(board, path + "/Design/Reports/report.drc",1,True)

        elif(int(minor.replace(")","")) >= 4):
            pcbnew.WriteDRCReport(board, path + "/Design/Reports/report.drc",1,True)



        #create jobFile
        
        #jb = pcbnew.GERBER_JOBFILE_WRITER(board)
        #jb.CreateJobFile(path + "/Design/Reports/jobFile")


        #generates 3D files (.wrl)
        pcbnew.ExportVRML(path + "/Doc/Board/3D.wrl",3,True,True,path + "/Doc/Board", 1.3, 1.2)

        #create report and auto-pos files

        
        pf = pcbnew.PLACE_FILE_EXPORTER(board, True, False, False, True, True, True, True)
        
        rpt = pf.GenReportData()
        pos = pf.GenPositionData()
        
        with open(path + "/Design/Reports/FootprintReport.rpt", "w" ) as file:
            file.write(rpt)
        
        with open(path + "/Fab/Assembly/AutoPos.dat", "w" ) as file:
            file.write(pos)

        self.displayProgress(75)

        #create position file

        posF = PositionFile.PositionFile()
        posF.WritePosFile(board, path + "/Fab/Assembly/")
        self.displayProgress(80)
        

        #creates stackup file
        stackup_data = self.set_stackup_data(board)
        stackup_data.update(self.stackup_reader.read_stackup(board.GetFileName()))

        for i in stackup_data["stackup"].values():
            i["side"] = pcbnew.IsFrontLayer(board.GetLayerID(i["layer"]))
        self.stackup_handler.write_stackup_file(stackup_data, path + "/Fab/PCB/Stackup/stackup.txt")
        self.displayProgress(90)
        
        
        
        #footprints = board.GetFootprints()
        #for footprint in footprints:
        #    pid = footprint.GetFPID()
        #    item = pid.GetLibItemName() -- GetLibNickname()
        
        #generate .pretty library, and updates footprints and symbols to reference said library
        pcbnew.ExportFootprintsToLibrary(True, path + "/Design/Components/" +self.user_data["FOOTPRINT_LIBRARY_NAME"])
        write_library_file(path + "/Design/fp-lib-table", self.user_data["FOOTPRINT_LIBRARY_NAME"])
        self.displayProgress(100)


        schematic_files = [x for x in os.listdir(path + "/Design") if x.endswith(".kicad_sch")]
        project_files = [x for x in os.listdir(path + "/Design") if x.endswith(".kicad_pcb")]
        
        #is there already a library?
        pattern = re.compile('"(.*):(.*)?"')
        

        for file in project_files:
            temp = []
            with open(path + "/Design/" + file) as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("  (footprint"):
                        library = pattern.search(line)
                        if(not library):
                           line = line.replace('  (footprint "', '  (footprint "'+ self.user_data["FOOTPRINT_LIBRARY_NAME"] + ":" )
                        else: 
                            line = re.sub(library.group(1), self.user_data["FOOTPRINT_LIBRARY_NAME"], line)
                    temp.append(line)
        
            with open(path + "/Design/" + file, "w") as f:
                f.writelines(temp)


        for file in schematic_files:
            temp = []
            with open(path + "/Design/" + file) as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("    (property 'Footprint'"):
                        library = pattern.search(line)
                        if(not library):
                           line = line.replace('(property "Footprint" "', '(property "Footprint" "'+ self.user_data["FOOTPRINT_LIBRARY_NAME"] + ":" )
                        else: 
                            line = re.sub(library.group(1), self.user_data["FOOTPRINT_LIBRARY_NAME"], line)
                    temp.append(line)
        
            with open(path + "/Design/" + file, "w") as f:
                f.writelines(temp)

        self.toggleProgressBarArchive()

    def get_project_path(self, board):
        project_path = os.path.dirname(os.path.dirname(board.GetFileName()))
        return project_path

    def dir_picker_path_archiver(self, event):
        msg = "Select the path "
        dlg = wx.DirDialog(None, msg, "", wx.DD_DEFAULT_STYLE )
        dlg.ShowModal()

        selection = dlg.GetPath()
        self.lineEditArchiverPath.SetValue(selection)

    def nav_home(self, event):
        navigate(self, HomeLogic)

    def nav_hierarchy(self, event):
        navigate(self, HierarchyLogic)
          
    def write_drill_files(self, path, board):
        """write drill files"""
        #args :  path, boolean: create .gbr, boolean : create .pdf
        drWriter = pcbnew.GERBER_WRITER(board)
        drWriter.CreateDrillandMapFilesSet(path + "/Fab/PCB/Gerber", False,True)

        exWriter = pcbnew.EXCELLON_WRITER(board)
        exWriter.CreateDrillandMapFilesSet(path + "/Fab/PCB/Gerber", True,False)

    def write_equipment_files(self, board, path):
        """write equipment files
        
        prepare layers IDs to create files
        divides layers in 3 categories : Top only - Bottom only and Common(both)
        makes plotting easier, as files are separated into a Top and a Bottom file"""
        
        equipmentLayers = { 
                            LAYER_CATEGORY_TOP : {"F.Courtyard" : None, "F.Fab" : None},
                            LAYER_CATEGORY_BOTTOM : {"B.Courtyard" : None, "B.Fab" : None},
                            LAYER_CATEGORY_COMMON : {"Edge.Cuts" : None}
                        }

        for category in equipmentLayers.values():
            for layer in category.keys():
                category[layer] = board.GetLayerID(layer)
        
        plotter = pcbnew.PLOT_CONTROLLER(board)
        plotterOpt = plotter.GetPlotOptions()
        plotterOpt.SetOutputDirectory(path + "/Fab/Assembly")
        plotter.OpenPlotfile("Equipment - Top" , pcbnew.PLOT_FORMAT_PDF, "Equipment - Top")
        for category in equipmentLayers.keys():
            if(category != LAYER_CATEGORY_BOTTOM):
                for layer in equipmentLayers[category].values():
                    plotter.SetLayer(layer)
                    plotter.PlotLayer()
        plotter.ClosePlot()


        plotter.OpenPlotfile("Equipment - Bottom" , pcbnew.PLOT_FORMAT_PDF, "Equipment - Bottom")
        for category in equipmentLayers.keys():
            if(category != LAYER_CATEGORY_TOP):
                for layer in equipmentLayers[category].values():
                    plotter.SetLayer(layer)
                    plotter.PlotLayer()
        plotter.ClosePlot()

    def write_gerber_files(self, path, board):
        plotterGerber = pcbnew.PLOT_CONTROLLER(board)
        popt = plotterGerber.GetPlotOptions()
        popt.SetOutputDirectory(path + "/Fab/PCB/Gerber")


        visibleLayersIds = []
        visibleLayers = board.GetEnabledLayers()
        visibleSeq = visibleLayers.Seq()

        for i in range (visibleSeq.size()):
            visibleLayersIds.append(visibleSeq.pop())


        for id in visibleLayersIds:
            if(not "User" in board.GetLayerName(id)):
                plotterGerber.SetLayer(id)
                plotterGerber.OpenPlotfile(board.GetLayerName(id), pcbnew.PLOT_FORMAT_GERBER, board.GetLayerName(id))
                plotterGerber.PlotLayer()

        plotterGerber.ClosePlot()

    def write_meca_files(self, board, path):
        """write meca files
        
        prepare layers IDs to create files
        divides layers in 3 categories : Top only - Bottom only and Common(both)
        makes plotting easier, as files are separated into a Top and a Bottom file"""
        mecaLayers = {  
                        LAYER_CATEGORY_TOP : {"F.Courtyard" : None},
                        LAYER_CATEGORY_BOTTOM : {"B.Courtyard" : None},
                        LAYER_CATEGORY_COMMON : {"User.Drawings" : None, "Edge.Cuts" : None}
                    }
        
        for category in mecaLayers.values():
            for layer in category.keys():
                category[layer] = board.GetLayerID(layer)


        plotter = pcbnew.PLOT_CONTROLLER(board)
        plotterOpt = plotter.GetPlotOptions()
        plotterOpt.SetOutputDirectory(path + "/Doc/Meca")

        ##
        #mecaOpt.SetPlotFrameRef(False)
        #mecaOpt.SetAutoScale(False)
        #mecaOpt.SetScale(1)
        #mecaOpt.SetMirror(False)
        #mecaOpt.SetUseGerberAttributes(False)
        #mecaOpt.SetUseGerberProtelExtensions(True)
        #mecaOpt.SetExcludeEdgeLayer(True)
        #mecaOpt.SetUseAuxOrigin(False)
        #plotterOpt.SetDrillMarksType(pcbnew.PCB_PLOT_PARAMS.FULL_DRILL_SHAPE)
        #mecaOpt.SetSkipPlotNPTH_Pads(True)
        ##
        
             
        #gestion d'erreurs ---- if None in mecaLayers
        #else

        plotter.OpenPlotfile("Meca - Top" , pcbnew.PLOT_FORMAT_PDF, "Meca - Top")
        for category in mecaLayers.keys():
            if(category != LAYER_CATEGORY_BOTTOM):
                for layer in mecaLayers[category].values():
                    plotter.SetLayer(layer)
                    plotter.PlotLayer()

        plotter.ClosePlot()


        plotter.OpenPlotfile("Meca - Bottom" , pcbnew.PLOT_FORMAT_PDF, "Meca - Bottom")
        for category in mecaLayers.keys():
            if(category != LAYER_CATEGORY_TOP):
                for layer in mecaLayers[category].values():
                    plotter.SetLayer(layer)
                    plotter.PlotLayer()

        plotter.ClosePlot()

    def update_archive_file(self, card_number, date):
        archive_file_path = self.user_data["ARCHIVE_FILE_PATH"]
        new_lines =[]
        with open(archive_file_path, 'r+') as file:
            for line in file:
                if line.startswith(self.user_data["CARD_LINE_CHAR"] + card_number):
                    line = line.replace("\n", date + "\n")
                new_lines.append(line)
        with open(archive_file_path, 'w') as file:
            file.writelines(new_lines) 

    def set_stackup_data(self, board):
        precision = 10**3

        data = {
            "date" : date.today().strftime("%d-%m-%Y"),
            "board" : os.path.basename(board.GetFileName()).split(".")[0]
        }

        boardBounds = board.GetBoardEdgesBoundingBox()
        boardWidth = round(boardBounds.GetWidth() / precision) / precision
        boardHeight = round(boardBounds.GetHeight() / precision) / precision
        data["width"] = boardWidth
        data["height"] = boardHeight
        
        return data
        
class HierarchyLogic(FabDialog.HierarchyFrame):
    def __init__(self, parent):
        super(HierarchyLogic, self).__init__(parent)

        with open(os.path.join(os.path.dirname(__file__) + "./Utils/UserData.json")) as file: 
            self.user_data = json.load(file)

        for key, value in self.user_data.items():
            self.user_data[key] = self.user_data[key].replace("\\","\\\\")

        self.EXCEL_PCB_FILE =  self.user_data["PLUGIN_PATH"] + "/Utils/PCB_Class.xlsx"
        self.DEFAULT_PATH = self.user_data["DEFAULT_PATH"]
        
        self.archive_handler = Archive.ArchiveTxt(self.user_data)
        self.pcb_standards_handler = ExcelPcbStandards.ExcelPcbStandards()
        self.hierarchy_handler = Hierarchy.Hierarchy()
        self.pcb_file_handler = PcbFile.PcbFile()
        self.pro_file_handler = ProFile.ProFile()
        self.log_file_handler = LogFile.LogFile(self.user_data)
        self.stackup_handler = StackupFile.StackupFile()

        self.displayInitialPCBInfo()

        self.comboBoxExistingPcb.Append("")

        try:
            for cardname in self.archive_handler.getEveryCardNumber():
                self.comboBoxExistingPcb.Append(cardname)

        except Exception as e:
            wx.LogError(str(e))
    def nav_home(self, event):
        navigate(self, HomeLogic)

    def nav_archiver(self, event):
        navigate(self, ArchiveLogic)

    def toggleProgressBarValidation(self):
        self.buttonValidation.Show(not self.buttonValidation.IsShown())
        self.progressBarValidation.Show(not self.progressBarValidation.IsShown())
        self.Layout()

    def displayProgress(self, percent):
        self.progressBarValidation.SetValue(percent)
    
    def generate_hierarchy(self, event):
        """generates hierarchy, and creates kicad project files"""

        try:
            self.entries_verification()
        except Exception as e:
            wx.LogError("At least 1 field isn't properly filled.\nError message : " + str(e))
            return
            
        
        self.toggleProgressBarValidation()
        self.displayProgress(0)

        # update archive file
        dateFormat = "%Y%m%d"

        cardInfoToArchive =   [   
                            self.lineEditCardNumber.GetValue(),
                            self.editDateCreation.GetValue().Format(dateFormat),
                            self.lineEditProjectName.GetValue(),
                            self.lineEditCardName.GetValue(),
                            self.lineEditClaimer.GetValue(),
                            self.lineEditRouter.GetValue(),
                            self.lineEditCommentary.GetValue(),
                        ]
        other_info = [
                self.checkBoxAllowBuriedVia.IsChecked(),
                self.checkBoxAllowMicroVia.IsChecked(),
                self.comboBoxLayers.GetValue(),
                self.lineEditThickness.GetValue(),
                self.lineEditCopperInnerThickness.GetValue(),
                self.lineEditCopperOuterThickness.GetValue(),
                self.comboBoxFinish.GetValue(),
                self.comboBoxSolderMask.GetValue(),
                self.comboBoxSilkscreen.GetValue()
            ]

        log_info = []
        log_info.extend(cardInfoToArchive)
        log_info.extend(other_info)

        try:            
            cardNum = self.lineEditCardNumber.GetValue()
            if(cardNum in self.archive_handler.getEveryCardNumber()):
                wx.LogError("Card number already taken")
                self.toggleProgressBarValidation()
                return
            self.archive_handler.writeArchiveLine(cardInfoToArchive)
        except Exception as e:
            wx.LogMessage(str(e))
            self.archive_handler.write_temp_archive_file(log_info)

        self.displayProgress(30) 

        
        # create hierarchy 
        
        cardNumber = self.lineEditCardNumber.GetValue()
        path = self.lineEditHierarchyPath.GetValue()

        if (path):
            path += "/" + cardNumber
            self.hierarchy_handler.hierarchyCreation(path)
        else:
            path = self.DEFAULT_PATH + "/" + cardNumber
            self.hierarchy_handler.hierarchyCreation(path)
        
        self.displayProgress(40)

        #write logfile
        self.log_file_handler.write_log_file( log_info, path + "/log.txt" )
        
        #write .kicad_pcb file
        kicadPcbData = self.set_kicad_pcb_data()
        pathToKicadPcb_File = "/Design/{}.kicad_pcb".format(kicadPcbData["fileName"])
        self.pcb_file_handler.write_pcb_file(path + pathToKicadPcb_File, kicadPcbData)
        
        self.displayProgress(70)
        
        #write .kicad_pro file
        kicadProData = self.set_kicad_pro_data()
        path_to_kicad_pro_file = "/Design/{}.kicad_pro".format(kicadProData["fileName"])
        self.pro_file_handler.write_kicad_pro_file(path + path_to_kicad_pro_file, kicadProData)

        #write .kicad_sch file
        kicadSchData = self.set_kicad_schematic_data()
        write_kicad_schematic_file(path, kicadSchData)
       

        self.displayProgress(80)
        
        storage = str(self.comboBoxClassNumber.GetValue()) + "-" +  str(self.comboBoxElectricalTest.GetValue())
        self.stackup_handler.store_data(storage, path + "/Fab/PCB/Stackup/stackup.txt")
        #display error or succes 

        ##runs pcbnew, to let user save .pcb file
        try:
            subprocess.call([os.getcwd() + "/bin/pcbnew.exe", path+ pathToKicadPcb_File])
        except:
            wx.LogError(os.getcwd() + "/6.0/bin/pcbnew.exe" + " --- " + path+ pathToKicadPcb_File )
        #updates .pro file
        
        self.pro_file_handler.update_kicad_pro_file(path + path_to_kicad_pro_file, kicadProData)
        self.toggleProgressBarValidation()

        #end

    def toggle_micro_via(self, event) :        
        self.labelUViaDiameter.Show(not self.labelUViaDiameter.IsShown())
        self.lineEditUViaDiameter.Show(not self.lineEditUViaDiameter.IsShown())

        self.labelUViaDrillDiameter.Show(not self.labelUViaDrillDiameter.IsShown())
        self.lineEditUViaDrillDiameter.Show(not self.lineEditUViaDrillDiameter.IsShown())

        self.Layout()
        
    def selectClassNumber(self, event):
        self.updatePCBInfo()

    def selectDrill(self, event):
        self.updatePCBInfo()
    
    def toggleCustomKicadProData(self, event):

        items = [
                self.lineEditTrackWidth,
                self.lineEditTrackToTrackSpace,
                self.lineEditViaDrillDiameter,
                self.lineEditViaDiameter,
                self.lineEditHoleToHole,
                self.comboBoxClassDrill,
                self.comboBoxClassNumber
                ]
        
        if (event.GetEventObject().IsChecked()):
            for elem in items:
                elem.Enable(not elem.IsEnabled())
                
                
        else:
            for elem in items:
               elem.Enable(not elem.IsEnabled())
            self.updatePCBInfo()

    def displayInitialPCBInfo(self):
        self.comboBoxClassNumber.SetSelection(0)
        self.comboBoxClassDrill.SetSelection(0)
        self.updatePCBInfo()
         
    def updatePCBInfo(self):
        pcb_info = self.pcb_standards_handler.getPCBInfo(self.EXCEL_PCB_FILE, int(self.comboBoxClassNumber.GetStringSelection()), self.comboBoxClassDrill.GetStringSelection())
        self.displayPCBInfo(pcb_info)
    
    def displayPCBInfo(self, pcbInfo):   
        self.lineEditTrackWidth.SetValue(str(pcbInfo[0]))
        self.lineEditTrackToTrackSpace.SetValue(str(pcbInfo[1]))
        self.lineEditViaDrillDiameter.SetValue(str(pcbInfo[2]))
        self.lineEditViaDiameter.SetValue(str(pcbInfo[3]))
        self.lineEditHoleToHole.SetValue(str(pcbInfo[4]))      
        
    def ExistingPcb(self, event):
        self.pushButtonPcbVersionning.Enable(not self.pushButtonPcbVersionning.IsEnabled())
        self.comboBoxExistingPcb.Enable(not self.comboBoxExistingPcb.IsEnabled())
        self.pushButtonLoadPcb.Enable(not self.pushButtonLoadPcb.IsEnabled())

    def AutoPcbNumber(self, event) :
        """displays an automatically generated next card number, from archive file"""
        cardInfo = self.archive_handler.retrieveArchivedCardInfo()
        self.lineEditCardNumber.SetValue(Archive.getNextCardNum(cardInfo["cardNum"]))

    def LoadPcb(self, event):
        """load archived data from a previous pcb, and displays it"""
        number = self.comboBoxExistingPcb.GetStringSelection()
        if(number):
            info = self.archive_handler.retrieveArchivedCardInfo(number)
            self.display_card_info(info)
        
    def PcbVersionning(self, event):
        """sets card number field to a newer version of selectionned card"""
        newVersion = self.get_next_version_number(self.comboBoxExistingPcb.GetStringSelection())
        self.lineEditCardNumber.SetValue(newVersion)

    def get_next_version_number(self, card):
        """ returns incremented version number of a card"""
        tabVers = card.split("V")
        cardNumber = tabVers[0]
        versionNumber =  tabVers[1]

        if (not versionNumber):
            cardNumber +="V2"
            return cardNumber
        else:
            newVersion = int(versionNumber)+1
            cardNumber+= "V" + str(newVersion)
            return cardNumber

    def block_non_numbers(self, event):
        """blocks key entries except numbers, '.' and backspace"""
        key_code = event.GetKeyCode()

        if ord("0") <= key_code <= ord("9"):
            event.Skip()
        elif key_code == ord(".") or key_code == ord("\b") : 
            event.Skip()
        return

    def capitalize_letters(self, event):
        """capitalize letters inputs"""
        keycode = event.GetKeyCode()
        text_ctrl=event.GetEventObject()

        if ord("a") <= keycode <= ord("z"):  
            text_ctrl.AppendText(chr(keycode).upper())
            return
        event.Skip()

    def display_help(self, event):
        message = """ Plugin documentation is disponible within the plugin files
        
        Contact developper : creator@net_c.com"""
        display_message(message)

    def display_about(self, event):
        message = "Creator is a KiCad plugin to automate Projects creation and archiving"
        display_message(message)


    def load_from_file(self, event):
        """load PCB from a temp archive file"""
        dlg = wx.FileDialog(None, "Load Pcb from file", "", "", "", wx.FLP_OPEN | wx.FLP_FILE_MUST_EXIST)
        res = dlg.ShowModal()

        
        if (res == wx.ID_OK):
            filePath = dlg.GetPath()
            try:
                with open(filePath) as file:
                    line = file.readline()
                sep =  self.user_data["CARD_LINE_CHAR"]
                split = line.split(sep)
                card_info = self.archive_handler.decomposeCardInfo(sep.join(split[:8]))
                self.display_card_info(card_info, num=True)

                for i in range(8):
                    split.pop(0)
                self.fill_other_info(split)
            except Exception as e:
                wx.LogError("Unexpected Error during file loading" + str(e))
                #str(e) to display error

    def display_card_info(self, cardInfo:dict, num=False):
        if num:
            self.lineEditCardNumber.SetValue(cardInfo["cardNum"])
        self.lineEditCardName.SetValue(cardInfo["cardName"])
        self.lineEditProjectName.SetValue(cardInfo["projectName"]) 
        self.lineEditClaimer.SetValue(cardInfo["claimerName"]) 
        self.lineEditRouter.SetValue(cardInfo["routerName"])

    def fill_other_info(self, args):
        if parse_boolean(args[0]):
            self.checkBoxAllowBuriedVia.SetValue(True)
            self.checkBoxAllowBuriedVia.GetEventHandler().ProcessEvent(wx.PyCommandEvent(wx.EVT_CHECKBOX.typeId, self.checkBoxAllowBuriedVia.GetId()))
        if parse_boolean(args[1]):
            self.checkBoxAllowMicroVia.SetValue(True)
            self.checkBoxAllowMicroVia.GetEventHandler().ProcessEvent(wx.PyCommandEvent(wx.EVT_CHECKBOX.typeId, self.checkBoxAllowMicroVia.GetId()))
        self.comboBoxLayers.SetValue(args[2])
        self.lineEditThickness.SetValue(args[3])
        self.lineEditCopperInnerThickness.SetValue(args[4])
        self.lineEditCopperOuterThickness.SetValue(args[5])
        self.comboBoxFinish.SetValue(args[6])
        self.comboBoxSolderMask.SetValue(args[7])
        self.comboBoxSilkscreen.SetValue(args[8])

    def char(self, event):
        """blocks every key entry"""
        return
    
    def dir_picker_hierarchy(self, event):
        """creates a dir picker control"""
        msg = "Select a directory"
        dlg = wx.DirDialog(None, msg, "", wx.DD_DEFAULT_STYLE )
        dlg.ShowModal()

        selection = dlg.GetPath()
        self.lineEditHierarchyPath.SetValue(selection)

    def entries_verification(self):
        """checks that mandatory fields are correctly filled"""

        try:
            is_valid_card_number(self.lineEditCardNumber.GetValue())
            try:
                int(self.lineEditTrackWidth.GetValue())
                int(self.lineEditTrackToTrackSpace.GetValue())
                int(self.lineEditViaDrillDiameter.GetValue())
                int(self.lineEditViaDiameter.GetValue())
                int(self.lineEditHoleToHole.GetValue())
            except Exception:
                raise Exception("PCB data must be integers")

            try:
                float(self.lineEditThickness.GetValue())
                float(self.lineEditCopperInnerThickness.GetValue())
                float(self.lineEditCopperOuterThickness.GetValue())
            except Exception:
                raise Exception("Board data must be floating point numbers")

            try:
                if(self.checkBoxAllowMicroVia.IsChecked()):
                    float(self.lineEditUViaDiameter.GetValue())
                    float(self.lineEditUViaDrillDiameter.GetValue())
            except Exception:
                raise Exception("Micro via data must be floating point numbers")

            if not (self.comboBoxFinish.GetValue() and self.comboBoxSolderMask.GetValue()
                 and self.comboBoxSilkscreen.GetValue()):
                    raise Exception("A value within the list must be selected")

        except Exception as e:
            raise Exception(str(e))

    def set_kicad_pcb_data(self):
        """returns data used to write kicad_pcb file"""

        nbLayers= int(self.comboBoxLayers.GetValue())
        thickness = float(self.lineEditThickness.GetValue())
        trackWidth = int(self.lineEditTrackWidth.GetValue())
        trackToTrackSpace = int(self.lineEditTrackToTrackSpace.GetValue())
        viaDrillDiameter = int(self.lineEditViaDrillDiameter.GetValue()) 
        viaDiameter = int(self.lineEditViaDiameter.GetValue())
        holeToHole = int(self.lineEditHoleToHole.GetValue())
        fileName = self.lineEditCardName.GetValue()
        finish = self.comboBoxFinish.GetValue()
        silkscreen = self.comboBoxSilkscreen.GetValue()
        solder_mask = self.comboBoxSolderMask.GetValue()
        allow_micro_vias = self.checkBoxAllowMicroVia.IsChecked()
        copper_inner_thickness = float(self.lineEditCopperInnerThickness.GetValue())
        copper_outer_thickness = float(self.lineEditCopperOuterThickness.GetValue())
        dielectric_thickness = calculate_dielectric_thickness(thickness, copper_outer_thickness, copper_inner_thickness, nbLayers)

        data = {"Layers" : nbLayers, "Thickness" : thickness,
                "Copper_line_width" : trackWidth,
                "Min_Copper_Edge" : trackToTrackSpace,
                "UVias" : allow_micro_vias,
                "Clearance" : trackToTrackSpace,
                "Diff_pair_gap" : trackToTrackSpace,
                "Diff_pair_via_gap" : holeToHole - viaDiameter,
                "Diff_pair_width" : trackWidth,
                "Track_width" : trackWidth,
                "Via_diameter" : viaDiameter,
                "Hole_To_Hole" : holeToHole,
                "Via_drill_diameter" :  viaDrillDiameter,
                "fileName" : fileName,
                "finish" : finish,
                "silkscreen" : silkscreen,
                "solder_mask" : solder_mask,
                "copper_inner_thickness" : copper_inner_thickness,
                "copper_outer_thickness": copper_outer_thickness,
                "dielectric_thickness" : dielectric_thickness
                }
    
        if allow_micro_vias:
            data["uvia_diameter"] = float(self.lineEditUViaDiameter.GetValue())
            data["uvia_drill_diameter"] = float(self.lineEditUViaDrillDiameter.GetValue())
        
        return data

    def set_kicad_pro_data(self):
        """returns data used to write kicad_pro file"""

        file_name = self.lineEditCardName.GetValue()
        track_width = int(self.lineEditTrackWidth.GetValue()) / 10**3
        track_to_track_space = int(self.lineEditTrackToTrackSpace.GetValue()) / 10**3
        via_drill_diameter = int(self.lineEditViaDrillDiameter.GetValue()) / 10**3
        via_diameter = int(self.lineEditViaDiameter.GetValue()) / 10**3
        hole_to_hole = int(self.lineEditHoleToHole.GetValue()) / 10**3
        allow_micro_vias = self.checkBoxAllowMicroVia.IsChecked()
        allow_buried_vias = self.checkBoxAllowBuriedVia.IsChecked()

        data = {
                "fileName":file_name,
                "rules": {
                    "allow_blind_buried_vias": allow_buried_vias,
                    "allow_microvias": allow_micro_vias,
                    "min_clearance": track_to_track_space,
                    "min_track_width": track_width,
                    "min_via_diameter": via_diameter,
                    "min_hole_clearance": hole_to_hole,
                },
                "net_settings": {
                    "classes": [
                        {
                        "clearance": track_to_track_space,
                        "diff_pair_gap": track_to_track_space,
                        "diff_pair_via_gap": hole_to_hole - via_diameter,
                        "diff_pair_width": track_width,
                        "name": "Default",
                        "pcb_color": "rgba(0, 0, 0, 0.000)",
                        "schematic_color": "rgba(0, 0, 0, 0.000)",
                        "track_width": track_width,
                        "via_diameter": via_diameter,
                        "via_drill": via_drill_diameter,
                        }
                    ],
                    "meta": {
                    "version": 2
                    },
                }
        }

        if(allow_micro_vias):
            data["rules"]["min_microvia_diameter"] = float(self.lineEditUViaDiameter.GetValue())
            data["rules"]["min_microvia_drill"] = float(self.lineEditUViaDrillDiameter.GetValue())
        return data

    def set_kicad_schematic_data(self):
        """returns data used to write kicad_sch file"""
        data = {}
        data["fileName"] = self.lineEditCardName.GetValue()
        data["version"] = get_kicad_format_version()
        return data

        
# Action Plugin To be launched by Kicad
class FabAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Creator_Mzn"
        self.category = "Action Plugin"
        self.description = "Generate Archive"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./Pictures/Plugin.png")
        self.show_toolbar_button = True

    def Run(self):
        a = HomeLogic(None)
        a.Show()    

FabAction().register() # For launching from pcbnew