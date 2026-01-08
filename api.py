import asyncio
from paraprocess import activate_download

def download_images(urls):
    return asyncio.run(activate_download(urls))