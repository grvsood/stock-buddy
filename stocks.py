from tkinter import *
import requests as rq
from bs4 import BeautifulSoup
import sys

#keeps track of all the labels in the root window
labels = []

#func to create a new label with args label text, grid row and column
def get_label(item, rw, col):
    lbl = Label(window, text = item)
    lbl.grid(row = rw, column = col)
    labels.append(lbl)

#func for web scrapping
def stock():

    #clear previos labels if any
    if len(labels) != 0:
        for lbl in labels:
            lbl.destroy()

    #url for web scrapping
    url = "https://finance.yahoo.com/quote/" + str(txt.get()).upper()

    try:
        page = rq.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        #Stock Name
        stock_name = soup.select(".Mt(15px)")[0].find('h1').get_text()
        get_label(stock_name, 2, 0)

        #short description of stock value
        desc = soup.select(".Mt(15px)")[0].find(class_ = "C($c-fuji-grey-j)").get_text()
        get_label(desc, 3, 0)

        #Current Value of Stock
        price_tag = list(soup.select(".My(6px)")[0].find_all(class_ = "Trsdu(0.3s)"))
        price_items = [item.get_text() + " " for item in price_tag]
        price = ""
        for value in price_items:
            price += value + "  "
        get_label(price, 4 , 0)

        #Current status of stock: market closed or open etc.
        quote_market_notice = "Current Status: "
        quote_market_notice += list(soup.select(".My(6px)")[0].find(id = "quote-market-notice"))[0].get_text()
        get_label(quote_market_notice,5,0)

        # ....Following futher stock details are scrapped:
        # ....
        # ....Previous Close, Open, Bid, Ask, Day's Range,
        # ....52 Week Range, Volume, Avg. Volume, Market Cap,
        # ....Beta, PE Ratio(TTM), EPS(TTM), Earning Date,
        # ....Forward Dividend & Yield, Ex-Dividend Date,
        # ....1y Target ESt
        # ....
        quote_summary = soup.select("#quote-summary")[0]
        tables = quote_summary.find_all(class_ = "W(100%)")
        details = {}
        for table in tables:
            for row in table.find_all("tr"):
                values = row.find_all('td')
                details[values[0].text.strip()] = values[1].text.strip()

        row_index = 6
        for key,value in details.items():
            get_label(key + ": " + value, row_index, 0)
            row_index += 1

    except Exception as e:
        print("Error: " + e)
        print("Wrong Usage")
        print("Usage: Enter correct Ticker Symbol of company")
        print("for instance:Try these\nAMZN for Amazon.com, Inc.\nBHARTIARTL.NS for Bharti Airtel Limited")
        sys.exit(1)

#GUI
window = Tk()
window.title("Stock Buddy")
window.geometry('480x470')
txt = Entry(window, width=35)
txt.grid(row=0, column=0)
txt.focus()
bttn = Button(window, text="Get Stock", command=stock)
bttn.grid(row=0, column=1)
window.mainloop()
