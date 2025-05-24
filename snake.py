import turtle
import random
import time
from abc import ABC, abstractmethod
from enum import Enum

# Configuración del juego
ANCHO_PANTALLA = 600  # Ancho de la ventana del juego en píxeles
ALTO_PANTALLA = 600   # Alto de la ventana del juego en píxeles
TAMAÑO_CELDA = 20     # Tamaño de cada celda en la cuadrícula (píxeles)
VELOCIDAD_BASE = 150  # Velocidad inicial del juego (ms por movimiento)
PUNTOS_POR_NIVEL = 50 # Puntos necesarios para subir de nivel

# Definición de los tipos de comida usando Enum
class TipoComida(Enum):
    VENENOSA = "venenosa"      # Comida que reduce tamaño y puntaje
    FIT = "fit"                # Comida que da crecimiento normal
    ALTO_GRASAS = "alto_grasas" # Comida que da más puntos pero ralentiza
    REAL = "real"              # Comida que da muchos puntos y acelera

# ===== PATRÓN ABSTRACT FACTORY =====

class Comida(ABC):
    """Clase abstracta para todos los tipos de comida"""
    def __init__(self, x, y):
        # Inicializa la comida en las coordenadas (x, y)
        self.x = x
        self.y = y
        self.turtle = turtle.Turtle()  # Objeto Turtle para representar la comida
        self.turtle.speed(0)           # Sin animación para movimientos instantáneos
        self.turtle.penup()            # No dibujar líneas al moverse
        self.turtle.goto(x, y)         # Mover a la posición especificada
        self.turtle.shape("circle")    # Forma circular para la comida
        self.configurar_apariencia()   # Configurar color y apariencia
    
    @abstractmethod
    def configurar_apariencia(self):
        """Método abstracto para configurar el color de la comida"""
        pass
    
    @abstractmethod
    def aplicar_efecto(self, juego):
        """Método abstracto para aplicar el efecto específico al juego"""
        pass
    
    def ocultar(self):
        """Oculta la comida de la pantalla"""
        self.turtle.hideturtle()

class ComidaVenenosa(Comida):
    """🟣 Comida Venenosa: Reduce tamaño y puntaje"""
    def configurar_apariencia(self):
        # Establece el color morado para la comida venenosa
        self.turtle.color("purple")
    
    def aplicar_efecto(self, juego):
        # Si la serpiente tiene más de un segmento, elimina el último y resta 1 punto
        if len(juego.serpiente) > 1:
            ultimo_segmento = juego.serpiente.pop()  # Remueve el último segmento
            ultimo_segmento.hideturtle()             # Oculta el segmento
            juego.puntaje = max(0, juego.puntaje - 1)  # No permite puntaje negativo
            juego.mostrar_mensaje("¡Comida Venenosa! -1 punto", "purple")
        else:
            # Si solo queda la cabeza, no reduce tamaño
            juego.mostrar_mensaje("¡Comida Venenosa! Sin efecto", "purple")

class ComidaFit(Comida):
    """🟢 Comida Fit: Crecimiento normal (+1 punto)"""
    def configurar_apariencia(self):
        # Establece el color verde para la comida fit
        self.turtle.color("green")
    
    def aplicar_efecto(self, juego):
        # Hace crecer la serpiente y suma 1 punto
        juego.crecer_serpiente()
        juego.puntaje += 1
        juego.mostrar_mensaje("¡Comida Fit! +1 punto", "green")

class ComidaAltoGrasas(Comida):
    """🟡 Comida Alto en Grasas: +3 puntos pero ralentiza"""
    def configurar_apariencia(self):
        # Establece el color dorado para la comida alta en grasas
        self.turtle.color("gold")
    
    def aplicar_efecto(self, juego):
        # Hace crecer la serpiente, suma 3 puntos y reduce la velocidad
        juego.crecer_serpiente()
        juego.puntaje += 3
        juego.velocidad_actual = max(50, juego.velocidad_actual - 50)  # Ralentiza (mínimo 50)
        juego.efecto_temporal = {"tipo": "lento", "duracion": 5}  # Efecto temporal de 5 movimientos
        juego.mostrar_mensaje("¡Alto en Grasas! +3 puntos (Lento)", "gold")

