# -*- coding: utf-8 -*-

# import libraries
import urllib2
from bs4 import BeautifulSoup
import re
import csv
import time
import getopt
import sys

# read commandline arguments, first
full_cmd_arguments = sys.argv

# - further arguments
argument_list = full_cmd_arguments[1:]

unix_options = 'a:A:ho:O:s:t:v:V:'
gnu_options = ['ano-min=', 'ano-max=', 'help', 'marca-modelo=', 'obs=', 'opc=', 'sleep=', 'timeout=', 'valor-min=', 'valor-max=', 'version']

#Define parametros de busca
param_ano_min = None
param_ano_max = None
param_marca = None
param_obs = None
param_opc_acessorios = None
param_sleep = 5
param_timeout = 5
param_valor_min = None
param_valor_max = None

help_text = '''
usage: app.py [options]
  options:
    -a,     --ano-min       Define ano minimo da busca [1]
    -A,     --ano-max       Define ano maximo da busca [1]
    -h,     --help          Mostra esse texto
    -o,     --obs           Define conteudo do campo obs da busca [2]
    -O,     --opc           Define lista de acessorios buscando [5]
    -m,     --marca-modelo  Define marca/modelo da busca [2]
    -s,     --sleep         Define o tempo entre um request e outro [3]
    -t,     --timeout       Define o timeout do request [3]
    -v,     --valor-min     Define valor minimo da busca [4]
    -V,     --valor-max     Define valor minimo da busca [4]
    
    [1] O ano deve ser informado por completo. Exemplo: 2010 ou 1990
    [2] Todos os valores de texto devem ser informados entre aspas caso seja mais de uma palavra e devem ser evitados caracteres especiais, como acentos, cedilha e etc. Exemplo: para buscar \'Documento pronto em maos\', use o texto 'pronto em m' que tera o mesmo efeito.
    [3] Valor default: 5
    [4] Os valores devem ser inseridos com centavos e sem virgula ou ponto. Exemplo: para 10.500,00 use 1050000
    [5] Valores devem ser separados por virgula, dentro de aspas e em maiusculo. Valores possiveis: DH, AR, VE, TE, MANUAL, CHAVE RESERVA, 5 LUGARES, BASICO. FLEX, GASOLINA, DIESEL. Exemplo: \'DH, AR, VE\'
'''

__version__ = '1.1.1'

#Recebe parametros de busca do terminal
try:  
    arguments, values = getopt.getopt(argument_list, unix_options, gnu_options)
    
    for current_argument, current_value in arguments:  
        if current_argument in ('-a', '--ano-min'):
            if len(current_value) != 4:
                print('Informe o ano com 4 caracteres. Exemplo 2010 ou 1990')
                sys.exit(2)
            param_ano_min = int(current_value)
        elif current_argument in ('-A', '--ano-max'):
            if len(current_value) != 4:
                print('Informe o ano com 4 caracteres. Exemplo 2010 ou 1990')
                sys.exit(2)
            param_ano_max = int(current_value)
        elif current_argument in ('-h', '--help'):
            print (help_text)
            sys.exit()
        elif current_argument in ('-o', '--obs'):
            param_obs = current_value.lower()
        elif current_argument in ('-O', '--opc'):
            temp_opc_acessorios = current_value.split(',')
            param_opc_acessorios = []
            for param in temp_opc_acessorios:
                param_opc_acessorios.append(param.strip())
        elif current_argument in ('-m', '--marca-modelo'):
            param_marca = current_value
        elif current_argument in ('-s', '--sleep'):
            param_marca = current_value
        elif current_argument in ('-t', '--timeout'):
            param_marca = current_value
        elif current_argument in ('-v', '--valor-min'):
            param_valor_min = int(current_value.replace(',', '').replace('.', ''))
        elif current_argument in ('-V', '--valor-max'):
            param_valor_max = int(current_value.replace(',', '').replace('.', ''))
        elif current_argument == '--version':
            print('Guariglia Leiloes Scrapping App Version: ' + __version__)
            sys.exit()

        
except getopt.error as err:  
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)

#Inicia execucao do codigo da raspagem    
# specify the url
pagina_base = 'http://www.guariglia.com.br/'
pagina_leiloes = pagina_base + '?ir=filtraleiloes&tp=vei'

# query the website and return the html to the variable ‘page'
page = urllib2.urlopen(pagina_leiloes, timeout=param_timeout)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')
pag_leiloes = []

for pag in soup.find_all('td', onclick=re.compile('ir=lotes_veiculos_nsl&leilao=')):
    pag = pag['onclick'].encode('utf-8').replace('location.href=', '').replace('\'', '')
    pag_leiloes.append(pagina_base + pag)

