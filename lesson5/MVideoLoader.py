from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class MVideoLoader:

    def load_goods(self, driver: webdriver.Chrome):
        driver.get('https://www.mvideo.ru')

        # Scroll the shelf group into view to initiate load
        shelf = driver.find_element(By.CSS_SELECTOR, 'mvid-shelf-group')
        ActionChains(driver).move_to_element(shelf).perform()
        # ..scroll down a little more
        driver.execute_script("window.scrollTo(0, window.scrollY + 200)")

        # Wait until buttons appear
        buttons_selector = 'mvid-shelf-group mvid-switch-shelf-tab-selector mvid-carousel .mvid-carousel-inner button'
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, buttons_selector)
        ))

        # Switch to Trending view
        buttons = driver.find_elements(By.CSS_SELECTOR, buttons_selector)
        buttons[1].click()

        # Get all the trending goods cards
        cards = driver.find_elements(By.CSS_SELECTOR, 'mvid-shelf-group mvid-product-cards-group '
                                                      '.product-mini-card__image a')

        # Extract goods data
        goods = []
        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, 'img').get_attribute('alt')
            link = card.get_attribute('href')
            good = {
                'title': title,
                'link': link,
            }
            goods.append(good)
        return goods
