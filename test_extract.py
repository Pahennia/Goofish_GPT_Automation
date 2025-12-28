from playwright.sync_api import sync_playwright
import requests

#定位网站URL
URL = "https://www.goofish.com/item?spm=a21ybx.search.searchFeedList.2.1d3d41db5sx6bc&id=1007751981044&categoryId=126860474"

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
        for i in range(15):
            img_url.append(GetImageURL(page,i))



        #浏览器合法化请求头
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": URL,
        }

        #下载图片
        for n in range(15):
            #定义图片
            img = page.query_selector(f'.slick-slide[data-index="{n}"] img')
            #定位图片的上层分类元素
            slide = img.evaluate_handle("el => el.closest('.slick-slide')")
            #获取class属性
            class_attr = slide.get_attribute("class") or ""
            #判断有没有clone标记
            if "slick-cloned" in class_attr:
                #若被标记，跳过下载
                break
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
