from email import message
import json
import token
import undetected_chromedriver as uc
from time import sleep
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import re
from notifiers import get_notifier

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from auth_data import API_key, email, phone, telegram_bot_token, user_id #!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



if __name__ == "__main__":
    seconds = time.time()
    loop = 1
    count = 0
    driver = uc.Chrome()
    result_list = []
    
    cities_list = ["Москва", "Казань", "Екатеринбург", "Ростов-на-Дону", "Новосибирск", "Нижний Новгород", "Самара"]
    window_handlers = {
        "Москва" : 0,
        "Казань" : 0,
        "Екатеринбург" : 0,
        "Ростов-на-Дону" : 0,
        "Новосибирск" : 0,
        "Нижний Новгород" : 0,
        "Самара" : 0,
        "Почта" : 0
    }

    request_id = dict(window_handlers)
    otp_token = dict(window_handlers)

    telegram = get_notifier('telegram')

    restart_city = ""
    
            
    def check_exists_by_xpath(xpath):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True
    
    def check_exists_by_id(id):
        try:
            driver.find_element(By.ID, id)
        except NoSuchElementException:
            return False
        return True
    
    def wait(elem_type, elem):
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((elem_type, elem)))
            
        
        except:
            if (check_exists_by_id("cf-challenge-hcaptcha-wrapper") and check_exists_by_id("cf-challenge-running")):
                current_url = driver.current_url
                driver.close()
                driver.switch_to.new_window("tab")
                driver.get(current_url)
            else: 
                driver.refresh()
            print("Error... Starting this page again...")
            raise Exception("Restarting page...")
            


    def auth():
        
        #Проверяем нет ли открытых вкладок с прошлых попыток бота
        if len(driver.window_handles) != 1:
            while len(driver.window_handles) != 1:
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
        
        
        # Открываем страницы городов и отправляем капчи на решение
        for city in cities_list:
            initial_auth(city) 
        telegram.notify(token=telegram_bot_token, chat_id=user_id, message="Start authorization!")
        # Получаем OTP ключи для каждого города
        for city in cities_list:
            OTP_auth(city)
        
        # Ждём решения капчи и завершаем авторизацию
        # for city in cities_list:
        #     wait_for_captha(city) 

    # Blsspain Page
    def initial_auth(city):
        
        initial_url = "https://blsspain-russia.com/moscow/apply_for.php"
        try:
            driver.get(initial_url)
            
        except:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.new_window()
            driver.get(initial_url)
            

        window_handlers[city] = driver.current_window_handle #Записали ID текущей вкладки под названием города
        
        wait(By.CLASS_NAME, "appByIndFam")
        driver.find_elements(By.CLASS_NAME, "appByIndFam")[-1].click()

        wait(By.LINK_TEXT, "Продолжить оформление записи")
        driver.find_element(By.LINK_TEXT, "Продолжить оформление записи").click()

        # hCaptcha
        wait(By.CLASS_NAME, "h-captcha")
        data_sitekey = driver.find_element(By.CLASS_NAME, "h-captcha").get_attribute("data-sitekey")
        print(data_sitekey)
        URL = f"http://rucaptcha.com/in.php?key={API_key}&method=hcaptcha&sitekey={data_sitekey}&pageurl=https://blsspain-russia.com/moscow/book_appointment.php&json=1"
        response = requests.get(URL).json()
        print(response)
        request_id[city] = response["request"] # Отправили капчу на распознавание и записали ID запроса для ЭТОЙ вкладки
        print(f"{city} Request ID = " + request_id[city])
        
        
        wait(By.ID, "centre") # Выбрали город
        city_list = Select(driver.find_element(By.ID, "centre"))
        city_list.select_by_visible_text(city)
        driver.switch_to.new_window('tab') # Открыли новую вкладку для следующего города
        
        
    def OTP_auth(city):
        driver.switch_to.window(window_handlers[city]) #Переключаемся на вкладку нужного города
        wait(By.ID, "category")
        category_list = Select(driver.find_element(By.ID, "category"))
        category_list.select_by_visible_text("Обычная подача")

        wait(By.ID, "phone")
        driver.find_element(By.ID, "phone").send_keys(phone)
        driver.find_element(By.ID, "email").send_keys((email[city]))
        driver.find_element(By.ID, "email").send_keys(("@mailto.plus"))
        
        try: 
            driver.find_element(By.XPATH, '//a[@onclick="setCookie();"]').click()
        except:
            print("No cookie pop-up")
        
        driver.find_element(By.ID, "verification_code").click()
        sleep(1)

        # Tempmail Page
        driver.switch_to.new_window("tab")
        window_handlers["Почта"] = driver.current_window_handle
        driver.get("https://tempmail.plus/ru/#!")

        try:
            wait(By.ID, "pre_button")
            driver.find_element(By.ID, "pre_button").send_keys(Keys.BACKSPACE*20)
            driver.find_element(By.ID, "pre_button").send_keys(email[city])
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
        
        wait(By.XPATH, "//span[@class='font-weight-bold']")
        driver.find_element(By.XPATH, "//span[@class='font-weight-bold']").click()
        wait(By.LINK_TEXT, "Click here to view your verification code")
        driver.find_element(By.LINK_TEXT, "Click here to view your verification code").click()
        driver.close()
        
        #Select and switch to OTP Page
        # for window_handler in driver.window_handles:
        #     if window_handler not in window_handlers.values():
        #         driver.switch_to.window(window_handler)
        #         break

        # OTP Page
        driver.switch_to.window(driver.window_handles[-1])
        wait(By.XPATH, "//input[@type='text']")
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys((email[city]))
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(("@mailto.plus"))
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        wait(By.CLASS_NAME, "blurry-text")
        otp_token[city] = driver.find_element(By.CLASS_NAME, "blurry-text").get_attribute("textContent").split(" ")[3] # Переменная с токеном
        print(f"{city} OTP Token:", otp_token[city])

        # Close OTP Page
        driver.close()

        # Blsspain Page
        driver.switch_to.window(window_handlers[city])
        sleep(1)

        driver.find_element(By.ID, "otp").send_keys(otp_token[city])

        
        
    # def wait_for_captha(city):
        
        driver.switch_to.window(window_handlers[city])
        URL = f"http://rucaptcha.com/res.php?key={API_key}&action=get&id={request_id[city]}&json=1"
        print(URL)
        
        response = requests.get(URL).json()
        
        print(response)
        
        while response["status"] == 0:
            sleep(5)
            print(f"{city} Captcha Not Ready Yet")
            response = requests.get(URL).json()
        
        
        print("Request Result: " + response["request"])
        
        captcha_response = response["request"]

        driver.execute_script(f"document.querySelector('textarea[name=\"g-recaptcha-response\"]').innerHTML = '{captcha_response}'")
        driver.execute_script(f"document.querySelector('textarea[name=\"h-captcha-response\"]').innerHTML = '{captcha_response}'")
        
        try: 
            driver.find_element(By.XPATH, '//a[@onclick="setCookie();"]').click()
        except:
            print("No cookie pop-up")
        
        wait(By.XPATH, '//input[@onclick="return validateFrm();"]')
        driver.find_element(By.XPATH, '//input[@onclick="return validateFrm();"]').click()
        
        #Agree BTN
        wait(By.NAME, "agree")
        driver.find_element(By.NAME, "agree").click()
        
        
        
    def resultYes():
        while True:
            telegram.notify(token=telegram_bot_token, chat_id=user_id, message="Есть место, Хозяин!")
            sleep(10)        
    
    
    
    def check_data_loop(cit):
        try:
            driver.switch_to.window(window_handlers[cit])
            
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
            result_list = []
            result_list.append(
                {
                    "result" : result,
                    "city" : cit,
                    # "number" : count,
                    "time" : time.strftime('%H:%M:%S'),
                    "available dates" : available_dates,
                    "full capicity dates" : fullCapicity_dates
                }
            )
            
            with open(f"./cities/{cit}/log.json", "w") as file:
                json.dump(result_list, file, indent=4, ensure_ascii=False)
            
            date_table.screenshot(f"./cities/{cit}/img/{result}__{time.strftime('%H:%M:%S')}.png")
            
            
            print(f"[INFO] {cit} Screen and log saves successfuly!")
            
            if result == "YES":
                resultYes()
            
            
            driver.refresh()
        except Exception as ex:
            print(ex)
            sleep(3)
            auth()
    
    
    
    auth()
    

    
    while loop != 0:
        for citya in cities_list:
            check_data_loop(citya)
        sleep(15)
    