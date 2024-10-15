from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time

def get_xpath_content(driver, xpath_expression):
    try:
        # Find the element using the XPath expression
        elements = driver.find_elements(By.XPATH, xpath_expression)
        # Extract text content from each element found
        return [element.text.strip() for element in elements if element.text.strip()]
    except Exception as e:
        return [f"Error: {e}"]

def main():
    # URL of the website
    url = 'https://njdg.ecourts.gov.in/hcnjdgnew/?p=main/index'
    
    # Set up Firefox options for headless mode
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run in headless mode

    # Set up the WebDriver
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    try:
        # Open the webpage
        driver.get(url)

        # Get user input for the case type
        case_type = input("Enter case type: ").strip().lower()

        # Define XPath expressions for different case types and detailed queries
        xpaths = {
            'civil case': {
                'total': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div[1]/span',
                'civil cases more than 1 year old': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[1]/span[1]',
                '0 to 1 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div[1]/span',
                '1 to 3 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/a',
                '3 to 5 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[4]/td[2]/a',
                '5 to 10 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[5]/td[2]/a',
                '10 to 20 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[6]/td[2]/a',
                '20 to 30 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[7]/td[2]/a',
                'above 30 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[8]/td[2]/a',
            },
            'criminal case': {
                'total': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[1]/span',
                'criminal cases more than 1 year old': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/span[1]',
                '0 to 1 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[2]/td[3]/a',
                '1 to 3 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[3]/td[3]/a',
                '3 to 5 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[4]/td[3]/a',
                '5 to 10 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[5]/td[3]/a',
                '10 to 20 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[6]/td[3]/a',
                '20 to 30 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[7]/td[3]/a',
                'above 30 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[8]/td[3]/a',
            },
            'total case': {
                'total': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[1]/div[1]/span',
                'cases more than 1 year old': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[3]/div/div/div/div[1]/div[1]/span[1]',
                '0 to 1 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[2]/td[4]/a',
                '1 to 3 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[3]/td[4]/a',
                '3 to 5 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[4]/td[4]/a',
                '5 to 10 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[5]/td[4]/a',
                '10 to 20 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[6]/td[4]/a',
                '20 to 30 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[7]/td[4]/a',
                'above 30 years': '/html/body/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div[2]/div[6]/div/div[3]/div[2]/table/tbody/tr[8]/td[4]/a',
            },
            
            # Add more case types and their details if needed
        }
        
        # Select XPath dictionary based on user input
        case_xpath = xpaths.get(case_type, None)
        
        if case_xpath:
            # Print the total cases
            total_xpath = case_xpath.get('total')
            if total_xpath:
                total_content = get_xpath_content(driver, total_xpath)
                print("Total:", total_content[0] if total_content else "No data found")
            
            # Print the detailed age range data
            for age_range, xpath in case_xpath.items():
                if age_range != 'total':
                    content = get_xpath_content(driver, xpath)
                    print(f"{age_range}: {content[0] if content else 'No data found'}")
        else:
            print("No data available for the specified case type or invalid input.")
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
