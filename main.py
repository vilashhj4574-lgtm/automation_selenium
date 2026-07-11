from tkinter import dialog

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()

options.add_argument("--force-device-scale-factor=0.8")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

from selenium.common.exceptions import NoSuchElementException

#this is for virtual scroll and click on the item in the list

def click_virtual_item(container_xpath, item_text):
    container = wait.until(
        EC.presence_of_element_located((By.XPATH, container_xpath)))

    last_height = -1

    while True:

        try:
            element = container.find_element(By.XPATH,
                f".//div[@role='listitem']//div[normalize-space()='{item_text}']"
            )

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                element
            )

            wait.until(
                EC.element_to_be_clickable(element)
            ).click()

            return

        except NoSuchElementException:

            driver.execute_script("arguments[0].scrollTop += 250;",container)
            time.sleep(0.5)

            current = driver.execute_script("return arguments[0].scrollTop;",container)

            if current == last_height:
                raise Exception(f"{item_text} not found")

            last_height = current


# this is for selecting dropdown option in the UI

def select_dropdown(label, option):

    # Click the dropdown
    dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//label[normalize-space()='{label}']/ancestor::div[contains(@class,'v-input')]//div[@role='button']"
        ))
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
    dropdown.click()

    # Wait for active menu
    menu = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class,'menuable__content__active')]"
        ))
    )

    while True:

        try:
            # ---------- COUNTRY ----------
            if label == "Country *":

                item = menu.find_element(By.XPATH,f".//div[@role='option']//div[normalize-space()='{option}']")
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});",item)
                item.click()

            # ---------- REGION & CITY ----------
            else:

                item = menu.find_element(
                    By.XPATH,
                    f".//div[@role='option'][.//div[@class='v-list-item__title' and normalize-space()='{option}']]"
                )

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    item
                )

                # Try normal click
                try:
                    item.click()

                except:

                    # Try ActionChains
                    try:
                        ActionChains(driver).move_to_element(item).pause(0.2).click().perform()

                    except:

                        # Final fallback
                        driver.execute_script(
                            "arguments[0].click();",
                            item
                        )

            break

        except NoSuchElementException:

            driver.execute_script(
                "arguments[0].scrollTop += 250;",
                menu
            )

            time.sleep(0.3)

# def scroll_until_store(driver, store_name, max_scrolls=30):

#     scroll_box = driver.find_element(
#         By.XPATH,
#         "//div[contains(@class,'ps') and contains(@class,'ps--active-y')]"
#     )

#     for _ in range(max_scrolls):

#         try:
#             store = driver.find_element(
#                 By.XPATH,
#                 f"//div[@class='v-list-item__title' and normalize-space()='{store_name}']"
#             )
#             return store

#         except NoSuchElementException:
#             driver.execute_script(
#                 "arguments[0].scrollTop += 120;",
#                 scroll_box
#             )
#             time.sleep(0.2)

#     raise Exception(f"{store_name} not found")


def scroll_down(driver, pixels=200):
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"div.ps.ps--active-y")))
    driver.execute_script("""arguments[0].scrollTop = arguments[0].scrollTop + arguments[1];""", scroll_box, pixels)

# Variables for product creation
STORE_CODE,NFC_DATA,EAN,Product_id,List_price,Sale_Price,Product,Template_Key='W101','www.google.com','12345678','W321','230','32','banana','one'
   

def login_to_website():
# Open a website
    driver.get("https://stage00.common.solumesl.com/login")

    wait.until(
    EC.visibility_of_element_located((By.ID, "email")))
    email = driver.find_element(By.ID, "email")
    email.send_keys("ramanpranav35@gmail.com")

    password = driver.find_element(By.ID, "password")
    password.send_keys("SoluM@2021")
    login_button = driver.find_element(By.ID, "next")
    login_button.click()
   

login_to_website()



def navigate_to_area_group_management():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='tab' and .//div[normalize-space()='Config']]")))
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "v-overlay__scrim")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='tab' and .//div[normalize-space()='Config']]"))).click()
    time.sleep(1)
    area_create()





