from bs4 import BeautifulSoup
import requests


def get_amazon_products(item):
    """
    This function is responsible for getting a list of products based on an item search query
    :param item: the item to be searched
    :return: an array of relevant products based on the search query, each product will have its name (string),
    price (float), url (string) and image (string)
    """

    # Follow the template specified by the website, words separated by spaces joined by +
    item_word = '+'.join(item.split(' '))

    search_link = f"https://www.amazon.sg/s?k={item_word}&crid=2J3NF4V3FF6EZ&" \
                      f"sprefix=water+bott%2Caps%2C310&ref=nb_sb_noss_2"

    # Send request to get the data
    item_data = requests.get(search_link)
    item_website = item_data.text

    soup = BeautifulSoup(item_website, "html.parser")

    # Some elements found with a-section may not be those with the items
    # So we need to do filtering when looping through (checking if == None)
    items = soup.find_all(name="div", class_="a-spacing-base")

    # For some reason there are duplicates (2 of each)
    # So I filter and put them into the final_objects
    item_objects = []
    final_objects = []

    for item in items:
        # Validation
        # If it is possible for us to get all the items, we will add the product into our array
        # If not, it means it is redundant
        image = item.find("img", class_="s-image")
        if image != None:
            image = image['src']
        name = item.find("span", class_="a-text-normal")
        if name == None:
            continue
        name = name.get_text()
        price = item.find("span", class_="a-offscreen")
        if price == None:
            continue
        price = price.get_text()
        link = item.find("a", class_="a-link-normal", href=True)
        url = f"https://amazon.sg/{link['href']}"

        # Create an object with the necessary data that we need
        new_item = {
            'name': name,
            'price': float(price[2:]),
            'url': url,
            'image': image
        }
        item_objects.append(new_item)

    for i in range(len(item_objects)):
        if i % 2 == 0:
            final_objects.append(item_objects[i])

    # The objects that we need
    for i in range(len(final_objects)):
        # print(final_objects[i])
        pass

    return final_objects

print(get_amazon_products("biscuits"))

# TODO: This is responsible for scraping the individual items to get updated price
# TODO: Not sure what the return value should be yet
def get_single_amazon_product(url):
    """
    This function is responsible for getting the updated price of a single product
    :param url: We would already have the url since it is an item that the user is tracking
    :return: The latest price in floating-point value
    """

    # Send request to get the data
    item_data = requests.get(url)
    item_website = item_data.text

    soup = BeautifulSoup(item_website, "html.parser")
    price = ""

    item_whole_price = soup.find("span", class_="a-price-whole").getText()
    price += item_whole_price
    item_decimal_price = soup.find("span", class_="a-price-fraction").getText()
    price += item_decimal_price

    return float(price)

# print(get_single_amazon_product("https://www.amazon.sg//All-Time-Assorted-Biscuits-524-7/dp/B07YNPXNDW"))


