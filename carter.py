from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, time, zipfile, io, threading
from selenium.webdriver.support.ui import Select



def openwinchrome():
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    try:
        driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    except:
        try:
            lat_v=requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
            r = requests.get(f"https://chromedriver.storage.googleapis.com/{lat_v}/chromedriver_win32.zip")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()
            driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
        except Exception as e:
            print(e)
            input("[+] Please update your google chrome browser")
    return driver





def main(win,iters):
    
    driver=openwinchrome()
    for i in range(iters):

        #Close Chrome every 100 loops
        if i%100==0 and i:
            try:driver.quit()
            except:pass
            time.sleep(5)
            driver=openwinchrome()
            
        print(f'[+] Window#{win}, Iter#{i+1}')
        
        try:
            driver.get('https://www.seetickets.us/event/EVENTURL')
            element_present = EC.presence_of_element_located((By.XPATH, '(//li[div/div/div[text()="A"]]/div[5]/select)[1]'))
            WebDriverWait(driver, 10).until(element_present)
            Select(driver.find_element_by_xpath('(//li[div/div/div[text()="A"]]/div[5]/select)[1]')).select_by_index(1)
        except Exception as e:
            print('[+] A ticket not found on the website')
            continue
        
        try:
            driver.execute_script("arguments[0].click();", driver.find_element_by_id('checkoutbnt'))
            time.sleep(5)
        except:
            print('[+] Couldn\'t click on Checkout btn')
        
            




target_url=input('[+] Enter the test URL:')
instances=int(input('[+] How Many Windows in Parallel:') or "4")
iters=int(input('[+] How Many Iteration per Window:') or "1000")
#Open Chrome Once and Quit
driver=openwinchrome()
driver.quit()

for thd in range(1,instances+1):
    threading.Thread(target=main,args=(thd,iters,)).start()



