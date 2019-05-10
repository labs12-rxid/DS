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

load_dotenv()
chromedriver_path = os.getenv("chromedriver_path")
headless = (os.getenv('headless') == 'False')
headless = True
print('headless', headless)

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
                return True

            m1l = ''.join(c for c in m1l if c not in punctuation)
            m2l = ''.join(c for c in m2l if c not in punctuation)
            if m1l == m2l:
                return True
    #         print('no match yet', m1l, m2l)

            for i in range(3):
                m1s = m1l.split()
                m2s = m2l.split()               
                if i == 1:
                    m2s.insert(0, m2s[0]) # dup first word (usually company name)
                elif i == 2:
                    m2s.extend(m2s)  # dup MPRINTS on each side

                for j in range(2):  

                    # print('m1s', m1s,'i',i,'j',j)
                    # print('m2s', m2s)
                    if "".join(m1s) == "".join(m2s):
                        return True

              # test every possible starting word (don't know where left/right break is)
                    m2sq = deque(m2s)
                    m1ss = "".join(m1s)
                    for _ in range(len(m2s) - 1):
                        l = m2sq.popleft()
                        m2sq.append(l)
                        if j == 1:
                            m2sq.insert(0,'logo')
                        # print('rotate',m1ss,m2sq)
                        if m1ss == "".join(m2sq):
                            return True
                        if j == 1:
                            m2sq.popleft() # remove 'logo' 
            return False

    def select_color(self, color_code):
        color_elem = self.driver.find_element(By.CSS_SELECTOR, "select[id='color-select']")
        print('color_elem', color_elem)
        color = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[id='color-select']")))
        # time.sleep(1)
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

    def select_shape(self, shape_code):
        shape_elem = self.driver.find_element(By.CSS_SELECTOR, "select[id='shape-select']")
        print('shape_elem', shape_elem)
        shape = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[id='shape-select']")))
        # time.sleep(1)
        shape.send_keys(Keys.RETURN)        
        target_shape_elem = shape_elem.find_element(
            By.XPATH, f"//option[@value={shape_code}]")
        print('target_shape_elem found', target_shape_elem)  
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", target_shape_elem)
        target_shape_elem = shape_elem.find_element(
            By.XPATH, f"//option[@value={shape_code}]")
        print('target_shape_elem after scroll\n', target_shape_elem)  
        print('shape scroll complete')
        self.driver.execute_script(
            "arguments[0].click();", target_shape_elem)            
        # time.sleep(2.5)
        print('shape click complete')


    def make_mark_down(self, isoup) -> str:
        markdown = ''
        n = ''
        try:
            h1 = isoup.find_all('h1')[0]
            title = h1.text
            markdown += '<h1>' + title.strip() + '</h1>' + n
            generic = None
            try:
                generic = h1.parent.p.i.text
            except:
                pass
            if generic != None:
                markdown += '<h2>Generic</h2> ' + generic + n
        #     ins = isoup.findAll(
        #         lambda tag: tag.name == "h2" and
        #         tag.text == 'In Summary')[0] 
            ins = isoup.find('h2', string='In Summary')
        #     if ins == None:
        #         print('ins == None')
        # #         ins = isoup.find('h2', string='For the Consumer')
        #         ins = isoup.find('h2')
        #     print(f'ins.text |{ins.text}|')

        #     print(type(ins))
            p = None
            if ins != None:
                ins_ = ins.parent.find_all('b')[3].parent.text
            #     print('ins_',ins_,type(ins_))
                ins__ = ins_[6:].replace('may not', '<i>may not</i>')
                markdown += '<p><h2>Note</h2></p> ' + ins__
                ss =  "Common side effects of "
                p = isoup.findAll(
                    lambda tag: tag.name == "b" and
                    len(tag.text) > len(ss) and
                    tag.text[0:len(ss)] == ss)
                if p != None:
                    if len(p) > 0:
                        p = p[0].parent
                    else:
                        p = None
            if p != None:
                markdown += '<h2>In Summary</h2>' + str(p) + n
        #     p = p.parent.findAll(
        #         lambda tag: tag.name == "h2" and
        #         tag.text.index('For the Consumer') >= 0)[0].parent.find('p')
                p = p.parent.find('h2', string="For the Consumer")
               # <h2>For the Consumer</h2> 
            if p == None:
                ss = "For the Consumer"
                try: 
                    p = isoup.findAll(
                        lambda tag: tag.name == "h2" and
                        len(tag.text) >= len(ss) and
                        tag.text.find(ss) >= 0)[0]
                except:
                    p = isoup.find('h2')
                    print('For the Consumer not found in ', p.text)
            markdown += str(p) + n
            # Applies to tadalafil : oral tablet
            markdown += '<p>' + p.parent.find_all('p')[4].text.replace('\n','') + '</p>' + n 
        #     div = p.parent.find('div', 'class': ["contentAd contentAdM1 contentAdAlone"]>
            markdown += '<p>' + p.parent.find_all('p')[5].text.replace('\n','') + '</p>' + n 
            p6 = str(p.parent.find_all('p')[6])

            if p6.find('\n') >= 0:
                p6 = p6.replace('\n','') 

            markdown += p6 + n
            markdown += '<h3>Less Common</h3><ul>'
            ul = p.parent.find_all('ul')[2]
            for li in ul.find_all('li'):
                markdown += '<li>' + li.text.replace('\n','') + '</li>' + n    
            markdown += '</ul>'
            markdown += "<h3>Incidence Not Known</h3><ul>"
            ul = p.parent.find_all('ul')[3]
            for li in ul.find_all('li'):
                markdown += '<li>' + li.text.replace('\n','') + '</li>' + n    
            markdown += '</ul>'
            p = ul.next_sibling.next_sibling
            markdown += str(p)
            markdown += "<h3>More Common</h3><ul>"
            ul = p.parent.find_all('ul')[3]   
            for li in ul.find_all('li'):
                markdown += '<li>' + li.text.replace('\n','') + '</li>' + n    
            markdown += '</ul><h3>Less Common</h3><ul>'  
            ul = p.parent.find_all('ul')[4]   
            for li in ul.find_all('li'):
                markdown += '<li>' + li.text.replace('\n','') + '</li>' + n    
            markdown += '</ul>'
        except Exception as e:
            print('error making markdown', repr(e))
            print(f'Error on line {sys.exc_info()[-1].tb_lineno}')
            return None        
        return markdown 

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
        side_target = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "img[src='/img/pillid/example.png']")))
        side_target.click()

        self.select_color(color_code)
        self.select_shape(shape_code)

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
            print('type!!', type(img.parent.parent))
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
            if headless == False:  
                self.select_color(color_code)  # for testing color select
                self.select_shape(shape_code)  # for testing shape select
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
            print('colors', colors)
            shapes = isoup.find_all('dt', string='Shape:')
            print('shapes', shapes)