def area_create():
    # wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@href='/System/DashboardConfigCloud']")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/System/DashboardConfigCloud']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Area Group Management']/parent::a"))).click()

    # for selecting company and click add to add country
    company = "NI01"
    xpath = f"//div[normalize-space()='{company}']/ancestor::div[@role='listitem']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    xpath_add = f"""//h4[normalize-space()='COUNTRY']/ancestor::div[contains(@class,'col')]//button[.//span[normalize-space()='Add']]"""
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_add))).click()
    company_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Input the new country']")))
    company_name.send_keys("29AB")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Save']/parent::button"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='OK']/parent::button"))).click()
    
    country = "29AB"
    region = "DOO1"
    click_virtual_item("//h4[normalize-space()='COUNTRY']/ancestor::div[contains(@class,'col')]//div[contains(@class,'v-virtual-scroll')]", country)
 
    xpath_add = f"""//h4[normalize-space()='REGION']/ancestor::div[contains(@class,'col')]//button[.//span[normalize-space()='Add']]"""
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_add))).click()
    region_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//div//input[@placeholder='Input the new region']")))
    time.sleep(1)
    region_name.send_keys("DOO1")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Save']/parent::button"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='OK']/parent::button"))).click()
    time.sleep(3)

    click_virtual_item("//h4[normalize-space()='COUNTRY']/ancestor::div[contains(@class,'col')]//div[contains(@class,'v-virtual-scroll')]", country)
    time.sleep(1)
    click_virtual_item("//h4[normalize-space()='REGION']/ancestor::div[contains(@class,'col')]//div[contains(@class,'v-virtual-scroll')]", region)
    time.sleep(1)
    xpath_add = f"""//h4[normalize-space()='CITY']/ancestor::div[contains(@class,'col')]//button[.//span[normalize-space()='Add']]"""
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_add))).click()
    city_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//div//input[@placeholder='Input the new city']")))
    city_name.send_keys("DOO2")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Save']/parent::button"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='OK']/parent::button"))).click()
    time.sleep(5)

# navigate_to_area_group_management()






def store_create():
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/Store/StoreInfo']"))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Add']/parent::button"))).click()
    select_dropdown("Country *", "29AB")
    time.sleep(2)
    select_dropdown("Region *", "DOO1")
    time.sleep(2)
    select_dropdown("City *", "DOO2")
    time.sleep(2)
    store_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Input store name']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", store_name)
    store_name.send_keys("WIN")
    time.sleep(1)
    store_code = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Input store code']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", store_code)
    store_code.send_keys("W101")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Save']/parent::button"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='OK']/parent::button"))).click()

# store_create()







def go_to_esl():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='tab' and .//div[normalize-space()='ESL']]")))
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='tab' and .//div[normalize-space()='ESL']]"))).click()
    
# go_to_esl()





def select_store():   
    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@id='contentWrap']//img[1]"))).click()
    store_select=wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='sol-searchTermStore']")))
    store_select.send_keys("W101")
    store_select.send_keys("a")
    store_select.send_keys(Keys.BACKSPACE)
    store_detail = "WIN (W101)"
    store = wait.until(EC.visibility_of_element_located((
        By.XPATH,f"//div[@title='{store_detail}']/ancestor::div[@role='listitem']")))
    ActionChains(driver).double_click(store).perform()

    time.sleep(2)

select_store()







def add_gateway():
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Gateway']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Add']/parent::button"))).click()
    gateway_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'popup') and contains(@class,'add_store_popup')]//input[@placeholder='Input MAC ID']")))
    gateway_name = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'popup') and contains(@class,'add_store_popup')]//input[@placeholder='Input MAC ID']")))

    driver.execute_script("arguments[0].click();", gateway_name)
    gateway_name.send_keys("D02544FFFE21B2EB")

    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Save']/parent::button"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='OK']/parent::button"))).click()

# add_gateway()






def template_add():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@href='/Template/TypeList']")))
    time.sleep(4)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/Template/TypeList']"))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='New']/parent::button"))).click()
    template_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'popup') and contains(@class,'add_store_popup')]//input[@placeholder='Input label code']")))
    template_name.send_keys("0822CB82C2D6")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='searchIcon']//img")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='searchIcon']//img"))).click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Input the type name']")))
    Template_name=wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Input the type name']")))
    Template_name.send_keys("UI_Template")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Save']/parent::button"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='OK']/parent::button"))).click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Input template type name']")))
    Template_search=wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Input template type name']")))
    Template_search.send_keys("UI_Template")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@id='contentWrapper']//img"))).click()

    Search= wait.until(EC.visibility_of_element_located((By.XPATH,"//span[normalize-space()='UI_Template']")))
    ActionChains(driver).double_click(Search).perform()

# give the Level where you want to upload the file  :::: Country,Region,City,Store
    level= "City"
    wait.until(EC.visibility_of_element_located((By.XPATH,f"//tr[td[1][normalize-space()='{level}']]//i[contains(@class,'mdi-magnify')]")))
    wait.until(EC.element_to_be_clickable((By.XPATH,f"//tr[td[1][normalize-space()='{level}']]//i[contains(@class,'mdi-magnify')]"))).click()


