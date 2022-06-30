import re
import fileinput
import os
from abc import ABC, abstractmethod

HAS_VERSION_PATTERN = "K[0-9]+V[0-9]+"

hasVersion = re.compile(HAS_VERSION_PATTERN)

def get_int_from_card_number(cardNumber:str):
    while(re.fullmatch(hasVersion, cardNumber)):
        cardNumber = cardNumber[:-1]

    cardNumber = cardNumber.replace("K","")
    cardNumber = cardNumber.replace("V","")

    return int(cardNumber)

def card_number_is_lower_than(myCard, otherCard):
    """returns True if the first card number is lower than the second
    returns False otherwise """
    return get_int_from_card_number(myCard) < get_int_from_card_number(otherCard)

def getNextCardNum(cardNum):
        #if version number, removes it
        if re.search("V\d+",cardNum):
            cardNum = cardNum.split("V")[0] + "V"

        lastNum = re.sub('[^0-9]','', cardNum)
        newNum = int(lastNum)+1
        newCardNum = cardNum.replace(str(lastNum), str(newNum))
        return newCardNum

def getPreviousVersionCardNum(cardNum):
    version = cardNum.split("V")[1]
    newVersion = int(version)-1
    newCardNum = cardNum.replace(str(version), str(newVersion))
    return newCardNum

class Archive(ABC):
    """abstract class to handle different PCB archiving methods"""
    
    @abstractmethod
    def getEveryCardNumber(self):
        pass
 
    @abstractmethod
    def getCardNumberFromCardLine(self, cardLine):
        pass

    @abstractmethod
    def decomposeCardInfo(self, cardLine):
        pass

    @abstractmethod
    def writeArchiveLine(self, args, archiveDate = None):
        pass

    @abstractmethod
    def retrieveArchivedCardInfo(self, cardnumber = None):
        pass

    
class ArchiveTxt(Archive):
    """archive method currently used : a .txt file"""
    def __init__(self, user_data):
        """@param : user_data -> dictionnary containing user-defined data, such as:
        archive_file_path, temp_archive_file_path, card_line_separator..."""
        self.user_data = user_data
        
    def getEveryCardNumber(self):
        nbrs = []
        with open(self.user_data["ARCHIVE_FILE_PATH"],"r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(self.user_data["CARD_LINE_CHAR"]):
                        cardInfo = self.decomposeCardInfo(line)
                        nbrs.append(cardInfo["cardNum"])
        return nbrs

    def manage_file(self, file):
        """manages white spaces, white lines, line breaks in excess"""

        self.deleteWhiteLines(file)
        if not self.last_line(file).endswith("\n"):
            with open(file, "a") as f:
                f.write("\n")
    
    def last_line(self, file):
        """return the last line of a file"""
        with open(file, "rb") as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            return f.readline().decode()

    def deleteWhiteLines(self, file):
            """deletes white spaces and white lines in archive file"""
            with open(file) as f:
                lines = f.readlines()
                
            with open(file,"w") as f:
                for line in reversed(lines):
                    if(not line.strip()):
                        lines.pop()
                    else:
                        break
                f.writelines(lines)

    def getCardNumberFromCardLine(self, cardLine:str):
        return cardLine.split(self.user_data["CARD_LINE_CHAR"])[1]

    def decomposeCardInfo(self, cardLine:str):
        values = [elem for elem in cardLine.split(self.user_data["CARD_LINE_CHAR"]) if elem != ""] 
        keys = ["cardNum", "dateCreation", "projectName", "cardName",
                "claimerName", "routerName", "commentary", "dateArchive" ]
        res = dict(zip(keys,values))
        return res 

    def write_temp_archive_file(self, args):
        lineToArchive = self.user_data["CARD_LINE_CHAR"] + self.user_data["CARD_LINE_CHAR"].join(str(arg) for arg in args) + self.user_data["CARD_LINE_CHAR"]
        with open(self.user_data["TEMP_ARCHIVE_FILE"],"w") as file:
            file.write(lineToArchive + "\n")

    def writeArchiveLine(self, args:list):
        try:
            self.manage_file(self.user_data["ARCHIVE_FILE_PATH"])

            cardNumber = args[0]
            lineToArchive = self.user_data["CARD_LINE_CHAR"] + self.user_data["CARD_LINE_CHAR"].join(args) + self.user_data["CARD_LINE_CHAR"]

            if (re.search("V\d+", cardNumber)):
                
                cardNumberVersionless, versionNumber = cardNumber.split("V")
                cardNumberVersionless += "V"
                
                if int(versionNumber) == 2:
                    for line in fileinput.FileInput(self.user_data["ARCHIVE_FILE_PATH"],inplace=1):
                        if(line.startswith(self.user_data["CARD_LINE_CHAR"]) and cardNumberVersionless == self.getCardNumberFromCardLine(line)):
                            line=line.replace(line,line+lineToArchive +"\n")
                        print(line,end='')

                elif int(versionNumber) > 2:
                    for line in fileinput.FileInput(self.user_data["ARCHIVE_FILE_PATH"],inplace=1):
                        if (line.startswith(self.user_data["CARD_LINE_CHAR"]) and
                            getPreviousVersionCardNum(cardNumber) == self.getCardNumberFromCardLine(line)):
                            line=line.replace(line,line+lineToArchive +"\n")
                        print(line,end='')
                    
            else:
                breaks = False
                for line in fileinput.FileInput(self.user_data["ARCHIVE_FILE_PATH"],inplace=1):
                    if(not breaks and line.startswith(self.user_data["CARD_LINE_CHAR"])
                    and  card_number_is_lower_than(cardNumber, self.getCardNumberFromCardLine(line))):
                        line=line.replace(line,lineToArchive +"\n"+line)
                        breaks = True
                    print(line,end='')          
                else:
                    if (not breaks):
                        with open(self.user_data["ARCHIVE_FILE_PATH"],"a") as file:
                            file.write(lineToArchive + "\n")

        except Exception as e:
            raise Exception("Failed to open archive file, writing into a temp file ")
            #str(e) to display error in KiCad

    def retrieveArchivedCardInfo(self, cardnumber = None):
        with open(self.user_data["ARCHIVE_FILE_PATH"],"r") as file:
            lines = file.readlines()
            if cardnumber == None:
                for line in reversed(lines):
                    if line.startswith(self.user_data["CARD_LINE_CHAR"]):
                        
                        ##depends on the way of stocking card information...
                        ##... in Nmr_Cartes.txt file
                        
                        cardInfo = self.decomposeCardInfo(line)
                        
                        ##
                        ########################################
                        
                        return cardInfo     
                raise Exception("no card archived")
            else:
                for line in lines:
                    if  line.startswith(self.user_data["CARD_LINE_CHAR"]) and self.getCardNumberFromCardLine(line) == cardnumber:
                        cardInfo = self.decomposeCardInfo(line)
                        return cardInfo    
                raise Exception("card not archived")

