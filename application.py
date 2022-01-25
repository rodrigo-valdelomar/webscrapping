from wsgiref import headers
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# url to web scrape from
my_url = "https://televisores.mercadolibre.com.ar/televisores/#menu=categories"

# opens the connection and downloads html page from url
uClient = uReq(my_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type
page_html = uClient.read()
page_soup = soup(page_html, "html.parser")
uClient.close()

# finds each product from the store page
containers = page_soup.findAll("li", {"class", "ui-search-layout__item"})

# name the output file to write to local disk
filename = "mercadolibre_tvs.csv"
f = open(filename, "w")
headers = "Titulo, Marca, Modelo, Precio, Link, Envío\n"

f.write(headers)


# loops over each product and grabs attributes about
# each product
for container in containers:
    title = container.findAll("a", {"class", "ui-search-item__group__element"})
    titulo = title[0].text

    link = title[0]["href"]

    # opens the connection and downloads html page from url for the specific product
    uClient_2 = uReq(link)
    page_html_item = uClient_2.read()
    page_soup = soup(page_html_item, "html.parser")
    uClient.close()

    brand_container = page_soup.findAll("span", {"class", "andes-table__column--value"})
    brand = brand_container[0].text

    model_container = page_soup.findAll("tr", {"class", "andes-table__row"})
    model_aux = model_container[1].findAll("span", {"class", "andes-table__column--value")
    model = model_aux[0].text

    price_container = page_soup.findAll("div", {"class", "ui-pdp-price__second-line"})
    price = price_container[0].meta["content"]

    shipping_container = page_soup.findAll({"p", "ui-pdp-media__title"})
    shipping = shipping_container[32].text

    print("Título: " + titulo)
    print("Marca: " + brand)
    print("Modelo: " + model)
    print("Precio: " + price)
    print("Link: " + link)
    print("Envío: " + shipping)

    f.write(titulo.replace(",", "|") + "," + "brand" + "," + "model" + "," + price + "," + "link" + "," + "shipping" + "\n")

f.close()
