#include <windows.h>
#include <iostream>
#include <tchar.h>

// Definir los punteros a las funciones de la DLL
typedef int (*FutronicInitializeFunc)();
typedef int (*FutronicEnrollFunc)();
typedef void (*FutronicTerminateFunc)();

// Punteros a las funciones
FutronicInitializeFunc FutronicInitialize = nullptr;
FutronicEnrollFunc FutronicEnroll = nullptr;
FutronicTerminateFunc FutronicTerminate = nullptr;

// Cargar la DLL y obtener las funciones
bool cargarFuncionesDLL(HINSTANCE &hInstLibrary) {
    hInstLibrary = LoadLibrary(_T("C:\\Users\\User\\Documents\\proyectogrado\\SDK_4.2_Java_dll_x86_x64\\SDK_4.2_Java_dll_x86_x64\\x64\\ftrJSDK.dll"));
    if (hInstLibrary) {
        FutronicInitialize=(FutronicInitializeFunc)GetProcAddress(hInstLibrary, "Java_com_futronic_SDKHelper_FutronicSdkBase_FutronicInitialize");
        FutronicEnroll=(FutronicEnrollFunc)GetProcAddress(hInstLibrary, "Java_com_futronic_SDKHelper_FutronicSdkBase_FutronicEnroll");
        FutronicTerminate = (FutronicTerminateFunc)GetProcAddress(hInstLibrary, "Java_com_futronic_SDKHelper_FutronicSdkBase_FutronicTerminate");

        return FutronicInitialize && FutronicEnroll && FutronicTerminate;
    } else {
        std::cerr << "Error al cargar la DLL." << std::endl;
        return false;
    }
}

void iniciarEscaneo() {
    if (FutronicInitialize) {
        int resultadoInicializacion = FutronicInitialize();

        if (resultadoInicializacion == 0) { // 0 indica éxito
            std::cout << "Escáner inicializado correctamente." << std::endl;

            if (FutronicEnroll) {
                int resultadoEnrolamiento = FutronicEnroll();
                if (resultadoEnrolamiento == 0) { // 0 indica éxito
                    std::cout << "Enrolamiento exitoso." << std::endl;
                } else {
                    std::cerr << "Error en el enrolamiento: Código " << resultadoEnrolamiento << std::endl;
                }
            }
        } else {
            std::cerr << "Error al inicializar el escáner: Código " << resultadoInicializacion << std::endl;
        }
    }
}

void finalizarEscaneo() {
    if (FutronicTerminate) {
        FutronicTerminate();
        std::cout << "Escáner finalizado." << std::endl;
    }
}

int main() {
    HINSTANCE hInstLibrary = nullptr;

    if (cargarFuncionesDLL(hInstLibrary)) {
        char opcion;
        do {
            std::cout << "Seleccione una opción: (i)niciar escaneo, (f)inalizar escaneo, (s)alir: ";
            std::cin >> opcion;

            if (opcion == 'i') {
                iniciarEscaneo();
            } else if (opcion == 'f') {
                finalizarEscaneo();
            }

        } while (opcion != 's');

        // Liberar la DLL
        FreeLibrary(hInstLibrary);
    }

    return 0;
}
