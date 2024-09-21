from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Specify the path to ChromeDriver
service = Service('/usr/local/bin/chromedriver')  # Update path accordingly

# Initialize WebDriver
driver = webdriver.Chrome(service=service)

# Open the website
driver.get("http://localhost:8000/login.html")

# Test with valid credentials
def test_valid_login():
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    username_field.send_keys("validUsername")
    password_field.send_keys("validPassword")
    
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for response

    try:
        logout_button = driver.find_element(By.ID, "logout")
        print("Valid login test passed.")
    except:
        print("Valid login test failed.")

# Test with invalid credentials
def test_invalid_login():
    driver.refresh()  # Refresh the page
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    username_field.send_keys("invalidUsername")
    password_field.send_keys("invalidPassword")
    
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for response

    try:
        error_message = driver.find_element(By.ID, "error")
        print("Invalid login test passed.")
    except:
        print("Invalid login test failed.")

# Run the tests
test_valid_login()
test_invalid_login()

# Close the browser
driver.quit()
