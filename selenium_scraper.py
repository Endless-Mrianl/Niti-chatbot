import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def wait_for_element(driver, xpath, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except Exception as e:
        print(f"Error waiting for element: {e}")
        return None


def get_xpath_content(driver, xpath_expression):
    try:
        elements = driver.find_elements(By.XPATH, xpath_expression)
        if not elements:
           print(f"No elements found for XPath: {xpath_expression}")
        # Strip text and return non-empty texts
        return [element.text.strip() for element in elements if element.text.strip()]
    except Exception as e:
        print(f"Error retrieving XPath content: {e}")
        # Return an error message if something goes wrong
        return [f"Error: {e}"]

def scrape_case_data(case_type):
    url = 'https://njdg.ecourts.gov.in/hcnjdg_v2/'
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        
        print(f"Page title: {driver.title}")
        xpaths = {
            'civil case': {
                'total': '//*[@id="Cases_data"]/div[1]/div[1]/div/div[1]/span',
                '0 to 1 years': '//*[@id="agewisePendTbl"]/table/tbody/tr[3]/td[1]/span/a',
                '1 to 3 years': '//*[@id="agewisePendTbl"]/table/tbody/tr[5]/td[1]',
                # Add more XPaths for civil cases if needed
            },
            'criminal case': {
                'total': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[1]/span',
                '0 to 1 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[2]/td[3]/a',
                
                # Add more XPaths for criminal cases if needed
            }
        }
        for key, xpath in xpaths.get(case_type, {}).items():
            content = get_xpath_content(driver, xpath)
            print(f"XPath: {xpath} - Content: {content}")

        case_xpath = xpaths.get(case_type)
        if case_xpath:
            total_xpath = case_xpath.get('total')
            if total_xpath:
                total_content = get_xpath_content(driver, total_xpath)
                print(f"Extracted total cases: {total_content}")  # Debugging line

                case_data = f"Total cases: {total_content[0] if total_content else 'No data found'}\n"

                # Extract age range details
                for age_range, xpath in case_xpath.items():
                    if age_range != 'total':
                        content = get_xpath_content(driver, xpath)
                        print(f"Extracted {age_range}: {content}")  # Debugging line
                        case_data += f"{age_range}: {content[0] if content else 'No data found'}\n"
                
                # Print final case data before writing to file
                print(f"Final case data:\n{case_data}")  # Debugging line

                # Write data to file
                with open('case_details.txt', 'w') as file:
                    file.write(case_data)
        else:
            print(f"Invalid case type: {case_type}")  # Debugging line
            with open('case_details.txt', 'w') as file:
                file.write("No data available for the specified case type.")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        case_type = sys.argv[1].strip().lower()
    else:
        # Provide a default value if no case type is provided
        case_type = "civil"

    scrape_case_data(case_type)
