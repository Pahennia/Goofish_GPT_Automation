from playwright.sync_api import sync_playwright
import requests
from pathlib import Path


def GetImageURL(page, index):
    #等待目标出现
    page.wait_for_selector(f'.slick-slide[data-index="{index}"] img')
    #取图片URL
    img = page.query_selector(f'.slick-slide[data-index="{index}"] img')
    return img.get_attribute("src")

def download_image(urls):
    print(len(urls))
    a = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        pages = []
        for i in range(2):
            context = browser.new_context()
            page = context.new_page()
            pages.append(page)
        pages[0].goto(urls[0])
        for i in range(len(urls)-1):
            pages[(i+1)%2].goto(urls[i+1])
            download(pages[i%2], urls[i])
        download(pages[(len(urls)-1)%2], urls[-1])
        # finished = []
        # for i in range(len(urls)//10):
        #     for n in range(9):
        #         #传送URL
        #         print(urls[((i)*10)+(n)])
        #         # pages[n-1].goto(urls[((i-1)*10)+(n-1)])
        #         # finished[(i-1)*10+(n-1)] = download(pages[n-1],urls[((i-1)*10)+(n-1)])

        # for i in range(len(urls)):
        #     print(urls[i])

def download(page, URL):
        #等待加载
        page.wait_for_function(
    """
    () => {
        const slides = document.querySelectorAll(
            '.slick-slide:not(.slick-cloned)[data-index]'
        );
        if (slides.length === 0) return false;

        if (!window.__lastCount) {
            window.__lastCount = slides.length;
            window.__lastChange = Date.now();
            return false;
        }

        if (slides.length !== window.__lastCount) {
            window.__lastCount = slides.length;
            window.__lastChange = Date.now();
            return false;
        }

        return Date.now() - window.__lastChange > 800;
    }
    """,
    timeout=20000
)
        
        #获取图片数量
        max_index = page.evaluate("""
() => {
    const slides = document.querySelectorAll('[data-index]');
    const indices = [...slides].map(el => Number(el.dataset.index));
    return Math.max(...indices);
}
""")
        img_num = (max_index + 1)//2
       
        #获取图片 URL
        img_url = []
        for i in range(img_num):
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

        #检测URL id
        URL_id = URL.split("id=")[1].split("&cat")[0]
        #创建目录
        path = Path(f"data/images/{URL_id}")
        path.mkdir(parents=True, exist_ok=True)
        txt_path = path / "img_num.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(str(img_num) + "\n")
        print("图片数量已保存：",img_num)
        #下载图片
        for n in range(img_num):
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
            #下载图片
            resp = requests.get(img_url[n], headers=headers, timeout=10)
            resp.raise_for_status()             
            img_path = path / f"img_{n}.jpg"
            img_path.write_bytes(resp.content)
            print(f"已保存：{img_path}")


        

        return True

if __name__ == "__main__":
    test_product_URL = "https://www.goofish.com/item?spm=a21ybx.search.searchFeedList.4.147641dbNLBFB2&id=1000595447381&categoryId=126860474"
    download_image(test_product_URL)
