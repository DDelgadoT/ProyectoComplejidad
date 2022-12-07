import tkinter as tk
import random

# ------------------------ FUNCIONES ------------------------
def getInfoOfCities():
    tamañoMatriz = int(textCiudades.get("1.0",'2.0-1c')) # Lee la primera linea
    cantidadCiudades = int(textCiudades.get("2.0",'3.0-1c')) # Lee la segunda linea
    textoCiudades = textCiudades.get("3.0",'end-1c').replace('\n',' ').split(" ") # Limpia las lineas de las ciudades
    textoCiudades = [x for x in textoCiudades if x != ''] # Limpieza de espacios vacios que queden si se escribe mal una ciudad
    ciudades = [textoCiudades[i:i + 3] for i in range(0, len(textoCiudades), 3)] # Separa en listas de 3 la lista donde esta toda la información de las ciudades
    return tamañoMatriz, cantidadCiudades, ciudades

def optimizar():
    tamañoMatriz, _, ciudades = getInfoOfCities()
    z, differentThan = "", ""
    try:
        for i in ciudades:
            z = z + f"abs(x - {i[1]}) + abs(y - {i[2]}) + " # Función a optimizar, que es abs(x1 - x) + abs(y1 - y) que es la distancia Manhattan
            differentThan += f"constraint (x != {i[1]} \/ y != {i[2]});\n" # Restricción para que ni la X ni la Y sean coordenadas de alguna ciudad
        z = z[:-3]
        differentThan = differentThan[:-1]
        textOptimizacion.insert(tk.END, "var int: x; \nvar int: y; \nvar float: z; \n\n")
        textOptimizacion.insert(tk.END, f"constraint x >= 0; \nconstraint y >= 0; \nconstraint x < {tamañoMatriz}; \nconstraint y < {tamañoMatriz}; \n\n") # Restricciones triviales
        textOptimizacion.insert(tk.END, differentThan + "\n\n") # Restricción para evitar que la solución esté en una ciudad
        textOptimizacion.insert(tk.END, f"z = {z}; \n\n") # Función a optimizar
        textOptimizacion.insert(tk.END, "solve minimize z; \n\n")
        textOptimizacion.insert(tk.END, "output[\"X: \", show(x), \" Y: \", show(y)];")
    except:
        labelErrores.config(text = "Error en la optimización")
"""
EJEMPLO
12
5
Palmira 2 3
Cali 10 2
Buga 11 0
Tulua 0 3
RioFrio 1 2
"""
def dibujarMatriz():
    canvas.delete("all")
    tamañoMatriz, cantidadCiudades, ciudades = getInfoOfCities()
    try:
        labelErrores.config(text = "")
        tamanoCuadrados = sizeRectangle/tamañoMatriz
        for i in range(tamañoMatriz):
            for j in range(tamañoMatriz):
                squarePosX = i * tamanoCuadrados
                squarePosY = j * tamanoCuadrados
                squareSizeX = squarePosX + tamanoCuadrados
                squareSizeY = squarePosY + tamanoCuadrados
                canvas.create_rectangle(squarePosX, squarePosY, squareSizeX, squareSizeY, width=1, fill="#FFFFFF")
        for i in ciudades:
            for j in range(3):
                # Generación de colores aleatorios
                r = "%02x"%random.randint(0,255)
                g = "%02x"%random.randint(0,255)
                b = "%02x"%random.randint(0,255)
                color="#"+r+g+b
            squarePosX = int(i[1]) * tamanoCuadrados
            squarePosY = int(i[2]) * tamanoCuadrados
            squareSizeX = squarePosX + tamanoCuadrados
            squareSizeY = squarePosY + tamanoCuadrados
            canvas.create_rectangle(squarePosX, squarePosY, squareSizeX, squareSizeY, width=1, fill=color)
    except:
        labelErrores.config(text = "Error en el dibujado")
# -------------------------------------------------------------

# ------------------------ CREACION INTERFAZ ------------------------
window = tk.Tk()
window.title("¿Dónde coloco mi arena de dragón?")
widthWindow = 1000
heightWindow = 700
window.geometry(f'{widthWindow}x{heightWindow}')

frameMaestro = tk.Frame(window)
frameMaestro.pack(side="top")

frameMatriz = tk.LabelFrame(frameMaestro, text="Matriz")
frameMatriz.pack(side="left", fill=tk.BOTH, expand=True)

frameCiudades = tk.LabelFrame(frameMaestro, text="Ingreso ciudades")
frameCiudades.pack(side="left")
# -------------------------------------------------------------


# ------------------------ COMPONENTES ------------------------

# ------------------------ MATRIZ ------------------------
sizeRectangle = 380
canvas = tk.Canvas(frameMatriz, bg='#FFFFFF')
canvas.pack(fill=tk.Y, expand=True)

labelErrores = tk.Label(frameMatriz, text=" ")
labelErrores.pack()
# -------------------------------------------------------------

# ------------------------ CIUDADES ------------------------
widthTexts = 50
heightTexts = 15
labelCiudades = tk.Label(frameCiudades, text="Ingrese aquí las ciudades (Si no sabe cómo debe ingresarse, consulte el documento)")
labelCiudades.pack()
textCiudades = tk.Text(frameCiudades, width=widthTexts, height=heightTexts, borderwidth=2)
textCiudades.pack()
frameBotonesCiudades = tk.Frame(frameCiudades)
frameBotonesCiudades.pack()
botonDibujarMatriz = tk.Button(frameBotonesCiudades, text="Dibujar ciudades", command=dibujarMatriz)
botonDibujarMatriz.pack(side="left")
botonGenerarCodigo = tk.Button(frameBotonesCiudades, text="Optimizar", command=optimizar)
botonGenerarCodigo.pack(side="left")
labelCiudades = tk.Label(frameCiudades, text="Aquí es el código para ser ingresado en MiniZinc")
labelCiudades.pack()
textOptimizacion = tk.Text(frameCiudades, width=widthTexts, height=heightTexts, borderwidth=2)
textOptimizacion.pack()
# -------------------------------------------------------------

# -------------------------------------------------------------

window.mainloop()