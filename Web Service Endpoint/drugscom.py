from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import io
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import re
import numpy as np
import os
import glob
import shutil
import json
import html
from string import punctuation
from collections import deque
from dotenv import load_dotenv

headless = True
print('headless', headless)

chromedriver_path = "/usr/local/bin/chromedriver"
#chromedriver_path = "./chromedriver"
print('chromedriver_path', chromedriver_path)

class ititle_contains(object):
    """ An expectation for checking that the title contains a case-insensitive
    substring. title is the fragment of title expected
    returns True when the title matches, False otherwise
    """
    def __init__(self, title):
        self.title = title

    def __call__(self, driver):
        return self.title.lower() in html.unescape(driver.title).lower()

class drugscom:
    def __init__(self):
        self.debug = False
        self.first = True
        self.nonmatch_unique_file = open('nonmatch_unique.txt', 'wt')
        self.wurl = 'https://www.drugs.com/pill_identification.html'
        self.base = "https://www.drugs.com"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        if headless:
            chrome_options.add_argument('--headless')
        self.driver = webdriver.chrome.webdriver.WebDriver(
            chromedriver_path, options=chrome_options)
        self.ddriver = webdriver.chrome.webdriver.WebDriver(
            chromedriver_path, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)
        self.dwait = WebDriverWait(self.ddriver, 5)
        self.driver.set_window_size(850, 1600)
        self.results = []
        self.actions = ActionChains(self.driver)
        self.shape_codes = [
            { "id": 0, "name": 'Round', 'code': 24 },
            { "id": 1, "name": 'Capsole', 'code': 5 },
            { "id": 2, "name": 'Oval',"code": 20 },
            { "id": 3, "name": 'Egg',"code":  9 },
            { "id": 4, "name": 'Barrel',"code": 1 },
            { "id": 5, "name": 'Rectangle',"code": 23 },
            { "id": 6, "name": '3 Sided',"code": 32 },
            { "id": 7, "name": '4 Sided',"code": 14 },
            { "id": 8, "name": '5 Sided',"code": 13 },
            { "id": 9, "name": '6 Sided',"code": 27 },
            { "id": 10, "name": '7 sided',"code": 25 },
            { "id": 11, "name": '8 sided',"code": 10 },
            { "id": 12, "name": 'U Shaped',"code": 33 },
            { "id": 13, "name": 'Figure 8',"code": 12 },
            { "id": 14, "name": 'Heart',"code": 16 },
            { "id": 15, "name": 'Kidney',"code": 18 },
            { "id": 16, "name": 'Gear',"code": 15 },
            { "id": 17, "name": 'Character',"code": 6 },
            { "id": 18, "name": 'Diamand',"code": 7 },
            { "id": 19, "name": 'Square',"code": 28 },
        ]
        self.color_codes = [{'id': 0, 'name': 'Beige', 'code': 14}, {'id': 1, 'name': 'Black', 'code': 73},
            {'id': 2, 'name': 'Blue', 'code': 1}, {'id': 3, 'name': 'Brown', 'code': 2},
            {'id': 4, 'name': 'Clear', 'code': 3}, {'id': 5, 'name': 'Gold', 'code': 4},
            {'id': 6, 'name': 'Gray', 'code': 5}, {'id': 7, 'name': 'Green', 'code': 6},
            {'id': 8, 'name': 'Maroon', 'code': 44}, {'id': 9, 'name': 'Orange', 'code': 7},
            {'id': 10, 'name': 'Peach', 'code': 74}, {'id': 11, 'name': 'Pink', 'code': 8},
            {'id': 12, 'name': 'Purple', 'code': 9}, {'id': 13, 'name': 'Red', 'code': 10},
            {'id': 14, 'name': 'Tan', 'code': 11}, {'id': 15, 'name': 'White', 'code': 12},
            {'id': 16, 'name': 'Yellow', 'code': 13}, {'id': 17, 'name': 'Beige & Red', 'code': 69},
            {'id': 18, 'name': 'Black & Green', 'code': 55}, {'id': 19, 'name': 'Black & Teal', 'code': 70},
            {'id': 20, 'name': 'Black & Yellow', 'code': 48}, {'id': 21, 'name': 'Blue & Brown', 'code': 52},
            {'id': 22, 'name': 'Blue & Grey'}, {'id': 23, 'name': 'Blue & Orange', 'code': 71},
            {'id': 24, 'name': 'Blue & Peach', 'code': 53}, {'id': 25, 'name': 'Blue & Pink', 'code': 34},
            {'id': 26, 'name': 'Blue & White', 'code': 19}, {'id': 27, 'name': 'Blue & White Specks', 'code': 26},
            {'id': 28, 'name': 'Blue & Yellow', 'code': 21}, {'id': 29, 'name': 'Brown & Clear', 'code': 47},
            {'id': 30, 'name': 'Brown & Orange', 'code': 54}, {'id': 31, 'name': 'Brown & Peach', 'code': 28},
            {'id': 32, 'name': 'Brown & Red', 'code': 16}, {'id': 33, 'name': 'Brown & White', 'code': 57},
            {'id': 34, 'name': 'Brown & Yellow', 'code': 27}, {'id': 35, 'name': 'Clear & Green', 'code': 49},
            {'id': 36, 'name': 'Dark & Light Green', 'code': 46}, {'id': 37, 'name': 'Gold & White', 'code': 51},
            {'id': 38, 'name': 'Grey & Peach'}, {'id': 39, 'name': 'Grey & Pink'}, {'id': 40, 'name': 'Grey & Red'},
            {'id': 41, 'name': 'Grey & White'}, {'id': 42, 'name': 'Grey & Yellow'},
            {'id': 43, 'name': 'Green & Orange', 'code': 65}, {'id': 44, 'name': 'Green & Peach', 'code': 63},
            {'id': 45, 'name': 'Green & Pink', 'code': 56}, {'id': 46, 'name': 'Green & Purple', 'code': 43},
            {'id': 47, 'name': 'Green & Turquoise', 'code': 62}, {'id': 48, 'name': 'Green & White', 'code': 30},
            {'id': 49, 'name': 'Green & Yellow', 'code': 22}, {'id': 50, 'name': 'Lavender & White', 'code': 42},
            {'id': 51, 'name': 'Maroon & Pink', 'code': 40}, {'id': 52, 'name': 'Orange & Turquoise', 'code': 50},
            {'id': 53, 'name': 'Orange & White', 'code': 64}, {'id': 54, 'name': 'Orange & Yellow', 'code': 23},
            {'id': 55, 'name': 'Peach & Purple', 'code': 60}, {'id': 56, 'name': 'Peach & Red', 'code': 66},
            {'id': 57, 'name': 'Peach & White', 'code': 18}, {'id': 58, 'name': 'Pink & Purple', 'code': 15},
            {'id': 59, 'name': 'Pink & Red Specks', 'code': 37}, {'id': 60, 'name': 'Pink & Turquoise', 'code': 29},
            {'id': 61, 'name': 'Pink & White', 'code': 25}, {'id': 62, 'name': 'Pink & Yellow', 'code': 72},
            {'id': 63, 'name': 'Red & Turquoise', 'code': 17}, {'id': 64, 'name': 'Red & White', 'code': 35},
            {'id': 65, 'name': 'Red & Yellow', 'code': 20}, {'id': 66, 'name': 'Tan & White', 'code': 33},
            {'id': 67, 'name': 'Turquoise & White', 'code': 59}, {'id': 68, 'name': 'Turquuise & Yellow'},
            {'id': 69, 'name': 'White & Blue Specks', 'code': 32}, {'id': 70, 'name': 'White & Red Specks', 'code': 41},
            {'id': 71, 'name': 'White & Yellow', 'code': 38}, {'id': 72, 'name': 'Yellow & Grey'},
            {'id': 73, 'name': 'Yellow & White', 'code': 36}]


    def get_color_code(self,id) -> int:
        for d in self.color_codes:
            if d['id'] == id:
                return d['code']
        print(f'unknown color id {id} ')
        return 12 # white 

    def get_shape_code(self,id) -> int:
        for d in self.shape_codes:
            if d['id'] == id:
                return d['code']
        print(f'unknown shape id {id} ')
        return 0 # round       

    def mprint_is_equal(self, m1, m2):  # m1 is drugs.com mprint, m2 is DB mprint
            m1l = m1.lower()
            m2l = m2.lower()
            if m1l == m2l:
                #             print('return True', m1l)
                return True
    #         print(f'm1l|{m1l}|  m2l|{m2l}|')
            # code matching "xmg" to "x mg"
    #         m1l = re.sub(r"(\s?mc?g)(?=$)", "", m1l)
    #         m2l = re.sub(r"(\s?mc?g)(?=$)", "", m2l)
    #         print(f'after sub m1l|{m1l}|  m2l|{m2l}|')
    #         m1m = re.search(r"(mc?g)(?=$)", m1l)
    #         m2m = re.search(r"(mc?g)(?=$)", m2l)
    # #         m1m = re.find(r"(mg)(?=$)", m1l)
    #         print('matches', m1m, m2m)
    #         if (m1m != None) and (m2m != None) and (m1m.group(1) == m2m.group(1)):
    #             m2l = m1l.replace(m1m.group(1), '').strip()
    #             m2l = m2l.replace(m2m.group(1), '').strip()
            m1l = ''.join(c for c in m1l if c not in punctuation)
            m2l = ''.join(c for c in m2l if c not in punctuation)
            if m1l == m2l:
                #             print('return True', m1l)
                return True
    #         print('no match yet', m1l, m2l)
            m1s = m1l.split()
            m2s = m2l.split()
            m2sLogo = m2l.split()
            if "".join(m1s) == "".join(m2s):
                #             print('returning true after dupped adjustments')
                #             print('match',  "".join(m1s), "".join(m2s))
                return True
    #         print('not match',  "".join(m1s), "".join(m2s))
    #         print('m1s', m1s, type(m1s), len(m1s), 'm2s', m2s, len(m2s))
            if len(m1s) == len(m2s) + 1:
                #             print('m2s befoe insert', m2s)
                m2s.insert(0, m2s[0])  # drugs.com first word dupped
                m2sLogo.insert(0, 'logo')  # drugs.com added first word of 'logo'
    #             print('m2s after insert', m2s)
    #         print('after +1 test')
            else:
                if len(m1s) == 2 * len(m2s):  # drugs.com entire mprint dupped
                    m2s.extend(m2s)
            if "".join(m1s) == "".join(m2s):
                #             print('returning true after dupped adjustments')
                #             print('match',  "".join(m1s), "".join(m2s))
                return True
    #         print('not match',  "".join(m1s), "".join(m2s))
    #         print('after dupped adjustments and no match', " ".join(m1s), " ".join(m2s))
            if len(m1s) == len(m2s):  # test every possible starting word (don't know where left/right break is)
                m2sq = deque(m2s)
                m1ss = "".join(m1l)
                for _ in range(len(m2s) - 1):
                    l = m2sq.popleft()
                    m2sq.append(l)
                    if m1ss == "".join(m2sq):
                        return True
            return False

    def get_data(self, ijo):
        pmprint = ijo['imprint']
        color_code = self.get_color_code(ijo['color'])
        shape_code = self.get_shape_code(ijo['shape'])
        print('starting get_data', pmprint, color_code, shape_code)

        #         self.driver.get(self.wurl)
        #         WebDriverWait(self.driver, 100).until(EC.title_contains(
        #             "Pill Identifier (Pill Finder) - Drugs.com"))
        #         try:
        #             elem = self.wait.until(
        #                 EC.element_to_be_clickable((By.LINK_TEXT, 'Accept' if len(self.results) == 0 else 'Search Again')))
        #         except:
        if self.first:
            self.driver.get(self.wurl)
            WebDriverWait(self.driver, 100).until(EC.title_contains(
                "Pill Identifier (Pill Finder) - Drugs.com"))
            if self.debug:
                print('started')
                time.sleep(3)
                self.driver.refresh()
            else:
                elem = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, 'Accept')))
                elem.click()
                print('accept clicked')
            self.first = False

        mprint = pmprint
