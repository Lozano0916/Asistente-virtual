import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
from random import randint
import random

#opciones de voz
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

#escuchar microfono y devolver el audio como texto

def trasformar_audio_en_texto():
    
    #almacenar el reconocedor
    r= sr.Recognizer()

    #configurar microfono

    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold=0.8

        #informar que comenzo la grabacion
        print("Ya puede hablar")

        #guardar lo que se dice como audio
        audio=r.listen(origen)

        try:
            #buscar en google 
            pedido=r.recognize_google(audio,language="es")

            #prueba que pudo ingresar
            print("Dijiste: " + pedido)

            #devolver pedido
            return pedido
        
        #Si no se puede hacer
        except sr.UnknownValueError:
            #prueba de que no comprendio
            print("No se entendio")

            #devolver error
            return "Sigo esperando"
        except sr.RequestError:
            #prueba de que no comprendio
            print("No hay servicio")

            #devolver error
            return "Sigo esperando"
        
        #error inesperado
        except:
            print("Algo ha salido mal")

            return "Sigo esperando"
    
# funcion para que el asistente pueda ser escuchado

def hablar(mensaje):

    #encender el motor de pyttsx3
    engine = pyttsx3.init()

    engine.setProperty('voice', id1)

    #pronunciar mensaje
    engine.say(mensaje)

    engine.runAndWait()

#informar dia de la semana

def pedir_dia():

    #crear variable de datos de hoy
    dia=datetime.date.today()
    

    #crear variable el dia de la semana 
    dia_semana=dia.weekday()
    

    #diccionario con los dias
    calendario={0:'Lunes',
                1:'Martes',
                2:'Miércoles',
                3:'Jueves',
                4:'Viernes',
                5:'Sábado',
                6:'Domingo'}
    #decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

#informar que hora es

def pedir_hora():

    #crear variable con datos de la hora

    hora=datetime.datetime.now()
    hora=f'Son las {hora.hour} de las {hora.minute}'

    #decir la hora
    hablar(hora)

#funcion saludo inicial
def saludo_inicial():

    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 18:
        momento = 'Buenas noches'
    elif hora.hour >= 6 and  hora.hour <13:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    #decir saludo
    hablar(f"{momento}, soy Helena, tu asistente personal. Por favor dime en que puedo ayudarte")

#funcion numero al azar
def numero_al_azar():
    numero = randint(1,100)
    hablar(numero)

def letra_al_azar():
    letras=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    letra_al= random.choice(letras)
    hablar(letra_al)
#funcion central
def pedir_cosas():

    #activar el saludo
    saludo_inicial()

    #variable de corte
    comenzar=True
    while comenzar:

        #activar el microfono y guardar el pedido
        pedido=trasformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Abriendo navegador')
            webbrowser.open('https://www.google.com')
            continue
        elif 'abrir spotify' in pedido:
            hablar('Abriendo spotify')
            webbrowser.open('https://www.spotify.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia sobre' in pedido:
            hablar('Realizando la busqueda')
            pedido = pedido.replace('busca en wikipedia sobre', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Segun wikipedia:')
            hablar(resultado)
            continue
        elif 'busca en internet sobre' in pedido:
            hablar('Realizando la busqueda')
            pedido=pedido.replace('busca en internet sobre', '')
            pywhatkit.search(pedido)
            hablar('Estos fueron los resultados')
            continue
        elif 'reproducir' in pedido:
            hablar('Dame un momento para reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_accion=accion_buscada.info['regularMarketPrice']
                hablar(f'El precio de {accion} es {precio_accion}')
                continue
            except:
                hablar('Perdon no encontre esa acción')
        elif 'número al azar' in pedido:
            numero_al_azar()
            continue
        elif 'letra al azar' in pedido:
            hablar("La letra: ")
            letra_al_azar()
        elif 'adiós' in pedido:
            hablar('Si necesitas mas ayuda llamame')
            break



pedir_cosas()