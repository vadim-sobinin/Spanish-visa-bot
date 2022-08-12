import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as wait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys





if __name__ == '__main__':

    email = "testmail@mailto.plus"

    driver = uc.Chrome()
    driver.get('https://blsspain-russia.com/moscow/apply_for.php')
    time.sleep(5)
    go_to_apply_form = driver.find_elements(By.CLASS_NAME, "appByIndFam")[-1].click()

    time.sleep(1)

    continue_btn = driver.find_element(By.LINK_TEXT, "Продолжить оформление записи").click()
    time.sleep(1)
    
    city_list = Select(driver.find_element(By.ID, "centre"))
    city_list.select_by_index(1)
    time.sleep(1)

    category_list = Select(driver.find_element(By.ID, "category"))
    category_list.select_by_index(1)
    time.sleep(1)

    phone_input = driver.find_element(By.ID, "phone").send_keys("9876543210")
    time.sleep(1)
    email_input = driver.find_element(By.ID, "email").send_keys(email)
    time.sleep(1)
    send_email_code = driver.find_element(By.ID, "verification_code").click()
    time.sleep(3)
    
    driver.switch_to.new_window('tab')
    
    driver.get("https://tempmail.plus/ru/#!")
    time.sleep(2)
    
    
    
    email_set = driver.find_element(By.ID, "pre_button").send_keys(Keys.BACKSPACE*20)
    time.sleep(1)
    email_set = driver.find_element(By.ID, "pre_button").send_keys("testmail")
    time.sleep(1)
    email_set = driver.find_element(By.ID, "pre_button").send_keys(Keys.ENTER)
    time.sleep(1)
    pin = driver.find_element(By.ID, "pin").send_keys("1234")
    verify_btn = driver.find_element(By.ID, "verify").click()
    time.sleep(2)
    last_mail = driver.find_element(By.CLASS_NAME, "mail").click()
    time.sleep(3)
    otp_link = driver.find_element(By.LINK_TEXT, "Click here to view your verification code").click()
    time.sleep(20)

#
#   Здесь нужно реализовать
#   получение OTP кода!
#

    time.sleep(10)

    
    driver.close()
    driver.switch_to.window('original_window')

    time.sleep(10)