#         elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/imprints.php']")))
        elem = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#livesearch-imprint")))
        elem.click()
        elem.clear()
        elem.send_keys(mprint)
        # elem.send_keys(Keys.RETURN)

        # color may be covered with a drugs.com pulldown without this
        shape = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "select[id='shape-select']")))
        shape.click()
        time.sleep(1)
        color_elem = self.driver.find_element(By.CSS_SELECTOR, "select[id='color-select']")
        print('color_elem', color_elem)
        color = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[id='color-select']")))
        time.sleep(1)
        color.send_keys(Keys.RETURN)
        # color.click()
        print('color.click')

        # self.wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//input[@type='submit']")))
        target_color_elem = color_elem.find_element(
            By.XPATH, f"//option[@value={color_code}]")
        print('target_color_elem found', target_color_elem)  
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", target_color_elem)
        target_color_elem = color_elem.find_element(
            By.XPATH, f"//option[@value={color_code}]")
        print('target_color_elem after scroll\n', target_color_elem)  
        print('scroll complete')
        self.driver.execute_script(
            "arguments[0].click();", target_color_elem)            
        # time.sleep(2.5)
        print('color click complete')


        shape_elem = self.driver.find_element(By.CSS_SELECTOR, "select[id='shape-select']")
        print('shape_elem', shape_elem)
        shape = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[id='shape-select']")))
        time.sleep(1)
        shape.send_keys(Keys.RETURN)
        # color.click()
        print('color.click')

        target_shape_elem = shape_elem.find_element(
            By.XPATH, f"//option[@value={shape_code}]")
        print('target_shape_elem found', target_shape_elem)  
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", target_shape_elem)
        target_color_elem = color_elem.find_element(
            By.XPATH, f"//option[@value={shape_code}]")
        print('target_shape_elem after scroll\n', target_shape_elem)  
        print('shape scroll complete')
        self.driver.execute_script(
            "arguments[0].click();", target_shape_elem)            
        # time.sleep(2.5)
        print('shape click complete')
        # if the python way of clicking submit works use it, otherwise use the JavaScript way
        try:
            elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
            elem.click()
        except:
            submit = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            self.driver.execute_script("arguments[0].click();", submit) 
            # print('submit input not clickable') 
        # self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search Again'))) 
        print('Search Again clickable')       
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        a = None
        mprint = None
        # with open('soup.html',"wt") as File:
        #     File.write(soup.prettify())
        # allimgs = soup.find_all(By.CSS_SELECTOR, 'img')
        # print('allimgs len', len(allimgs))
        imgs = soup.findAll(
            lambda tag: tag.name == "img" and
            len(tag.attrs) >= 1 and
            tag["src"][0:14] == '/images/pills/')
        print('len imgs',len(imgs))
        for img in imgs:
            #             s = img['src']
            #                       print('s',s)
            a = img.parent.parent('span', text='Pill Imprint:')[0].next_sibling.next_sibling
