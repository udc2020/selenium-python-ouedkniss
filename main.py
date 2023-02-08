from stores.stores import Stores


def main():

    URL: str = 'https://www.ouedkniss.com/?lang=en'

    try:

        with Stores(URL) as browser:

            browser.search_input("pc")
            browser.scroll_down()

            browser.get_allposts()

            print(browser.all())
            print(len(browser.all()))

            browser.loop(True)

    except Exception as e:
        print(f"we have Some Problems {e}")
        raise


if __name__ == '__main__':
    main()
