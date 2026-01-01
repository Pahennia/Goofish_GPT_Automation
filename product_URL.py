from playwright.sync_api import sync_playwright, TimeoutError
import requests


Test_Home_URL = "https://www.goofish.com/search?q=%E5%B7%B4%E9%BB%8E%E4%B8%96%E5%AE%B6track1.0&spm=a21ybx.search.searchInput.0"

def login_intercept_check(page):
    try:
        page.wait_for_selector(
            'iframe[src*="passport.goofish.com"]',
            timeout=3000
        )
        print("检测到登录拦截，刷新页面")
        page.reload(wait_until="domcontentloaded")
    except TimeoutError:
        print("未检测到登录拦截")

def waited_too_long(page):
    try:
        page.wait_for_selector(
            'div[class*="feed-list"]',
            timeout=3000
        )
    except TimeoutError:
        print("等待时间太长，重新加载页面")
        page.reload(wait_until="domcontentloaded")
    

def flip_page(page, page_num):
    if page_num <= 49:
        page.click('button:has(div[class*="arrow-right"])')
        print(f"已翻至第 {page_num+1} 页")

def wait_for_page_load(page):
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
    print("页面加载完成")
    

def get_product_URL(Home_URL):
    all_urls = []
    with sync_playwright() as p:
        #启动浏览器，初始化引擎
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(Home_URL, wait_until="domcontentloaded")
        #检测登录拦截
        login_intercept_check(page)
        #等待页面加载
        wait_for_page_load(page)

        #浏览器合法化请求头
        page.set_extra_http_headers({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": Home_URL
        })
        
        #定位URL容器
        container = page.query_selector('div[data-spm="searchFeedList"]')
        links = container.query_selector_all(
            'a[href^="https://www.goofish.com/item"]'
        
        )
        #为每一页循环获取URL
        for i in range(1, 30):
            #加载和初始化
            login_intercept_check(page)
            wait_for_page_load(page)
            #获取链接
            for a in links:
                href = a.get_attribute("href")
                all_urls.append(href)
            print(f"第 {i} 页 URL 获取完成")
            #页面翻页，初始化
            flip_page(page, i)
            

        
        
    return all_urls

if __name__ == "__main__":
    get_product_URL(Test_Home_URL)
