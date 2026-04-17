import random 
from collections import deque 
import copy
from dataclasses import dataclass

@dataclass
class Proceso:
    nombre: str
    tiempo_llegada: int
    tiempo_servicio: int 

    tiempo_restante: int = 0
    tiempo_retorno: int = 0
    tiempo_espera: int = 0

    def __post_init__(self):
        if self.tiempo_restante == 0:
            self.tiempo_restante = self.tiempo_servicio

def proceso_aleatorio(num_procesos):
    procesos = []
    for i in range(num_procesos):
        nombre = chr(65 + i)

        tiempo_llegada = random.randint(0,10)
        tiempo_servicio = random.randint(1,5)
        procesos.append(Proceso(nombre, tiempo_llegada, tiempo_servicio))
    procesos.sort(key=lambda p: p.tiempo_llegada)
    return procesos

def FCFS(procesos):
    ticks = 0
    secuencia = []

    procesos_por_llegar = deque(procesos)
    procesos_listos = deque()

    procesos_terminados = []

    while procesos_por_llegar or procesos_listos:
        
        while procesos_por_llegar and procesos_por_llegar[0].tiempo_llegada <= ticks:
            procesos_listos.append(procesos_por_llegar.popleft())
        
        if procesos_listos:
            proceso_actual = procesos_listos[0]

            secuencia.append(proceso_actual.nombre)

            proceso_actual.tiempo_restante -= 1

            if proceso_actual.tiempo_restante == 0:
                
                tiempo_finalizacion = ticks + 1

                proceso_actual.tiempo_retorno = tiempo_finalizacion - proceso_actual.tiempo_llegada
                proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.tiempo_servicio

                procesos_terminados.append(procesos_listos.popleft())
            
        else:
            secuencia.append('-')
            
        ticks += 1    

    prom_T, prom_E, prom_P = calculo_metricas(procesos_terminados)

    return {
        "algoritmo": "FCFS",
        "T":prom_T,
        "E":prom_E,
        "P":prom_P,
        "Secuencia": secuencia
    }

def RR(procesos, quantum):
    ticks = 0
    secuencia = []

    procesos_por_llegar = deque(procesos)
    procesos_listos = deque()

    procesos_terminados = []

    proceso_actual = None
    quantum_restante = 0

    while procesos_por_llegar or procesos_listos or proceso_actual:

        while procesos_por_llegar and procesos_por_llegar[0].tiempo_llegada <= ticks:
            procesos_listos.append(procesos_por_llegar.popleft())
    
        if not proceso_actual and procesos_listos:
            proceso_actual = procesos_listos.popleft()
            quantum_restante = quantum

        if proceso_actual:
            secuencia.append(proceso_actual.nombre)
            proceso_actual.tiempo_restante -= 1
            quantum_restante -= 1
        
            if proceso_actual.tiempo_restante == 0:
                tiempo_finalizacion = ticks + 1

                proceso_actual.tiempo_retorno = tiempo_finalizacion - proceso_actual.tiempo_llegada
                proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.tiempo_servicio

                procesos_terminados.append(proceso_actual)
                proceso_actual = None

                proceso_actual = None
            elif quantum_restante == 0:
                procesos_listos.append(proceso_actual)
                proceso_actual = None
        else:
            secuencia.append('-')
    
        ticks += 1
    
    prom_T, prom_E, prom_P = calculo_metricas(procesos_terminados)

    return {
        "algoritmo": "RR",
        "T":prom_T,
        "E":prom_E,
        "P":prom_P,
        "Secuencia": secuencia
    }
        
def SPN(procesos):
    ticks = 0
    secuencia = []

    procesos_por_llegar = deque(procesos)
    procesos_listos = deque()

    procesos_terminados = []
    proceso_actual = None

    while procesos_por_llegar or procesos_listos or proceso_actual:
        
        while procesos_por_llegar and procesos_por_llegar[0].tiempo_llegada <= ticks:
            procesos_listos.append(procesos_por_llegar.popleft())
        
        if not proceso_actual and procesos_listos:
            procesos_listos = deque(sorted(procesos_listos, key=lambda p: p.tiempo_servicio))
            proceso_actual = procesos_listos.popleft()
        
        if proceso_actual:
            secuencia.append(proceso_actual.nombre)
            proceso_actual.tiempo_restante -= 1

            if proceso_actual.tiempo_restante == 0:
                tiempo_finalizacion = ticks + 1
                
                proceso_actual.tiempo_retorno = tiempo_finalizacion - proceso_actual.tiempo_llegada
                proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.tiempo_servicio
                
                procesos_terminados.append(proceso_actual)
                proceso_actual = None
        else:
            secuencia.append('-')
            
        ticks += 1
        
    prom_T, prom_E, prom_P = calculo_metricas(procesos_terminados)

    return {
        "algoritmo": "SPN",
        "T": prom_T,
        "E": prom_E,
        "P": prom_P,
        "Secuencia": secuencia
    }


def calculo_metricas(procesos_terminados):
    total_procesos = len(procesos_terminados)

    prom_T = sum(p.tiempo_retorno for p in procesos_terminados) / total_procesos
    prom_E = sum(p.tiempo_espera for p in procesos_terminados) / total_procesos
    
    prom_P = sum(p.tiempo_retorno / p.tiempo_servicio for p in procesos_terminados) / total_procesos

    return (prom_T, prom_E, prom_P)

procesos_prueba = proceso_aleatorio(5)

print(FCFS(copy.deepcopy(procesos_prueba)))
print(RR(copy.deepcopy(procesos_prueba), 2))
print(SPN(copy.deepcopy(procesos_prueba)))