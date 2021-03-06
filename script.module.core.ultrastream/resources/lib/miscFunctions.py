# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 24 Jan 2016

@author: Seko
@summary: Miscellaneous functions

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmc
import os
import urlresolver
import downloaderModule
import strUtil
import kodiUtil
import constant
from unshortenurl import UnshortenUrl
from item import StreamItem

# ____________________     V A R I A B L E S     ____________________


# ____________________     F U N C T I O N S       ____________________

def downloadFile(streamItem,playAtEnd):
    """
        Method to download a file
        @param streamItem : the streamItem
    """
    constant.__LOGGER__.log('Download file :'+streamItem.getPlayingFile()+' to '+constant.__addon__.getSetting('dlfolder').decode('utf-8'))
        
    # ___ Get the filename from the url
    fileName = streamItem.getPlayingFile()
    xbmc.log("Url : "+streamItem.getPlayableUrl())   
    xbmc.log("FileName :"+streamItem.getPlayingFile())
    
    # ___ Init the downloader    
    dlMod = downloaderModule.getDownloadModule(constant.__addon__.getSetting('downloader_module'));
    
    params = {
             'fileName' : fileName.decode('utf-8'),
             'url': streamItem.getPlayableUrl().decode('utf-8'),
             'title':streamItem.getPlayingFile().decode('utf-8'),
             'destinationFolder':constant.__addon__.getSetting('dlfolder').decode('utf-8'),
             'webBrowserId': constant.__addon__.getSetting('android_web_browser').decode('utf-8'),
             'incomplete_path': constant.__addon__.getSetting('advdl_temp_dir').decode('utf-8'),
             'myjd_mail': constant.__addon__.getSetting('myjd_mail').decode('utf-8'),
             'myjd_pwd': constant.__addon__.getSetting('myjd_pwd').decode('utf-8'),
             'myjd_device': constant.__addon__.getSetting('myjd_device').decode('utf-8'),
             'playAtEnd' : str(playAtEnd).decode('utf-8')
             }
    
    dlMod.download(fileName,params);

def displayStreamItem(listStreamItems,urlParams=False):
    """
        Method to display a list of StreamItem
    """
    kodiUtil.beginContentDirectory(content='movies')
    
    if listStreamItems is not None and len(listStreamItems) > 0:
        for item in listStreamItems:
            item.addListItemToDirectory()
        
    kodiUtil.endOfDirectory()


    
def displayNotification(message, type='error'):
    """
        Method to display a notification
        @param message : the message to display
        @param type : the type of notification (er
    """
    xbmc.executebuiltin('Notification(\'UltraStream\','+message+',2000,'+type+')')                       
    constant.__LOGGER__.log(message, xbmc.LOGINFO)


def readSettingsTemplate():
    """
        Method to read the settings template
    """
    templateFilePath = os.path.join( constant.__addonDir__, 'resources', 'settings_tpl.xml')                      
    templateFile = open(templateFilePath,'r')
    result = templateFile.read()

    return result

def writeSettingsFile(settingsTxt,serviceSettingsTxt):
    """
        Method to write the settings file
    """
    settingsFilePath = os.path.join( constant.__addonDir__, 'resources', 'settings.xml')                      
    
    xmlTxt = readSettingsTemplate()
    #xmlTxt += sources.getSourcesXmlSettings()
    xmlTxt += serviceSettingsTxt
    xmlTxt += "    </category>\n      <category label=\"52000\">"
    xmlTxt += settingsTxt
    xmlTxt += "    </category>\n</settings>"
    try:
        with open(settingsFilePath, 'w') as f:
            f.write(xmlTxt)
        constant.__LOGGER__.log("Settings file created/updated.")
    except:
        raise

def filterLinksList(listItems):
    """
        Method to filter a links list, depends on settings
        @param listItems: the list of links
        @return the filtered links list
    """
    filteredList = []
    
    if constant.__addon__.getSetting('filter_screener_link') == 'true':
        for item in listItems:
            if not strUtil.isCAMQuality(item.getQuality()):
                filteredList.append(item)
    else:
        filteredList = listItems
    
    return filteredList