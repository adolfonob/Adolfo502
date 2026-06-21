#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import string
import threading
import time
from concurrent.futures import ThreadPoolExecutor

try:
    from colorama import init, Fore, Style
except ImportError:
    class MockColor:
        def __getattr__(self, name): return ""
    init = lambda autoreset=False: None
    Fore = MockColor()
    Style = MockColor()

init(autoreset=False)

# Colores definidos
VERDE   = Fore.GREEN + Style.BRIGHT if Fore.GREEN else ""
CELESTE = Fore.CYAN + Style.BRIGHT if Fore.CYAN else ""
DIM     = Style.DIM if Style.DIM else ""
RESET   = Style.RESET_ALL if Style.RESET_ALL else ""

# Candado para sincronización
print_lock = threading.Lock()

def banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(VERDE + " ╔═════════════════════════════════════════════════════════╗")
    print(CELESTE + " ║             ▄▀█ █▀▄ █▀█ █   █▀▀ █▀█                     ║")
    print(CELESTE + " ║             █▀█ █▄▀ █▄█ █▄▄ █▀  █▄█                     ║")
    print(VERDE + " ╚═════════════════════════════════════════════════════════╝")
    print(VERDE + " ═════════════════════ MENU PRINCIPAL ═════════════════════")
    print(CELESTE + "  [1] Crear Combo Masivo Multi-Hilos (Binary Rain)")
    print(CELESTE + "  [2] Eliminar Duplicados de un Archivo")
    print(CELESTE + "  [3] Configurar Longitud de Contraseña")
    print(CELESTE + "  [4] Cambiar Formato de Combinación")
    print(CELESTE + "  [0] Salir del Programa")
    print(VERDE + " ═════════════════════════════════════════════════════════")

def obtener_nombre_respaldo():
    nombres_base = ["Juan", "Maria", "Carlos", "Ana", "Jose", "Luis", "Pedro", "Sofia", "Miguel", "Laura"]
    return random.choice(nombres_base)

def cargar_nombres(ruta, cantidad_deseada):
    nombres = []
    if os.path.isfile(ruta):
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            nombres = [linea.strip() for linea in f if linea.strip()]
    while len(nombres) < cantidad_deseada:
        nombres.append(obtener_nombre_respaldo())
    return nombres[:cantidad_deseada]

def armar_linea_combo(nombre_base):
    numeros = "".join(random.choice(string.digits) for _ in range(5))
    return f"{nombre_base}{numeros}:{numeros}{nombre_base}\n"

def procesar_bloque_hilo(nombres_bloque, ruta_salida):
    lineas_combo = [armar_linea_combo(n) for n in nombres_bloque]
    
    with print_lock:
        with open(ruta_salida, "a", encoding="utf-8", errors="ignore") as f:
            f.writelines(lineas_combo)
        
        # EFECTO DE CAÍDA MATRIX: Genera varias columnas que parecen caer
        for _ in range(3): 
            columna = "".join(random.choice("01" if random.random() > 0.3 else " ") for _ in range(40))
            print(VERDE + f"  {columna}")
        time.sleep(0.05)

def opcion_crear_combo_multihilos():
    ruta = input(CELESTE + "  [*] Ruta archivo (.txt) ➜ " + RESET).strip()
    nombre_salida = input(CELESTE + "  [*] Nombre archivo salida ➜ " + RESET).strip() or "combo_masivo"
    try:
        cantidad = int(input(CELESTE + "  [*] Cantidad total ➜ " + RESET).strip())
    except: cantidad = 100

    nombres = cargar_nombres(ruta, cantidad)
    carpeta_salida = "/storage/emulated/0/Termux"
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta_final = os.path.join(carpeta_salida, f"{nombre_salida}.txt")
    if os.path.exists(ruta_final): os.remove(ruta_final)

    print(VERDE + "\n  [*] INICIANDO LLUVIA BINARIA (CAÍDA ACTIVADA)...\n")
    bloques = [nombres[i:i+5] for i in range(0, len(nombres), 5)]
    
    with ThreadPoolExecutor(max_workers=25) as executor:
        for b in bloques: executor.submit(procesar_bloque_hilo, b, ruta_final)
    
    print(VERDE + f"\n  [✓] Archivo guardado en: {ruta_final}")
    input(DIM + "  Presiona ENTER para volver..." + RESET)

def menu_principal():
    while True:
        banner()
        opcion = input(CELESTE + "  [+] Opción ➜ " + RESET).strip()
        if opcion == "1": opcion_crear_combo_multihilos()
        elif opcion == "0": break

if __name__ == "__main__":
    try: menu_principal()
    except KeyboardInterrupt: sys.exit(0)
