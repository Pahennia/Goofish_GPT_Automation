import image_download 



test_product_URL = "https://www.goofish.com/item?spm=a21ybx.item.itemCnxh.11.69aa3da6p4pIWN&id=1007091382903&categoryId=0"

def main():
    image_download.download_image(test_product_URL)




if __name__ == "__main__":
    main()
