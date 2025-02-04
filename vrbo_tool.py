# import libraries
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = "https://www.vrbo.com/search?regionId=235&semcid=VRBO-US.B.GOOGLE.BD-c-EN.VR&semdtl=a118921852681.b1145236417018.g1kwd-522436780534.e1c.m1CjwKCAiA74G9BhAEEiwA8kNfpQI3jfqFv5rIIHkaPzgVrlALK5ybAW4IImA5xRUpnmTkYFzWLtfjJxoCygwQAvD_BwE.r12e213678c473a12ebda4545133f2c07ecb5fc68c81df9a7bed9eff41fcdc4ffc.c1ioSXP-1MdtLmUk2KclVEuw.j19073655.k121160.d1639955023346.h1p.i1.l1.n1.o1.p1.q1.s1.t1.x1.f1.u1.v1.w1&gad_source=1&gclid=CjwKCAiA74G9BhAEEiwA8kNfpQI3jfqFv5rIIHkaPzgVrlALK5ybAW4IImA5xRUpnmTkYFzWLtfjJxoCygwQAvD_BwE&destination=North%20Carolina%2C%20United%20States%20of%20America&isInvalidatedDate=false&theme=&userIntent=&adults=2&children=&latLong=35.719758%2C-79.453125&mapBounds=&pwaDialog=&amenities=&sort=RECOMMENDED"


def open_chrome(url):
    """
    Opens a Chrome browser and navigates to the specified URL.
    This function initializes a Chrome WebDriver instance, navigates to the given URL,
    and attempts to find and click a button with a specific class name.
    Args:
        url (str): The URL to navigate to.
    Returns:
        WebDriver: The Chrome WebDriver instance after performing the operations.
    """

    driver = Chrome()
    # Open the url
    driver.get(url)

    # Find and click the done button
    done_button = driver.find_elements(
        By.XPATH,
        "//*[@class = 'uitk-button uitk-button-medium uitk-button-has-text uitk-button-primary uitk-layout-flex-item']",
    )
    done_button[0].click()

    return driver


def collect_urls(driver):
    """
    Collects all property URLs from a scrollable section of a webpage using a Selenium WebDriver.
    Args:
        driver (selenium.webdriver): The Selenium WebDriver instance used to interact with the webpage.
    Returns:
        list: A list of WebElement objects representing the collected property links.
    The function performs the following steps:
    1. Initializes an empty list to store all the collected links.
    2. Identifies the scrollable section of the webpage.
    3. Iterates over the pages by scrolling through the scrollable section in quarters.
    4. Collects the property links on each page and adds them to the list.
    5. Clicks the "Next" button to navigate to the next page.
    6. Repeats the process until a final message indicating no more properties is found.
    Note:
        The function assumes that the webpage has a specific structure with identifiable elements
        such as the scrollable section, property links, "Next" button, and final message.
    """

    all_links = []  # This will have all the links

    # Create the scrollable section
    scrollable_section = driver.find_element(
        By.XPATH,
        "//*[@class = 'uitk-layout-grid-item scrollable-result-section uitk-scrollable uitk-scrollable-vertical']",
    )

    len_final_message = 0  # The ending factor

    page_num = 1  # Print pages

    # for loop to itirate over pages
    while len_final_message == 0:
        time.sleep(5)  # Till the new page loads
        for index in range(4):  # 4 steps: 25%, 50%, 75%, 100%
            scroll_height = driver.execute_script(
                "return arguments[0].scrollHeight;", scrollable_section
            )
            scroll_position = (index + 1) * (scroll_height / 4)  # Move in quarters

            driver.execute_script(
                "arguments[0].scrollTop = arguments[1];",
                scrollable_section,
                scroll_position,
            )

            time.sleep(3)  # Allow content to load

        links = driver.find_elements(
            By.XPATH, "//*[@class = 'uitk-card-link']"
        )  # Links in the page

        # Extract href attributes
        all_urls = [link.get_attribute("href") for link in links]

        all_links.extend(all_urls)  # ADD the values to the entire links list

        # Next pages button
        next_button = driver.find_elements(
            By.XPATH,
            "//*[@class = 'uitk-button uitk-button-medium uitk-button-only-icon uitk-button-primary uitk-spacing uitk-spacing-margin-inlinestart-four']",
        )
        driver.execute_script(
            "arguments[0].click();", next_button[0]
        )  # Clicks the next button

        # End loop factor is the appearing of final message
        final_message = driver.find_elements(
            By.XPATH,
            '//h3[text()="We don\'t have any more properties that match your search criteria"]',
        )

        len_final_message = len(final_message)

        print("This is the page number: ", page_num)

    return all_links


def main(url):
    driver = open_chrome(url)
    all_links = collect_urls(driver)

    links_df = pd.DataFrame({"links": all_links})

    links_df.to_csv("vrbo_links.csv", index=False)

    return all_links
