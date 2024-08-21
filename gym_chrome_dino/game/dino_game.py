#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Elvis Yu-Jing Lin <elvisyjlin@gmail.com>
# Licensed under the MIT License - https://opensource.org/licenses/MIT

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time



from gym_chrome_dino.utils.helpers import download_chromedriver

class DinoGame():
    def __init__(self, render=False, accelerate=False, autoscale=False):
        if not os.path.exists('chromedriver') and not os.path.exists('chromedriver.exe'):
            download_chromedriver()
        
        options = Options()
        options.add_argument('--disable-infobars')
        options.add_argument('--mute-audio')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=800,600')
        if not render:
            options.add_argument('--headless')
        
        # Initialize WebDriver without specifying executable_path
        self.driver = webdriver.Chrome(options=options)
        # self.driver.get('chrome://dino')
        self.driver.get('https://elvisyjlin.github.io/t-rex-runner/')
        self.defaults = self.get_parameters()  # default parameters
        if not accelerate:
            self.set_parameter('config.ACCELERATION', 0)
        if not autoscale:
            self.driver.execute_script('Runner.instance_.setArcadeModeContainerScale = function(){};')
        self.press_space()
        
    def get_parameters(self):
        params = {}
        params['config.ACCELERATION'] = self.driver.execute_script('return Runner.config.ACCELERATION;')
        return params
    
    def is_crashed(self):
        return self.driver.execute_script('return Runner.instance_.crashed;')
    
    def is_inverted(self):
        return self.driver.execute_script('return Runner.instance_.inverted;')
    
    def is_paused(self):
        return self.driver.execute_script('return Runner.instance_.paused;')
    
    def is_playing(self):
        return self.driver.execute_script('return Runner.instance_.playing;')
    
    def press_space(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SPACE)
    
    def press_up(self):
        return self.driver.find_element_by_tag_name('body').send_keys(Keys.UP)
    
    def press_down(self):
        return self.driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
    
    def pause(self):
        return self.driver.execute_script('Runner.instance_.stop();')
    
    def resume(self):
        return self.driver.execute_script('Runner.instance_.play();')
    
    def restart(self):
        return self.driver.execute_script('Runner.instance_.restart();')
    
    def close(self):
        self.driver.close()
    
    def get_score(self):
        digits = self.driver.execute_script('return Runner.instance_.distanceMeter.digits;')
        return int(''.join(digits))
    
    def get_canvas(self):
        return self.driver.execute_script('return document.getElementsByClassName("runner-canvas")[0].toDataURL().substring(22);')
    
    def set_parameter(self, key, value):
        self.driver.execute_script('Runner.{} = {};'.format(key, value))
    
    def restore_parameter(self, key):
        self.set_parameter(key, self.defaults[key])