for pag_leilao in pag_leiloes:
    # query the website and return the html to the variable ‘page'
    page = urllib2.urlopen(pag_leilao, timeout=param_timeout)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    
    #Pega o numero do leilao
    leilao = pag_leilao[pag_leilao.encode('utf-8').index('leilao='):].replace('leilao=', '')


    #Procura por parte do texto 'Lotes deste leilão ainda não foram lançados'
    if ('otes deste leil').encode('utf-8') in soup.text.encode('utf-8'):
        print('Lostes do leilao %s ainda nao foram lancados' %leilao)
        break
    #if soup.find('img', attrs={'src':'imagens/andamento.png'}) is not None:
        #print('Leilao %s ja em andamento' %leilao)
        #continue
        
    #Cria um arquivo csv para cada leilao
    csv_leilao = open('dados_leilao_' + leilao + '.csv', 'w')
    cont = 0

    writer = csv.writer(csv_leilao)

    writer.writerow(['marca_modelo', 'ano', 'placa', 'acessorios','lance_inicial', 'maior_lance', 'obs', 'lote'])

    paginas = []
    paginas.append(pag_leilao)

    div_paginas = soup.find('div', attrs={'align':'center'})

    for pag in div_paginas.find_all('a', href=re.compile('ir=lotes_veiculos_nsl&leilao=')):
        paginas.append(pagina_base + pag['href'])

    #Remove o ultimo item da lista (Link 'Proxima')     
    del paginas[-1]

    #Itera sobre todas as paginas do leilao    
    for pagina in paginas:

        # query the website and return the html to the variable ‘page'
        page = urllib2.urlopen(pagina, timeout=param_timeout)

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')
        
        #Pega todas as linhas da tabela contendo informacoes dos veiculos
        table_box = soup.find_all('tr', attrs={'bgcolor':'#F3F4F5'})

        for tr in table_box:
            #Pega coluna da tabela onde possui as informações
            td = tr.find('td', attrs={'width':'100%', 'align': 'left'})

            #Pega observação do veiculo
            obs = td.find('font', attrs={'color':'#008080'}).find('b').text.encode('utf-8').strip() #fixme

            #Verifica se a observacao esta de acordo com o parametro passado
            if param_obs is not None and param_obs not in obs.lower():
                continue

            #Pega lance inicial do veiculo
            lance_inicial = int(td.find('font', attrs={'color':'#228B22'}).findNext().text.encode('utf-8').replace('R$ ', '').replace('.', '').replace(',', '').strip())

            #Pega maior lance
            maior_lance = int(tr.find('font', attrs={'color':'#FF0000'}).text.replace('R$ ', '').replace('.', '').replace(',', '').encode('utf-8').strip())

            #Verifica se o valor atual esta de acordo com o parametro passado
            if param_valor_max is not None and (lance_inicial > param_valor_max or maior_lance > param_valor_max):
                continue
            if param_valor_min is not None and lance_inicial < param_valor_min:
                continue

            #Pega acessorios
            acessorios = td.find_all('font', attrs={'color':'#505050'})
            acessorios = str(acessorios[4])
            if 'Acess' in acessorios:
                acessorios = str(td).split(acessorios)[1].split('<br/>\n')[0]
            else:
                acessorios = None

            if acessorios is not None:
                temp_acessorios = acessorios.encode('utf-8').split('-')
                acessorios = []
                for ace in temp_acessorios:
                    acessorios.append(ace.strip())
            
            #Verifica se os acessorios do veiculo atendem os parametros da busca
            if param_opc_acessorios is not None:
                if acessorios is None or len(acessorios) == 0:
                    continue
                else:
                    brk = False
                    for param in param_opc_acessorios:
                        if param not in acessorios:
                            brk = True
                            break
                    if brk:
                        continue
            

            # Pega a descricao (modelo/marca) do veiculo
            marca_modelo = td.find_all('b')
            lote = ''
            if u'Lote' in marca_modelo[0].text:
                lote = marca_modelo[1].text.encode('utf-8').strip()
                marca_modelo = marca_modelo[2].find('font').text.encode('utf-8').strip()
            elif 'Lance Inicial' in marca_modelo[1].text:
                marca_modelo = marca_modelo[0].find('font').text.encode('utf-8').strip()
            else:
                marca_modelo = marca_modelo[1].find('font').text.encode('utf-8').strip()
            
            #Verifica se a marca/modelo do veiculo atende os parametros da busca
            if param_marca is not None and param_marca.lower() not in marca_modelo.lower():
                continue

            # Pega o final da placa do carro
            placa = td.find(text=re.compile('Final')).encode('utf-8').strip()

            #Pega o ano do carro
            ano = td.find('font', attrs={'color':'#505050'})
            ano = str(td).split((ano).encode('utf-8'))[1].split((placa).encode('utf-8'))[0].split('|')[0].strip()
            
            #Verifica se o ano atende os parametros de busca
            if param_ano_min is not None and int(ano.split('/')[0]) < param_ano_min or param_ano_max is not None and int(ano.split('/')[1]) > param_ano_max:
                continue            
            
            writer.writerow([marca_modelo, ano, placa, acessorios, lance_inicial, maior_lance, obs, lote])
            cont += 1
        
        #Espera cinco segundos para não sobrecarregar o site
        time.sleep(param_sleep)

    #Fecha arquivo csv deste leilao
    csv_leilao.close()
    print('Foram encontrados %i veiculos para o leilao %s' %(cont, leilao))
