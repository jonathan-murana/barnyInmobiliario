try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import nltk
from bs4 import BeautifulSoup
import requests

import pandas as pd

import time



def punch(tipo):

    urlinmuebles= ''
    if 'inm' == tipo:
        urlinmuebles= 'https://inmuebles.mercadolibre.com.uy/'
    	
    if 'det' == tipo:
        urlinmuebles= 'https://listado.mercadolibre.com.uy/'	
    lista = ''
    if 'inm' == tipo:
        lista = [
	'apartamentos/alquiler/montevideo/centro/_PriceRange_15000UYU-20000UYU'
        #'casas/alquiler/montevideo/goes/dueno/alquileres-montevideo-casa_PriceRange_18000UYU-25000UYU'
        #'casas/alquiler/montevideo/brazo-oriental/dueno/alquileres-montevideo-casa_PriceRange_18000UYU-25000UYU',
        #'alquiler/montevideo/prado/dueno/alquileres-montevideo_PriceRange_18000UYU-25000UYU',
        #'casas/alquiler/montevideo/la-comercial/dueno/alquileres-montevideo-casa_PriceRange_18000UYU-25000UYU',
        #'casas/alquiler/montevideo/aguada/dueno/alquileres-montevideo_PriceRange_18000UYU-25000UYU',
        #'casas/alquiler/montevideo/jacinto-vera/alquileres-montevideo_PriceRange_18000UYU-25000UYU'
    ]

	
    if 'det' == tipo:
        lista = [
	'saxo','clarinete','saxofon alto', 'sasofon','saxofon soprano'        
	#'apartamentos/alquiler/montevideo/centro/_PriceRange_15000UYU-20000UYU'
        #'casas/alquiler/montevideo/goes/dueno/alquileres-montevideo-casa_PriceRange_18000UYU-25000UYU'
        #'casas/alquiler/montevideo/brazo-oriental/dueno/alquileres-montevideo-casa_PriceRange_18000UYU-25000UYU',
        #'alquiler/montevideo/prado/dueno/alquileres-montevideo_PriceRange_18000UYU-25000UYU',
        #'casas/alquiler/montevideo/la-comercial/dueno/alquileres-montevideo-casa_PriceRange_18000UYU-25000UYU',
        #'casas/alquiler/montevideo/aguada/dueno/alquileres-montevideo_PriceRange_18000UYU-25000UYU',
        #'casas/alquiler/montevideo/jacinto-vera/alquileres-montevideo_PriceRange_18000UYU-25000UYU'
    ]

    actualesCasas = []
    for item in lista:
        response = urllib2.urlopen(urlinmuebles+item)
        print(urlinmuebles+item)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        #print (html)

        links = soup.find_all(True, {'class':['rowItem']})
        #la lista alterna valores de nombre de producto y precio
        #   creamos una bandera para diferenciar si es valor o producto
        #print (links)
        for tag in links:
            if 'inm' == tipo:
                links2 = tag.find_all(True, {'class':['item-link']})
            if 'det' == tipo:
                links2 = tag.find_all(True, {'class':['item__info-title']})
            for tag1 in links2:
                actualesCasas.append(tag1["href"])
        paginas = soup.find_all(True, {'class':['pagination__page']})
        #print(paginas)
        for pagina in paginas[1:]:
            linkProxPagina = pagina.find_all('a')[0]["href"]
            #print (linkProxPagina)

#COPIADO TODO: hacer una funcion
            response = urllib2.urlopen(linkProxPagina)
            #print(urlinmuebles+item)
            html = response.read()
            soup = BeautifulSoup(html, "lxml")
            links = soup.find_all(True, {'class':['rowItem']})
            for tag in links:
                #links2 = tag.find_all(True, {'class':['item-link']})
                if 'inm' == tipo:
                    links2 = tag.find_all(True, {'class':['item-link']})
                if 'det' == tipo:
                    links2 = tag.find_all(True, {'class':['item__info-title']})
                for tag1 in links2:
                #print(tag1)
                    #print (tag1["href"])
                    actualesCasas.append(tag1["href"])
#COPIADO FIN

    pandaNuevo = pd.DataFrame(actualesCasas,columns=["url"])

    #print (pandaNuevo.head())

    pandaViejo=pd.read_csv("FILENAME.csv", sep=',', names = ["url"])

    #print (len(pandaNuevo.index))
    #print (len(pandaViejo.index))
    #print(pandaViejo["url"].head())
    dfNuevaCasas = []
    for url1 in pandaNuevo["url"]:
        existe = False
        for url2 in pandaViejo["url"]:
            #print("----")
            #print(url1)
            #print(url2)

            if url1==url2:
                #print("true")
                #print(url1)
                #print(url2)
                existe = True
            #print(existe)
        if existe==False:
            #print("si")
            dfNuevaCasas.append(url1)

    #print ("nuevo" + pandaNuevo[0])

    pandaNuevo.to_csv("FILENAME.csv", sep=',')


    #print (pandaNuevo[pandaViejo[0]!=pandaNuevo[0]])
    print (dfNuevaCasas)
    return dfNuevaCasas

def enviar(dfNuevaCasas,tipo):

    if 'inm' == tipo:
        token = '494292193:AAG4--mG6fXyXWCT2jZYViTkWJ5CldENUIE'
    if 'det' == tipo:
        token = '608953221:AAEerHvUjEAzNuN6EuXKDh0TR-4armGwaEE'
    method = 'getUpdates'

    response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
    data={}
    ).json()

    #print(response)	
    msg= "Hola amiguitos, esto parece sospechoso:"
    msg = msg + str(dfNuevaCasas)

    if 'det'==tipo:
        msg = msg + '\n'
        msg = msg + 'Y recuerden'
        msg = msg + '\n'
        msg = msg + 'Se buscan los siguientes instrumentos musicales:'
        msg = msg + '\n'
        msg = msg + '- saxo alto Yanagisawa 992 el metal tono dorado/rojizo'
        msg = msg + '\n'
        msg = msg + '- saxo soprano Yamaha 875 dorado'
        msg = msg + '\n'
        msg = msg + 'clarinete Buffet r13 de madera, negro,'
        msg = msg + '\n'
        msg = msg + '- los tres en valijas negras.'
        msg = msg + '\n'
        msg = msg + 'Se ofrece recompensa.'
   
    yaMande = []

    if len(dfNuevaCasas) > 0:
        for ident in response['result']:
            identificador = ident['message']['chat']['id']
            method = 'sendMessage'
            if identificador not in yaMande:
                print ("mandando a " + str(identificador))
                response = requests.post(
                url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                data={'chat_id': identificador , 'text': msg}
                ).json()
                yaMande.append(identificador)
                print (response)

import sys
tipo = 'inm' #inmoviliario
#a = 'det' #detective

if __name__ == "__main__":
    tipo = str(sys.argv[1])
    print (tipo)
FREQ_SECS=1800
if 'inm'==tipo:
    FREQ_SECS=1800
if 'det'==tipo:
    FREQ_SECS=3600*24

while True:
    print ("liberarndo a Barny " + tipo )
    nuevas = punch(tipo)
    #print(nuevas)
    enviar(nuevas,tipo)
    time.sleep(FREQ_SECS)
