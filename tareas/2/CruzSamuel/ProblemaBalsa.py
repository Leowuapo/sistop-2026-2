import threading
import time
import random
from enum import Enum

class Bando(Enum):
    HACKER = "Hacker"
    SERF = "Serf"

class Balsa:
    def __init__(self):   
        self.mutex = threading.Lock()
        self.condicion = threading.Condition(self.mutex)  
        self.hackers_esperando = 0
        self.serfs_esperando = 0
        self.grupo_actual = []
        self.balsa_ocupada = False
        self.viajes_realizados = 0
        self.finalizado = False
        self.personas_restantes = 0  # contador de personas que faltan por cruzar, IMPORTANTE! sino se queda esperando indefinidamente

        self.allowed_hackers = 0  
        self.allowed_serfs = 0    
    def _puede_formar_grupo(self):
        #Se implementan las reglas para formar un grupo valido, 4 del mismo bando o 2 de cada uno
        return (self.hackers_esperando >= 4 or 
                self.serfs_esperando >= 4 or 
                (self.hackers_esperando >= 2 and self.serfs_esperando >= 2))
    def _formar_grupo(self):
        # 2 hackers y 2 serfs
        if self.hackers_esperando >= 2 and self.serfs_esperando >= 2:
            self.grupo_actual = [Bando.HACKER] * 2 + [Bando.SERF] * 2
            self.hackers_esperando -= 2
            self.serfs_esperando -= 2
        # 4 hacekrs
        elif self.hackers_esperando == 4:
            self.grupo_actual = [Bando.HACKER] * 4
            self.hackers_esperando -= 4
        # 4 serfs
        elif self.serfs_esperando >= 4:
            self.grupo_actual = [Bando.SERF] * 4
            self.serfs_esperando -= 4

        
        self.allowed_hackers = sum(1 for b in self.grupo_actual if b == Bando.HACKER)  
        self.allowed_serfs = sum(1 for b in self.grupo_actual if b == Bando.SERF)       
        
        print(f"Grupo formado: {[b.value for b in self.grupo_actual]}")
        
# definicion de la funcion persona con atributos balsa, bando e id_persona
def persona(balsa, bando, id_persona):
    time.sleep(random.uniform(0.1, 2.0))
    balsa.abordar(bando, id_persona)
def main():
    print("SIMULACIÓN CRUCE DEL RIO - PROBLEMA DE SINCRONIZACIÓN")
    print("=" * 50)
    
    balsa = Balsa()
    
    hilos = []
    id_counter = 1
    
    print("\n" + "=" * 50)
    print(f"Total de viajes: {balsa.viajes_realizados}")
    print("Simulacion completada...")

if __name__ == "__main__":
    main()