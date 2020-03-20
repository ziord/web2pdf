import sys, os, platform
from typing import List, Tuple
from termcolor import colored
import time, shutil
import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
from PyPDF2 import (PdfFileReader, PdfFileWriter)
from pynput.keyboard import (Key, Controller)


class PlatformNotSupportedException(Exception):
    ...

def get_save_dir():
    dir_ = os.path.join(os.getcwd(), 'pdf')
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    return dir_

def rem_save_dir():
    shutil.rmtree(get_save_dir())

def driver_():
    options = webdriver.ChromeOptions()
    
    prefs = {
                "savefile.default_directory": get_save_dir(),
                "download.prompt_for_download": False
             }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    print(os.getcwd())
    
    return driver

def connect(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(link, headers=headers)
    if r.ok:
        html = r.text
        bsoj = BeautifulSoup(html, 'lxml')
        return bsoj
    
def log_(txt):
    with open("error.txt", "a") as file:
        file.write(datetime.datetime.now() + '\n' + txt + '\n')
        
        
def cache_url(url):
    with open('urls.txt', "a") as file:
        file.write(str(datetime.datetime.now()) + '\n' + url + '\n')

def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

def get_page_pdf(driver, timeout=5, cont_url_title="tester"):
    try:
        ch_title = "document.title='%s';"%cont_url_title
        driver.execute_script(ch_title)
        driver.set_script_timeout(timeout)
        cur_window = driver.window_handles[0]
        bsoj = BeautifulSoup(driver.page_source, 'lxml')
        try:
            while str(bsoj.find('h1').text) == 'This site can’t be reached':
                driver.refresh()
        except:
            pass
        driver.execute_script('window.print()')
        new_window = driver.window_handles[1]
        driver.switch_to_window(new_window)
        bsoj = BeautifulSoup(driver.page_source, 'lxml')
        print(bsoj.prettify())
    except:
        while len(driver.window_handles) <= 1:
            time.sleep(1)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        bsoj = BeautifulSoup(driver.page_source, 'lxml')
        # print(bsoj.prettify())

        shadow_section = driver.execute_script('return document.querySelector("print-preview-app").shadowRoot')
        root = shadow_section.find_element_by_id("sidebar")
        # print(root, shadow_section)
        shadow_section1 = expand_shadow_element(driver, root)
        root1 = shadow_section1.find_element_by_tag_name("print-preview-more-settings")
        # print(root1, shadow_section1)
        shadow_section2 = expand_shadow_element(driver, root1)
        root2 = shadow_section2.find_element_by_tag_name("cr-expand-button")
        # print(root2, shadow_section2)
        root2.click()
        time.sleep(1)
        root3 = shadow_section1.find_element_by_tag_name("print-preview-other-options-settings")
        shadow_section3 = expand_shadow_element(driver, root3)
        # print(root3, shadow_section3)
        root4_chkbx = shadow_section3.find_element_by_id("cssBackground")
        # print(root4_chkbx)
        if not root4_chkbx.is_selected():
            root4_chkbx.send_keys('\n')
            
        #resolve platform dependency
        if sys.platform == 'win32' or platform.system().lower() == 'windows':
            root_pp = shadow_section1.find_element_by_id("destinationSettings")
            shadow_section_pp = expand_shadow_element(driver, root_pp)
            root_pp2 = shadow_section_pp.find_element_by_tag_name("print-preview-destination-select")
            shadow_section_pp2 = expand_shadow_element(driver, root_pp2)
           
            select_lst = shadow_section_pp2.find_element_by_tag_name("select")
            select = Select(select_lst)
            # select by value 
            select.select_by_value('Save as PDF/local/')
            time.sleep(3)
            root5_save_btn = shadow_section1.find_element_by_tag_name("print-preview-button-strip")
            shadow_section4_save_btn = expand_shadow_element(driver, root5_save_btn)
            shadow_section4_save_btn.find_element_by_tag_name("cr-button").click()
            time.sleep(3)
            
            kbd = Controller()
            kbd.press(Key.enter)
            kbd.release(Key.enter)
            time.sleep(3)
            
        elif sys.platform == 'linux' or platform.system().lower() == 'linux': 
            root5_save_btn = shadow_section1.find_element_by_id("header")
            shadow_section4_save_btn = expand_shadow_element(driver, root5_save_btn)
            time.sleep(4)
            shadow_section4_save_btn.find_elements_by_class_name("action-button")[0].click()
            time.sleep(5)
            kbd = Controller()
            kbd.press(Key.enter)
            kbd.release(Key.enter)
            time.sleep(5)
            driver.switch_to.window(cur_window)
        
        else:
            raise PlatformNotSupportedException(f"{platform.system()} not supported")
    finally:
        try:
            
            driver.quit()
            ...
        except:
            log_(driver.current_url + ' Failed')
        
        
#TODO: 
def spawn_urls(site_url: str, base_url: str) -> Tuple[List[str], List[str]]:
    ...
    

def convert_wpages2pdf(links, titles):
    for i, link in enumerate(links):
        driver = driver_()
        driver.get(link)
        get_page_pdf(driver, cont_url_title=titles[i])
        cache_url(link)
    

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()
    try:
        for path in paths:
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        pg_num = pdf_writer.getNumPages()
        with open(output, 'wb') as out:
            pdf_writer.write(out)
        size = os.stat(output).st_size
        rem_save_dir()
        return True, pg_num, size
    except:
        return False, 0, 0

def web2pdf(pdf_file_name, func, **args):
    links, titles = func(**args)
    convert_wpages2pdf(links, titles)
    pdf_folder = get_save_dir()
    files = None
    root = None
    for root_, _, files_ in os.walk(pdf_folder):
        files = files_
        root = root_
        
    file_paths = []
    files.sort() 
    for file_ in files:
        file_paths.append(os.path.join(root, file_))
    file_paths.sort(key=lambda x:x[:3])
    pdf_file_name = pdf_file_name
    cvt_path = os.path.join(os.getcwd(), 'converted')
    if not os.path.exists(cvt_path):
        os.mkdir(cvt_path)
    output_path = os.path.join(cvt_path, pdf_file_name)
    is_suc, pgn, size = merge_pdfs(file_paths, output_path)
    if is_suc:
        if platform.system().lower()  == 'linux':
            print(colored(pdf_file_name, "green"), colored("created successfully", "yellow"))
            print(colored('Number of pages:', 'green'), colored("%d"% pgn, "yellow"))
            print(colored('File size:', 'green'), colored(f'{"%.2f"%(size / (1024 * 1024))}MB',  "yellow"))
            print(colored("File path:", "green"), colored(output_path, "yellow")); return
        else:
            print(pdf_file_name,  "created successfully" )
            print('Number of pages:',  "%d"% pgn, )
            print('File size:', f'{"%.2f"%(size / (1024 * 1024))}MB'  )
            print("File path:", output_path); return
    print(pdf_file_name, "failed to be created")





