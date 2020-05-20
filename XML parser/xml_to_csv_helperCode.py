# this helperCode extracts all the XML files in a directory, parses them for the important information and dumps everything into CSV
# this code workes for the XML files located at: "ftp://guest:guest@ted.europa.eu/daily-packages/2019/12/"
# author: amansingh9097

import pandas as pd
import os
import xml.dom.minidom as minidom
import argparse

def parseXMLtoCSV(dirName):
    files = os.listdir(path=dirName)
    df = pd.DataFrame(columns=['fileName', 'nodeName', 'DocID', 'Version', 'URL', 'Title', 'OfficialName', 
                               'NUTScode', 'MainActivity', 'OtherActivity', 'Title_byContractingAuthority', 
                               'ReferenceNum', 'MainCPVcode', 'ContractType', 'shortDescription', 'estimatedTotalValue', 
                               'LOTdivision', 'additionalInfo', 'NoticeDispatchDate', 'ProcedureType', 
                               'ContractDuration', 'LANG'])
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        
    for ix, file in enumerate(listOfFiles):
        doc = minidom.parse(file)
        print('#{} parsing {} file...'.format(ix, file))

        df.loc[ix, 'fileName'] = file.split('/')[-1]
        df.loc[ix, 'nodeName'] = doc.nodeName
        df.loc[ix, 'DocID'] = doc.firstChild.getAttribute('DOC_ID')
        df.loc[ix, 'Version'] = doc.firstChild.getAttribute('VERSION')
        df.loc[ix, 'URL'] = "https://ted.europa.eu/udl?uri=TED:NOTICE:"+doc.firstChild.getAttribute('DOC_ID')+":TEXT:EN:HTML"

        for item in doc.firstChild.getElementsByTagName('ML_TI_DOC'):
            if item.getAttribute('LG') == 'EN':
                title = ""
                for child in item.childNodes:
                    if child.tagName == "TI_CY":
                        title += child.childNodes[0].wholeText + "-"
                    if child.tagName == "TI_TOWN":
                        title += child.childNodes[0].wholeText + ": "
                    if child.tagName == "TI_TEXT":
                        title += child.childNodes[0].childNodes[0].wholeText
        df.loc[ix, 'Title'] = title

        for child in doc.firstChild.getElementsByTagName('ML_AA_NAMES')[0].childNodes:
                if child.getAttribute('LG') == 'EN':
                    df.loc[ix, 'OfficialName'] = child.childNodes[0].wholeText

        lang_list = doc.firstChild.childNodes[0].childNodes[2].childNodes[0].wholeText.split(' ')
        if 'EN' in lang_list:
            EN_pos = lang_list.index('EN')
            df.loc[ix, 'LANG'] = 'EN'
        else:
            EN_pos = 0
            df.loc[ix, 'LANG'] = lang_list[0]
        
        if doc.getElementsByTagName('n2016:NUTS'):
            df.loc[ix, 'NUTScode'] =  doc.getElementsByTagName('n2016:NUTS')[EN_pos].getAttribute('CODE')
        
        if doc.firstChild.getElementsByTagName('MA_MAIN_ACTIVITIES'):
            df.loc[ix, 'MainActivity'] = doc.firstChild.getElementsByTagName('MA_MAIN_ACTIVITIES')[0].childNodes[0].wholeText
        
        if doc.firstChild.getElementsByTagName('CA_ACTIVITY_OTHER'):
            df.loc[ix, 'OtherActivity'] = doc.firstChild.getElementsByTagName('CA_ACTIVITY_OTHER')[EN_pos].childNodes[0].wholeText

        for item in doc.firstChild.getElementsByTagName('ML_TI_DOC'):
            if item.getAttribute('LG') == 'EN':
                title = ""
                for child in item.childNodes:
                    if child.tagName == "TI_CY":
                        title += child.childNodes[0].wholeText + "-"
                    if child.tagName == "TI_TOWN":
                        title += child.childNodes[0].wholeText + ": "
                    if child.tagName == "TI_TEXT":
                        title += child.childNodes[0].childNodes[0].wholeText
        df.loc[ix, 'Title_byContractingAuthority'] = title

        if doc.firstChild.getElementsByTagName('REFERENCE_NUMBER'):
            df.loc[ix, 'ReferenceNum'] = doc.firstChild.getElementsByTagName('REFERENCE_NUMBER')[EN_pos].childNodes[0].wholeText
        
        if doc.firstChild.getElementsByTagName('CPV_MAIN'):
            df.loc[ix, 'MainCPVcode'] = doc.firstChild.getElementsByTagName('CPV_MAIN')[EN_pos].childNodes[0].getAttribute('CODE')
    
        if doc.firstChild.getElementsByTagName('TYPE_CONTRACT'):
            df.loc[ix, 'ContractType'] = doc.firstChild.getElementsByTagName('TYPE_CONTRACT')[EN_pos].getAttribute('CTYPE')

        if doc.firstChild.getElementsByTagName('F01_2014'):
            for element in doc.firstChild.getElementsByTagName('F01_2014'):
                if element.getAttribute('LG')=='EN':
                    
                    df.loc[ix, 'shortDescription'] = element.getElementsByTagName('SHORT_DESCR')[0].childNodes[0].childNodes[0].wholeText
                    
                    if element.getElementsByTagName('INFO_ADD'):
                        tags = element.getElementsByTagName('INFO_ADD')[0]
                        desc = ""
                        for p_tags in tags.childNodes:
                            if p_tags.childNodes:
                                desc += p_tags.childNodes[0].wholeText
                                df.loc[ix, 'additionalInfo'] = desc
                    
                    if element.getElementsByTagName('LOT_DIVISION'):
                        lots = element.getElementsByTagName('LOT_DIVISION')[0]
                        if lots.childNodes:
                            df.loc[ix, 'LOTdivision'] = "".join([ele.childNodes[0].wholeText for ele in lots.childNodes[0].getElementsByTagName('P')])
                        else:
                            lot_description = []
                            while lots.nextSibling.tagName == 'OBJECT_DESCR':
                                for titles in lots.nextSibling.getElementsByTagName('TITLE'):
                                    lot_description.append(titles.childNodes[0].childNodes[0].wholeText)
                                    lots = lots.nextSibling
                            df.loc[ix, 'LOTdivision'] = ",".join(lot_description)
                                           
        elif doc.firstChild.getElementsByTagName('F02_2014'):
            for element in doc.firstChild.getElementsByTagName('F02_2014'):
                if element.getAttribute('LG')=='EN':
                    
                    df.loc[ix, 'shortDescription'] = element.getElementsByTagName('SHORT_DESCR')[0].childNodes[0].childNodes[0].wholeText
                    
                    if element.getElementsByTagName('INFO_ADD'):
                        tags = element.getElementsByTagName('INFO_ADD')[0]
                        desc = ""
                        for p_tags in tags.childNodes:
                            if p_tags.childNodes:
                                desc += p_tags.childNodes[0].wholeText
                                df.loc[ix, 'additionalInfo'] = desc

                    if element.getElementsByTagName('LOT_DIVISION'):
                        lots = element.getElementsByTagName('LOT_DIVISION')[0]
                        if lots.childNodes:
                            df.loc[ix, 'LOTdivision'] = "".join([ele.childNodes[0].wholeText for ele in lots.childNodes[0].getElementsByTagName('P')])
                        else:
                            lot_description = []
                            while lots.nextSibling.tagName == 'OBJECT_DESCR':
                                for titles in lots.nextSibling.getElementsByTagName('TITLE'):
                                    lot_description.append(titles.childNodes[0].childNodes[0].wholeText)
                                    lots = lots.nextSibling
                            df.loc[ix, 'LOTdivision'] = ",".join(lot_description)

        if doc.firstChild.getElementsByTagName('VAL_ESTIMATED_TOTAL'):
            df.loc[ix, 'estimatedTotalValue'] = doc.firstChild.getElementsByTagName('VAL_ESTIMATED_TOTAL')[EN_pos].childNodes[0].wholeText + " " + doc.firstChild.getElementsByTagName('VAL_ESTIMATED_TOTAL')[EN_pos].getAttribute('CURRENCY')

        if doc.firstChild.getElementsByTagName('DATE_DISPATCH_NOTICE'):
            df.loc[ix, 'NoticeDispatchDate'] = doc.firstChild.getElementsByTagName('DATE_DISPATCH_NOTICE')[0].childNodes[0].wholeText

        if doc.firstChild.getElementsByTagName('DURATION'):
            df.loc[ix, 'ContractDuration'] = doc.firstChild.getElementsByTagName('DURATION')[0].childNodes[0].wholeText + " " + doc.firstChild.getElementsByTagName('DURATION')[0].getAttribute('TYPE')

        if doc.firstChild.getElementsByTagName('PR_PROC'):
            df.loc[ix, 'ProcedureType'] = doc.firstChild.getElementsByTagName('PR_PROC')[0].childNodes[0].wholeText
        
        if doc.firstChild.getElementsByTagName('DURATION'):
            df.loc[ix, 'ContractDuration'] = doc.firstChild.getElementsByTagName('DURATION')[0].childNodes[0].wholeText + " months"
        
        if doc.firstChild.getElementsByTagName('MA_MAIN_ACTIVITIES'):
            df.loc[ix, 'MainActivity'] = doc.firstChild.getElementsByTagName('MA_MAIN_ACTIVITIES')[0].childNodes[0].wholeText

    # return df
    save_filename = 'TEDparsed.csv'
    df.to_csv(save_filename, index=False)
