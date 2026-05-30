import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv
import os
import random
from selenium.webdriver.chrome.options import Options

CSV_FILE_NAME = "server_metrics_log.csv"
TEST_RUN_ID = ""

def pytest_session_start(session):

    global TEST_RUN_ID

    TEST_RUN_ID = f"RUN-{uuid.uuid4().hex[:8]}"

@pytest.fixture
def synthetic_server_metric(request) :

    yield

    is_anomaly = random.random() < 0.15

    if is_anomaly :
        cpu_usage = round(random.uniform(85.0,99.9) , 2)
        ram_usage = round(random.uniform(90.0 , 98.5) , 2)
        response_time_ms = round(random.uniform(5000.0 , 12000.0), 2)

    else : 
        cpu_usage = round(random.uniform(10.0, 45.0), 2)
        ram_usage = round(random.uniform(40.0, 65.0), 2)
        response_time_ms = round(random.uniform(200.0, 1500.0), 2)

    
    timestamp = datetime.utcnow().isoformat()
    test_iteration = request.node.name
    
    file_exists = os.path.isfile(CSV_FILE_NAME)
    try:
        with open(CSV_FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["test_run_id", "timestamp", "test_iteration", "is_anomaly", "cpu_usage_percent", "ram_usage_percent", "response_time_ms"])
            
            writer.writerow([
                TEST_RUN_ID, 
                datetime.utcnow().isoformat(), 
                request.node.name, 
                is_anomaly,  
                cpu_usage, 
                ram_usage, 
                response_time_ms
            ])
    except ValueError:
        
        pass


@pytest.fixture
def browser() :

    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    wait = WebDriverWait(driver, 10)


    yield driver , wait

    driver.quit()

def test_laptop_search(browser , synthetic_server_metric) :

    driver , wait = browser
    driver.get("https://demowebshop.tricentis.com/")


    driver.find_element(By.ID , "small-searchterms").send_keys("laptop")

    autocomplete_list = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.ui-autocomplete"))
    )
    
    autocomplete_list.find_element(By.TAG_NAME, "li").click()

def test_add_to_cart(browser , synthetic_server_metric) : 

    driver , wait = browser
    driver.get("https://demowebshop.tricentis.com/141-inch-laptop")

    driver.find_element(By.ID , "add-to-cart-button-31").click()

    notification_bar = wait.until(
        EC.visibility_of_element_located((By.ID, "bar-notification"))
    )

    notification_text = notification_bar.text

    assert "The product has been added to your shopping cart" in notification_text







