class DataParse:
    #methods used to load data from ronma
    @staticmethod
    def ParseCut(contentToParse,refCaracter,numCaracToCut):
        result = contentToParse.get_text()
        index = result.index(refCaracter)
        result = result[:index-numCaracToCut]
        return result
        
    @staticmethod    
    def ParseTrunk(contentToParse,numToTrunk):
        result = contentToParse.get_text()
        result = result[:-numToTrunk]
        return result
        
    @staticmethod    
    def ParseHour(contentToParse):
        return contentToParse[4 if contentToParse[3]==' ' else 3:]
     
    @staticmethod    
    def convertDate(txtToParse):
        day = txtToParse[30:32]
        month = txtToParse[33:37].upper()
        yearIndex = txtToParse[37:].index('2')
        year = txtToParse[37+yearIndex:41+yearIndex]
        if (month=='JANV'):
            return day+'/01/'+year
        elif (month == 'FEVR'):
            return day+'/01/'+year
        elif (month == 'MARS'):
            return day+'/03/'+year
        elif (month == 'AVRI'):
            return day+'/04/'+year
        elif (month == 'MAI '):
            return day+'/05/'+year
        elif (month == 'JUIN'):
            return day+'/06/'+year
        elif (month == 'JUIL'):
            return day+'/07/'+year
        elif (month == 'AOUT'):
            return day+'/08/'+year
        elif (month == 'SEPT'):
            return day+'/09/'+year
        elif (month == 'OCTO'):
            return day+'/10/'+year
        elif (month == 'NOVE'):
            return day+'/11/'+year
        elif (month == 'DECE'):
            return day+'/12/'+year
        else: 
            print 'couldnt read month'
            return