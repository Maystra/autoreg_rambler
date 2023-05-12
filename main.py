from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from urllib.parse import urlparse, parse_qs
import undetected_chromedriver as uc
import time
import names
import random
import string
from fake_headers import Headers


def click_verify(driver):
    try:
        iframe = driver.find_element(By.XPATH, "//iframe[@title='Виджет с флажком для проверки безопасности hCaptcha']")
        driver.switch_to.frame(iframe)
        checkbox = driver.find_element(
            by=By.XPATH,
            value="//div[@id='anchor']",
        )

        if checkbox:
            checkbox.click()

    except Exception as e:
        print(e)
    finally:
        driver.switch_to.default_content()


def random_password(length):
    password = ''.join(random.choice(string.ascii_letters+string.digits) for x in range(length))
    if not has_numbers(password):
        password = password[:-1] + "1"
    return password


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


for i in range(5):
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
    header_dict = header.generate()

    # Set up Chrome options and undetected driver
    options = uc.ChromeOptions()
    #options.add_argument('Accept-Encoding={}'.format(header_dict['Accept-Encoding']))
    #options.add_argument('User-Agent={}'.format(header_dict['User-Agent']))
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    #options.add_argument("--disable-extensions")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en")
    #options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
      'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    # Navigate to rambler.ru and click on registration
    driver.get("https://id.rambler.ru/login-20/mail-registration?rname=mail&theme=&session=false&back=https%3A%2F%2Fmail"
               ".rambler.ru%2F&param=embed&iframeOrigin=https%3A%2F%2Fmail.rambler.ru")
    #  registration_link = driver.find_element(By.XPATH, '//*[@id="mainmenu"]/li[7]/a')
    #  registration_link.click()

    wait = WebDriverWait(driver, 40)
    wait_short = WebDriverWait(driver, 1)

    time.sleep(5)

    user_name = names.get_full_name(gender='male').replace(" ", "_").lower() + str(random.randint(100, 10000))
    user_password = random_password(12)
    user_real_name = "Acc"
    secret_question = "Почтовый индекс ваших родителей"
    secret_answer = str(random.randint(1000, 9999))
    gender = "Женский"
    birthday = ("1", "Январь", "1999")
    city = "Москва"

    # Fill out registration form
    email_field = driver.find_element(By.XPATH, '//*[@id="reg_login"]')
    email_field.send_keys(user_name)

    password_field = driver.find_element(By.XPATH, '//*[@id="reg_new_password"]')
    password_field.send_keys(user_password)

    confirm_password_field = driver.find_element(By.XPATH, '//*[@id="reg_confirm_password"]')
    confirm_password_field.send_keys(user_password)

    secret_answer_field = driver.find_element(By.XPATH, '//*[@id="reg_answer"]')
    secret_answer_field.send_keys(secret_answer)

    click_verify(driver)

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@data-cerber-id="login_form::main::login_button"]')))
    continue_button.click()

    register_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@data-cerber-id="registration_form::step_2::add_later"]')))
    register_button.click()

    reg_complete = wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Регистрация успешно завершена"))

    driver.get("https://mail.rambler.ru/folder/INBOX")

    mail = user_name + "@rambler.ru"

    with open("reg_mails.txt", "a") as f:
        f.write(f"\n{mail}:{user_password} ; {secret_answer}")
        f.close()

    driver.switch_to.new_window('tab')
    driver.get("https://account.battle.net/creation/flow/creation-full")

    #country_select = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="capture-country"]'))))
    #country_select.select_by_value("Kazakhstan")
    #b_day = driver.find_element(By.XPATH, '//*[@name="dob-day"]')
    #b_day.send_keys("01")
    #b_month = driver.find_element(By.XPATH, '//*[@name="dob-month"]')
    #b_month.send_keys("01")
    #b_year = driver.find_element(By.XPATH, '//*[@name="dob-year"]')
    #b_year.send_keys("1999")
    #confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flow-form-submit-btn"]')))
    #confirm_button.click()
    #time.sleep(0.5)
    #first_name = driver.find_element(By.XPATH, '//*[@id="capture-first-name"]')
    #first_name.send_keys(user_real_name)
    #last_name = driver.find_element(By.XPATH, '//*[@id="capture-last-name"]')
    #last_name.send_keys(user_real_name)
    #confirm_button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flow-form-submit-btn"]')))
    #confirm_button2.click()
    #time.sleep(0.5)
    #email_input = driver.find_element(By.XPATH, '//*[@id="capture-email"]')
    #email_input.send_keys(mail)
    #confirm_button3 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flow-form-submit-btn"]')))
    #confirm_button3.click()
    #time.sleep(0.5)
    #agreement = driver.find_element(By.XPATH, '//*[@name="tou-agreements-implicit"]')
    #agreement.click()
    #confirm_button4 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flow-form-submit-btn"]')))
    #confirm_button4.click()
    #time.sleep(0.5)
    #password_input = driver.find_element(By.XPATH, '//*[@id="capture-password"]')
    #password_input.send_keys(user_password)
    #confirm_button5 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flow-form-submit-btn"]')))
    #confirm_button5.click()
    #time.sleep(0.5)
    #confirm_button6 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flow-form-submit-btn"]')))
    #confirm_button6.click()

    input("Press Enter to continue...")

    driver.quit()
