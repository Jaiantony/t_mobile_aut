from flask import Flask
from flask import render_template, request
import time
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint


# Function to Generate random 10 digit mobile number
def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


app = Flask(__name__)


@app.route('/email', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        street_name = request.form["street_Name"]
        zip_code = request.form['zip_Code']
        url = "https://www.t-mobile.com/isp/eligibility?icid=HE__19HMEINTPL_D2U90RACRINA9I116498&channel=retail"
        # options = webdriver.ChromeOptions()
        # options.add_argument("no-sandbox")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=800,600")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver')
        driver.get(url)
        time.sleep(2)
        driver.implicitly_wait(10)

        # To send the dealer code to the UI
        driver.find_element(By.XPATH, '//*[@id="mat-input-2"]').send_keys('2253916')
        time.sleep(2)
        driver.implicitly_wait(2)

        # To find the submit button
        submit = driver.find_element(By.XPATH,
                                     value='//*[@id="mat-dialog-0"]/isp-retail-modal/mat-dialog-actions/button[2]')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.implicitly_wait(2)

        # To find the mobile no field
        mobile_number = driver.find_element(By.XPATH, '//*[@id="mat-input-0"]')
        time.sleep(2)
        driver.implicitly_wait(2)
        mobile_number.send_keys(random_with_N_digits(10))
        time.sleep(2)

        # To find the address field
        address = driver.find_element(By.XPATH, '//*[@id="mat-input-1"]')
        time.sleep(2)
        address_data = f'{street_name},{zip_code}'
        address.send_keys(address_data)
        driver.implicitly_wait(10)
        time.sleep(10)
        address.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.implicitly_wait(2)

        # To find the availability of the address
        button = driver.find_element(By.XPATH, '//*[@id="form"]/form/div/button')
        button.send_keys(Keys.ENTER)
        driver.implicitly_wait(2)
        time.sleep(5)
        # To find the result
        try:
            result = driver.find_element(By.XPATH,value='/html/body/isp-root/div[1]/isp-root/isp-eligibility/isp-eligibility-form/mat-card/form/section[3]/div/button[2]/span')

            result_data = result.text
        except:
            result_data="Available"
        return render_template('result.html', result=result_data, address=address_data)

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
