import os
import time

#from abc import ABC,abstractmethod

import selenium.webdriver as webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.common.exceptions import WebDriverException
import urllib.request


class EasySelenium():
    def __init__(self,link:str,headless:bool=False):

        #dir should look like "/the/path/to/current/dir"
        dir=os.path.dirname(__file__)
        
        #init driver
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
        FireFoxDriverPath = os.path.join(os.getcwd(), 'Drivers', os.path.join(dir,'geckodriver'))
        #FireFoxDriverPath = os.path.join(dir,'/geckodriver')
        firefox_service = Service(FireFoxDriverPath)
        firefox_option = Options()
        firefox_option.set_preference("general.useragent.override", user_agent)
        if headless:
            firefox_option.add_argument("--headless")
        self.driver=webdriver.Firefox(service=firefox_service, options=firefox_option)
        self.driver.get(link)

        #store data to self
        self.dir=dir
        self.link=link

    @property
    def defaultImgLoc(self):
        return self.imgLocByTime(self.dir)
    def imgLocByTime(self,loc):
        return os.path.join(loc,os.popen('date +%Y%m%d%H%M%S').read().strip('\n')+".png")
    
    def screenshot(self,imgLoc:str=defaultImgLoc):
        self.setToFullScreen()
        # driver.save_screenshot(path)  # has scrollbar
        time.sleep(5)
        self.driver.find_element('tag name','body').screenshot(imgLoc)  # avoids scrollbar
        self.setToOriginalSize()

    def setToFullScreen(self):
        self.original_size = self.driver.get_window_size()
        required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        time.sleep(1)
        self.driver.set_window_size(required_width, required_height)

    def setToOriginalSize(self):
        self.driver.set_window_size(self.original_size['width'], self.original_size['height'])

    def sendToTheBottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    
    def saveFromSrc(self,elementTypeAndName:list,saveAs:str):
        src=self.driver 
        # elementTypeAndName be like ["class name","imgContainer","css selector",'img']
        # [type,name,type,name,...]
        for i in range(int(len(elementTypeAndName)/2)):
            src=src.find_element(elementTypeAndName[i*2],elementTypeAndName[i*2+1])
        urllib.request.urlretrieve(src.get_attribute('src'),saveAs)
    

    def _keepDoing(self,error,sec:int=1):
        loop=None
        while loop:
            loop=False
            try:
                error
            except WebDriverException:
                loop=True
            except Exception:
                loop=True
            time.sleep(sec)

    #wait until element appear / disappear
    def waitUntilE(self,untilAppear:bool,elementType:str,name:str,sec:int):
        if untilAppear:
            self._keepDoing(self.driver.find_element(elementType,name).is_displayed(),sec)
            #WebDriverWait(self.driver, timeout=86400).until(self.driver.find_element(elementType,name).is_displayed())
        else:
            while self.driver.find_element(elementType,name).is_displayed():
                time.sleep(sec)
    #click element
    def eClick(self,elementType:str,name:str):
        self._keepDoing(self.driver.find_element(elementType,name).click())
    #eClick but better but make sure the element is visible
    def eUltraClick(self,elementType:str,name:str):
        self._keepDoing(ActionChains(self.driver).move_to_element(self.driver.find_element(elementType,name)).click().perform())
        
    #rewrite the text in a element
    def idRewrite(self,id:str,new:str):
        self._keepDoing(self.driver.find_element("id",id).clear())
        self.driver.find_element("id",id).send_keys(new)

    def idSelectDropdown(self,id:str,element:str):
        self.eSelectDropdown("id",id,element)
    def eSelectDropdown(self,elementType:str,name:str,element:str):
        self._keepDoing(Select(self.driver.find_element(elementType,name)).select_by_visible_text(element))

    
    def close(self):
        self.driver.close()

