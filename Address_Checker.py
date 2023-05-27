from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from addresses import adr
import time

#=================================settings==============================================
logs_with_balance = ""  # insert a path in which will be stored addresses WITH balance
logs_without_balance = "" # insert a path in which will be stored addresses WITHOUT balance
balacne_threshold = 100  # USD
separator = 60*"="
#=======================================================================================

# setting for Linux
# driver_path = '/home/shereshevsky/Downloads/chromedriver'
# brave_path = '/usr/bin/brave-browser'
# s = Service(driver_path)
# option = webdriver.ChromeOptions()
# option.binary_location = brave_path
# driver = webdriver.Chrome(service=s, options = option)
# driver.get('https://portfolio.nansen.ai/dashboard')

#Settings for Windows
driver_path = '' # input your chromedriver path
brave_path = '' # input yout brabe path 
s = Service(driver_path)
option = webdriver.ChromeOptions()
option.binary_location = brave_path
#option.add_experimental_option('excludeSwitches', ['enable-logging'])  >  enable/disable logs
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://portfolio.nansen.ai/dashboard')

# First Address
first_address = "0x657651B3745eb5686B37ad298D920146a1fe6eAd"

# Inserting address in search bar
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, ":r1o:"))
)
element.send_keys(first_address)

# Click on search 
time.sleep(3)
click_to_check = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/form/div[2]/div/div/button")
click_to_check.click()

# Waiting "loading" to disapear -> all token loaded
loading_element1 = WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/div/div/div[2]/div/div[3]/div[3]/div[1]/div[1]/div/div[2]/p[2]"))) 
WebDriverWait(driver, 240).until(EC.staleness_of(loading_element1))

# Checking Balance
balance = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/h1").text
balance1 = float(balance.replace('$', '').replace(",", ""))

print(f'${balance1}')
# If balance is more than setted threshold...
if balance1 > 100:
    print(f"{first_address}")
    print(separator)
    with open(logs_with_balance, "w") as file:
        file.writelines(f'${balance1} \n{first_address} \n{separator}\n')
# If balance is less than setted threshold...   
else:
    print(f"{first_address}")
    print(separator)
    with open(logs_without_balance, "w") as file:
        file.writelines(f'${balance1} \n{first_address} \n{separator}\n')

time.sleep(3)

# I continue with checking
for x in adr:
    # Click on search
    time.sleep(2)                                     
    next_coin_search = WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/header/div/div[1]/button[1]")))
    time.sleep(1)
    next_coin_search.click()
    time.sleep(1)  

    # Inserting address in search bar
    paste_coin_address = WebDriverWait(driver, 240).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[placeholder='Search by address, ENS, TNS or shared code']")))
    paste_coin_address.send_keys(x)
    time.sleep(1)
    paste_coin_address.send_keys(Keys.ENTER)
    
    # Waiting "loading" to disapear -> all token loaded                
    loading_element1 = WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/div/div/div[2]/div/div[3]/div[3]/div[1]/div[1]/div/div[2]/p[2]"))) 
    WebDriverWait(driver, 240).until(EC.staleness_of(loading_element1))
    
    # Checking Balance
    bal = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/h1").text
    bal1 = float(bal.replace('$', '').replace(',',''))
    print(f'${bal1}')

    # If balance is more than setted threshold...
    if bal1 > balacne_threshold:
        print(f"{x}")
        print(separator)
        with open(logs_with_balance, "a") as file:
            file.writelines(f'${bal1} \n{x} \n{separator}\n')
    # If balance is less than setted threshold...
    else:
        print(f"{x}")
        print(separator)
        with open(logs_without_balance, "a") as file:
            file.writelines(f'${bal1} \n{x} \n{separator}\n')
        
    
   




