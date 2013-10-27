import datetime

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
        
    @staticmethod
    def saveSummary(path,dataVersion,okStations,skippedStations):
        myFile = open(path+'summary.txt', 'a')
        time =  str(datetime.datetime.now())[:-7]
        myFile.write(time+'\n')
        myFile.write('OkStations : ')
        for ok in okStations:
            myFile.write(ok+';')
        myFile.write('\nSkipped : ')
        for skipped in skippedStations:
            myFile.write(skipped+';')
        myFile.write('\n')
        myFile.close()
        return