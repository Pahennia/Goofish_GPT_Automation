from playwright.sync_api import sync_playwright
import requests
import image_download 

#定位网站URL
Home_URL = "https://www.goofish.com/search?spm=a21ybx.home.searchHistory.1.4c053da6Hs9GW9&q=%E5%B7%B4%E9%BB%8E%E4%B8%96%E5%AE%B6Track1.0"

test_product_URL = "https://www.goofish.com/item?spm=a21ybx.item.itemCnxh.11.69aa3da6p4pIWN&id=1007091382903&categoryId=0"

def main():
    with sync_playwright() as p:
        #启动浏览器，初始化引擎
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        #打开页面
        page.goto(Home_URL)
        #浏览器合法化请求头
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": Home_URL,
        }
        image_download.download_image(Home_URL)



        browser.close()

if __name__ == "__main__":
    main()
