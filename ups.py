import os
import time
from datetime import datetime
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def do_the_thing():
    while True:
        get_ups_status()
        time.sleep(1800)


def get_ups_status():
    driver = webdriver.Chrome()
    driver.get(URL)
    timeout = 5

    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "p.jss281"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        pass

    elem = driver.find_element(By.CSS_SELECTOR, "svg + p")
    slots = int(elem.text[0:1])
    driver.quit()

    send_mail(slots)

    if slots == 0:
        dt = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{dt}] No road test slots are currently available. Sleeping for 30 minutes.")
    else:
        print("OH MY GOD!!! GO! GO! GO!")


def send_mail(slots: int) -> None:
    if slots == 0:
        msg = MIMEText("Sorry, buddy. No current slots for road tests at UPS.", "plain")
        msg["Subject"] = "There are no road test slots open at UPS"
    else:
        msg = MIMEText(f"Get going, buddy. There's an opening!\n\n{URL}", "plain")
        if slots == 1:
            msg["Subject"] = f"There is {slots} road test slot open at UPS!"
        else:
            msg["Subject"] = f"There are {slots} road test slots open at UPS!"

    conn = SMTP(os.getenv("MAIL_HOST"))
    conn.set_debuglevel(False)
    conn.login("charlie@griefer.com", os.getenv("MAIL_PW"))

    try:
        conn.sendmail("charlie@griefer.com", "charlie@griefer.com", msg.as_string())
    finally:
        conn.quit()


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv("UPS_URL")
    do_the_thing()
