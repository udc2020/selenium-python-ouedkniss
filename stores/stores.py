from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import time


class Stores(webdriver.Chrome):
    body_size: int
    reached_page_end: bool
    store_data: list

    def __init__(self, URL):
        # disable all errors from webriver manager 
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        super(Stores, self).__init__(options=options)
        
        # open URL & miximize the window
        self.get(URL)
        self.maximize_window()

        # get body height for scrolling 
        self.body_size = self.find_element(
            By.TAG_NAME, 'body').size["height"]

        self.reached_page_end = False

        # final data stored here
        self.store_data = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exit & quit 
        print("Exit....")
        self.quit()

        self.loop(False)

    def loop(self, life=True):
        # kill the proccess 
        while life:
            pass

    def search_input(self, query: str):
        # waiting loading 
        self.implicitly_wait(4)

        # Search input & write the keyword with click button 
        search = self.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Your search"]'
        )
        search.send_keys(query)

        search_btn = self.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="append icon"]'
        )

        search_btn.click()

    def scroll_down(self):
        # Scrolling down (anti lazyloading)
        while not self.reached_page_end:
            # ? select the body elemnt from HTML Dom
            body = self.find_element(By.TAG_NAME, 'body')

            time.sleep(2)

            # ? press DOWN key
            body.send_keys(Keys.PAGE_DOWN)

            # ? stop in the end of body
            new_height = int(body.size["height"])

            # ? repeat them with recursion
            if self.body_size == new_height:
                self.reached_page_end = True
            else:
                self.body_size = new_height

    def get_allposts(self):
        try:
            root_cards = self.find_element(
                By.CSS_SELECTOR, '#search-content > div > div:nth-child(4)')
            cards = root_cards.find_elements(
                By.CLASS_NAME, "o-announ-card-column")
            self.implicitly_wait(5)

            for card in cards:

                link = card.find_element(
                    By.CSS_SELECTOR, 'a[href^="/"]').get_attribute("href")

                title = card.find_element(
                    By.CSS_SELECTOR, 'h2[class="pt-1"]').get_attribute("innerText")

                price = ""
                seler = ""
                try:
                    price = card.find_element(
                        By.CLASS_NAME, 'price').get_attribute("innerText")

                    seler = card.find_element(
                        By.CSS_SELECTOR, '.d-inline.flex-grow-0 > a > div:nth-child(2)').get_attribute("innerText")
                except Exception as e:
                    price = "No Price"
                    seler = "Not a Store"
                    pass

                location = card.find_element(
                    By.CSS_SELECTOR, '.line-height-1 > span:nth-child(1)').get_attribute("innerText")

                img_src = card.find_element(
                    By.CSS_SELECTOR, '.v-image__image.v-image__image--cover').get_attribute("style")

                img = list(img_src.split(" "))[1].replace(
                    'url("', '').replace('")', '').strip(";")

                self.store_data += [[link, img, title, price, location, seler]]

        except Exception as e:
            pass

    # getter (all data was here)
    def all(self): return self.store_data
