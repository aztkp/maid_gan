# -*- coding: utf-8 -*-
import os
import time
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
            self.__download_img(url_full)

    def __download_img(self, url):
        try:
            with urllib.request.urlopen(quote(url, safe=":/")) as web_file:
                data = web_file.read()
                file_name = url.split("/")[-1]
                with open(self.dst_path+"/"+file_name, mode='wb') as local_file:
                    local_file.write(data)
                print("ファイルを保存しました : "+file_name)
        except urllib.error.URLError as e:
            print(e)

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
