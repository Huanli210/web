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

# 初始化Edge服務
service = Service(executable_path=edge_driver_path)

# 初始化Edge選項
options = Options()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 初始化Edge WebDriver
wd = webdriver.Edge(service=service, options=options)

# 打開目標網站
wd.get("https://elearning.nptu.edu.tw/mooc/index.php")
time.sleep(5)  # 等待頁面加載，可以根據需要調整

# 等待登錄按鈕並點擊
login_button = WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "header.container.lcms-header:nth-child(1) div.title div.narrow div.tools:nth-child(3) div.profile ul.nav.nav-up:nth-child(1) li:nth-child(3) > a:nth-child(1)")))
login_button.click()

# 等待用戶名和密碼欄位
username = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
password = wd.find_element(By.XPATH, "//input[@id='password']")
username.send_keys("CBE111027")  # 請替換為您的用戶名
password.send_keys("Jonny20040210")  # 請替換為您的密碼

# 點擊提交按鈕
submit_button = wd.find_element(By.XPATH, "//button[@id='btnSignIn']")
submit_button.click()

# 等待框架可用並切換到它
WebDriverWait(wd, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "s_main")))

# 收集並打印課程信息
try:
    # 等待課程元素出現
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
        print(f"課程名稱: {course_name}")

except Exception as e:
    print(f"獲取課程信息時發生錯誤: {str(e)}")
    # 如果出錯，可以打印頁面源代碼以進行調試
    print("頁面源代碼:")
    print(wd.page_source)

# 切換回主內容
wd.switch_to.default_content()

# 點擊登出按鈕
logout_button = WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'登出')]")))
logout_button.click()

# 關閉驅動
wd.quit()