#             imgs = isoup.find_all('img')
#             print('imgs len',len(imgs))
            imgs = isoup.findAll(
                lambda tag: tag.name == "img" and
                len(tag.attrs) >= 1 and
                tag["src"][0:14] == '/images/pills/')
            print('imgs length', len(imgs))
#             print('brand', brand, 'generic', generic, mprint, )
            for img in imgs:
                #                   print('img', img)
                try:
                    s = img['src']
                    a = isoup.find_all('a', string='Side Effects')[0]
                    # ul = isoup.find_all('ul', {'class': ['more-resources-list', 'more-resources-list-general']})
                    # print('len ul',len(ul))
                    # if len(ul) > 0:
                    #     li = ul[0].find('li')
                    #     if li != None:
                    #         print('li text', li.text)
        
                    # with open('isoup.html',"wt") as File:
                    #     File.write(isoup.prettify())
                    
                    print('side effects a href',a['href'])
                    self.ddriver.get(self.base + a['href'])
                    print('side effects page title', self.ddriver.title)
                    WebDriverWait(self.ddriver, 100).until(ititle_contains('Side Effects in Detail'))
                    isoup = BeautifulSoup(self.ddriver.page_source, 'html.parser')
                    # with open('./html/' + generic + '.html',"wt") as File:
                    #     File.write(isoup.prettify())
                    mark_down = self.make_mark_down(isoup)
                    print('mark_down i:', i)
                    print(colors[i].next_sibling.text)
                    print(shapes[i].next_sibling.text)

                    # #                       print('s',s)
                    #                     if s[0:14] == '/images/pills/':
                    #                          print('found img', s, ' mprint ', mprint)
                    #                         self.img = base + s
                    self.results.append(
                        {'brand': brand, 'generic': generic, 'mprint': mprint, 'img': self.base + s,
                            'color': colors[i].next_sibling.text, 'shape': shapes[i].next_sibling.text,
                            'side effects': mark_down
                            })
                    print(f'appending {brand} {s} {len(self.results)} results' )
                    break
                except Exception as e:
                    print('error appending', repr(e))
                    break
#             if self.mprint_is_equal(mprint,pmprint) & appended: # works because drugs.com puts matching mprint first
#                 break
#             print( mprint.lower(), pmprint.lower())
            i += i
            return json.dumps(self.results, indent=4)

    def reset(self):
        del self.results
        self.results = []

    def close(self):
        self.driver.quit()
        self.ddriver.quit()
        self.nonmatch_unique_file.close()
        del self.results
        
#            <option value="1">Blue</option>
#            <option value="2">Brown</option>        

