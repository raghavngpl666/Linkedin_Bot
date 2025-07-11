import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

def linkedin_login(email, password):
    """
    Automates the LinkedIn login process using Selenium WebDriver.

    Args:
        email (str): The user's LinkedIn email address.
        password (str): The user's LinkedIn password.
    """
 
    chrome_options = webdriver.ChromeOptions()
    # Uncomment the line below if you want to run Chrome in headless mode (without a UI)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("start-maximized") 
    chrome_options.add_argument("disable-infobars")  
    chrome_options.add_argument("--disable-extensions")  
    chrome_options.add_argument("--incognito") 

    try:
        # Initialize the Chrome WebDriver
        print("Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30) # Set page load timeout to 30 seconds
        print("WebDriver initialized successfully.")

        # --- Navigate to LinkedIn Login Page ---
        linkedin_login_url = "https://www.linkedin.com/login"
        print(f"Navigating to: {linkedin_login_url}")
        driver.get(linkedin_login_url)
        print("Page loaded. Waiting for login elements...")

        wait = WebDriverWait(driver, 20) 

        try:
            email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
            sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            print("Login elements found.")
        except TimeoutException:
            print("Error: Login fields or sign-in button not found after waiting.")
            print("This might be due to a page layout change or slow loading.")
            driver.quit()
            return False

        # --- Enter Credentials ---
        print("Entering email and password...")
        email_field.send_keys(email)
        password_field.send_keys(password)
        time.sleep(1) 

        # --- Click Sign In Button ---
        print("Clicking 'Sign In' button...")
        sign_in_button.click()
        print("Sign In button clicked. Waiting for redirection...")


        try:

            wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]")))
            print("Login successful! Redirected to feed (search bar found).")

            screenshot_path = "linkedin_login_success.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to: {os.path.abspath(screenshot_path)}")
            return True

        except TimeoutException:
            print("Login verification failed (feed elements not found).")
            # This could be due to incorrect credentials or a CAPTCHA.
            # --- Handle Incorrect Credentials or CAPTCHA ---
            print("Checking for common error messages or CAPTCHA...")
            try:
                # Check for incorrect credentials message
                error_message_element = driver.find_element(By.XPATH, "//*[contains(text(), 'incorrect') or contains(text(), 'wrong password')]")
                print(f"Login failed: {error_message_element.text}")
                return False
            except NoSuchElementException:
                # No explicit error message found, check for CAPTCHA
                print("No explicit incorrect credentials message. Checking for CAPTCHA...")
                # Common CAPTCHA indicators: iframe with reCAPTCHA, specific text, or a challenge div
                try:
                    captcha_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Verify your identity') or contains(text(), 'captcha') or @id='challenge-form']")
                    print("CAPTCHA detected! Please complete the CAPTCHA manually in the browser window.")
                    print("The script will pause for 60 seconds. Complete the CAPTCHA and then press Enter in the console to resume.")
                    input("Press Enter to continue after solving CAPTCHA...")
                
                    print("Resuming script after manual CAPTCHA intervention.")
                    # You might want to add another verification step here after CAPTCHA.
                    return True # Assuming user solved CAPTCHA and is now logged in
                except NoSuchElementException:
                    print("Neither incorrect credentials message nor common CAPTCHA indicators found.")
                    print("Login might have failed for an unknown reason or the page is still loading.")
                    return False
        except WebDriverException as e:
            print(f"A WebDriver error occurred during verification: {e}")
            return False

    except WebDriverException as e:
        print(f"An error occurred with the WebDriver (e.g., ChromeDriver not found or incompatible version): {e}")
        print("Please ensure ChromeDriver is installed and its path is correctly configured in your system's PATH environment variable.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    finally:
        if 'driver' in locals() and driver:
            print("Closing browser...")
            driver.quit()

if __name__ == "__main__":
    # --- IMPORTANT: Replace with your actual LinkedIn credentials ---

    # DO NOT COMMIT YOUR ACTUAL CREDENTIALS TO VERSION CONTROL!
    my_email = "enter email" # <--- REPLACE THIS
    my_password = "enter password" # <--- REPLACE THIS

    if my_email == "your_linkedin_email@example.com" or my_password == "your_linkedin_password":
        print("\n--- WARNING ---")
        print("Please update 'my_email' and 'my_password' variables in the script with your actual LinkedIn credentials.")
        print("The script will not proceed with placeholder credentials.")
        print("-----------------\n")
    else:
        print("Attempting LinkedIn login...")
        success = linkedin_login(my_email, my_password)
        if success:
            print("\nScript finished: LinkedIn login process completed successfully (or CAPTCHA handled).")
        else:
            print("\nScript finished: LinkedIn login process failed.")

