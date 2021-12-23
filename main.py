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

protocol = "https"  # Protocol (default https) can also be http which is way faster!
# Adds :// for convenience so there's no need to type it out
if not (protocol.endswith("://")):
    protocol = protocol + "://"

root_url = 'books.toscrape.com'  # Root page of Book to Scrape (books.toscrape.com)
# Removes protocol part from root_url
if "https://" in root_url:
    root_url = root_url.replace("https://", "")
if "http://" in root_url:
    root_url = root_url.replace("http://", "")
# Checks if root_url contains slash and if not then adds a slash at the end
if root_url[-1] != "/":
    root_url += "/"

# URL to be scraped (can be root_url, but takes awhile to get all 50 pages worth of data), works with all categories
next_url = root_url
# Removes protocol part from next_url
if "https://" in next_url:
    next_url = next_url.replace("https://", "")
if "http://" in next_url:
    next_url = next_url.replace("http://", "")
# Modifies next_url to not contain index.html at the end as it's not necessary
if next_url.endswith("index.html"):
    next_url = next_url.replace("index.html", "")

# Removes root_url part from next_url
if root_url in next_url:
    next_url = next_url.replace(root_url, "")

# Variables needed for looping multiple pages
page_start = 1  # Page starts at 1
current_page = 0  # Current page starts at 0
page_end = current_page + 1  # Default ending page is 1 more than current_page so the while loop runs at least once
category = ""  # Category of books, starts with empty string, main landing page can have no category in URL sometimes

# While loop that loops until current_page
while current_page != page_end:
    # Removes root_url from next_url
    next_url = next_url.replace(root_url, "")

    # Calls for a custom function that checks for exceptions and then gets response from given URL if request is OK
    res = get_response(protocol + root_url + next_url)

    landing_tree = etree.HTML(res.text)  # Creates a tree based on the response in text format
    products = landing_tree.xpath('//article[@class="product_pod"]')  # Finds and returns products from the tree

    # Tries to get pagination element as text
    try:
        pagination = landing_tree.xpath('//li[contains(@class, "current")]/text()')[0]  # Gets pagination
    # Catches IndexError
    except IndexError:
        pagination = None   # Sets pagination = None meaning there are no pages to this URL
    # If there is pagination (isn't None)
    if pagination is not None:
        pagination = pagination.strip()  # For some reason, some pages contain whitespace, removes that
        pagination = [number for number in pagination.split() if number.isdigit()]  # Finds all numbers in pagination
        # and puts them inside a list that is named pagination
        current_page = pagination[0]  # Sets current page to be the first element of the list
        page_end = pagination[1]  # Sets end page to be the second element of the list
    else:
        current_page = 1    # This is the first page
        page_end = current_page  # And also the last page
    print(f"Page {current_page} of {page_end}")  # Print's out the pager to view what page the program is on

    # If URL contains "category" then find the category, else the category was not found, it means next_url was set to
    # root_url at the start and the unique characteristic happens where the URL will not contain category at all
    if "category" in next_url:
        # Iterates over words in url separated by "/"
        for word in next_url.split("/"):
            # If the word contains "_" it means it has found the correct URL part with the category
            if "_" in word:
                category = word  # Saves category
    else:
        category = ""   # Sets category to be empty since URL doesn't require it (next_url at start)

    # For every product found on page, cycles through them and gets their Title, Price, UPC and Availability via XPath
    for product in products:
        title = product.xpath('h3/a/@title')[0]  # Gets title of product from category page
        print(title)
        price = product.xpath('.//p[@class="price_color"]/text()')[0]  # Gets price of product from category page
        product_link = product.xpath('h3/a/@href')[0]  # Gets the product link to get the rest of the variables

        # # If href contains relative paths then remove them, found this uniqueness in some hrefs, quick workaround fix
        if "../" in product_link:
            product_link = product_link.replace("../", "")

        # If href starts with catalogue/ then no modification is required, else modify request URL to contain catalogue/
        if product_link.startswith('catalogue/'):
            product_res = get_response(f'{protocol}{root_url}{product_link}')  # Builds the link, unmodified
        else:
            product_res = get_response(f'{protocol}{root_url}catalogue/{product_link}')  # Builds the link, modified

        product_tree = etree.HTML(product_res.text)  # Gets the product page element tree
        upc = product_tree.xpath('//*[@id="content_inner"]/article/table/tr[1]/td/text()')[0]  # Gets the product's UPC
        # Gets the string that contains how many products are in stock, saves it as availability_string
        availability_string = product_tree.xpath('//*[@id="content_inner"]/article/table/tr[6]/td/text()')[0]
        # Creates a new empty string called availability
        availability = ""
        # Finds the numbers in the availability_string and adds them to availability which means now availability is the
        # correct value of stock for the given product (book)
        for letter in availability_string:
            if letter.isdigit():
                availability += letter

        # Appends all retrieved product data on page as a list to output_list variable, which is also a list
        output_list.append([title, price, upc, availability])

    # If not the last page / there's more pages
    if current_page != page_end:
        next_page_href = landing_tree.xpath('//li[contains(@class, "next")]/a/@href')[0]  # Get href of the next page
        if not (next_page_href.startswith("/")):
            next_page_href = "/" + next_page_href  # Adds slash to the start of href link for uniformity

        # Found on page with this unique lack of uniformity in href where next_url = root_url, quick workaround fix
        if "catalogue/" in next_page_href:
            next_url = f"{root_url}{next_page_href}"  # Creates the next page URL
        # If category is books_1 then the URL system is unique from the rest so the URL must be built differently (it
        # doesn't contain books/ but all the other categories do
        elif category == "books_1":
            next_url = f"{root_url}catalogue/category/{category}{next_page_href}"   # Creates the next page URL
        # Else if normal href
        else:
            next_url = f"{root_url}catalogue/category/books/{category}{next_page_href}"  # Creates the next page URL

print("\n//////////////////////////////Finished scraping!//////////////////////////////")   # Scraped
print(f"Found {str(len(output_list))} entries (books)")  # Books found
for output in output_list:
    print(output)

print("\nWriting to files..")   # Starts writing to files
# Write CSV file out of data
write_csv(output_list, headers)
print("Wrote output.csv")

# Create a JSON object from data and headers to be written into a json file
json_list = make_json(output_list, headers)
print("Made some JSON")

# Write JSON file out of the list of json objects (json_list)
write_json(json_list)
print("Wrote output.json")
