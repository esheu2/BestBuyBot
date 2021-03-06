from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import info

# make sure this path is correct
PATH = r"C:\Users\Everett Sheu\Downloads\chromedriver_win32\chromedriver.exe"

driver = webdriver.Chrome(PATH)

RTX3070LINKS = [
    # "https://www.bestbuy.com/site/apple-10-2-inch-ipad-latest-model-8th-generation-with-wi-fi-32gb-space-gray/5199701.p?skuId=5199701",
    "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",
    # "https://www.bestbuy.com/site/apple-10-2-inch-ipad-latest-model-8th-generation-with-wi-fi-32gb-space-gray/5199701.p?skuId=5199701"
    # "https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3070-aorus-master-8gb-gddr6-pci-express-4-0-graphics-card/6439384.p?skuId=6439384",
    # "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-3070-ventus-3x-oc-bv-8gb-gddr6-pci-express-4-0-graphics-card/6438278.p?skuId=6438278",
    # "https://www.bestbuy.com/site/asus-nvidia-geforce-tuf-rtx3070-8gb-gddr6-pci-express-4-0-graphics-card-black/6439128.p?skuId=6439128"
]
idx = 0
driver.get(RTX3070LINKS[idx])

isComplete = False

while not isComplete:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
        idx += 1
        if idx == len(RTX3070LINKS):
            idx = 0
        driver.get(RTX3070LINKS[idx])
        continue

    print("Add to cart button found")

    try:
        # add to cart
        atcBtn.click()

        # go to cart and begin checkout as guest
        driver.get("https://www.bestbuy.com/cart")

        checkoutBtn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".checkout-buttons__checkout"))
        )
        checkoutBtn.click()
        print("Successfully added to cart - beginning check out")

        # fill in email and password
        emailField = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "fld-e"))
        )
        emailField.send_keys(info.email)

        pwField = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "fld-p1"))
        )
        pwField.send_keys(info.password)

        # click sign in button

        signInBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".cia-form__controls__submit"))
        )

        signInBtn.click()
        print("Signing in")

        # fill in card cvv
        cvvField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "credit-card-cvv"))
        )
        cvvField.send_keys(info.cvv)
        print("Attempting to place order")

        # place order
        placeOrderBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".button__fast-track"))
        )
        placeOrderBtn.click()

        isComplete = True
    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        idx += 1
        if idx == len(RTX3070LINKS):
            idx = 0
        driver.get(RTX3070LINKS[idx])
        print("Error - restarting bot")
        continue

print("Order successfully placed")
