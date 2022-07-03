from bs4 import BeautifulSoup
import requests

def get_qooten_products(item):
    """
    This function is responsible for getting a list of products based on an item search query
    :param item: the item to be searched
    :return: an array of relevant products based on the search query, each product will have its
    platform (string), name (string), price (float), url (string) and image (string)
    """
    product_name = item.strip()
    PLATFORM = "Qoo10"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox / 50.0'}


               # Follow the template specified by the website, words separated by spaces joined by +
    item_word = '+'.join(item.split(' '))

    search_link = f"https://www.qoo10.sg/s/IPHONE?keyword={product_name}"

    # Send request to get the data
    item_data = requests.get(search_link, headers=headers)
    item_website = item_data.text

    soup = BeautifulSoup(item_website, "html.parser")
    item_images = soup.find_all('td', class_="td_thmb")
    item_names = soup.find_all('td', class_="td_item")
    item_prices = soup.find_all("td", class_="td_prc")


    products = []
    for i in range(len(item_images)):
        name_tag= item_names[i].find(name="div", class_="sbj")
        name = name_tag.get_text()
        url = name_tag.find(name="a")['href']
        price = item_prices[i].find(name="div", class_="prc").find(name="strong").get_text()
        image = item_images[i].find(name="div", class_="inner").find("img")['gd_src']

        new_product = {
            'platform': PLATFORM,
            'name': name,
            'price': price,
            'image': image,
            'url': url
        }
        products.append(new_product)

    return products

# TODO: This is responsible for scraping the individual items to get updated price
# TODO: Not sure what the return value should be yet
def get_single_qooten_product(url):
    """
    This function is responsible for getting the updated price of a single product
    :param url: We would already have the url since it is an item that the user is tracking
    :return: The latest price in floating-point value
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox / 50.0'}

    # Send request to get the data
    item_data = requests.get(url, headers=headers)
    item_website = item_data.text


    soup = BeautifulSoup(item_website, "html.parser")
    price = soup.find(id="qprice_span").get_text()

    return price