#             print('a', a, type(a), a.text)
            mprint = a.text
            # remove repeated internal spaces
            mprint = ' '.join(mprint.split())
            print('mprint', mprint)
            if not self.mprint_is_equal(mprint, pmprint):
                #                     print('not equal',mprint,pmprint)
                if len(imgs) == 1:  # unique image result from drugs.com
                    self.nonmatch_unique_file.write(
                        f"mprint {mprint} pmprint {pmprint}")
                    break
#                 print(f"nonmatch continue mprint {mprint} pmprint {pmprint}")
                a = None
                mprint = None
                continue
#             print('soup breaking out of imgs loop')
            break

        try:
           
            elem = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Search Again')))
            elem.click()
        except:
            pass
        if a == None:
            print('null a')
            return self.results
        i = 0
        if a != None:
            #             a = elem.parent.find_next('a')
            #             print(f"img: {a['href']} MPRINT: {a.text}")
            #             mprint = a.text
            #             mprint = ' '.join(mprint.split()) # remove repeated internal spaces
            #             if not self.mprint_is_equal(mprint,pmprint):
            #                 continue
            # time.sleep(10)
            self.ddriver.get(self.base + a['href'])
            print(f'waiting for mprint {mprint}')
            WebDriverWait(self.ddriver, 100).until(ititle_contains(mprint))
