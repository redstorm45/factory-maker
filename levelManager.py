'''

    Copyright 2014 Pierre Cadart


    This file is part of Factory Maker.

    Factory Maker is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Factory Maker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Factory Maker.  If not, see <http://www.gnu.org/licenses/>.


    Description:
        This class will load all the levels found in
        /data wich are valid
'''


import level
import cell.input
import cell.output
import cell.belt
import cell.advancedBelt
import cell.toolCell
import cell.detector

class LevelManager:
    def __init__(self):
        self.levelList = []
    
    def getLevelByNum(self,n):
        for l in self.levelList:
            if l.number == n:
                return l

    def loadLevels(self):
        num = 0
        foundLvl = True
        while foundLvl:
            num += 1
            loaded = None
            self.specialSpawns = 0
            try:
                #openning file
                l = open("data/"+str(num)+".level","r")

                #reading basic info (name and size)
                name = l.readline().strip()
                size = l.readline().strip().split(",")

                width = int(size[0])
                height = int(size[1])

                #reading each predefined cell
                table = [["n" for y in range(height)] for x in range(width)]
                
                for y in range(height):
                    for x in range(width):
                        readC = l.readline().strip()
                        table[x][y] = self.readCell(readC)
                        if table[x][y]:
                            table[x][y].placed = False

                #reading input config
                inputConfigs = []
                if self.specialSpawns>0:
                    for i in range(self.specialSpawns):
                        readC = l.readline().strip()
                        inputConfigs.append( self.readInConfig( readC ) )

                #reading objectives
                nbObj = int(l.readline().strip())
                objectives = []
                for i in range(nbObj):
                    readC = l.readline().strip()
                    objectives.append( self.readObjective(readC,table) )
                
                #reading tools
                nbTools = int(l.readline().strip())
                listTools = []
                for i in range(nbTools):
                    readC = l.readline().strip()
                    listTools.append( self.readTool(readC) )
                    
                l.close()

                #create level
                loaded = level.Level(num,name,table,inputConfigs,objectives,listTools)

            except Exception as e:
                print(str(e)) #debugging
                foundLvl = False
                num -= 1
            else:
                self.levelList.append(loaded)
        self.levelNb = num

    def readCell(self,data):
        try:
            if data == "n":
                return None
            elif data[0:2] == "in":
                opt = data[3:].strip(")").split(",")
                c = cell.input.Input(opt)
                if not c.standardSpawn:
                    self.specialSpawns += 1
                return c
            elif data[0:3] == "out":
                opt = data[4:].strip(")").split(",")
                return cell.output.Output(opt)
        except Exception as e:
            print(str(e)) #debugging
        print("invalid : "+data)#debugging only
        return None

    def readTool(self,data):
        dList = data.split("x",1)
        toolObject = None
        try:
            if dList[1][0:2] == "in":
                opt = dList[1][3:].strip(")").split(",")
                toolObject = cell.input.Input(opt)
            elif dList[1][0:3] == "out":
                opt = dList[1][4:].strip(")").split(",")
                toolObject = cell.output.Output(opt)
            elif dList[1][0:4] == "belt":
                opt = dList[1][5:].strip(")").split(",")
                toolObject = cell.belt.Belt(opt)
            elif dList[1][0:7] == "advbelt":
                opt = dList[1][8:].strip(")").split(",")
                toolObject = cell.advancedBelt.AdvancedBelt(opt)
            elif dList[1][0:6] == "detect":
                opt = dList[1][7:].strip(")").split(",")
                toolObject = cell.detector.Detector(opt)
        except Exception as e:
            print(str(e)) #debugging
        else:
            dataList = [ int(dList[0]) , toolObject ]
            return cell.toolCell.ToolCell(dataList)
        return None
        
    def readInConfig(self,data):
        listData = data.split("]",1)
        colors = listData[0][1:].split(",") #list of possible colors
        distrib = {}
        if listData[1][0] == "r":    #random creation
            distrib["type"] = "random"
            probs = listData[1].strip("r[").rstrip("]").split(",")
            distrib["proba"] = [ float(i) for i in probs ]
        return { "colors" : colors , "distrib" : distrib }

    def readObjective(self,data,table):
        listData = data.split(".",1)
        obj = [ self.findOutputCoord(int(listData[0]),table) , int(listData[1]) ]
        return obj
    
    def findOutputCoord(self,outputNum,table):
        for x in range(len(table)):
            for y in range(len(table[0])):
                if table[x][y]:
                    if isinstance(table[x][y],cell.output.Output):
                        if table[x][y].id == outputNum:
                            return (x,y)
                













        
