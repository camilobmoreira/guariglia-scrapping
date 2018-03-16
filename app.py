# -*- coding: utf-8 -*-


# import libraries
import urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://www.guariglia.com.br/?ir=lotes_veiculos_nsl&leilao=1569'

# query the website and return the html to the variable ‘page'
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
table_box = soup.find('table', attrs={'width':'1000', 'border':'0', 'cellpadding':'0', 'cellspacing':'0'})

for tr in table_box.find('tr'):
    td = tr.find('td', attrs={'align': 'left'})
    print(td)

print(table_box)