class ComidaReal(Comida):
    """🟠 Comida para Reyes: +5 puntos y aumenta velocidad"""
    def configurar_apariencia(self):
        # Establece el color naranja para la comida real
        self.turtle.color("orange")
    
    def aplicar_efecto(self, juego):
        # Hace crecer la serpiente, suma 5 puntos y aumenta la velocidad
        juego.crecer_serpiente()
        juego.puntaje += 5
        juego.velocidad_actual = min(300, juego.velocidad_actual + 30)  # Acelera (máximo 300)
        juego.efecto_temporal = {"tipo": "rapido", "duracion": 5}  # Efecto temporal de 5 movimientos
        juego.mostrar_mensaje("¡Comida Real! +5 puntos (Rápido)", "orange")

# ===== FÁBRICAS CONCRETAS =====

class FabricaComida(ABC):
    """Interfaz Abstract Factory para crear comida"""
    @abstractmethod
    def crear_comida(self, x, y):
        """Método abstracto para crear una comida en las coordenadas (x, y)"""
        pass

class FabricaComidaVenenosa(FabricaComida):
    def crear_comida(self, x, y):
        # Crea una instancia de ComidaVenenosa
        return ComidaVenenosa(x, y)

class FabricaComidaFit(FabricaComida):
    def crear_comida(self, x, y):
        # Crea una instancia de ComidaFit
        return ComidaFit(x, y)

class FabricaComidaAltoGrasas(FabricaComida):
    def crear_comida(self, x, y):
        # Crea una instancia de ComidaAltoGrasas
        return ComidaAltoGrasas(x, y)

class FabricaComidaReal(FabricaComida):
    def crear_comida(self, x, y):
        # Crea una instancia de ComidaReal
        return ComidaReal(x, y)

# ===== GESTOR DE FÁBRICAS =====

class GestorFabricas:
    """Gestiona las diferentes fábricas de comida"""
    def __init__(self):
        # Inicializa un diccionario con las fábricas para cada tipo de comida
        self.fabricas = {
            TipoComida.VENENOSA: FabricaComidaVenenosa(),
            TipoComida.FIT: FabricaComidaFit(),
            TipoComida.ALTO_GRASAS: FabricaComidaAltoGrasas(),
            TipoComida.REAL: FabricaComidaReal()
        }
    
    def crear_comida_aleatoria(self):
        """Crea una comida aleatoria en posición aleatoria"""
        # Genera coordenadas aleatorias dentro de los límites de la pantalla
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        
        # Redondea las coordenadas a múltiplos de TAMAÑO_CELDA para alinear a la cuadrícula
        x = round(x / TAMAÑO_CELDA) * TAMAÑO_CELDA
        y = round(y / TAMAÑO_CELDA) * TAMAÑO_CELDA
        
        # Define probabilidades: 40% Fit, 30% Alto Grasas, 20% Real, 10% Venenosa
        tipos_comida = [TipoComida.FIT] * 4 + [TipoComida.ALTO_GRASAS] * 3 + \
                      [TipoComida.REAL] * 2 + [TipoComida.VENENOSA] * 1
        
        # Selecciona un tipo de comida aleatoriamente
        tipo_elegido = random.choice(tipos_comida)
        fabrica = self.fabricas[tipo_elegido]
        
        # Crea y retorna la comida usando la fábrica correspondiente
        return fabrica.crear_comida(x, y)

# ===== CLASE OBSTÁCULO =====

class Obstaculo:
    """Representa un obstáculo/pared en el juego"""
    def __init__(self, x, y):
        # Inicializa el obstáculo en las coordenadas (x, y)
        self.x = x
        self.y = y
        self.turtle = turtle.Turtle()  # Objeto Turtle para el obstáculo
        self.turtle.speed(0)           # Sin animación
        self.turtle.penup()            # No dibujar líneas
        self.turtle.goto(x, y)         # Mover a la posición
        self.turtle.shape("square")    # Forma de cuadrado
        self.turtle.color("red")       # Color rojo
    
    def ocultar(self):
        """Oculta el obstáculo"""
        self.turtle.hideturtle()

# ===== JUEGO PRINCIPAL =====

