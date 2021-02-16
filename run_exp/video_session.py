import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from time import sleep


def video_session(url = "http://localhost/myindex_BB.html", process_id = "0",\
    run_time = 320, default_chrome_user_dir = '../abr_browser_dir/chrome_data_dir',
    chrome_driver = '../chromedriver/ToChrome87/chromedriver_linux64/chromedriver', visible = 1):

    try:
        # copy over the chrome user dir    
        chrome_user_dir = '/tmp/chrome_user_dir_id_' + process_id
        os.system('rm -r ' + chrome_user_dir)
        os.system('cp -r ' + default_chrome_user_dir + ' ' + chrome_user_dir)

        # to not display the page in browser
        display = Display(visible=visible, size=(800,600))
        display.start()

        # initialize chrome driver
        options=Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--user-data-dir=' + chrome_user_dir)
        options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--autoplay-policy=no-user-gesture-required')
        driver=webdriver.Chrome(chrome_driver, options=options)
        print(url)
        #driver.set_page_load_timeout(120)
        driver.get(url)

        element = wait(driver, 5).until(EC.visibility_of_element_located((By.ID, "videoPlayer")))
        driver.find_element_by_id("videoPlayer").click()

        sleep(run_time)

        driver.quit()
        display.stop()
        
    except Exception as e:
        try: 
            display.stop()
            print("Failed")
        except:
            pass
        try:
            driver.quit()
        except:
            pass
        print(e)



if __name__ == "__main__":
    # execute only if run as a script
    video_session()