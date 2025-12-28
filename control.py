import image_download 
import product_URL


test_page_URL = "https://www.goofish.com/search?q=%E5%B7%B4%E9%BB%8E%E4%B8%96%E5%AE%B6Track1.0&spm=a21ybx.search.searchInput.0"

def main():
    current_page_URLs = product_URL.get_product_URL(test_page_URL)
    for url in current_page_URLs:
        image_download.download_image(url)


if __name__ == "__main__":
    main()
