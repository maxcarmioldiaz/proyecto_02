import os
def recorrer_directorio(ruta):
    """
    Funcion principal que valida la ruta y llama
    a la funcion auxiliar.
    Entradas: 
    - ruta: str, ruta del directorio a recorrer.
    Salidas:
    - dict: diccionario con la estructura de directorios y archivos encontrados.
    """
    if not os.path.exists(ruta):
        raise Exception("La ruta no existe")
    if not os.path.isdir(ruta):
        raise Exception("La ruta no es un directorio")
    return recorrer_directorio_aux(ruta, 0)


def recorrer_directorio_aux(ruta, profundidad):
    """
    Funcion que recorre recursivamente un directorio y sus subdirectiorios, y 
    devuelve un diccionario con la estructura de directiorios y archivos encontrados.
    Entradas:
    - ruta: str, ruta del directorio a recorrer.
    Salidas:
    - dict: diccionario con la estructura de directorios y archivos encontrados.
    """
    pesos = []
    nombres_archivos = []
    dic = {
        "nombre": os.path.basename(ruta),
        "ruta": ruta,
        "peso": 0,
        "hijos": [],
        "profundidad": profundidad,
        "archivos_cantidad": 0,
        "archivos_peso": {}
    } 
    entradas = os.listdir(ruta)
    for entrada in entradas:
        ruta_entrada = os.path.join(ruta, entrada)

        if os.path.isdir(ruta_entrada):
            hijo = recorrer_directorio_aux(ruta_entrada, profundidad + 1)
            dic["hijos"].append(hijo)
            dic["peso"] += hijo["peso"]

        elif os.path.isfile(ruta_entrada):
            dic["archivos_cantidad"] += 1
            dic["peso"] += os.path.getsize(ruta_entrada)
            nombres_archivos.append(ruta_entrada)
            pesos.append(os.path.getsize(ruta_entrada))

        else:
            pass

    return dic
        

