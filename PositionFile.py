from prettytable import PrettyTable
import csv

class PositionFile:
    """to write kicad's position file, in both .csv and .dat formats"""
    def WritePosFile(self, board, path):
        
        footprints = board.GetFootprints()
        footprints.sort(key=lambda ft: ft.GetReference())

        gridOrigin = board.GetDesignSettings().GetAuxOrigin()
        precision = 10**6

        tab = PrettyTable()
        tab.field_names = ["Ref","Value","Package","PosX", "PosY", "Rot","Side"]
        
        with open(path + "Pos.csv" ,"w", newline='') as file:
            wr = csv.writer(file)
            for ft in footprints:
                ref = ft.GetReference()
                value = ft.GetValue()

                pid=ft.GetFPID()
                package =pid.GetUniStringLibItemName()

                posOrigin = ft.GetPosition()
                pos = posOrigin - gridOrigin

                posX = pos[0] / precision
                posY = - pos [1]  / precision

                rotation = ft.GetOrientationDegrees()
                side = "top" if ft.IsFlipped() else "bottom"

                attributs = [ref, value, package, posX, posY, rotation, side]
                tab.add_row(attributs)
                wr.writerow(attributs)
        


        with open(path + "Pos.dat","w") as file:
            file.write(tab.get_string())
        
