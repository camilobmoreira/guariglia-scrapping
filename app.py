# -*- coding: utf-8 -*-

# import libraries
import urllib2
from bs4 import BeautifulSoup
import re

#Parametros para busca no site
param_obs = 'Pronto em m'
param_valor_max = 99999999


# specify the url
quote_page = 'http://www.guariglia.com.br/?ir=lotes_veiculos_nsl&leilao=1570'

# query the website and return the html to the variable ‘page'
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
#table_box = soup.find_all('table', attrs={'width':'1000', 'border':'0'})
table_box = soup.find_all('tr', attrs={'bgcolor':'#F3F4F5'})

for tr in table_box:
    #Pega coluna da tabela onde possui as informações
    td = tr.find('td', attrs={'width':'100%', 'align': 'left'})

    #Pega observação do veiculo
    obs = td.find('font', attrs={'color':'#008080'}).find('b').text.strip()

    #Verifica se a observacao esta de acordo com o parametro passado
    if param_obs != None and param_obs not in obs:
        continue

    #Pega lance inicial do veiculo
    lance_inicial = int(td.find('font', attrs={'color':'#228B22'}).findNext().text.replace('R$ ', '').replace('.', '').replace(',', '').strip())

    #Pega maior lance
    maior_lance = int(tr.find('font', attrs={'color':'#FF0000'}).text.replace('R$ ', '').replace('.', '').replace(',', '').strip())

    #Verifica se o valor atual esta de acordo com o parametro passado
    if param_valor_max is not None and (lance_inicial > param_valor_max or maior_lance > param_valor_max):
        continue    

    #Pega a descricao (modelo/marca) do veiculo
    marca_modelo = td.find('b').find('font').text.strip()

    # Pega o final da placa do carro
    placa = td.find(text=re.compile('Final')).strip()

    #Pega o ano do carro
    ano = td.find('font', attrs={'color':'#505050'})
    ano = str(td).split(str(ano))[1].split(str(placa))[0].split('|')[0].strip()