from bs4 import BeautifulSoup
import requests
import json


def get_lazada_products(item):
    """
     This function is responsible for getting a list of products based on an item search query
     :param item: the item to be searched
     :return: an array of relevant products based on the search query, each product will have its
     platform (string), name (string), price (float), url (string) and image (string)
     """
    PLATFORM = 'Lazada'
    return_products = []
    # Magic Number is the number of characters I have to delete to get a valid JSON String Object
    # To be parsed into a JSON Object
    MAGIC_NUMBER = 9

    item_word = '+'.join(item.split(' '))
    search_link = f"https://www.lazada.sg/catalog/?q={item_word}&_keyori=ss&from=input&spm=" \
                      f"a2o42.pdp_revamp.search.go.26b05b66laE9tR"

    item_data = requests.get(search_link)
    item_website = item_data.text


    soup = BeautifulSoup(item_website, "html.parser")
    list_of_scripts = soup.find_all("script")
    jsonObj = None
    for script in list_of_scripts:
        # Get the data which is in the script
        if script.contents and "window.pageData = " in script.contents[0]:
            jsonStr = script.contents[0]
            jsonStr = jsonStr.split("window.pageData = ")[1].strip().strip(";")
            redundant = jsonStr.find("// prevent")
            # Trial run to finally get the valid JSON Object
            jsonStr = jsonStr[:redundant - MAGIC_NUMBER]
            jsonObj = json.loads(jsonStr)
            break
    products = jsonObj["mods"]["listItems"]
    for item in products:
        new_product = {
            'platform': PLATFORM,
            'name': item['name'],
            'price': float(item['price']),
            'url': 'https://' + item['itemUrl'][2:],
            'image': item['image']
        }
        return_products.append(new_product)

    return return_products


# print(get_lazada_products("toys"))

# TODO: This is responsible for scraping the individual items to get updated price
# TODO: Not sure what the return value should be yet
def get_single_lazada_product(url):
    """
    This function is responsible for getting the updated price of a single product
    :param url: We would already have the url since it is an item that the user is tracking
    :return: The latest price in floating-point value
    """

    # Send request to get the data
    item_data = requests.get(url)
    item_website = item_data.text

    soup = BeautifulSoup(item_website, "html.parser")
    price = soup.find(name="span", class_="pdp-price").get_text()
    return float(price[1:])

print(get_single_lazada_product("https://www.lazada.sg/products/ready-stock-"
                                "dancing-cactus-dencing-cactus-cactus-plush-toy-talk-dancing-toy-song"
                                "-plush-early-childhood-christmas-i2140856908.html"))