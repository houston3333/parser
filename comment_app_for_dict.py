from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import ssl
import pandas as pd
import os
import pickle
from review_dict import REVIEW_DICT
from generating_review import generate_review


def get_driver(chrome_driver_path):

    options = Options()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36") 
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--disable-blink-features=AutomationControlled') 
    options.add_argument("disable-infobars") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False) 

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    return driver


def send_comment(driver, hotel, wait, comment, mail):
    driver.get(hotel)
    time.sleep(3) 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        # button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="basiclayout"]/div/div/div/div/div/div/div/div/div/section/div/div/div/div/div/div/button')))
        button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="basiclayout"]/div/div/div/div/div/div/div/section/div/div/div/div/div/div/button')))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)
    
    except TimeoutException:
        print("Failed to find the button within the given time.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    frame = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'f0c216ee26') and @role='dialog' and @aria-modal='true']"))) 
    try:
        time.sleep(1)
        question_input = wait.until(EC.presence_of_element_located((By.NAME, 'questionInput')))
        question_input.click()
        question_input.send_keys(comment)
    except TimeoutException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="b2hotelPage"]/div/div/div/div/div/div/div/div/div/div/div/div/button'))                   
    try:
        mail_input = wait.until(EC.presence_of_element_located((By.NAME, 'emailInput')))
        mail_input.send_keys(mail)
    except TimeoutException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="b2hotelPage"]/div/div/div/div/div/div/div/div/div/div/div/div/button'))
    
    
    return True


def main():
    # REGION_ID = 0
    mail = 'gptforhotel@gmail.com'
    chrome_driver_path = r'chromedriver-win64\chromedriver.exe'
    max_num = 500
    hotels_num = 0

    ssl._create_default_https_context = ssl._create_unverified_context
    driver = get_driver(chrome_driver_path)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    wait = WebDriverWait(driver, 20)

    with open("dict\hotels.pkl","rb") as f:
        HOTELS = pickle.load(f)

    for hotel in range(len(HOTELS)):
        comment = generate_review(REVIEW_DICT)
        if HOTELS[hotel]['status'] == None:
            HOTELS[hotel]['status'] = send_comment(driver, HOTELS[hotel]['url'], wait, comment, mail)
            hotels_num += 1
            print(HOTELS[hotel])
            print(hotel)
            os.remove("dict\hotels.pkl")
            with open("dict\hotels.pkl","wb") as f:
                pickle.dump(HOTELS,f)

        if hotels_num >= max_num:
            break
        
    driver.quit()
    print(hotels_num)


def comment():
    # REGION_ID = 0
    mail = 'gptforhotel@gmail.com'
    chrome_driver_path = r'C:\chromedriver\chromedriver-win64\chromedriver.exe'
    max_num = 500
    hotels_num = 0

    ssl._create_default_https_context = ssl._create_unverified_context
    driver = get_driver(chrome_driver_path)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    wait = WebDriverWait(driver, 20)

    with open("dict\hotels.pkl","rb") as f:
        HOTELS = pickle.load(f)

    for hotel in range(len(HOTELS)):
        comment = generate_review(REVIEW_DICT)
        if HOTELS[hotel]['status'] == None:
            HOTELS[hotel]['status'] = send_comment(driver, HOTELS[hotel]['url'], wait, comment, mail)
            hotels_num += 1
            # print(HOTELS[hotel])
            # print(hotel)
            os.remove("dict\hotels.pkl")
            with open("dict\hotels.pkl","wb") as f:
                pickle.dump(HOTELS,f)

        if hotels_num >= max_num:
            break
        
    driver.quit()
    return hotels_num


if __name__ == "__main__":
    main()