# -*- coding: utf-8 -*-
#Day027_HW
#載入套件
import os
import json

from pathlib import Path
from datetime import datetime

class Day027_HwPipeline(object):
    #每個 Item Pipeline 都需要實作，用來檢查資料數據與是否丟棄等決定
    def process_item(self, item, spider):
        return item


class JSONPipeline(object):
     #當爬蟲開啟時需要處理的流程 
    def open_spider(self, spider):
        self.start_crawl_datetime = datetime.now().strftime('%Y%m%dT%H:%M:%S')

        # 在開始爬蟲的時候建立暫時的 JSON 檔案
        # 避免有多筆爬蟲結果的時候，途中發生錯誤導致程式停止會遺失所有檔案
        self.dir_path = Path(__file__).resolve().parents[1] / 'crawled_data'
        self.runtime_file_path = str(self.dir_path / '.tmp.json.swp')
        if not self.dir_path.exists():
            self.dir_path.mkdir(parents=True)
        spider.log('Create temp file for store JSON - {}'.format(self.runtime_file_path))

        # 設計 JSON 存的格式為
        # [
        #  {...}, # 一筆爬蟲結果
        #  {...}, ...
        # ]
        self.runtime_file = open(self.runtime_file_path, 'w+', encoding='utf8')
        self.runtime_file.write('[\n')
        self._first_item = True
    #每個 Item Pipeline 都需要實作，用來檢查資料數據與是否丟棄等決定   
    def process_item(self, item, spider):
        # 把資料轉成字典格式並寫入文件中
        if not isinstance(item, dict):
            item = dict(item)

        if self._first_item:
            self._first_item = False
        else:
            self.runtime_file.write(',\n')

        self.runtime_file.write(json.dumps(item, ensure_ascii=False))
        return item
    #當爬蟲關閉時需要處理的流程
    def close_spider(self, spider):
        self.end_crawl_datetime = datetime.now().strftime('%Y%m%dT%H:%M:%S')

        # 儲存 JSON 格式
        self.runtime_file.write('\n]')
        self.runtime_file.close()
        
        # 將暫存檔改為以日期為檔名的格式
        self.store_file_path = self.dir_path / '{}-{}.json'.format(self.start_crawl_datetime,
                                                                   self.end_crawl_datetime)
        self.store_file_path = str(self.store_file_path)
        os.rename(self.runtime_file_path, self.store_file_path)
        spider.log('Save result at {}'.format(self.store_file_path))