class JuegoSnake:
    def __init__(self):
        # Configura la ventana, inicializa el juego, crea el gestor de fábricas y configura controles
        self.configurar_pantalla()
        self.inicializar_juego()
        self.gestor_fabricas = GestorFabricas()
        self.generar_nueva_comida()
        self.configurar_controles()
        
    def configurar_pantalla(self):
        """Configura la ventana del juego"""
        self.pantalla = turtle.Screen()  # Crea la ventana del juego
        self.pantalla.title("Snake Game - Abstract Factory Pattern")  # Título
        self.pantalla.bgcolor("black")   # Fondo negro
        self.pantalla.setup(ANCHO_PANTALLA, ALTO_PANTALLA)  # Dimensiones
        self.pantalla.tracer(0)          # Desactiva animación automática para control manual
        
        # Configura el texto de puntaje
        self.texto_puntaje = turtle.Turtle()
        self.texto_puntaje.speed(0)
        self.texto_puntaje.color("white")
        self.texto_puntaje.penup()
        self.texto_puntaje.hideturtle()
        self.texto_puntaje.goto(0, 260)  # Posición en la parte superior
        
        # Configura el texto de mensajes temporales
        self.texto_mensaje = turtle.Turtle()
        self.texto_mensaje.speed(0)
        self.texto_mensaje.color("white")
        self.texto_mensaje.penup()
        self.texto_mensaje.hideturtle()
        self.texto_mensaje.goto(0, 230)  # Posición debajo del puntaje
        
    def inicializar_juego(self):
        """Inicializa las variables del juego"""
        # Limpia la serpiente anterior si existe
        if hasattr(self, 'serpiente'):
            for segmento in self.serpiente:
                segmento.hideturtle()
        
        # Limpia obstáculos anteriores si existen
        if hasattr(self, 'obstaculos'):
            for obstaculo in self.obstaculos:
                obstaculo.ocultar()
        
        # Limpia comida anterior si existe
        if hasattr(self, 'comida'):
            self.comida.ocultar()
            
        # Inicializa listas y variables
        self.serpiente = []              # Lista para los segmentos de la serpiente
        self.obstaculos = []             # Lista para los obstáculos
        self.direccion = "derecha"       # Dirección inicial de la serpiente
        
        # Inicializa puntaje, nivel y partidas solo la primera vez
        if not hasattr(self, 'puntaje'):
            self.puntaje = 0
            self.nivel = 1
            self.juegos_jugados = 0
            
        # Configura velocidad según el nivel
        self.velocidad_actual = VELOCIDAD_BASE + (self.nivel - 1) * 20
        self.efecto_temporal = None      # Efectos temporales (lento/rápido)
        self.mensaje_actual = ""         # Mensaje temporal actual
        self.tiempo_mensaje = 0          # Duración del mensaje
        
        # Crea la cabeza de la serpiente
        cabeza = turtle.Turtle()
        cabeza.speed(0)
        cabeza.shape("square")           # Forma cuadrada
        cabeza.color("white")            # Color blanco
        cabeza.penup()
        cabeza.goto(0, 0)                # Posición inicial en el centro
        self.serpiente.append(cabeza)
        
        # Genera obstáculos según el nivel
        self.generar_obstaculos()
        
    def configurar_controles(self):
        """Configura los controles del juego"""
        self.pantalla.listen()  # Escucha eventos del teclado
        # Asocia teclas de flecha con cambios de dirección
        self.pantalla.onkey(lambda: self.cambiar_direccion("arriba"), "Up")
        self.pantalla.onkey(lambda: self.cambiar_direccion("abajo"), "Down")
        self.pantalla.onkey(lambda: self.cambiar_direccion("izquierda"), "Left")
        self.pantalla.onkey(lambda: self.cambiar_direccion("derecha"), "Right")
        
    def cambiar_direccion(self, nueva_direccion):
        """Cambia la dirección de la serpiente"""
        # Define direcciones opuestas para evitar movimientos inválidos
        direcciones_opuestas = {
            "arriba": "abajo", "abajo": "arriba",
            "izquierda": "derecha", "derecha": "izquierda"
        }
        
        # Cambia la dirección solo si no es opuesta a la actual
        if nueva_direccion != direcciones_opuestas.get(self.direccion):
            self.direccion = nueva_direccion
            
    def mover_serpiente(self):
        """Mueve la serpiente en la dirección actual"""
        cabeza = self.serpiente[0]  # Obtiene la cabeza de la serpiente
        x, y = cabeza.xcor(), cabeza.ycor()  # Coordenadas actuales
        
        # Calcula la nueva posición según la dirección
        if self.direccion == "arriba":
            y += TAMAÑO_CELDA
        elif self.direccion == "abajo":
            y -= TAMAÑO_CELDA
        elif self.direccion == "izquierda":
            x -= TAMAÑO_CELDA
        elif self.direccion == "derecha":
            x += TAMAÑO_CELDA
            
        # Mueve los segmentos del cuerpo a la posición del segmento anterior
        for i in range(len(self.serpiente) - 1, 0, -1):
            x_anterior = self.serpiente[i-1].xcor()
            y_anterior = self.serpiente[i-1].ycor()
            self.serpiente[i].goto(x_anterior, y_anterior)
            
        # Mueve la cabeza a la nueva posición
        cabeza.goto(x, y)
        
    def crecer_serpiente(self):
        """Añade un nuevo segmento a la serpiente"""
        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")  # Forma cuadrada
        nuevo_segmento.color("gray")   # Color gris para el cuerpo
        nuevo_segmento.penup()
        self.serpiente.append(nuevo_segmento)  # Añade el segmento a la lista
        
    def verificar_colisiones(self):
        """Verifica colisiones con bordes y cuerpo"""
        cabeza = self.serpiente[0]
        x, y = cabeza.xcor(), cabeza.ycor()
        
        # Verifica colisión con los bordes de la pantalla (±290 píxeles)
        if (x > 290 or x < -290 or y > 290 or y < -290):
            return True
            
        # Verifica colisión con el cuerpo de la serpiente
        for segmento in self.serpiente[1:]:
            if cabeza.distance(segmento) < 10:
                return True
                
        return False
        
    def verificar_colision_obstaculos(self):
        """Verifica colisión con obstáculos"""
        cabeza = self.serpiente[0]
        for obstaculo in self.obstaculos:
            if cabeza.distance(obstaculo.turtle) < 15:  # Colisión si está a menos de 15 píxeles
                return True
        return False
        
    def generar_obstaculos(self):
        """Genera obstáculos según el nivel actual"""
        num_obstaculos = (self.nivel - 1) * 2  # 2 obstáculos por nivel después del 1
        
        for _ in range(num_obstaculos):
            while True:
                # Genera coordenadas aleatorias
                x = random.randint(-280, 280)
                y = random.randint(-280, 280)
                
                # Redondea a múltiplos de TAMAÑO_CELDA
                x = round(x / TAMAÑO_CELDA) * TAMAÑO_CELDA
                y = round(y / TAMAÑO_CELDA) * TAMAÑO_CELDA
                
                # Evita obstáculos cerca del centro (±40 píxeles)
                if abs(x) > 40 or abs(y) > 40:
                    # Verifica que no coincida con otros obstáculos
                    conflicto = False
                    for obstaculo_existente in self.obstaculos:
                        if abs(obstaculo_existente.x - x) < 40 and abs(obstaculo_existente.y - y) < 40:
                            conflicto = True
                            break
                    
                    if not conflicto:
                        self.obstaculos.append(Obstaculo(x, y))
                        break
        
    def verificar_comida(self):
        """Verifica si la serpiente ha comido"""
        cabeza = self.serpiente[0]
        # Si la cabeza está a menos de 15 píxeles de la comida
        if cabeza.distance(self.comida.turtle) < 15:
            self.comida.aplicar_efecto(self)  # Aplica el efecto de la comida
            self.comida.ocultar()             # Oculta la comida
            self.generar_nueva_comida()       # Genera una nueva comida
            self.verificar_subida_nivel()     # Verifica si sube de nivel
            
    def verificar_subida_nivel(self):
        """Verifica si el jugador debe subir de nivel"""
        nuevo_nivel = (self.puntaje // PUNTOS_POR_NIVEL) + 1
        if nuevo_nivel > self.nivel:
            self.nivel = nuevo_nivel
            self.velocidad_actual = VELOCIDAD_BASE + (self.nivel - 1) * 20  # Aumenta velocidad
            self.mostrar_mensaje(f"¡NIVEL {self.nivel}! Más velocidad y obstáculos", "cyan")
            self.generar_obstaculos()  # Genera nuevos obstáculos
            
    def generar_nueva_comida(self):
        """Genera una nueva comida usando el patrón Factory"""
        while True:
            comida = self.gestor_fabricas.crear_comida_aleatoria()
            
            # Verifica que la comida no aparezca sobre obstáculos o la serpiente
            conflicto = False
            for obstaculo in self.obstaculos:
                if abs(comida.x - obstaculo.x) < 20 and abs(comida.y - obstaculo.y) < 20:
                    conflicto = True
                    break
            
            if not conflicto:
                for segmento in self.serpiente:
                    if abs(comida.x - segmento.xcor()) < 20 and abs(comida.y - segmento.ycor()) < 20:
                        conflicto = True
                        break
            
            if not conflicto:
                self.comida = comida  # Asigna la comida válida
                break
            else:
                comida.ocultar()  # Oculta la comida inválida
        
    def actualizar_efectos_temporales(self):
        """Actualiza los efectos temporales"""
        if self.efecto_temporal:
            self.efecto_temporal["duracion"] -= 1
            # Si el efecto termina, restaura la velocidad base
            if self.efecto_temporal["duracion"] <= 0:
                self.velocidad_actual = VELOCIDAD_BASE
                self.efecto_temporal = None
                
    def mostrar_mensaje(self, mensaje, color="white"):
        """Muestra un mensaje temporal en pantalla"""
        self.mensaje_actual = mensaje
        self.tiempo_mensaje = 60  # Duración de 60 frames
        self.texto_mensaje.color(color)
        
    def actualizar_pantalla(self):
        """Actualiza todos los elementos en pantalla"""
        # Actualiza el texto de puntaje y nivel
        self.texto_puntaje.clear()
        efecto_texto = ""
        if self.efecto_temporal:
            if self.efecto_temporal["tipo"] == "lento":
                efecto_texto = " (LENTO)"
            elif self.efecto_temporal["tipo"] == "rapido":
                efecto_texto = " (RÁPIDO)"
                
        self.texto_puntaje.write(f"Puntaje: {self.puntaje} | Nivel: {self.nivel} | Partidas: {self.juegos_jugados}{efecto_texto}", 
                               align="center", font=("Arial", 14, "normal"))
        
        # Actualiza el mensaje temporal
        self.texto_mensaje.clear()
        if self.tiempo_mensaje > 0:
            self.texto_mensaje.write(self.mensaje_actual, align="center", 
                                   font=("Arial", 12, "normal"))
            self.tiempo_mensaje -= 1
            
    def game_over(self):
        """Muestra pantalla de Game Over y reinicia automáticamente"""
        game_over_turtle = turtle.Turtle()
        game_over_turtle.color("red")
        game_over_turtle.penup()
        game_over_turtle.hideturtle()
        game_over_turtle.goto(0, 0)
        game_over_turtle.write(f"GAME OVER\nPuntaje: {self.puntaje} | Nivel: {self.nivel}\nReiniciando en 3 segundos...", 
                             align="center", font=("Arial", 20, "normal"))
        
        # Actualiza la pantalla y espera 3 segundos
        self.pantalla.update()
        time.sleep(3)
        
        # Limpia el mensaje de Game Over
        game_over_turtle.clear()
        
        # Incrementa el contador de partidas
        self.juegos_jugados += 1
        
        # Reinicia el juego manteniendo el puntaje y nivel
        self.inicializar_juego()
        self.generar_nueva_comida()
        
        # Muestra mensaje de reinicio
        self.mostrar_mensaje(f"¡Juego Reiniciado! Partida #{self.juegos_jugados}", "yellow")
        
    def ejecutar(self):
        """Bucle principal del juego"""
        while True:
            self.pantalla.update()  # Actualiza la pantalla
            
            # Verifica colisiones con bordes o cuerpo
            if self.verificar_colisiones():
                self.game_over()
                continue
                
            # Verifica colisiones con obstáculos
            if self.verificar_colision_obstaculos():
                self.game_over()
                continue
                
            # Mueve la serpiente
            self.mover_serpiente()
            
            # Verifica si comió
            self.verificar_comida()
            
            # Actualiza efectos temporales
            self.actualizar_efectos_temporales()
            
            # Actualiza la interfaz gráfica
            self.actualizar_pantalla()
            
            # Controla la velocidad del juego
            time.sleep(1.0 / self.velocidad_actual * 100)

# ===== INSTRUCCIONES DE USO =====

def mostrar_instrucciones():
    """Muestra las instrucciones del juego"""
    print("=== SNAKE GAME - ABSTRACT FACTORY PATTERN ===")
    print("\nTipos de Comida:")
    print("🟣 VENENOSA (Morado): Reduce tamaño y puntaje (-1)")
    print("🟢 FIT (Verde): Crecimiento normal (+1)")
    print("🟡 ALTO EN GRASAS (Dorado): +3 puntos pero ralentiza")
    print("🟠 REAL (Naranja): +5 puntos y aumenta velocidad")
    print("\nSistema de Niveles:")
    print("🎯 Cada 50 puntos = Nuevo nivel")
    print("🚀 Cada nivel aumenta velocidad")
    print("🧱 Cada nivel añade 2 obstáculos rojos")
    print("🔄 El juego se reinicia automáticamente al morir")
    print("\nControles: Flechas del teclado")
    print("¡El juego continuará indefinidamente!")
    print("="*50)

# ===== EJECUCIÓN =====

if __name__ == "__main__":
    mostrar_instrucciones()  # Muestra las instrucciones en consola
    juego = JuegoSnake()     # Crea una instancia del juego
    juego.ejecutar()         # Inicia el bucle principal
