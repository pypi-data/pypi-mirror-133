# -*- coding = UTF-8 -*-
# Author   : buxiubuzhi
# Project  : lazyTest
# FileName : config.py
# Describe :
# ---------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lazyTest

locator = {
    'i': By.ID,
    'id': By.ID,
    'n': By.NAME,
    'name': By.NAME,
    'c': By.CLASS_NAME,
    'class': By.CLASS_NAME,
    'x': By.XPATH,
    'xpath': By.XPATH,
    's': By.CSS_SELECTOR,
    'css': By.CSS_SELECTOR,
    't': By.TAG_NAME,
    'tag_name': By.TAG_NAME,
    'l': By.LINK_TEXT,
    "link_text": By.LINK_TEXT,
    'pl': By.PARTIAL_LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'xc': By.XPATH,
    'xi': By.XPATH,
}

Dirver = {
    "Chrome": webdriver.Chrome,
    "Firefox": webdriver.Firefox,
    "Edge": webdriver.Edge,
    "ChromeOptions": webdriver.ChromeOptions,
}


# 对动态class和动态id的处理
def OPtionElements(by, value):
    if by == 'xc':
        value = '//*[contains(@class,"{}")]'.format(value)
        return value
    if by == 'xi':
        value = '//*[contains(@id,"{}")]'.format(value)
        return value
    return value


class Config:

    def __init__(self, Browser_type: str, url: str) -> None:
        """
        初始化浏览器，并输入地址
        :param Browser_type: 浏览器类型
        :param url: 需要打开的网址
        """
        lazyTest.logger.debug(f"Browser_type:{Browser_type}\turl:{url}")
        self.baseDriver = Dirver[Browser_type]()
        self.implicitlyWait(10)
        self.baseUrl = url
        self.baseDriver.get(url)
        self.baseDriver.maximize_window()

    def implicitlyWait(self, s: int) -> None:
        """
        隐式等待
        :param s: 休眠时间，单位：秒
        :return:
        """
        lazyTest.logger.success(f"implicitly_wait：{s} s")
        self.baseDriver.implicitly_wait(s)

    def webdriver_wait(self, selector: str) -> None:
        """显示等待元素"""
        lazyTest.logger.success(f"webdriver_wait  presence_of_element_located")
        locator = self.__locate_Element_selector(selector)
        WebDriverWait(self.baseDriver, 10, 0.5).until(
            EC.presence_of_element_located(locator))

    def __locate_Element_selector(self, selector: str) -> tuple:
        """
        八种定位方式选择
        :param selector: 传入的格式必须为：定位方式，定位元素值，顺序不可改变
        :return: 返回定位方式
        """
        selector_by = selector.split(',')[0].strip()
        selector_value = selector.split(',',1)[1].strip()
        lazyTest.logger.success(f"__locate_Element_selector:{locator[selector_by]},{selector_value}")
        selector_value = OPtionElements(selector_by, selector_value)
        return locator[selector_by], selector_value

    def locate_element(self, selector: str) -> WebElement:
        """
        定位单个元素
        :param selector: 定位元素的方式和定位元素的值
        :return: 返回定位元素对象
        """
        self.webdriver_wait(selector)
        if selector.find(":") == -1:
            locator = self.__locate_Element_selector(selector)
            element = self.baseDriver.find_element(*locator)
            return element
        else:
            start = selector.split(":")[0]
            condition = selector.split(":")[1]
            locator = self.__locate_Element_selector(start)
            elements = self.baseDriver.find_elements(*locator)
            try:
               i =  int(condition)
               return elements[i]
            except ValueError as e:
                lazyTest.logger.debug(f"condition valueError {e}")
                for ele in elements:
                    if ele.text == condition:
                        return ele
                else:
                    return elements[0]


    def locate_elements(self, selector: str) -> list:
        """
        定位一组元素值
        :param selector: 定位元素的方式和定位元素的值
        :return:
        """
        locator = self.__locate_Element_selector(selector)
        elements = self.baseDriver.find_elements(*locator)
        return elements
