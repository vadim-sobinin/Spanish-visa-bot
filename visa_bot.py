import json
import undetected_chromedriver as uc
from time import sleep
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import re


from auth_data import API_key, email, phone #!!!!!!!!!!!!



if __name__ == "__main__":
    seconds = time.time()
    loop = 1
    count = 0
    driver = uc.Chrome()
    result_list = []

    def wait(elem_type, elem):
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((elem_type, elem)))

    # Blsspain Page
    def auth(city):
        initial_url = "https://blsspain-russia.com/moscow/apply_for.php"
        try:
            driver.get(initial_url)
            
        except:
            driver.close()
            driver.get(initial_url)

        wait(By.CLASS_NAME, "appByIndFam")
        driver.find_elements(By.CLASS_NAME, "appByIndFam")[-1].click()

        wait(By.LINK_TEXT, "Продолжить оформление записи")
        driver.find_element(By.LINK_TEXT, "Продолжить оформление записи").click()

        # hCaptcha
        data_sitekey = driver.find_element(By.CLASS_NAME, "h-captcha").get_attribute("data-sitekey")
        print(data_sitekey)
        URL = f"http://rucaptcha.com/in.php?key={API_key}&method=hcaptcha&sitekey={data_sitekey}&pageurl=https://blsspain-russia.com/moscow/book_appointment.php&json=1"
        response = requests.get(URL).json()
        print(response)
        request_id = response["request"]
        print("Request ID = " + request_id)
        
        
        wait(By.ID, "centre")
        city_list = Select(driver.find_element(By.ID, "centre"))
        city_list.select_by_visible_text(city)

        sleep(1)
        category_list = Select(driver.find_element(By.ID, "category"))
        category_list.select_by_visible_text("Обычная подача")

        wait(By.ID, "phone")
        driver.find_element(By.ID, "phone").send_keys(phone)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "verification_code").click()
        sleep(1)

        # Tempmail Page
        driver.switch_to.new_window("tab")
        driver.get("https://tempmail.plus/ru/#!")

        try:
            wait(By.ID, "pre_button")
            driver.find_element(By.ID, "pre_button").send_keys(Keys.BACKSPACE*20)
            driver.find_element(By.ID, "pre_button").send_keys("testmail")
            driver.find_element(By.ID, "pre_button").send_keys(Keys.ENTER)
            
            
        except:
            print("Mail already log-in")
        
        try:
            sleep(1)
            wait(By.ID, "pin")
            driver.find_element(By.ID, "pin").send_keys("1234")
            driver.find_element(By.ID, "verify").click()
        except:
            print("Don't need pin")
        wait(By.CLASS_NAME, "mail")
        driver.find_element(By.CLASS_NAME, "mail").click()
        wait(By.LINK_TEXT, "Click here to view your verification code")
        driver.find_element(By.LINK_TEXT, "Click here to view your verification code").click()
        

        # OTP Page
        driver.switch_to.window(driver.window_handles[2])

        wait(By.NAME, "email")
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        wait(By.CLASS_NAME, "blurry-text")
        otp_token = driver.find_element(By.CLASS_NAME, "blurry-text").get_attribute("textContent").split(" ")[3] # Переменная с токеном
        print("OTP Token:", otp_token)

        # Close OTP Page
        driver.close()

        # Blsspain Page
        driver.switch_to.window(driver.window_handles[0])
        sleep(1)

        driver.find_element(By.ID, "otp").send_keys(otp_token)

        
        
        sleep(5)
        
        URL = f"http://rucaptcha.com/res.php?key={API_key}&action=get&id={request_id}&json=1"
        print(URL)
        
        response = requests.get(URL).json()
        
        print(response)
        
        while response["status"] == 0:
            sleep(5)
            print("Not Ready Yet")
            response = requests.get(URL).json()
        
        
        print("Request Result: " + response["request"])
        
        captcha_response = response["request"]

        driver.execute_script(f"document.querySelector('textarea[name=\"g-recaptcha-response\"]').innerHTML = '{captcha_response}'")
        driver.execute_script(f"document.querySelector('textarea[name=\"h-captcha-response\"]').innerHTML = '{captcha_response}'")
        
        try: 
            driver.find_element(By.XPATH, '//a[@onclick="setCookie();"]').click()
        # wait(By.NAME, "save")
        # driver.find_element(By.NAME, "save").click()
        except:
            print("No cookie pop-up")
        wait(By.XPATH, '//input[@onclick="return validateFrm();"]')
        driver.find_element(By.XPATH, '//input[@onclick="return validateFrm();"]').click()
        
        #Agree BTN
        wait(By.NAME, "agree")
        driver.find_element(By.NAME, "agree").click()
        sleep(2)
            
    
    def check_data_loop():
        try:
            sleep(2)
            driver.find_element(By.ID, "app_date").is_displayed()
            
            
            
            driver.find_element(By.ID, "app_date").click()
            wait(By.CLASS_NAME, "table-condensed")
            date_table = driver.find_element(By.CLASS_NAME, "table-condensed")
            # count = count + 1
            
            fullCapicity_dates = re.search(r'var fullCapicity_dates = (.*?);', driver.page_source).group().split(" = ")[1].replace("[", "").replace("]", "").replace('"', '').replace(";", "").split(",")

            available_dates = re.search(r'var available_dates = (.*?);', driver.page_source).group().split(" = ")[1].replace("[", "").replace("]", "").replace('"', '').replace(";", "").split(",")
            
            
            
            if (len(available_dates) <= 1):
                result = "No"
            
            else:
                result = "YES"
            
            result_list.append(
                {
                    "result" : result,
                    # "number" : count,
                    "time" : time.strftime('%H:%M:%S'),
                    "available dates" : available_dates,
                    "full capicity dates" : fullCapicity_dates
                }
            )
            
            with open("log.json", "w") as file:
                json.dump(result_list, file, indent=4, ensure_ascii=False)
            
            date_table.screenshot(f"./img/{result}__{time.strftime('%H:%M:%S')}.png")
            
            
            print("[INFO] Screen and log saves successfuly!")
            print("Waiting 30 seconds for refresh...")
            

            sleep(30)
            driver.refresh()
        except Exception as ex:
            print(ex)
            sleep(3)
            auth("Москва")
    
    
    auth("Москва")
    
    while loop != 0:
        check_data_loop()
        sleep(3)
    