# uploading the file 
    file_path = r"C:\selenium_SAAS\Data\Templates\new_today - 2.9_HD_ _ 384 X 168-BINARY.xsl"
    inputs = driver.find_elements(By.XPATH, "//input[@accept='.xsl']")
    print("Number of file inputs:", len(inputs))
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'popup')] //input[@accept='.xsl']")))
    file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'popup')] //input[@accept='.xsl']")))
    file_input.send_keys(file_path)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Update']/parent::button"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='OK']/parent::button"))).click()
    time.sleep(3)

# template_add()





Delete_product =["TR65","TR67"]
product_ID=["TR61","TR63","TR62"]
def go_to_product_page():
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/Product/ProductInfo']"))).click()
    time.sleep(1)
    # add_product()
    # product_upload()

go_to_product_page()






def add_product():
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Add']"))).click()
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the STORE_CODE']")))
    S.send_keys(STORE_CODE)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the NFC_DATA']")))
    S.send_keys(NFC_DATA)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the EAN']")))
    S.send_keys(EAN)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the Product_id']")))
    S.send_keys(Product_id)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the List_price']")))
    S.send_keys(List_price)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the Sale_Price']")))
    S.send_keys(Sale_Price) 
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the Product']")))
    S.send_keys(Product)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input the Template_Key']")))
    S.send_keys(Template_Key)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Save']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='OK']"))).click()





def product_upload():
    wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='File Upload']"))).click()
    file_path=r"C:\selenium_SAAS\Data\upload_file.csv"
    x=wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'popup')] //input[@accept='.csv']")))
    x.send_keys(file_path)
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'popup')]//span[normalize-space()='Upload']"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='OK']"))).click()





def select_product_to_blink_led_through_product():
    for product in product_ID:
        # x=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input Product ID']")))
        # x.click()
        # x.send_keys(Keys.CONTROL, "a")
        # x.send_keys(Keys.DELETE)
        # x.send_keys(product)
        # wait.until(EC.element_to_be_clickable((By.XPATH,"//Span[normalize-space()='Search']/parent::button"))).click()
        # time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH,f"//tr[td[normalize-space()='{product}']]//td[1]"))).click()
        time.sleep(1)
       
    wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='Blink LED']"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH,"//span[normalize-space()='Save']"))).click()

# select_product_to_blink_led_through_product()







def delete_product():
    for prod in Delete_product:
        x=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input Product ID']")))
        x.click()
        x.send_keys(Keys.CONTROL, "a")
        x.send_keys(Keys.DELETE)       
        x.send_keys(prod)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//Span[normalize-space()='Search']/parent::button"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH,f"//tr[td[normalize-space()='{prod}']]//td[1]"))).click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='Delete']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='Yes']"))).click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='OK']"))).click()
        time.sleep(2)

# delete_product()




Name,ON_Time,OF_time,IDLE_time,Active_count="LED1",20,30,2,5

def LED_pattern_ADD():
    wait.until(EC.presence_of_element_located((By.XPATH,"//a[@href='/Multifunction/LED']"))).click()
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'table-options')]//span[normalize-space()='New']"))).click()
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input The Name']")))
    S.send_keys(Name)
    time.sleep(0.5)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input On Time(msec) Value(10~2250, unit:10)']")))
    S.send_keys(ON_Time)
    time.sleep(0.5)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input Off Time(msec) Value(10~2250, unit:10)']")))
    S.send_keys(OF_time)
    time.sleep(0.5)    
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input Idle Time(sec) Value(1~225, unit:1)']")))
    S.send_keys(IDLE_time)
    time.sleep(0.5)
    S=wait.until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Input Active Count Value(1~225, unit:1)']")))
    S.send_keys(Active_count)
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='Save']"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='OK']"))).click()
# LED_pattern_ADD()

LED_pattern_name ='LED1'
def LED_pattern_delete():
    wait.until(EC.presence_of_element_located((By.XPATH,"//a[@href='/Multifunction/LED']"))).click()
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH,f"//tr[td[normalize-space()='{LED_pattern_name}']]//td[1]"))).click()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='Delete']"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='Yes']"))).click()
   
LED_pattern_delete()


def Button_configuration_ADD():
    wait.until(EC.presence_of_element_located((By.XPATH,"//a[@href='/Multifunction/ButtonConfig']"))).click()
    

# Button_configuration_ADD()




# # Keep the browser open until you press Enter


input("Press Enter to close the browser...") 
# Close the browser
driver.quit()
