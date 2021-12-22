"""
  Assignment:

  Extract all product urls from category:
  http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html

  Crawl all the products and get each of their:
      - name
      - price
      - upc
      - availability (how many available)

  Return data as CSV file (add headers for fields).

  Bonuses:
   - use an error catch when calling request.get()
   - clean price
   - create extra output file where data is JSON serialized

  Here we have a template for you:
  It gets the products from landing page and writes name / price to csv.
  Modify the code as needed

"""
from requester import get_response
from file_writer import write_csv, write_json
from jsonifier import make_json
from lxml import etree

output_list = []  # Empty placeholder list for scraped data
headers = ['Title', 'Price', 'UPC', 'Availability']  # Headers for the scraped data
protocol = "https://"   # Protocol (default https://) can also be http
root_url = 'https://books.toscrape.com/'  # Page to be scraped (must be root of the page) https://books.toscrape.com/

# Removes protocol from root_url
if "https://" in root_url:
    root_url = root_url.replace("https://", "")
if "http://" in root_url:
    root_url = root_url.replace("http://", "")

# Checks if URL contains slash and if not adds a slash at the end
if root_url[-1] != "/":
    root_url += "/"


# URL to be scraped (can be root_url, but takes awhile to get all 50 pages worth of data)
next_url = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"

# Removes protocol from next_url
if "https://" in next_url:
    next_url = next_url.replace("https://", "")
if "http://" in next_url:
    next_url = next_url.replace("http://", "")

# Removes root_url from next_url
if root_url in next_url:
    next_url = next_url.replace(root_url, "")

page_start = 1  # Page starts at 1
current_page = 0  # Current page starts at 0
page_end = current_page + 1  # Default ending page is 1 more than current_page so the while loop runs at least once
category_url_part = ""  # Structural part for building URLs


# While loop that loops until current_page
while current_page != page_end:
    # Modifies next_url to not contain index.html at the end as it's not necessary
    if next_url.endswith("index.html"):
        next_url = next_url.replace("index.html", "")
    # Removes root_url from next_url
    next_url = next_url.replace(root_url, "")


    # Builds new middle structure inside category_url_part variable if next_url contains string "category"
    if "category" in next_url:
        for value in next_url.split("/"):
            category_url_part += "/" + value
        # Takes out the category section of the URL
        next_url = next_url.replace(category_url_part, "")
        print(category_url_part)
    else:
        category_url_part = ""

    # Calls for custom function that checks for exceptions and then gets response from given URL if request is OK
    res = get_response(protocol + root_url + category_url_part + next_url)
    print(res.url)
    current_page += 1   # Every time a new response is called, increment current_page by 1
    landing_tree = etree.HTML(res.text)  # Creates a tree based on the response in text format
    products = landing_tree.xpath('//article[@class="product_pod"]')  # Finds and returns products from the tree

    # Tries to get the next button and if it's unable to, proceeds with next_button being None, meaning current_page is
    # the last page
    try:
        next_li = landing_tree.xpath('//li[contains(@class, "next")]')[0]
    except IndexError:
        next_li = None
    # If statement that checks if it's the first loop cycle and retrieves li element with class "current" as text that
    # has a value of, for example, "Page 1 of 50" and retrieves the last page from that string and tries to cast it as
    # int, if it fails at casting, throws ValueError exception and exits; not being able to retrieve the li element also
    # ends up in the program exiting
    if current_page == 1:
        try:
            pagination = landing_tree.xpath('//li[contains(@class, "current")]/text()')[0]
        except IndexError:
            pagination = None
        if pagination is not None:
            pages_list = pagination.split()
            try:
                page_end = int(pages_list[3])
            except ValueError as ex:
                SystemExit(ex)
        else:
            page_end = current_page

    # For every product found on page, gets their Title, Price, UPC and Availability
    for product in products:
        title = product.xpath('h3/a/@title')[0]
        print(title)
        price = product.xpath('.//p[@class="price_color"]/text()')[0]
        product_link = product.xpath('h3/a/@href')[0]

        gibberish = "../../../"
        if gibberish in product_link:
            product_link = product_link.replace(gibberish, '')
        if product_link.startswith('catalogue/'):
            product_res = get_response(f'{root_url}{product_link}')
        else:
            product_res = get_response(f'{protocol}{root_url}catalogue/{product_link}')
        product_tree = etree.HTML(product_res.text)
        upc = product_tree.xpath('//*[@id="content_inner"]/article/table/tr[1]/td/text()')[0]
        availability_string = product_tree.xpath('//*[@id="content_inner"]/article/table/tr[6]/td/text()')[0]
        availability = ""
        for letter in availability_string:
            if letter.isdigit():
                availability += letter

        # Appends all retrieved product data on page as a list to output_list variable, which is also a list
        output_list.append([title, price, upc, availability])

    if next_li is not None:
        next_page_href = landing_tree.xpath('//li[contains(@class, "next")]/a/@href')[0]
        if next_page_href.startswith('catalogue/'):
            next_url = root_url + next_page_href
        else:
            if "category" in next_url and "":
                next_url = root_url + 'catalogue/category' + next_page_href
            else:
                next_url = root_url + 'catalogue/' + next_page_href

print(output_list)
print("Length of output_list: " + str(len(output_list)))

# Write CSV file out of data and headers
write_csv(output_list, headers)

# Create a JSON object from data and headers to be written into a json file
json_list = make_json(output_list, headers)

# Write JSON file
write_json(json_list)
