# -*- coding: utf-8 -*-
import os
import cv2
import time
import numpy as np
import urllib.error
import urllib.request
import chromedriver_binary
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse, quote
from selenium.webdriver.chrome.options import Options

class Scraper():
    def __init__(self, target_url, dst_path):
        self.target_url = quote(target_url, safe="/:")
        self.base_url = quote('{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(target_url)), safe="/:")
        self.dst_path = dst_path

    def scraping(self):
        # selenium設定
        options = Options()
        options.set_headless(True)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(self.target_url)

        #ページのhtml取得
        html = self.__get_html(driver)
        print("----- ページを取得できました！ -----")

        #画像URLを取得
        soup = BeautifulSoup(html, "html.parser")
        imgs = soup.findAll('img', class_="maid-item__photo")

        #画像を保存
        count = 0
        for img in imgs:
            url = img.get("src")
            if url[0:5] == "https":
                url_full = url
            else:
                url_full = self.base_url+url
            print("画像URL : "+url_full)
            file_path = self.__download_img(url_full)

            #画像を200x200にリサイズ
            self.__resize_img(file_path)

    def __get_html(self, driver):
        html = driver.page_source.encode('utf-8')
        while 1:
            print("----- スクロール中 -----")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            html_tmp = driver.page_source.encode('utf-8')
            if html != html_tmp:
                html = html_tmp
            else:
                break
        return html

    def __download_img(self, url):
        try:
            with urllib.request.urlopen(quote(url, safe=":/")) as web_file:
                data = web_file.read()
                file_name = url.split("/")[-1]
                file_path = self.dst_path+"/"+file_name
                with open(file_path, mode='wb') as local_file:
                    local_file.write(data)
                print("ファイルを保存しました : "+file_name)
                return file_path
        except urllib.error.URLError as e:
            print(e)

    def __resize_img(self, file_path):
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        height, width = img.shape[:2]

        # 昔の小さい画像の場合削除
        if height < 200 or width < 200:
            os.remove(file_path)
        else:
            resized_img = cv2.resize(img, (200, 200), interpolation = cv2.INTER_AREA)
            cv2.imwrite(file_path, resized_img)
