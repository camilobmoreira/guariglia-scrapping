# -*- coding: utf-8 -*-

# import libraries
import urllib2
from bs4 import BeautifulSoup
import re

#Parametros para busca no site
param_obs = 'Pronto em m'
param_lance_inicial = 99999999


# specify the url
quote_page = 'http://www.guariglia.com.br/?ir=lotes_veiculos_nsl&leilao=1570'

# query the website and return the html to the variable ‘page'
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
table_box = soup.find('table', attrs={'width':'1000', 'border':'0', 'cellpadding':'0', 'cellspacing':'0'})

for tr in table_box.find('tr'):
    #Pega coluna da tabela onde possui as informações
    td = tr.find('td', attrs={'width':'100%', 'align': 'left'})

    #Pega observação do veiculo
    obs = td.find('font', attrs={'color':'#008080'}).find('b').text.strip()
    if param_obs != None and param_obs not in obs:
        print('a')
        continue

    #Pega lance inicial do veiculo
    lance_inicial = int(td.find('font', attrs={'color':'#228B22'}).findNext().text.replace('R$ ', '').replace('.', '').replace(',', '').strip())
    if param_lance_inicial != None and param_lance_inicial < lance_inicial:
        print(lance_inicial)
        continue    

    marca_modelo = td.find('b').find('font').text.strip()
    ano = td.find('font', attrs={'color':'#505050'})
    temp = td.find_all('font', attrs={'color':'#505050'})
    placa = td.find(text=re.compile('Final')).strip()
    temp = str(td)
    ano = temp.split(str(ano))[1].split(str(placa))[0].split('|')[0].strip()
    print(ano)
    
    break
