# This script is to test http://automationpractice.com


import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class TestSession():

    def __init__(self, username, password):
        """ Initialize test session."""

        self.log_progress("==============================================")
        self.log_progress("Setup driver")
        # setup webdriver
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.implicitly_wait(10)
        # go to homepage
        self.homepage_url = "http://automationpractice.com"
        self.open_homepage()
        # sign in using provided username and password
        self.sign_in(username, password)
        self.init_cart()

    def log_progress(self, string):
        """To log the test execution progress"""
        print string

    def init_cart(self):
        """to initilize expected cart"""
        self.cart = []
        self.temp_cart = {'name':'', 'price':0}

    def verify_cart(self):
        """to verify the cart page shows the correct data """
        driver = self.driver
        verify_pass = False
        expected_total_price = 0
        item_num = 0
        for item in self.cart:
            item_num = item_num + 1
            expected_price = item['price']
            expected_total_price = expected_total_price + float(expected_price[1:])
            expected_name = item['name']
            self.log_progress("Verifying item {} in cart".format(item_num))
            self.verify_equal(driver.find_element_by_xpath('//*[@id="cart_summary"]/tbody/tr[{}]/td[2]/p'.format(item_num)).text, expected_name)
            self.verify_equal(driver.find_element_by_xpath('//*[@id="cart_summary"]/tbody/tr[{}]/td[4]'.format(item_num)).text, expected_price)

        self.log_progress("Verifying total product price in cart")
        actual_total_product = driver.find_element_by_xpath('//*[@id="total_product"]').text
        actual_total_product = float(actual_total_product[1:])
        self.verify_equal(actual_total_product, expected_total_price)
        self.log_progress("Verifying total price with shipping")
        actual_total_price = float(driver.find_element_by_xpath('//*[@id="total_price"]').text[1:])

        self.verify_equal(actual_total_price, expected_total_price+2)


    def open_homepage(self):
        """To open homepage."""
        self.log_progress("Opening homepage")
        self.driver.get(self.homepage_url)
        self.log_progress("Verifying homepage title")
        self.verify_equal(self.driver.title, "My Store")

    def sign_in(self, username, password):
        """
        This function is to sign in with provided username and password
        """
        driver = self.driver
        if self.check_exists_by_linktext("Sign out"):
            # need to sign out if already signed in
            print "Signing out"
            driver.find_element_by_link_text("Sign out").click()
        self.log_progress("Signing in")
        driver.find_element_by_link_text("Sign in").click()
        driver.find_element_by_id("email").send_keys(username)
        driver.find_element_by_id("passwd").send_keys(password)
        driver.find_element_by_id("SubmitLogin").click()
        # verify current page is my account
        self.log_progress("Verifying signed in state")
        self.verify_equal(driver.title, "My account - My Store")


    def check_exists_by_xpath(self, xpath):
        """To check by xpath that element exist """
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_linktext(self, linktext):
        """To check by linktext that element exist """
        try:
            self.driver.find_element_by_link_text(linktext)
        except NoSuchElementException:
            return False
        return True

    def verify_equal(self, actual, expected):
        """To verify actual value based on expected value"""
        if actual == expected:
            result = True
            self.log_progress("Verification passed")
        else:
            result = False
            self.log_progress("Verification failed")
            self.log_progress("actual = {}, expected = {}".format(actual, expected))

    def search_product(self, keyword):
        """To use product search feature
        """
        driver = self.driver
        self.log_progress("Searching product, keyword: {}".format(keyword))
        driver.find_element_by_id("search_query_top").send_keys("blouse")
        driver.find_element_by_id("searchbox").submit()

    def find_in_wishlist(self, keyword):
        """To verify that an item is in wishlist"""
        driver = self.driver
        driver.get("http://automationpractice.com/index.php?fc=module&module=blockwishlist&controller=mywishlist")
        driver.find_element_by_link_text("My wishlist").click()
        self.log_progress("Verify item is in wishlist")
        wish_list = driver.find_elements_by_id("s_title")
        found = False
        for item in wish_list:
            if keyword in item.text:
                self.log_progress("verification pass, {} is found in wishlist".format(keyword))
                found = True
                break
        if not found:
            self.log_progress("verification failed, {} not found in wishlist".format(keyword))
        return found

    def tc001(self):
        """
        This test case verify user scenario:
            homepage>click sale banner>promotion page
        """
        driver = self.driver
        self.log_progress("==============================================")
        self.log_progress("Executing tc001")
        self.log_progress("Scenario: homepage>click banner>promotion page")
        # "Going to homepage"
        self.open_homepage()
        # click sale/promotion banner
        self.log_progress("Click promotion banner")
        driver.find_element_by_xpath("//*[@id='header']/div[1]/div/div/a/img").click()
        self.log_progress("Verify promotion page title")
        # I assume the page name should be Promo
        self.verify_equal(driver.title, "Promo")


    def tc002(self):
        """
        This test case verify user scenario:
            homepage>search>item description page>add to wishlist
        """
        driver = self.driver
        self.log_progress("==============================================")
        self.log_progress("Executing tc002")
        self.log_progress("Scenario: homepage>search>add item to wishlist>wishlist page")
        # "Going to homepage"
        self.open_homepage()
        # Search for keyword "Blouse"
        self.log_progress("Use search feature for 'Blouse'")
        self.search_product("Blouse")
        self.log_progress("Verifying search successful")
        self.verify_equal(driver.find_element_by_xpath('//*[@id="center_column"]/ul/li/div/div[2]/h5/a').text, "Blouse")
        # open product description page
        self.log_progress("Go to item description page")
        driver.find_element_by_xpath('//*[@id="center_column"]/ul/li/div/div[1]/div/a[1]/img').click()
        self.log_progress("Verifying page title is correct")
        self.verify_equal(driver.title, 'Blouse - My Store')
        # add product to wishlist
        self.log_progress("Adding item to wishlist")
        driver.find_element_by_id("wishlist_button").click()
        self.log_progress("Verify item added to wishlist")
        self.verify_equal(driver.find_element_by_xpath('//*[@id="product"]/div[2]/div/div/div/div/p').text, "Added to your wishlist.")
        driver.find_element_by_xpath('//*[@id="product"]/div[2]/div/div/a').click()
        # verify in wishlist page
        self.find_in_wishlist("Blouse")



    def tc003(self):
        """
        This test case verify user scenario:
            homepage>category>add to cart>payment
        """
        driver = self.driver
        self.log_progress("==============================================")
        self.log_progress("Executing tc003")
        self.log_progress("Scenario: homepage>woman category>add cart>payment")
        # "Going to homepage"
        self.open_homepage()
        # go to Woman category
        self.log_progress("Go to woman category")
        driver.find_element_by_xpath('//*[@id="block_top_menu"]/ul/li[1]/a').click()

        # add several items in the grid into cart
        item_num = 3  # item_num is the number of item that we want to add to cart
        for index in range(1, item_num+1):
            self.log_progress("Adding item {} to cart".format(index))
            item_name = driver.find_element_by_xpath('//*[@id="center_column"]/ul/li[{}]/div/div[2]/h5/a'.format(index)).text
            item_price = driver.find_element_by_xpath('//*[@id="center_column"]/ul/li[{}]/div/div[2]/div[1]/span'.format(index)).text
            self.cart.append({'name':item_name, 'price':item_price})
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="center_column"]/ul/li[{}]/div/div[2]/div[2]/a[1]/span'.format(index)).click()
            self.log_progress("Verify adding item {} to cart".format(index))
            time.sleep(1)
            self.verify_equal(driver.find_element_by_xpath('//*[@id="layer_cart"]/div[1]/div[1]/h2').text, 'Product successfully added to your shopping cart')
            time.sleep(1)
            if index < item_num:
                # continue shopping
                driver.find_element_by_xpath('//*[@id="layer_cart"]/div[1]/div[2]/div[4]/span/span/i').click()
            else:
                # go to cart, proceed to checkout
                driver.find_element_by_xpath('//*[@id="layer_cart"]/div[1]/div[2]/div[4]/a/span/i').click()
        self.verify_cart()

        # proceed to checkout and payment
        self.log_progress("Proceed to checkout and payment")
        driver.find_element_by_xpath('//*[@id="center_column"]/p[2]/a[1]').click()
        driver.find_element_by_xpath('//*[@id="center_column"]/form/p/button/span').click()
        driver.find_element_by_xpath('//*[@id="cgv"]').click()
        driver.find_element_by_xpath('//*[@id="form"]/p/button').click()
        self.log_progress("Select visa payment method")
        try:
            driver.find_element_by_class_name("visa").click()
            driver.find_element_by_xpath('//*[@id="cart_navigation"]/button').click()
            self.verify_equal(driver.find_element_by_xpath('//*[@id="center_column"]/div/p/strong').text, "Your order on My Store is complete.")
        except NoSuchElementException:
            self.log_progress("payment failed")



def main():
    """ This is the main function."""

    # Setup test
    test_session1 = TestSession("dhimas_sm@hotmail.com", "12345")

    # test scenario: homepage>click sale banner>promotion page
    test_session1.tc001()

    # test scenario: homepage>search>item description page>add to wishlist
    test_session1.tc002()

    # test scenario: homepage>category>add to cart>payment
    test_session1.tc003()



if __name__ == '__main__':
    main()
    os.system("pause")

