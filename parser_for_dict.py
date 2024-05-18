from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pickle
import os
import random
from urls import URLS
from proxies import PROXIES


def create_driver(proxy):
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36") 
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--disable-blink-features=AutomationControlled') 
    options.add_argument("disable-infobars") 
    # options.add_argument("--proxy-server=%s" % proxy) 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False) 

    chrome_driver_path = r'chromedriver-win64\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    return driver


def find_value(list_of_dicts, value_to_find):
    for item in list_of_dicts:
        if item.get('name') == value_to_find:
            return True
    return False


def scrape_hotels(urls, proxies, HOTELS):
    driver = None
    sum_hotels = 0
    count = 0
    num = 0
    for url in urls:
        # if driver:
        #     driver.quit()  
        driver = create_driver(random.choice(proxies))
        # time.sleep(3.5)
        
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            # num = 0
            while True:
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                try:
                    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='bottom_of_basiclayout']/parent::div/div/div/div/button/span")))
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    driver.execute_script("arguments[0].click();", button)
                    num+=1
                except TimeoutException:
                    print("No more buttons to click or button not found within the specified time.")
                    break
                except NoSuchElementException:
                    print("Button not found.")
                    break
            
            hotels = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
            # sum_hotels = 0
            # count = 0
            for hotel in hotels:
                
                name = hotel.find_element(By.XPATH, './/div[@data-testid="title"]').text
                
                link = hotel.find_element(By.XPATH, './/a[@data-testid="title-link"]').get_attribute('href')


                if find_value(HOTELS, name) == False:
                    HOTELS.append({'name': name,
                                'url': link,
                                'status': None})
                    count+=1

                    os.remove("dict\hotels.pkl")
                    with open("dict\hotels.pkl","wb") as f:
                        pickle.dump(HOTELS,f)

                sum_hotels+=1
                # if sum_hotels % 1000 == 0:
                #     if sum_hotels >= 2000:
                #         break
                #     time.sleep(910)
        

            print("Scraping:", url)
        except Exception as e:
            print("Error scraping", url, ":", str(e))
    
    # if driver:
    #     driver.quit()
    return sum_hotels, num, count


def main():

    with open("dict\hotels.pkl","rb") as f:
        HOTELS = pickle.load(f)
    
    sum, num, count = scrape_hotels(URLS, PROXIES, HOTELS)
    scrape_hotels(URLS, PROXIES, HOTELS)

    # os.remove("dict\hotels.pkl")
    # with open("dict\hotels.pkl","wb") as f:
    #     pickle.dump(HOTELS,f)

    print(f'Total {sum} hotels')
    print(num)
    print(count)
    print('finish')


def parser():

    with open("dict\hotels.pkl","rb") as f:
        HOTELS = pickle.load(f)
    
    sum, num, count = scrape_hotels(URLS, PROXIES, HOTELS)
    scrape_hotels(URLS, PROXIES, HOTELS)

    # os.remove("dict\hotels.pkl")
    # with open("dict\hotels.pkl","wb") as f:
    #     pickle.dump(HOTELS,f)

    # print(f'Total {sum} hotels')
    # print(num)
    # print(count)
    # print('finish')
    return sum, count

if __name__ == "__main__":
    main()