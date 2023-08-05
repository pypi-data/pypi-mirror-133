import time
from selenium import webdriver
import os
from urllib.parse import urlparse
from quick_crawler import page
from urllib.parse import urlparse
import os

def get_domain(url):
    domain = urlparse(url).netloc
    return domain

def get_html_str_with_browser(url,driver_path="chromedriver.exe",implicitly_wait=0.5,root_ele="html",slient=False, wait_seconds=-1):

    if not os.path.exists(driver_path):
        print("Please set browser driver path in this function, versions between driver and browser must be same!")
        return

    # set chromedriver.exe's path
    if slient:
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.headless = True
        driver = webdriver.Chrome(executable_path=driver_path,
                                   chrome_options=options
                                  )
    else:
        driver = webdriver.Chrome(executable_path=driver_path
                                  )
    driver.implicitly_wait(implicitly_wait)
    # launch the page
    driver.get(url)

    html_obj = driver.find_element_by_tag_name(root_ele)
    if wait_seconds!=-1:
        time.sleep(5)

    html_str=html_obj.get_attribute("outerHTML")

    driver.close()
    return html_str

def revise_config_path(file_path,dict_kv):
    current_path = os.path.dirname(os.path.realpath(__file__))
    # spider_path = current_path + "/scrapy_projects/news_site/news_site/spiders/news_spider_template.py"
    script_text = open(file_path, 'r', encoding='utf-8').read()
    for k in dict_kv:
        script_text = script_text.replace(k, str(dict_kv[k]))

    spider_path_new = file_path.replace("_template", "")
    f_out = open(spider_path_new, 'w', encoding='utf-8')
    f_out.write(script_text)
    f_out.close()

def fetch_meta_info_from_sites(list_item,saved_folder="",download_time_out=30,dns_time_out=20,max_num_urls=1000,is_save_fulltext=False,use_plain_text=False):

    from pathlib import Path
    # list_result = page.quick_read_csv("datasets/news_sites.csv", fields=['Id', 'Title', 'Name', 'URL'])

    current_path = os.path.dirname(os.path.realpath(__file__))


    # url = list_result[330]
    for url in list_item:
        name = url[0]
        start_url = url[1]
        domain = get_domain(url[1])
        keywords=""
        if len(url)>=3:
            keywords=url[2]
        else:
            keywords=""
        print(start_url)
        # spider
        dict_kv = {
            "$NAME$": name,
            "$START_URL$":start_url,
            "$DOMAIN$":domain,
            "'$NAX_NUM_URLS$'":str(max_num_urls),
            "$DATA_ROOT$": str(saved_folder).replace("\\","/"),
            "$IS_SAVE_FULLTEXT$": str(is_save_fulltext),
            "$USE_PLAIN_TEXT$": str(use_plain_text),
            "$KEYWORDS$": str(keywords),
        }
        revise_config_path(current_path + "/scrapy_projects/news_site/news_site/spiders/news_spider_template.py",dict_kv=dict_kv)
        # settings
        dict_kv = {
            "'$DOWNLOAD_TIMEOUT$'": download_time_out,
            "'$DNS_TIMEOUT$'": dns_time_out
        }
        revise_config_path(current_path + "/scrapy_projects/news_site/news_site/settings_template.py",
                           dict_kv=dict_kv)

        current_path = os.path.dirname(os.path.realpath(__file__))
        # datasets_path=Path(current_path).parent.absolute()

        os.chdir(current_path+"/scrapy_projects/news_site")

        if saved_folder=="":
            os.system(f"scrapy crawl {name}")
        else:
            saved_path = f"{saved_folder}/{name}.csv"
            saved_path = saved_path.replace("\\", "/")
            print(saved_path)
            os.system(f"scrapy crawl {name} -o \"file:///{saved_path}\" -t csv")
        os.chdir(current_path)


