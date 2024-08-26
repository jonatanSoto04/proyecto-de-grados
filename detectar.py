import ctypes

# Cargar la DLL
ftr_sdk = ctypes.WinDLL('"C:\Users\User\Documents\proyectogrado\SDK_4.2_Java_dll_x86_x64\SDK_4.2_Java_dll_x86_x64\x64\ftrJSDK.dll"')

# Definir las funciones que vas a usar
FutronicInitialize = ftr_sdk.Java_com_futronic_SDKHelper_FutronicSdkBase_FutronicInitialize
FutronicInitialize.restype = ctypes.c_int

FutronicEnroll = ftr_sdk.Java_com_futronic_SDKHelper_FutronicSdkBase_FutronicEnroll
FutronicEnroll.restype = ctypes.c_int

FutronicTerminate = ftr_sdk.Java_com_futronic_SDKHelper_FutronicSdkBase_FutronicTerminate
FutronicTerminate.restype = None
def iniciar_escaneo():
    # Inicializar el escaner
    resultado_inicializacion = FutronicInitialize()

    if resultado_inicializacion == 0:  # 0 indica exito en muchos SDKs
        print("Escaner inicializado correctamente.")

        # Iniciar el proceso de enrolamiento
        resultado_enrolamiento = FutronicEnroll()
        if resultado_enrolamiento == 0:  # 0 indica exito
            print("Enrolamiento exitoso.")
        else:
            print(f"Error en el enrolamiento: Codigo {resultado_enrolamiento}")
    else:
        print(f"Error al inicializar el escaner: Codigo {resultado_inicializacion}")

def finalizar_escaneo():
    # Terminar el uso del escáner
    FutronicTerminate()
    print("Escáner finalizado.")
import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Escaneo de Huellas Dactilares")

# Botón para iniciar el escaneo
btn_iniciar = tk.Button(root, text="Iniciar Escaneo", command=iniciar_escaneo)
btn_iniciar.pack()

# Botón para finalizar el escaneo
btn_finalizar = tk.Button(root, text="Finalizar Escaneo", command=finalizar_escaneo)
btn_finalizar.pack()

root.mainloop()
