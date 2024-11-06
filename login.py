# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:06:11 2022

@author: omer.adiguzel
"""
from selenium.webdriver.common.by import By

import time

class MainWpPage:
    def __init__(self,driver):
        self.driver = driver


    def load(self,url=None):
        if not url:
            self.driver.get("https://web.whatsapp.com/")
        else:
            self.driver.get(url)
        time.sleep(3)
        
    def openedChats(self):

        driver = self.driver
        elements = driver.find_elements(By.CSS_SELECTOR, "#pane-side ._3OvU8")
        return elements
        
   
    def name(self,element):
        return element.find_element(By.CSS_SELECTOR, ".zoWT4").text

   
    def last_message_time(self,element):
        return element.find_element(By.CSS_SELECTOR, "._1i_wG").text

    
    def last_message(self,element):
        return element.find_element(By.CSS_SELECTOR, "._2kHpK ._1582E ._3Whw5").text
   
    
    def notifications(self,element):
        try:
            return int(element.find_element(By.CSS_SELECTOR, "._1pJ9J").text)
        except:
            return 0
    
    def has_notifications(self,element):
        try:
            notifications = int(element.find_element(By.CSS_SELECTOR, "._1pJ9J").text)
            if notifications > 0:
                return True
        except:
            return False
    
    def click(self,element):
        element.click()
        time.sleep(3)
    
        