from playwright.async_api import async_playwright
import asyncio
import requests
from pathlib import Path

#获取图片 URL
async def GetImageURL(page, index):
    #等待目标出现
    await page.wait_for_selector(f'.slick-slide[data-index="{index}"] img')
    #取图片URL
    img = await page.query_selector(f'.slick-slide[data-index="{index}"] img')
    return await img.get_attribute("src")

#下载控制器
async def download_image(urls):
    Task = []
    print(len(urls))
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        pages = []
        for i in range(1):
            context = await browser.new_context()
            page = await context.new_page()
            pages.append(page)
            request = context.request
        for i in range(len(urls)):
            await pages[0].goto(urls[i])
            print(i)
            print("你好")
            await download(pages[0], urls[i], request)
            


    


#下载模块
async def download(page, URL, request):
        #等待加载
        await page.wait_for_function(
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
        max_index = await page.evaluate("""
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
            img_url.append(await GetImageURL(page,i))



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
        Task = []
        i = 0
        for n in range(img_num):
            #定义图片
            img = await page.query_selector(f'.slick-slide[data-index="{n}"] img')
            #定位图片的上层分类元素
            slide = await img.evaluate_handle("el => el.closest('.slick-slide')")
            #获取class属性
            class_attr = await slide.get_attribute("class") or ""
            #判断有没有clone标记
            if "slick-cloned" in class_attr:
                #若被标记，跳过下载
                break
            #处理相对URL
            if img_url[n].startswith("//"):
                img_url[n] = "https:" + img_url[n]
            #下载图片

            Task.append(
                asyncio.create_task(
                    download_image_async(img_url, n, path, request)
                )
            )
            await asyncio.gather(*Task)
            i += 1
        
        for n in range(img_num):
            await Task[n]
        return True

#下载图片
async def download_image_async(img_url, n, path, request): 
    resp = await request.get(img_url[n])

    if not resp.ok:
        raise RuntimeError(f"HTTP {resp.status}")

    data = await resp.body()

    img_path = path / f"img_{n+1}.jpg"
    img_path.write_bytes(data)

    print(f"已保存：{img_path}")  
    


async def main():
    urls = ['https://www.goofish.com/item?id=991876721317&categoryId=126860474', 'https://www.goofish.com/item?id=970820651619&categoryId=126860474', 'https://www.goofish.com/item?id=1008220737174&categoryId=126860474', 'https://www.goofish.com/item?id=1010927284852&categoryId=126860474', 'https://www.goofish.com/item?id=993885913571&categoryId=126860474', 'https://www.goofish.com/item?id=1005161660357&categoryId=126860474', 'https://www.goofish.com/item?id=992367336573&categoryId=126888001', 'https://www.goofish.com/item?id=922906821551&categoryId=126860474', 'https://www.goofish.com/item?id=947642837225&categoryId=126860474', 'https://www.goofish.com/item?id=1007349653351&categoryId=126860474', 'https://www.goofish.com/item?id=995158145235&categoryId=126860474', 'https://www.goofish.com/item?id=973888217184&categoryId=126860474', 'https://www.goofish.com/item?id=1003885636478&categoryId=126860474', 'https://www.goofish.com/item?id=981652986161&categoryId=126860474', 'https://www.goofish.com/item?id=1007345139505&categoryId=126888001', 'https://www.goofish.com/item?id=967124400466&categoryId=126888001', 'https://www.goofish.com/item?id=1004423161791&categoryId=126888001', 'https://www.goofish.com/item?id=990868130075&categoryId=126888001', 'https://www.goofish.com/item?id=874543726983&categoryId=126866685', 'https://www.goofish.com/item?id=922012341386&categoryId=126860474', 'https://www.goofish.com/item?id=970820559284&categoryId=126860474', 'https://www.goofish.com/item?id=912298840345&categoryId=126888001', 'https://www.goofish.com/item?id=1006195622751&categoryId=126860474', 'https://www.goofish.com/item?id=944317877335&categoryId=126860474', 'https://www.goofish.com/item?id=1011089076392&categoryId=126860474', 'https://www.goofish.com/item?id=948646466285&categoryId=126860474', 'https://www.goofish.com/item?id=979962186134&categoryId=126888001', 'https://www.goofish.com/item?id=1007777839551&categoryId=126888001', 'https://www.goofish.com/item?id=952008757251&categoryId=126866685', 'https://www.goofish.com/item?id=982797184575&categoryId=126860474', 'https://www.goofish.com/item?id=994163591397&categoryId=126860474', 'https://www.goofish.com/item?id=1009796346231&categoryId=126860474', 'https://www.goofish.com/item?id=1008041019528&categoryId=126860474', 'https://www.goofish.com/item?id=997580591170&categoryId=126860474', 'https://www.goofish.com/item?id=1006275455211&categoryId=126888001', 'https://www.goofish.com/item?id=1002902246938&categoryId=126860474', 'https://www.goofish.com/item?id=991855564857&categoryId=126888001', 'https://www.goofish.com/item?id=980598657359&categoryId=126866685', 'https://www.goofish.com/item?id=977314501493&categoryId=126860474', 'https://www.goofish.com/item?id=1005029743931&categoryId=126888001', 'https://www.goofish.com/item?id=969377482281&categoryId=126888001', 'https://www.goofish.com/item?id=910821330043&categoryId=126860474', 'https://www.goofish.com/item?id=1010635969460&categoryId=126860474', 'https://www.goofish.com/item?id=1000476102110&categoryId=126860474', 'https://www.goofish.com/item?id=1001408071962&categoryId=126860474', 'https://www.goofish.com/item?id=941178114912&categoryId=126860474', 'https://www.goofish.com/item?id=1005572547072&categoryId=126860474', 'https://www.goofish.com/item?id=962227213531&categoryId=126860474', 'https://www.goofish.com/item?id=1009349491841&categoryId=126860474', 'https://www.goofish.com/item?id=923416204740&categoryId=126866685', 'https://www.goofish.com/item?id=983262722284&categoryId=126860474', 'https://www.goofish.com/item?id=923084217926&categoryId=126866685', 'https://www.goofish.com/item?id=1008154202594&categoryId=126860474', 'https://www.goofish.com/item?id=994824280791&categoryId=126860474', 'https://www.goofish.com/item?id=958231748477&categoryId=126860474', 'https://www.goofish.com/item?id=1009491141500&categoryId=126860474', 'https://www.goofish.com/item?id=994619388313&categoryId=126888001', 'https://www.goofish.com/item?id=868311192280&categoryId=126860474', 'https://www.goofish.com/item?id=945776252876&categoryId=126860474', 'https://www.goofish.com/item?id=1007785376262&categoryId=126860474']

    await (download_image(urls))

async def activate_download(urls):
    await (download_image(urls))

if __name__ == "__main__":
    asyncio.run(main())
    
