from playwright.sync_api import sync_playwright
import requests

# ⚠️ 换成你自己的商品页面完整 URL
URL = "https://www.goofish.com/item?spm=a21ybx.search.searchFeedList.2.1d3d41dbIy2gK1&id=848180106380&categoryId=126860474"

def GetImageURL(page, index):
    #等待目标出现
    page.wait_for_selector(f'.slick-slide[data-index="{index}"] img')

    #取图片URL
    img = page.query_selector(f'.slick-slide[data-index="{index}"] img')
    return img.get_attribute("src")

def main():
    with sync_playwright() as p:
        #启动浏览器，初始化引擎
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #打开页面
        page.goto(URL)

        #获取图片 URL
        img_url = []
        for i in range(5):
            img_url.append(GetImageURL(page,i))



        #假装是用户
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": URL,
        }

        #下载图片
        for n in range(5):
            #处理相对URL
            if img_url[n].startswith("//"):
                img_url[n] = "https:" + img_url[n]
            resp = requests.get(img_url[n], headers=headers, timeout=10)
            resp.raise_for_status()             
            with open(f"test{n}.jpg", "wb") as f:
                f.write(resp.content)
                print(f"图片已保存为 test{n}.jpg")


        

        browser.close()

if __name__ == "__main__":
    main()
