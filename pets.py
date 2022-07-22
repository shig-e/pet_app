from time import sleep

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import  Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

from logger import set_logger

log = set_logger()

def set_driver(hidden_chrome=True):
    options = ChromeOptions()
    
    # ヘッドレスモードの設定
    if hidden_chrome == True:
        options.add_argument("--headless")
        
    options.add_argument(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    # 不要なエラーは非表示にする
    options.add_argument("log-level=3") # 不要なログを非表示にする
    options.add_argument("--certificate-errors") # 認証エラー回避
    options.add_argument("--ignore-ssl-errors") # 認証エラー回避
    options.add_argument("--incognito") # シークレットモードの設定を付与    
    
    service = Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

def new_item():
    """
    Discription: petwebのサイトから新商品の商品名、画像url、金額、JANcode,ITEMcodeを取得する
    Returns: DataFrame
    """
    driver = set_driver(hidden_chrome=False)
    url = "https://petweb.jp/"
    driver.get(url)

    driver.implicitly_wait(10)

    elem = driver.find_element(by=By.CSS_SELECTOR, value="#sidecontents > div > form > div.categorylist")
    new_item = elem.find_element(by=By.CSS_SELECTOR, value="#sidecontents > div > form > div.categorylist > ul:nth-child(3) > li > a")
    _newitem_link = new_item.get_attribute("href")
    driver.get(_newitem_link)
    sleep(3)

    count = 0
    succes = 0
    fail = 0
    new_item_links = []
    df = pd.DataFrame()
    log.info("========スクレイピング開始========")
    while True:
        try:
        # 新商品のdivタグ
            _new_item_elem = driver.find_element(by=By.CSS_SELECTOR, value="#maincontents > section > div.searchheader.uk-margin > div.product-list > div")
            item_boxs = _new_item_elem.find_elements(by=By.CLASS_NAME, value="itembox")
            sleep(3)
            # 初めに全ての商品のページurlを取得
            for item_box in item_boxs:
                new_box_link = item_box.find_element(by=By.CSS_SELECTOR, value="div.desc > span > a")
                new_item_link = new_box_link.get_attribute("href")
                new_item_links.append(new_item_link)

            next_page = driver.find_elements(by=By.CSS_SELECTOR, value="#maincontents > section > div.searchheader.uk-margin > div.searchheader.uk-margin > div.uk-flex.uk-flex-middle.uk-visible\@s > div:nth-child(2) > ul > li.next > a")
            # nex_pageがある場合urlを取得
            if next_page:
                next_page_link = next_page[0].get_attribute("href")
                sleep(5)
                driver.get(next_page_link)
            else:
                break
        except Exception as e:
                print(e)

    for new_item_link in new_item_links:
        driver.get(new_item_link)
        sleep(3)
        try:
            new_item_elem = driver.find_element(by=By.CSS_SELECTOR, value="#maincontents")
            # タイトル
            _title = new_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > h1").text
            title = _title.replace("\u3000", " ")
            # img要素1取得
            _img1 = new_item_elem.find_elements(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li.uk-active > a > img")
            if _img1:
                img1 = new_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li.uk-active > a > img").get_attribute("src")
            else:
                img1 = None
            # img要素2取得
            _img2 = new_item_elem.find_elements(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li:nth-child(2) > a > img")
            if _img2:
                img2 = new_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li:nth-child(2) > a > img").get_attribute("src")
            else:
                img2 = None
            # 金額取得
            _price = new_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.cartbox > div.cartbox-inner > dl:nth-child(1) > dd").text
            price= int(_price.replace("円", "").replace(",", "").rstrip())
            # コード取得
            code = new_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.uk-margin-large > div:nth-child(1) > p").text
            jan_code = code.replace("\u3000", ",").split(",")[0]
            item_code = code.replace("\u3000", ",").split(",")[1]

            df = df.append({"url": new_item_link,
                    "title": title,
                    "img1": img1,
                    "img2": img2,
                    "price": price,
                    "jan_code": jan_code,
                    "item_code": item_code},
                    ignore_index=True)
            log.info(f"[成功]{count} 件目: {title}")
            succes += 1
        except Exception as e:
            log.info(f"[失敗]{count}件目: {title}")
            log.info(e)
            fail += 1
        finally:
            count += 1

    df.to_csv("new_item_csv", encoding="utf-8")  
    log.info(f"処理完了 成功件数: {succes} 件 / 失敗件数 : {fail} 件")
    log.info("========スクレイピング終了========")
    return df

def pets(arg1, arg2):
    '''
    Discription: petswebのサイトから新商品以外の商品名、画像url、金額、JANcode,ITEMcodeを取得する、引数で取得するページを変えてcsvに出力
    Returns: DataFrame
    '''
    
    driver = set_driver(hidden_chrome=True)
    url = "https://petweb.jp/"
    driver.get(url)

    driver.implicitly_wait(10)

    elem = driver.find_element(by=By.CSS_SELECTOR, value="#sidecontents > div > form > div.categorylist")
    pets_li = elem.find_element(by=By.CSS_SELECTOR, value=f"#sidecontents > div > form > div.categorylist > ul.uk-accordion > li:nth-child({arg1}) > a:nth-child(1)")
    _pets_link = pets_li.get_attribute("href")
    driver.get(_pets_link)
    sleep(3)
    
    count = 0
    succes = 0
    fail = 0
    pets_item_links = []
    df = pd.DataFrame()
    
    log.info("========スクレイピング開始========")
    while True:
        # 最初にページのurlを取得
        try:
            pets_elem = driver.find_element(by=By.CSS_SELECTOR, value="#maincontents > section > div.searchheader.uk-margin > div.product-list > div")
            pets_items = pets_elem.find_elements(by=By.CLASS_NAME, value="itembox")
            sleep(3)
            for _pets_item in pets_items:
                pets_item = _pets_item.find_element(by=By.TAG_NAME, value="a")
                pet_item_link = pets_item.get_attribute("href")
                pets_item_links.append(pet_item_link)

            next_page = driver.find_elements(by=By.CSS_SELECTOR, value="#maincontents > section > div.searchheader.uk-margin > div.searchheader.uk-margin > div.uk-flex.uk-flex-middle.uk-visible\@s > div:nth-child(2) > ul > li.next > a")
            if next_page:
                next_page_link = next_page[0].get_attribute("href")
                sleep(3)
                driver.get(next_page_link)
            else:
                break
        except Exception as e:
                log.info(e)
                
    for pet_item_link in pets_item_links:
        driver.get(pet_item_link)
        sleep(3)
        try:  
            pet_item_elem = driver.find_element(by=By.CSS_SELECTOR, value="#maincontents")
            # タイトル取得
            _title = pet_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > h1").text
            title = _title.replace("\u3000", " ")
            # imgtag
            _img1 = pet_item_elem.find_elements(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li.uk-active > a > img")
            if _img1:
                img1 = pet_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li.uk-active > a > img").get_attribute("src")
            else:
                img1 = None
            _img2 = pet_item_elem.find_elements(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li:nth-child(2) > a > img")
            if _img2:
                img2 = pet_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.itemphoto.uk-flex.uk-flex-wrap > ul.uk-subnav.uk-subnav-pill.uk-width-1-1.uk-flex-last.uk-margin > li:nth-child(2) > a > img").get_attribute("src")
            else:
                img2 = None
            # 金額取得
            _price = pet_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.cartbox > div.cartbox-inner > dl:nth-child(1) > dd").text
            price= int(_price.replace("円", "").replace(",", "").rstrip())
            # コード取得
            code = pet_item_elem.find_element(by=By.CSS_SELECTOR, value="#maincontents > div > div.itemdetail-main.uk-flex.uk-flex-between > div.itemdetail-inner.uk-flex.uk-flex-wrap > div.uk-margin-large > div:nth-child(1) > p").text
            jan_code = code.replace("\u3000", ",").split(",")[0]
            item_code = code.replace("\u3000", ",").split(",")[1]

            df= df.append({"url": pet_item_link,
                        "title": title,
                        "img1": img1,
                        "img2": img2,
                        "price": price,
                        "jan_code": jan_code,
                        "item_code": item_code},
                        ignore_index=True)
            log.info(f"[成功]{count} 件目: {title}")
            succes += 1
        except Exception as e:
            log.info(f"[失敗]{count}件目: {title}")
            log.info(e)
            fail += 1
        finally:
            count += 1
        
    df.to_csv(f"{arg2}", encoding="utf-8")  
    log.info(f"処理完了 成功件数: {succes} 件 / 失敗件数 : {fail} 件")
    log.info("========スクレイピング終了========")
    return df


# 並列処理
def main():
    executor = ProcessPoolExecutor(max_workers=2)
    executor.submit(new_item)
    executor.submit(pets(1, "food_item_csv"))
    executor.submit(pets(2, "trimming_item_csv"))
    executor.submit(pets(3, "accessory_item_csv"))
    executor.submit(pets(4, "life_item_csv"))
    executor.submit(pets(5, "bird_item_csv"))
                                    
if __name__ == "__main__":
    main()
