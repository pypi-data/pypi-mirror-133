from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
class DankBot():
    """
    DankBot Class Initialises the Headless browser followed by the necessary automation fucntionalities.
    Controls the curses inlay.
    """
    TYPE_BOX = 'markup-2BOw-j.slateTextArea-1Mkdgw.fontSize16Padding-3Wk7zP'
    BASE_URL = 'https://discord.com/login'
    DEF_BROWSER = "Chrome"
    driver = ''
    _running = False
    status = 'initiated'

    def __init__(self, def_brow='Chrome'):
        self.DEF_BROWSER = def_brow
        self._running = False

    def start_thread(self):
        self._running = False
        self.driver = webdriver.Chrome()
        self.driver.get(self.BASE_URL)
        self.exec_base_script()

    def terminate(self):
        self._running = False

    def start_bot(self):
        self._running = True

    def exec_base_script(self):
        while(not self._running):
            pass
        self.status = 'Working'
        while(self._running):
            self.type_box = self.driver.find_element_by_class_name(self.TYPE_BOX)
            self.type_box.send_keys('pls beg')
            self.type_box.send_keys(Keys.ENTER)
            time.sleep(5)
            self.type_box.send_keys('pls hunt')
            self.type_box.send_keys(Keys.ENTER)
            time.sleep(5)
            self.type_box.send_keys('pls dig')
            self.type_box.send_keys(Keys.ENTER)
            time.sleep(5)
            self.type_box.send_keys('pls fish')
            self.type_box.send_keys(Keys.ENTER)
            time.sleep(5)
            self.type_box.send_keys('pls deposit all')
            self.type_box.send_keys(Keys.ENTER)
            time.sleep(3)
            self.type_box.send_keys('pls use horseshoe')
            self.type_box.send_keys(Keys.ENTER)
            time.sleep(5)
            try:
                self.type_box.send_keys('pls search')
                self.type_box.send_keys(Keys.ENTER)
                time.sleep(3)
                options = self.driver.find_elements_by_class_name('container-1v9gV9')
                q = options[-1].find_elements_by_tag_name('button')
                for i in range(len(q)):
                    if q[i].text == 'Vacuum':
                        to_click = i
                        break
                    elif q[i] in ['Basement', 'Bus', 'Car', 'Coat', 'Dresser', 'Fridge', 'Pocket', 'Washer']:
                        to_click = i
                    else:
                        to_click = i
                q[i].click()
            except IndexError as error:
                print("Error")
            time.sleep(10)
            try:
                self.type_box.send_keys('pls highlow')
                self.type_box.send_keys(Keys.ENTER)
                time.sleep(5)
                options = self.driver.find_elements_by_class_name('container-1v9gV9')
                description = self.driver.find_elements_by_class_name('grid-1nZz7S')[-1]
                print(description.text)
                number = int(description.text.split()[21][:-1])
                print(number)
                if 100 - number < number - 0:
                    choice = 0
                    print('Higher')
                else:
                    choice = 2
                    print('Lower')
                q = options[-1].find_elements_by_tag_name('button')
                q[choice].click()
                time.sleep(3)
            except IndexError as error:
                time.sleep(5)
            time.sleep(15)
        self.status = 'Ended'
