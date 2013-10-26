

class DataSave:

    delimited = ';'

    #get the whole data from a particular station
    @staticmethod
    def saveStation(obsStation,path,dataVersion):
        myFile = open(path+obsStation['StationName']+'.txt', 'a')
        myFile.write(str(obsStation['Version'])+DataSave.delimited)
        for obsName in dataVersion:
            print obsName+':'+obsStation[obsName]
            myFile.write(str(obsStation[obsName])+DataSave.delimited)
        myFile.write('\n')
        myFile.close()
        return