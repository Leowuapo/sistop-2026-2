# Santa Claus
# Gonzalez Falcon Luis & Lopez Morales Fernando

import threading
import time
import random

NUM_ELFOS = 5
NUM_RENOS = 9
NUM_BARRERA_ELFOS = 3 #Se ocupa para definir la barrera para los elfos



# tenemos que crear n elfos y 9 renos
#cada elfo tiene un hilo y cada reno tiene un hilo
#usamos una barrera para los elfos y una barrera para los renos

#Contadores para abrir cada barrera
cuentaBarreraElfos = 0
cuentaBarreraRenos = 0

#Mutex de cada barrera
mutexElfo = threading.Semaphore(1)
mutexReno = threading.Semaphore(1)
mutexSanta = threading.Semaphore(1)

#Barrera de elfos y renos
barreraElfos = threading.Semaphore(0)
barreraRenos = threading.Semaphore(0)  

santaSemaforo = threading.Semaphore(0)




def accionReno(num):
    while True:
        print(f"Soy el reno {num} y estoy vacacionando :D")
        numRandom = random.randint(1,1000)
        while(numRandom != 10):
            numRandom = random.randint(1,1000)
            time.sleep(0.0005)
        print(f"=======================RENO {num} esta de vuelta ==================")
        llamadaRenos(num)

def llamadaRenos(num):
    global cuentaBarreraRenos
    mutexReno.acquire()
    cuentaBarreraRenos = cuentaBarreraRenos+1
    if cuentaBarreraRenos == 9:
        print("YA LLEGAMOS LOS 9 RENOS ++++++++++++++++++++++++++")
        santaSemaforo.release()
    mutexReno.release()
    barreraRenos.acquire()






def trabajoElfo(num):
    while True:
        print(f"Soy el elfo {num} y estoy trabajando...")
        numRandom = random.randint(1,100)
        while(numRandom != 10):
            time.sleep(0.2)
            numRandom = random.randint(1,10)
        print(f"Elfo {num} encontre un problema")
        llamadaProblema(num)


#Funcion donde se gestiona la barrera de elfo
def llamadaProblema(num):
    global cuentaBarreraElfos
    mutexElfo.acquire()
    if cuentaBarreraElfos < NUM_BARRERA_ELFOS:
        cuentaBarreraElfos += 1
        print(f"[{num}] me formo para pedir ayuda a santa: {cuentaBarreraElfos} esperando")
        if cuentaBarreraElfos == NUM_BARRERA_ELFOS:
            print("Hablando a Santa porque somos 3")
            santaSemaforo.release()
        mutexElfo.release()
        barreraElfos.acquire()
        print("Los elfos se ponen a trabajar de nuevo")
    else: # Cuando hay 3 elfos, se ponen a trabajar de nuevo
        print("Ya hay 3 elfos actualmente, regresare a trabajar")
        mutexElfo.release()
        time.sleep(0.2)


def santaAyudando():
    global cuentaBarreraElfos, cuentaBarreraRenos
    while True:
        santaSemaforo.acquire() # Se duemre hasta que los renos o los elfos lo despierten
        #Revisando si son los renos o los elfos
        mutexReno.acquire()
        if cuentaBarreraRenos == 9:
            print("<<<<<<<<<<<< ES NAVIDAD A ENTREGAR LOS REGALOS!!! >>>>>>>>>>>>>>>")
            #liberando a los 9 renos (optimizar con for)
            barreraRenos.release()
            barreraRenos.release()
            barreraRenos.release()
            barreraRenos.release()
            barreraRenos.release()
            barreraRenos.release()
            barreraRenos.release()
            barreraRenos.release()
            barreraRenos.release()
            cuentaBarreraRenos = 0
            print("<<<<<<<<<<<< REGLAOS ENTREGADOS, VUELVO A DORMIR!!! >>>>>>>>>>>>>>>")
        mutexReno.release()


        mutexElfo.acquire()
        if cuentaBarreraElfos == NUM_BARRERA_ELFOS:
            print("---------------DESPERTE Y Y VOY A AYUDAR-------------")
            barreraElfos.release()
            barreraElfos.release()
            barreraElfos.release()
            time.sleep(0.1)

            #Se resetea
            cuentaBarreraElfos = 0
            print("---------------VOLVERE A DORMIR --------------------")
        mutexElfo.release()

#Creando hilo Santa Claus
threading.Thread(target=santaAyudando, args=()).start() 

#creando hilos ELFOS
for i in range(NUM_ELFOS):
    threading.Thread(target= trabajoElfo, args=[i]).start()

#Creando hilos renos
for i in range(NUM_RENOS):
    threading.Thread(target= accionReno, args=[i]).start()
    


#creando 
