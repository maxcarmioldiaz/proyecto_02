import easygui as gui
import pygame
import colorsys
import os
import analisis_espacio_logic as log
from random import choice as rand

def dibujo_recursivo(directorio_carpetas, window, rect_x, rect_y, rect_ancho, rect_alto):
    """Funcion recursiva que dibuja los rectangulos del grafico de tipo \"Treemap\"
    Entradas:
        -superficie: Es la superficie donde se va a dibujar.
    Salidas:
        -Dibujo del treemap
    """
    peso_padre = directorio_carpetas["peso"]

    def dibujo_recursivo_aux(diccionario, window, rect_x, rect_y, rect_ancho, rect_alto, peso_padre, h_padre, v_padre, s_padre):

        profundidad = diccionario["profundidad"]

        if profundidad < 7:

            nombre = diccionario["nombre"]
            peso = diccionario["peso"]
            peso_reducido = peso
            peso_padre_reducido = peso_padre

            while peso_padre_reducido >= 1000:
                peso_padre_reducido /= 1024
            
            divisiones = 0
            
            while peso_reducido >= 1000:
                peso_reducido /= 1024
                divisiones += 1
            peso_reducido = round(peso_reducido, 2)
            peso_str = str(peso_reducido)

            match divisiones:
                case 0:
                    prefijo = "B"
                case 1:
                    prefijo = "KB"
                case 2:
                    prefijo = "MB"
                case 3:
                    prefijo = "GB"
                case 4:
                    prefijo = "TB"
                case 5:
                    prefijo = "PB"

            r, g, b = colorsys.hsv_to_rgb(h_padre, s_padre, v_padre)

            r, g, b = (
                int(r * 255),
                int(g * 255),
                int(b * 255) 
            )
            if peso_padre != 0:
                rect_ancho*=(peso/peso_padre)
            else:
                rect_ancho = 2

            if int(rect_ancho) == 0:
                rect_ancho = 2

            font = pygame.font.Font(None, 40)

            #REVISION EN EL PRINT
            print(f"""El nombre es: {nombre}, 
            rect_x es {rect_x}, 
            rect_y es {rect_y}, 
            rect_ancho es {int(rect_ancho)}, 
            peso es {peso}, 
            profundidad es {profundidad}""")

            pygame.draw.rect(window, (r, g, b), (rect_x, rect_y, int(rect_ancho), rect_alto), border_radius=5)
            if rect_ancho > 10:
                pygame.draw.rect(window, (0, 0, 0), (rect_x, rect_y, int(rect_ancho), rect_alto), 2, border_radius=5)
            texto = font.render(peso_str + " " + prefijo + " " + nombre, True, (0, 0, 0))

            ancho_texto= texto.get_width()
            alto_texto= texto.get_height()

            texto_rect = texto.get_rect(
                center =(
                    rect_x + rect_ancho/2,
                    rect_y + rect_alto/2
                    )
                )

            if ancho_texto <= rect_ancho and alto_texto <= rect_alto:
                window.blit(texto, texto_rect)

            for i in range(len(diccionario["hijos"])):

                if diccionario["hijos"][i] == []:

                    dibujo_recursivo_aux(diccionario["hijos"][i+1], window, rect_x + rect_ancho, rect_y, rect_ancho, rect_alto, peso_padre, h_padre, v_padre, (s_padre + rand([-0.2 -0.01, 0.01, 0.02]))%1)

                else:

                    dibujo_recursivo_aux(diccionario["hijos"][i], window, rect_x, rect_y + rect_alto, rect_ancho, rect_alto, peso, h_padre, (v_padre + rand([ -0.05, -0.03, 0.03, 0.05, 0.07, 0.14]))%1, (s_padre + rand([-0.3 -0.02, 0.01, 0.03, 0.06]))%1)
            
    return dibujo_recursivo_aux(directorio_carpetas, window, rect_x, rect_y, rect_ancho, rect_alto, peso_padre, 0.6, 0.3, 0.3)



def main():
    """
    Programa principal de analisis de espacio
    Desarrollado por:
        -Maximiliano Carmiol 2026006978
        -Santiago Arrieta 2026017372
    """
    pygame.init()

    while True:

        try:
            ruta = gui.diropenbox(
                msg= "Seleccione el directorio de carpetas a revisar.",
                title= "Directorio"
            )

            if not os.path.isdir(ruta):
                raise Exception("Debe seleccionar un directorio de carpetas.")
            
            if ruta == None:
                raise Exception("Seleccione un directorio")
            
            break

        except Exception:
            pass

    directorio_carpetas = log.recorrer_directorio(ruta)
    
    monitor = pygame.display.Info()

    ancho = monitor.current_w
    alto = monitor.current_h

    ancho = int(ancho * 0.875)
    alto = int(alto * 0.875)

    window = pygame.display.set_mode((ancho, alto))

    rect_ancho = int(ancho * 0.8)
    rect_alto = 50
    rect_x = int(ancho * 0.05)
    rect_y = int(alto * 0.05)

    window.fill((255, 255, 255))

    dibujo_recursivo(directorio_carpetas, window, rect_x, rect_y, rect_ancho - rect_x, rect_alto)

    rect_y = rect_alto * 9

    font = pygame.font.Font(None, 20)

    top_archivos = log.top10_archivos(directorio_carpetas)

    texto = font.render("Top 10 archivos más pesados de la estructura", True, (0, 0, 0))
    window.blit(texto, (rect_x, rect_y))

    rect_y += texto.get_height()*1.5

    for archivo in top_archivos:
        peso, ruta = archivo

        divisiones = 0

        while peso >= 1000:
            peso /= 1024
            divisiones += 1
        peso = round(peso, 2)
        peso_str = str(peso)

        match divisiones:
            case 0:
                prefijo = "B"
            case 1:
                prefijo = "KB"
            case 2:
                prefijo = "MB"
            case 3:
                prefijo = "GB"
            case 4:
                prefijo = "TB"
            case 5:
                prefijo = "PB"

        texto = font.render(ruta + "   " + "El peso es:" + " " + peso_str + " " + prefijo , True, (0, 0, 0))

        ancho_texto = texto.get_width()

        if ancho_texto <= ancho:
            window.blit(texto, (rect_x, rect_y))

        else:
            texto = font.render(ruta[:35] + "..." + "   " + "El peso es:" + " " + peso_str + " " + prefijo, True, (0, 0, 0))

        rect_y += texto.get_height()

    top_directorios = log.top10_directorios(directorio_carpetas)

    rect_y += texto.get_height()*3

    texto = font.render("Top 10 directorios más grandes de la estructura", True, (0, 0, 0))
    window.blit(texto, (rect_x, rect_y))

    rect_y += texto.get_height()*1.5

    for directorio in top_directorios:
        cantidad, ruta = directorio
        cantidad = str(cantidad)

        texto = font.render(ruta + "   " + "El directorio tiene " + cantidad + " archivos.", True, (0, 0, 0))
        
        ancho_texto = texto.get_width()

        if ancho_texto <= ancho:
            window.blit(texto, (rect_x, rect_y))

        else:
            texto = font.render(ruta[:35] + "..." + "   " + "El directorio tiene " + cantidad + " archivos.", True, (0, 0, 0))

        window.blit(texto, (rect_x, rect_y))
        
        rect_y += texto.get_height()
    
    pygame.display.flip()

    loop = True
    while loop:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                loop = False
    
    pygame.quit()
    
if __name__ == "__main__":
    main()
