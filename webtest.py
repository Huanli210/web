from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# 使用EdgeChromiumDriverManager獲取正確的EdgeDriver路徑
edge_driver_path = EdgeChromiumDriverManager().install()

service = Service(executable_path=edge_driver_path)

# 初始化Edge選項
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Edge(service=service, options=options)

wd.get("https://elearning.nptu.edu.tw/mooc/index.php")
time.sleep(5) 


login_button = WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "header.container.lcms-header:nth-child(1) div.title div.narrow div.tools:nth-child(3) div.profile ul.nav.nav-up:nth-child(1) li:nth-child(3) > a:nth-child(1)")))
login_button.click()


username = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
password = wd.find_element(By.XPATH, "//input[@id='password']")
username.send_keys("*****")  
password.send_keys("*****")  


submit_button = wd.find_element(By.XPATH, "//button[@id='btnSignIn']")
submit_button.click()

# 等待框架可用並切換到它
WebDriverWait(wd, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "s_main")))

try:
    # 等待元素出現
    courses = WebDriverWait(wd, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'cssAnchor')]"))
    )
    
    valid_courses = []
    
    for course in courses:
        course_name = course.text.strip()
        
        # 只保留課程名稱不為 "0" 和 "1" 的課程
        if course_name not in ["0", "1"]:
            valid_courses.append(course_name)
    
    
    for course_name in valid_courses:
        print(f"{course_name}")

except Exception as e:
    print(f"獲取課程信息時發生錯誤: {str(e)}")
    # 如果出錯，可以查看頁面源代碼以進行調整
    print("頁面源代碼:")
    print(wd.page_source)

wd.switch_to.default_content()


logout_button = WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'登出')]")))
logout_button.click()

wd.quit()