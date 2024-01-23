import httpx
import os
import asyncio
from bs4 import BeautifulSoup

def download_file(url, path) -> None:
    with httpx.stream('GET', url) as resp:
        with open(path, "wb") as out_file:
            for chunk in resp.iter_bytes():
                out_file.write(chunk)

folder_path = os.path.join(os.path.curdir, "downloaded")

print(folder_path)

if (os.path.isdir(folder_path)):
    pass
else:
    os.mkdir("downloaded")
url = "https://xkcd.com/"

last_index_comix = 10

async def inspect_file(index):
    async with httpx.AsyncClient() as client:
        r = await client.get(os.path.join(url, str(index) + "/"))
        soup = BeautifulSoup(r, "html5lib")
        div = soup.find('div', {'id':'comic'})

        img_src = div.find('img').attrs['src']
        file_name = "xkcd#" + str(index) +".png"
        download_file("https:" + img_src, os.path.join(folder_path, file_name))
        

    
async def main():
    tasks = []

    for index in range(1, last_index_comix):
        tasks.append(inspect_file(index))
    results = await asyncio.gather(*tasks)

asyncio.run(main())

        

    


