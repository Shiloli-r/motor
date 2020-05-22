import requests
from bs4 import BeautifulSoup

url = "https://www.carlogos.org/car-brands/"
base_download_url = "https://www.carlogos.org{}"


data = requests.get(url).text
soup = BeautifulSoup(data, features='html.parser')
image_list = soup.find_all('ul', {'class': 'logo-list'})  # [0].find('img').get('src')
img = image_list[0].find_all('li')

for image in img:
    logo = image.find('img').get('src')
    download_url = base_download_url.format(logo)
    title = image.find('a').text
    strip = image.find('span').text
    index = title.index(strip[0])
    title = title[0:index]+".png"
    print(download_url, title)

    # Download the image
    r = requests.get(download_url, allow_redirects=True)
    open(title, 'wb').write(r.content)
print("Download completed")
