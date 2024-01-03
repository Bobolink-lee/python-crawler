from selenium import webdriver
from lxml import etree
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import pymysql
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def CreateTable():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='stocks',
                             charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    
    creatSql = """create table if not exists total_stocks(
                `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `code` INT NOT NULL UNIQUE,
                `name` VARCHAR(20) NOT NULL,
                `price` FLOAT NOT NULL,
                `up_down_rate` FLOAT NOT NULL,
                `up_down` FLOAT NOT NULL,
                `up_rate` FLOAT NOT NULL,
                `change_rate` FLOAT NOT NULL,
                `quantity_rate` FLOAT NOT NULL,
                `amplitude_rate` FLOAT NOT NULL,
                `transaction` VARCHAR(20) NOT NULL,
                `circulating` VARCHAR(20) NOT NULL,
                `circulation_market` VARCHAR(20) NOT NULL,
                `pe_ratio` VARCHAR(20) NOT NULL
                );"""
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(creatSql)
        connection.commit()
    finally:
        connection.close()


def writeData(trlist):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='stocks',
                             charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    sql = """
            INSERT total_stocks (`code`, `name`, `price`, `up_down_rate`, `up_down`, `up_rate`,
            `change_rate`, `quantity_rate`, `amplitude_rate`, `transaction`, `circulating`,
            `circulation_market`, `pe_ratio`)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
           """
    try:
        with connection.cursor() as cursor:
            # execute执行一条，executemany批量插入
            cursor.executemany(sql, trlist)
        print("some data already insert database")
        connection.commit()
    finally:
        connection.close()

def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
    return bool(pattern.match(string))

def main():
    CreateTable()
    
    # 添加启动参数，ban掉windows.navigator.webdriver
    option = webdriver.EdgeOptions()
    # 一种反爬机制，若为真，则无法正常显示内容
    option.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Edge(options=option,keep_alive=True)
    driver.implicitly_wait(1)
    for page in range(1, 264):
        trlist = []
        driver.get(f'https://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{page}/ajax/1/')
        print(f"this is the {page}st page down")
        table = driver.find_element(By.XPATH, '//table[@class="m-table m-pager-table"]')
        tbody = table.find_element(By.XPATH, './tbody')
        trs = tbody.find_elements(By.XPATH, './tr')
        start = time.time()
        for tr in trs:
            tds = tr.find_elements(By.XPATH, './td')
            tdlist = []
            for i, td in enumerate(tds):
                if is_number(td.text) and i != 13:
                    if '.' in td.text:
                        text = float(td.text)
                    else:
                        text = int(td.text)
                    tdlist.append(text)
                elif '--' in td.text:
                    tdlist.append(None)
                else:
                    tdlist.append(td.text)
            trlist.append(tdlist[1: -1])
        end = time.time()
        print("the data of page append list used time: %.2f" % (end -  start))
        print(trlist)
        writeData(trlist)
    driver.close()

if __name__ == "__main__":
    main()