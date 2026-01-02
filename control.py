import image_download 
import product_URL
import time
test_page_URL = "https://www.goofish.com/search?q=%E5%B7%B4%E9%BB%8E%E4%B8%96%E5%AE%B6Track1.0&spm=a21ybx.search.searchInput.0"

def grab_all_urls():
    all_urls = []
    #加载全部URL
    all_urls = product_URL.get_product_URL(test_page_URL)
    #下载全部URL图片
    print(all_urls)
    image_download.download_image(all_urls)
    #保存所有URL到本地文件
    with open("urls.txt", "w", encoding="utf-8") as f:
        for url in all_urls:
            f.write(url + "\n")
            
if __name__ == "__main__":
    grab_all_urls()