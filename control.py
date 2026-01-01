import image_download 
import product_URL


test_page_URL = "https://www.goofish.com/search?q=%E5%B7%B4%E9%BB%8E%E4%B8%96%E5%AE%B6Track1.0&spm=a21ybx.search.searchInput.0"

def main():
    all_urls = []
    all_urls = product_URL.get_product_URL(test_page_URL)
    # for url in all_urls:
    #     image_download.download_image(url)
    print(all_urls)
    
    with open("urls.txt", "w", encoding="utf-8") as f:
        for url in all_urls:
            f.write(url + "\n")
            
if __name__ == "__main__":
    main()

