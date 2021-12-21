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

url = 'http://books.toscrape.com/'
res = get_response(url)

landing_tree = etree.HTML(res.text)
# Prepare data (Element.xpath() always returns a list!)
output_list = []
headers = ['Title', 'Price', 'UPC', 'Availability']
products = landing_tree.xpath('//article[@class="product_pod"]')
for product in products:
    title = product.xpath('h3/a/@title')[0]
    price = product.xpath('.//p[@class="price_color"]/text()')[0]
    product_link = product.xpath('h3/a/@href')[0]

    product_res = get_response(f'{url}/{product_link}')
    product_tree = etree.HTML(product_res.text)
    #print(product_res.text)
    #print(product_tree)
    upc = product_tree.xpath('//*[@id="content_inner"]/article/table/tr[1]/td/text()')[0]
    #print(f"UPC: {upc}")
    availability_string = product_tree.xpath('//*[@id="content_inner"]/article/table/tr[6]/td/text()')[0]
    #print(f"Availability string: {availability_string}")
    availability = ""
    for letter in availability_string:
        if letter.isdigit():
            availability += letter
    #print(f"Availability: {availability}")

    output_list.append([title, price, upc, availability])

print(output_list)

# Write CSV file
write_csv(output_list, headers)

# Create a JSON object from data and headers
json_list = make_json(output_list, headers)

# Write JSON file
write_json(json_list)
