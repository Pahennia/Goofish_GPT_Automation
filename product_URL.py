from playwright.sync_api import sync_playwright
import requests

Test_Home_URL = "https://www.goofish.com/search?spm=a21ybx.home.searchHistory.1.6d833da6XHiYYZ&q=%E5%B7%B4%E9%BB%8E%E4%B8%96%E5%AE%B6Track1.0"
def get_product_URL(Home_URL):
    with sync_playwright() as p:
        #启动浏览器，初始化引擎
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(Home_URL)
        page.wait_for_function(
            """
            () => {
               const container = document.querySelector(
                    'div[data-spm="searchFeedList"]'
                );
                if (!container) return false;

                return container.querySelectorAll(
                    'a[href^="https://www.goofish.com/item"]'
                ).length >= 30;
            }
            """,
           timeout=20000
        )

        #浏览器合法化请求头
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": Home_URL,
        }
        #获取所有商品 URL
        container = page.query_selector('div[data-spm="searchFeedList"]')
        links = container.query_selector_all(
            'a[href^="https://www.goofish.com/item"]'
        )
        #赋值URL列表
        urls = []
        for a in links:
            href = a.get_attribute("href")
            urls.append(href)


        browser.close()
    return urls

if __name__ == "__main__":
    print(get_product_URL(Test_Home_URL))
