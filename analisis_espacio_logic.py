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

    dic = {
        "nombre": os.path.basename(ruta),
        "ruta": ruta,
        "peso": 0,
        "hijos": [],
        "profundidad": profundidad,
        "archivos_cantidad": 0,
        "archivos_peso": []
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
            dic["archivos_peso"].append((os.path.getsize(ruta_entrada), ruta_entrada))

    return dic

def top10_archivos(dic):
    """
    Funcion que devuelve una lista con los 10 archivos mas pesados
    encontrados en el directorio y sus subdirectorios.
    Entradas:
    - dic: dict, diccionario con la estructura de directorios y archivos encontrados.
    Salidas:
    - list: lista con los 10 archivos mas pesados encontrados en el directorio y sus subdirectorios.
    """ 
    lista_archivos = []
    for peso, ruta in dic["archivos_peso"]:
        lista_archivos.append((peso, ruta))
    for hijo in dic["hijos"]:
        lista_archivos += top10_archivos(hijo)
    lista_archivos.sort(reverse=True)
    return lista_archivos[:10]

def top10_directorios(dic):
    """
    Funcion que devuelve una lista con los 10 directorios con mas archivos encontrados.
    Entradas:
    - dic: dict, diccionario con la estructura de directorios y archivos encontrados.
    Salidas:
    - list : lista con los 10 directorios mas pesados encontrados.
    """
    lista_directorios = []
    lista_directorios.append((dic["archivos_cantidad"], dic["ruta"]))
    for hijo in dic["hijos"]:
        lista_directorios += top10_directorios(hijo)
    lista_directorios.sort(reverse=True)
    return lista_directorios[:10]