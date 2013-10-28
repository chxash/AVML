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
        myFile = open(path+'log/summary.txt', 'a')
        time =  str(datetime.datetime.now())[:-7]
        myFile.write('=====================================================')
        myFile.write(time+'\n')
        myFile.write('OkStations\n')
        for ok in okStations:
            print ok
            myFile.write(ok+'\n')
        myFile.write('\nSkipped\n')
        for skipped in skippedStations:
            print skipped
            myFile.write(skipped+'\n')
        myFile.write('\n')
        myFile.close()
        return