#             print(a.text, ' title')
            isoup = BeautifulSoup(self.ddriver.page_source, 'html.parser')
            div = isoup.find_all('div', {'class': 'contentBox'})[0]
            brand = div.h1.text
            brand = brand[brand.index('(') + 1:-1]
            generic = None
            f_generic = None
            try:
                f_generic = isoup.find_all(
                    'p', {'class': 'drug-subtitle'})[0].text
                generic = f_generic[14:]
                print('generic', generic)
            except:
                print('generic error, full generic',f_generic)
                if f_generic == None:
                    generic = brand
                    brand = None
            # <dt class="pid-item-title pid-item-inline">Color:</dt>
            colors = isoup.find_all('dt', string='Color:')
#             print('colors', colors)
            shapes = isoup.find_all('dt', string='Shape:')
#             imgs = isoup.find_all('img')
#             print('imgs len',len(imgs))
            imgs = isoup.findAll(
                lambda tag: tag.name == "img" and
                len(tag.attrs) >= 1 and
                tag["src"][0:14] == '/images/pills/')
#             print('imgs length', len(imgs))
#             print('brand', brand, 'generic', generic, mprint, )
            for img in imgs:
                #                   print('img', img)
                try:
                    s = img['src']
                    # #                       print('s',s)
                    #                     if s[0:14] == '/images/pills/':
                    #                          print('found img', s, ' mprint ', mprint)
                    #                         self.img = base + s
                    self.results.append(
                        {'brand': brand, 'generic': generic, 'mprint': mprint, 'img': self.base + s,
                            'color': colors[i].next_sibling.text, 'shape': shapes[i].next_sibling.text})
                    print(f'appending {brand} {s}')
                    break
                except Exception as e:
                    print('error appending', repr(e))
                    pass
#             if self.mprint_is_equal(mprint,pmprint) & appended: # works because drugs.com puts matching mprint first
#                 break
#             print( mprint.lower(), pmprint.lower())
            i += i
            print('!!!!!!!!!!!! S U C C E S S !!!!!!!!!!!')
            return self.results

    def reset(self):
        self.results = []

    def close(self):
        self.driver.quit()
        self.ddriver.quit()
        self.nonmatch_unique_file.close()
        
#            <option value="1">Blue</option>
#            <option value="2">Brown</option>        
