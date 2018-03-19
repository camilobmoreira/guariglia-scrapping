# -*- coding: utf-8 -*-

# import libraries
import urllib2
from bs4 import BeautifulSoup
import re
import csv
import time

#Parametros para busca no site
param_obs = 'Pronto em m'
param_valor_max = 99999999

# specify the url
leiloes = ['1570', '1571']

for leilao in leiloes:
    pagina_base = 'http://www.guariglia.com.br/'
    quote_page = pagina_base + '?ir=lotes_veiculos_nsl&leilao=' + leilao

    #Cria um arquivo csv para cada leilao
    csv_leilao = open('dados_leilao_' + leilao + '.csv', 'w')

    writer = csv.writer(csv_leilao)

    writer.writerow(['marca_modelo', 'ano', 'placa', 'lance_inicial', 'maior_lance', 'obs', 'lote'])

    # query the website and return the html to the variable ‘page'
    page = urllib2.urlopen(quote_page)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    paginas = []
    paginas.append(quote_page)

    div_paginas = soup.find('div', attrs={'align':'center'})

    for pag in div_paginas.find_all('a', href=re.compile('ir=lotes_veiculos_nsl&leilao=1570&pag')):
        paginas.append(pagina_base + pag['href'])

    #Remove o ultimo item da lista (Link 'Proxima')     
    del paginas[-1]

    #Itera sobre todas as paginas do leilao    
    for pagina in paginas:

        # query the website and return the html to the variable ‘page'
        page = urllib2.urlopen(pagina)

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')

        # Take out the <div> of name and get its value
        #table_box = soup.find_all('table', attrs={'width':'1000', 'border':'0'})
        table_box = soup.find_all('tr', attrs={'bgcolor':'#F3F4F5'})

        for tr in table_box:
            #Pega coluna da tabela onde possui as informações
            td = tr.find('td', attrs={'width':'100%', 'align': 'left'})

            #Pega observação do veiculo
            obs = td.find('font', attrs={'color':'#008080'}).find('b').text.encode('utf-8').strip()

            #Verifica se a observacao esta de acordo com o parametro passado
            if param_obs != None and param_obs not in obs:
                continue

            #Pega lance inicial do veiculo
            lance_inicial = int(td.find('font', attrs={'color':'#228B22'}).findNext().text.encode('utf-8').replace('R$ ', '').replace('.', '').replace(',', '').strip())

            #Pega maior lance
            maior_lance = int(tr.find('font', attrs={'color':'#FF0000'}).text.replace('R$ ', '').replace('.', '').replace(',', '').encode('utf-8').strip())

            #Verifica se o valor atual esta de acordo com o parametro passado
            if param_valor_max is not None and (lance_inicial > param_valor_max or maior_lance > param_valor_max):
                continue

            #Pega a descricao (modelo/marca) do veiculo
            marca_modelo = td.find('b').find('font').text.encode('utf-8').strip()

            # Pega o final da placa do carro
            placa = td.find(text=re.compile('Final')).encode('utf-8').strip()

            #Pega o ano do carro
            ano = td.find('font', attrs={'color':'#505050'})
            ano = str(td).split((ano).encode('utf-8'))[1].split((placa).encode('utf-8'))[0].split('|')[0].strip()
            
            lote = ''
            
            writer.writerow([marca_modelo, ano, placa, lance_inicial, maior_lance, obs, lote])
        
        #Espera cinco segundos para não sobrecarregar o site
        time.sleep(2)

    #Fecha arquivo csv deste leilao
    csv_leilao.close()
