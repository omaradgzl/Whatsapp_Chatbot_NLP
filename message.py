# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:20:52 2022

@author: omer.adiguzel
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Messenger:
    
    def __init__(self , driver):
        self.driver = driver
        
    
    def read_last_message(self, who='in', count = 0):
        """
        Reading the last message that you got in from the chatter
        --who parameter takes two , in for recieved messages and out for messages has been sent
        --count parameter is for reading how many messages 
        
        
        """
        message = ""
        messageList = []
        messageNew = ""
                
        for messages in self.driver.find_elements(By.XPATH,
                "//div[contains(@class,'message-{}')]".format(who)):
            try:

                message_container = messages.find_element(By.XPATH,
                    ".//div[@class='copyable-text']")

                message = message_container.find_element(By.XPATH,
                    ".//span[contains(@class,'copyable-text')]"
                ).text
                
                messageList.append(message)
                
            except :  # In case there are only emojis in the message
                    pass

        if count > 1 :
            for i in range(len(messageList)-count,len(messageList)):
                messageNew += messageList[i] + "\n"
            return messageNew
        return message
    
    def send_message(self,text):
            """
            Send a message to the chatter.
            You need to open a conversation 
            before you can use this function.
            """

            input_box = self.driver.find_element(By.XPATH, '//*[@id="main"]//footer//div[contains(@contenteditable, "true")]')
            # input_box.clear()
            input_box.click()
    
            action = ActionChains(self.driver)
            if "\n" in text:
                for part in text.split('\n'):
                    action.send_keys(part)
                    action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
                action.send_keys(Keys.RETURN)
                action.perform()
                return True


            action.send_keys(text)
            action.send_keys(Keys.RETURN)
            action.perform()
            
            return True






