# ============================================================================
#  MODULO: GESTOR DE PARTICULAS (NIEVE, LLUVIA Y EFECTOS PERSONALIZADOS)
#  Version: 1.0
#  Compatibilidad: Ren'Py 7.x / 8.x
#  Licencia: MIT. Copyright (c) 2026 davinzifc.
#            Puedes usar, copiar, modificar y redistribuir este archivo,
#            siempre que mantengas este aviso de copyright y la licencia
#            MIT (ver el archivo LICENSE del repositorio) en las copias.
#            Es decir: hay que dar credito al desarrollador.
#
#  Para instrucciones de instalacion, ejemplos de uso dentro del guion y
#  mas detalles, abri el archivo "README.md" que viene junto a este
#  script, en esta misma carpeta.
#
#  Resumen rapido de uso (ver el README para mas ejemplos):
#      $ id = gp_crear_particulas(color="#FFFFFF", tamano_min=3, tamano_max=8,
#                                  cantidad=70, angulo_base=90, angulo_variacion=20,
#                                  velocidad_min=30, velocidad_max=80)
#      $ gp_terminar_particulas(id)       # apaga ese efecto en particular
#      $ gp_terminar_todas()              # apaga todos los efectos activos
#
#      $ id_nieve = gp_nieve()            # atajo: nieve ya configurada
#      $ id_lluvia = gp_lluvia()          # atajo: lluvia ya configurada
#      $ id_luces = gp_luciernagas()      # atajo: luciernagas ya configuradas
# ============================================================================


# ============================================================================
#  EL "MOTOR" DEL MODULO
# ----------------------------------------------------------------------------
#  No necesitas editar nada de lo que sigue para usar el modulo.
#
#  Los efectos ya armados (GP_NIEVE, GP_LLUVIA y GP_LUCIERNAGAS, al final
#  de esta seccion) son ejemplos listos para usar. Si queres otro efecto,
#  o uno parecido con otros valores, no hace falta editar este archivo:
#  se arma desde tu propio script.rpy con gp_crear_particulas(...) o
#  GP_TipoParticula(...), como se explica en el README.md.
# ============================================================================
init python:

    import random as _gp_random
    import math as _gp_math
    import copy as _gp_copy

    class GP_TipoParticula(object):
        """
        Guarda TODA la configuracion de un efecto de particulas (nieve,
        lluvia, o cualquier efecto propio). No dibuja nada por si sola:
        es simplemente la "receta" que despues usa GestorParticulas para
        crear y animar las particulas.

        Parametros:

            imagenes (list o None):
                Lista de rutas de imagen (dentro de la carpeta "game/")
                o de displayables ya armados, para usar como particula.
                Si hay mas de una, cada particula elige una al azar. Si
                es None, la particula se dibuja como una figura de color
                plano (ver "color" y "forma") en vez de una imagen.
                Las imagenes con bordes suaves evitan el pixelado de las
                figuras planas. Para darle color a una imagen blanca, se
                puede pasar un displayable tenido, por ejemplo
                im.MatrixColor(ruta, im.matrix.colorize(c, c)).

            color (str o list):
                Color plano de la particula, en formato "#RRGGBB". Se
                puede pasar una lista de colores (por ejemplo
                ["#FFFFFF", "#DDEEFF"]) para que cada particula elija uno
                al azar. Solo se usa si "imagenes" es None.

            forma ("circulo" o "rectangulo"):
                Forma de la particula de color plano. "circulo" sirve
                para nieve, polvo, chispas, etc. "rectangulo" sirve para
                lluvia o rayas de luz. Solo se usa si "imagenes" es None.

            tamano_min, tamano_max (numeros):
                Rango de tamanio de la particula, en pixeles (para
                imagenes, es el lado mas largo de la imagen ya
                escalada; para rectangulos, es el largo). Cada particula
                elige un tamanio al azar dentro del rango. Usa el mismo
                valor en los dos para que no varie.

            ancho_min, ancho_max (numeros o None):
                Solo para forma "rectangulo": rango de GROSOR del
                rectangulo (distinto del largo, que es "tamano"). Si se
                dejan en None, se usa el mismo valor que tamano_min /
                tamano_max (o sea, la particula queda cuadrada).

            cantidad (int):
                Cuantas particulas hay en pantalla al mismo tiempo.

            angulo_base (grados), angulo_variacion (grados):
                Direccion en la que "salen" las particulas. 0 = derecha,
                90 = abajo, 180 = izquierda, 270 = arriba. Cada
                particula recibe un angulo al azar entre
                (angulo_base - angulo_variacion) y
                (angulo_base + angulo_variacion). Con variacion 0, todas
                las particulas van exactamente en angulo_base.

            velocidad_min, velocidad_max (pixeles por segundo):
                Rango de velocidad de cada particula. Con los dos
                valores iguales, todas las particulas van a la misma
                velocidad (sin aleatoriedad).

            ondulado (bool), amplitud_ondulado (pixeles),
            frecuencia_ondulado (ondas por segundo):
                Si "ondulado" es True, el movimiento deja de ser una
                linea recta y se le suma un vaiven lateral tipo
                "viento" (util para nieve, hojas, polvo). Si es False,
                el movimiento es perfectamente lineal (util para
                lluvia).

            rotar (bool), rotacion_velocidad_min,
            rotacion_velocidad_max (grados por segundo):
                Si "rotar" es True, cada particula gira sobre si misma
                mientras se mueve, a una velocidad de rotacion al azar
                dentro del rango indicado (puede ser negativa, para que
                gire al reves). Solo tiene efecto visible con imagenes:
                las figuras de color plano (circulo y rectangulo) se
                dibujan siempre sin rotar.

            opacidad_min, opacidad_max (de 0.0 a 1.0):
                Rango de transparencia de cada particula. Variarla da
                sensacion de profundidad.

            origen ("auto", "arriba", "abajo", "izquierda", "derecha" o
            "toda_pantalla"):
                De que borde de la pantalla "nacen" las particulas
                cuando se reciclan. Con "auto" (recomendado) se calcula
                solo a partir del angulo: si van para abajo nacen
                arriba, si van para arriba nacen abajo, si van para la
                derecha nacen a la izquierda, etc. "toda_pantalla" hace
                que puedan aparecer en cualquier parte (util para
                efectos ambiente como luciernagas o polvo en el aire,
                sobre todo combinado con tiempo_vida_min/max).

            origen_min, origen_max (de 0.0 a 1.0):
                Limita la zona del borde de nacimiento (por ejemplo,
                para que la nieve solo nazca en la mitad izquierda de la
                pantalla). Por defecto es 0.0 a 1.0, o sea, todo el
                borde.

            tiempo_vida_min, tiempo_vida_max (segundos, o None):
                Si se dejan en None (por defecto), cada particula vive
                hasta que sale de la pantalla, momento en el que
                reaparece del otro lado (reciclado infinito: es lo que
                se usa para nieve y lluvia). Si se les pone un numero,
                ademas la particula desaparece y se reinicia despues de
                ese tiempo, haya salido de pantalla o no (util para
                efectos que no dependen de "caer", como chispas que se
                apagan solas).

            tiempo_vida (segundos o None):
                Atajo: fija la vida exacta de cada particula (equivale a
                poner el mismo numero en tiempo_vida_min y
                tiempo_vida_max).

            fade_in, fade_out (segundos):
                Aparicion y desaparicion suaves: durante "fade_in"
                segundos la opacidad sube de 0 hasta su valor, y durante
                los ultimos "fade_out" segundos baja hasta 0. Asi la
                particula nunca "salta" de la nada, como una luciernaga
                que se prende y se apaga. La particula queda prendida
                (opacidad completa) el resto de su vida. "fade_out"
                necesita que haya tiempo de vida; si fade_in + fade_out
                es mas largo que la vida, se achican proporcionalmente.
                Por defecto es 0 (sin fade).

            movimiento ("lineal" o "aleatorio"):
                "lineal" (por defecto): la particula viaja en linea
                recta segun angulo y velocidad (nieve, lluvia).
                "aleatorio": la particula vaga por toda la pantalla,
                cambiando de rumbo suavemente al azar, y rebota en los
                bordes en vez de salir (luciernagas, polvo, burbujas).
                En este modo las particulas nacen en cualquier parte de
                la pantalla; "angulo_base" solo define el rumbo inicial
                (con angulo_variacion=180 sale en cualquier direccion).

            vagar_giro (grados por segundo):
                Solo con movimiento="aleatorio": que tan brusco cambia
                de rumbo. Numeros chicos (20-40) = curvas suaves y
                lentas; grandes (120+) = movimiento nervioso.

            zorder (int):
                Orden de dibujado del efecto dentro de su capa. Ver
                gp_crear_particulas() para mas detalle.
        """

        def __init__(
            self,
            imagenes=None,
            color="#FFFFFF",
            forma="circulo",
            tamano_min=6,
            tamano_max=6,
            ancho_min=None,
            ancho_max=None,
            cantidad=60,
            angulo_base=90,
            angulo_variacion=0,
            velocidad_min=60,
            velocidad_max=60,
            ondulado=False,
            amplitud_ondulado=15,
            frecuencia_ondulado=1.0,
            rotar=False,
            rotacion_velocidad_min=-60,
            rotacion_velocidad_max=60,
            opacidad_min=1.0,
            opacidad_max=1.0,
            origen="auto",
            origen_min=0.0,
            origen_max=1.0,
            tiempo_vida_min=None,
            tiempo_vida_max=None,
            tiempo_vida=None,
            fade_in=0.0,
            fade_out=0.0,
            movimiento="lineal",
            vagar_giro=60,
            zorder=-10,
        ):

            if forma not in ("circulo", "rectangulo"):
                raise Exception("GP_TipoParticula: 'forma' tiene que ser 'circulo' o 'rectangulo' (recibido: %r)" % (forma,))

            if origen not in ("auto", "arriba", "abajo", "izquierda", "derecha", "toda_pantalla"):
                raise Exception("GP_TipoParticula: 'origen' invalido: %r" % (origen,))

            if movimiento not in ("lineal", "aleatorio"):
                raise Exception("GP_TipoParticula: 'movimiento' tiene que ser 'lineal' o 'aleatorio' (recibido: %r)" % (movimiento,))

            if tiempo_vida is not None:
                tiempo_vida_min = tiempo_vida
                tiempo_vida_max = tiempo_vida
            # Si se da solo uno de los dos extremos, el otro lo iguala.
            if tiempo_vida_min is None and tiempo_vida_max is not None:
                tiempo_vida_min = tiempo_vida_max
            elif tiempo_vida_max is None and tiempo_vida_min is not None:
                tiempo_vida_max = tiempo_vida_min

            if fade_out > 0 and tiempo_vida_max is None:
                raise Exception("GP_TipoParticula: 'fade_out' necesita que definas tiempo_vida (o tiempo_vida_min/max)")
            if fade_in < 0 or fade_out < 0:
                raise Exception("GP_TipoParticula: 'fade_in' y 'fade_out' no pueden ser negativos")

            self.imagenes = imagenes
            self.color = color
            self.forma = forma
            self.tamano_min = tamano_min
            self.tamano_max = tamano_max
            self.ancho_min = ancho_min
            self.ancho_max = ancho_max
            self.cantidad = cantidad
            self.angulo_base = angulo_base
            self.angulo_variacion = angulo_variacion
            self.velocidad_min = velocidad_min
            self.velocidad_max = velocidad_max
            self.ondulado = ondulado
            self.amplitud_ondulado = amplitud_ondulado
            self.frecuencia_ondulado = frecuencia_ondulado
            self.rotar = rotar
            self.rotacion_velocidad_min = rotacion_velocidad_min
            self.rotacion_velocidad_max = rotacion_velocidad_max
            self.opacidad_min = opacidad_min
            self.opacidad_max = opacidad_max
            self.origen = origen
            self.origen_min = origen_min
            self.origen_max = origen_max
            self.tiempo_vida_min = tiempo_vida_min
            self.tiempo_vida_max = tiempo_vida_max
            self.fade_in = fade_in
            self.fade_out = fade_out
            self.movimiento = movimiento
            self.vagar_giro = vagar_giro
            self.zorder = zorder

    def _gp_color_a_rgba(color_hex, opacidad):
        """
        Convierte un color en formato "#RRGGBB" o "#RRGGBBAA" y una
        opacidad (0.0 a 1.0) en una tupla (r, g, b, a) de 0 a 255, lista
        para usar con las funciones de dibujo de Ren'Py.
        """
        color_hex = color_hex.lstrip("#")
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        a = int(color_hex[6:8], 16) if len(color_hex) >= 8 else 255
        a = int(a * max(0.0, min(1.0, opacidad)))
        return (r, g, b, a)

    class GestorParticulas(renpy.Displayable):
        """
        Displayable interno que crea, mueve y dibuja las particulas de
        un GP_TipoParticula. No se usa directamente desde el guion: se
        activa y se apaga con gp_crear_particulas() / gp_terminar_particulas(),
        mas abajo.
        """

        def __init__(self, tipo, **kwargs):
            super(GestorParticulas, self).__init__(**kwargs)
            self.tipo = tipo
            self.particulas = None
            self.st_anterior = None
            self.imagenes_resueltas = [renpy.displayable(ruta) for ruta in tipo.imagenes] if tipo.imagenes else []
            # Se completa la primera vez que se renderiza (necesita "st"
            # y "at", que recien estan disponibles en render()).
            self.imagenes_info = None

        def visit(self):
            # Le avisa a Ren'Py que precargue estas imagenes, para que
            # no se note una pausa la primera vez que aparece cada una.
            return list(self.imagenes_resueltas)

        def _elegir_origen(self, vx, vy):
            tipo = self.tipo
            origen = tipo.origen
            if origen == "auto":
                if abs(vy) >= abs(vx):
                    origen = "arriba" if vy >= 0 else "abajo"
                else:
                    origen = "izquierda" if vx >= 0 else "derecha"
            return origen

        def _generar_particula(self, ancho, alto, st, dispersar):
            tipo = self.tipo

            tamano = _gp_random.uniform(tipo.tamano_min, tipo.tamano_max)
            if tipo.ancho_min is not None:
                ancho_particula = _gp_random.uniform(tipo.ancho_min, tipo.ancho_max)
            else:
                ancho_particula = tamano

            angulo = _gp_math.radians(
                tipo.angulo_base + _gp_random.uniform(-tipo.angulo_variacion, tipo.angulo_variacion)
            )
            velocidad = _gp_random.uniform(tipo.velocidad_min, tipo.velocidad_max)
            vx = _gp_math.cos(angulo) * velocidad
            vy = _gp_math.sin(angulo) * velocidad

            vagando = tipo.movimiento == "aleatorio"
            origen = "toda_pantalla" if vagando else self._elegir_origen(vx, vy)
            margen = tamano + ancho_particula

            if dispersar and origen != "toda_pantalla":
                # Al activar el efecto por primera vez, se reparten las
                # particulas por toda la pantalla (no solo en el borde
                # de origen) para que el efecto se vea "en marcha" desde
                # el primer instante, en vez de aparecer todas juntas en
                # una linea.
                x = _gp_random.uniform(0, ancho)
                y = _gp_random.uniform(0, alto)
            elif origen == "toda_pantalla":
                x = _gp_random.uniform(0, ancho)
                y = _gp_random.uniform(0, alto)
            elif origen == "arriba":
                x = _gp_random.uniform(tipo.origen_min * ancho, tipo.origen_max * ancho)
                y = -margen
            elif origen == "abajo":
                x = _gp_random.uniform(tipo.origen_min * ancho, tipo.origen_max * ancho)
                y = alto + margen
            elif origen == "izquierda":
                x = -margen
                y = _gp_random.uniform(tipo.origen_min * alto, tipo.origen_max * alto)
            else:  # "derecha"
                x = ancho + margen
                y = _gp_random.uniform(tipo.origen_min * alto, tipo.origen_max * alto)

            color = tipo.color
            if isinstance(color, list):
                color = _gp_random.choice(color)

            imagen_indice = None
            escala = 1.0
            if self.imagenes_info:
                imagen_indice = _gp_random.randrange(len(self.imagenes_info))
                _disp, ancho_natural, alto_natural = self.imagenes_info[imagen_indice]
                referencia = max(1.0, float(max(ancho_natural, alto_natural)))
                escala = tamano / referencia

            vida = None
            if tipo.tiempo_vida_max is not None:
                vida = _gp_random.uniform(tipo.tiempo_vida_min, tipo.tiempo_vida_max)

            opacidad = _gp_random.uniform(tipo.opacidad_min, tipo.opacidad_max)

            nacimiento = st
            if vida is not None and dispersar:
                # Al arrancar el efecto, cada particula empieza en un
                # punto distinto de su ciclo de vida, para que no se
                # prendan y apaguen todas sincronizadas.
                nacimiento = st - _gp_random.uniform(0, vida)

            # El color final (en RGBA) y las medidas en pixeles enteros
            # se calculan aca, UNA sola vez por particula, en vez de
            # recalcularlos en cada cuadro dentro de render(): con
            # muchas particulas en pantalla, evitar ese trabajo repetido
            # todo el tiempo es lo que mas ayuda a poder tener mas
            # cantidad sin que se note en el rendimiento.
            color_rgba = None
            radio_px = 0
            ancho_px = 0
            tamano_px = 0
            if imagen_indice is None:
                color_rgba = _gp_color_a_rgba(color, opacidad)
                if tipo.forma == "rectangulo":
                    ancho_px = max(1, int(ancho_particula))
                    tamano_px = max(1, int(tamano))
                else:
                    radio_px = max(1, int(tamano / 2.0))

            return {
                "x": x,
                "y": y,
                "vx": vx,
                "vy": vy,
                "tamano": tamano,
                "ancho": ancho_particula,
                "imagen_indice": imagen_indice,
                "escala": escala,
                "color_rgba": color_rgba,
                "radio_px": radio_px,
                "ancho_px": ancho_px,
                "tamano_px": tamano_px,
                "opacidad": opacidad,
                "rotacion": _gp_random.uniform(0, 360) if tipo.rotar else 0.0,
                "velocidad_rotacion": (
                    _gp_random.uniform(tipo.rotacion_velocidad_min, tipo.rotacion_velocidad_max)
                    if tipo.rotar else 0.0
                ),
                "fase_ondulado": _gp_random.uniform(0, 2 * _gp_math.pi),
                "nacimiento": nacimiento,
                "vida": vida,
                "angulo": angulo,
                "velocidad": velocidad,
            }

        def render(self, width, height, st, at):
            tipo = self.tipo

            # La primera vez que se dibuja, se mide el tamanio natural
            # de cada imagen (para poder escalarla despues a "tamano").
            if tipo.imagenes and self.imagenes_info is None:
                self.imagenes_info = []
                for disp in self.imagenes_resueltas:
                    render_natural = renpy.render(disp, width, height, st, at)
                    self.imagenes_info.append((disp, render_natural.width, render_natural.height))

            # La primera vez que se dibuja, se crean todas las
            # particulas de una.
            if self.particulas is None:
                self.particulas = [
                    self._generar_particula(width, height, st, True)
                    for _ in range(tipo.cantidad)
                ]
                self.st_anterior = st

            dt = st - self.st_anterior
            self.st_anterior = st
            # Si el tiempo retrocedio (rollback) o hubo un salto muy
            # grande (por ejemplo, el juego estuvo pausado), se ignora
            # ese instante en vez de mover las particulas de un salto.
            if dt < 0 or dt > 0.25:
                dt = 0.0

            r = renpy.Render(width, height)
            lienzo = r.canvas()
            margen = tipo.tamano_max * 2 + tipo.amplitud_ondulado + 20

            # Se sacan del bucle los valores que no cambian particula a
            # particula (no cambian en todo este render()), para no
            # tener que consultarlos de nuevo en cada vuelta: con
            # cientos de particulas, esa consulta repetida se nota.
            particulas = self.particulas
            rotar = tipo.rotar
            ondulado = tipo.ondulado
            frecuencia_ondulado = tipo.frecuencia_ondulado
            amplitud_ondulado = tipo.amplitud_ondulado
            forma_rectangulo = tipo.forma == "rectangulo"
            imagenes_info = self.imagenes_info
            vagando = tipo.movimiento == "aleatorio"
            giro_rad = _gp_math.radians(tipo.vagar_giro) * _gp_math.sqrt(dt) if dt > 0 else 0.0
            fade_in = tipo.fade_in
            fade_out = tipo.fade_out
            hay_fade = fade_in > 0 or fade_out > 0

            for indice in range(len(particulas)):
                p = particulas[indice]

                if vagando:
                    # Caminata aleatoria suave: el rumbo se desvia un poco
                    # al azar en cada cuadro, sin saltos bruscos.
                    p["angulo"] += _gp_random.gauss(0.0, giro_rad)
                    p["vx"] = _gp_math.cos(p["angulo"]) * p["velocidad"]
                    p["vy"] = _gp_math.sin(p["angulo"]) * p["velocidad"]

                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt

                if vagando:
                    # Rebota en los bordes: la particula nunca sale.
                    if p["x"] < 0:
                        p["x"] = 0.0
                        p["angulo"] = _gp_math.pi - p["angulo"]
                    elif p["x"] > width:
                        p["x"] = float(width)
                        p["angulo"] = _gp_math.pi - p["angulo"]
                    if p["y"] < 0:
                        p["y"] = 0.0
                        p["angulo"] = -p["angulo"]
                    elif p["y"] > height:
                        p["y"] = float(height)
                        p["angulo"] = -p["angulo"]

                if rotar:
                    p["rotacion"] = (p["rotacion"] + p["velocidad_rotacion"] * dt) % 360.0

                vencida = p["vida"] is not None and (st - p["nacimiento"]) > p["vida"]
                fuera_de_pantalla = (
                    p["x"] < -margen or p["x"] > width + margen or
                    p["y"] < -margen or p["y"] > height + margen
                )

                if vencida or fuera_de_pantalla:
                    p = self._generar_particula(width, height, st, False)
                    particulas[indice] = p

                x_dibujo = p["x"]
                if ondulado:
                    fase = st * frecuencia_ondulado * 2 * _gp_math.pi + p["fase_ondulado"]
                    x_dibujo += _gp_math.sin(fase) * amplitud_ondulado

                # Factor de fade (0.0 a 1.0): sube al nacer y baja al
                # final de la vida, para que aparezca/desaparezca suave.
                factor = 1.0
                if hay_fade:
                    edad = st - p["nacimiento"]
                    vida = p["vida"]
                    f_in = fade_in
                    f_out = fade_out if vida is not None else 0.0
                    if vida is not None and f_in + f_out > vida:
                        escala_fade = vida / (f_in + f_out)
                        f_in *= escala_fade
                        f_out *= escala_fade
                    if f_in > 0 and edad < f_in:
                        factor = max(0.0, edad / f_in)
                    if f_out > 0 and vida is not None and edad > vida - f_out:
                        factor = min(factor, max(0.0, (vida - edad) / f_out))

                imagen_indice = p["imagen_indice"]
                if imagen_indice is not None:
                    disp, _aw, _ah = imagenes_info[imagen_indice]
                    transformada = Transform(disp, zoom=p["escala"], rotate=p["rotacion"], alpha=p["opacidad"] * factor)
                    render_hijo = renpy.render(transformada, width, height, st, at)
                    hw, hh = render_hijo.width, render_hijo.height
                    r.blit(render_hijo, (x_dibujo - hw / 2.0, p["y"] - hh / 2.0))
                else:
                    rgba = p["color_rgba"]
                    if factor < 1.0:
                        rgba = (rgba[0], rgba[1], rgba[2], int(rgba[3] * factor))
                    if forma_rectangulo:
                        aw = p["ancho_px"]
                        ah = p["tamano_px"]
                        lienzo.rect(rgba, (int(x_dibujo - aw / 2.0), int(p["y"] - ah / 2.0), aw, ah))
                    else:
                        lienzo.circle(rgba, (int(x_dibujo), int(p["y"])), p["radio_px"])

            # Vuelve a pedir un cuadro nuevo lo antes posible, para que
            # la animacion sea continua.
            renpy.redraw(self, 0)

            return r

    def _gp_imagenes_tenidas(rutas, colores):
        """
        Devuelve la lista de imagenes lista para pasar a "imagenes": si
        hay "colores", una version de cada imagen tenida de cada color
        (la imagen original debe ser blanca); si "colores" es None, las
        rutas tal cual.
        """
        if not rutas or not colores:
            return rutas
        return [
            im.MatrixColor(ruta, im.matrix.colorize(color, color))
            for ruta in rutas
            for color in colores
        ]

    # Efectos ya armados: son EJEMPLOS listos para usar. Los usan
    # gp_nieve(), gp_lluvia() y gp_luciernagas() (mas abajo), pero tambien
    # los podes usar directamente con gp_crear_particulas(tipo=GP_NIEVE).
    # Para cambiar algo puntual, pasale el parametro con nombre, por ejemplo
    # gp_nieve(cantidad=40). Para un efecto propio, crealo con
    # gp_crear_particulas(...) o GP_TipoParticula(...) en tu propio script.
    # Las imagenes "luz.png" y "gota.png" estan en la carpeta "imagenes" de
    # este modulo. Con imagenes=None se dibujan como figuras de color plano.

    GP_NIEVE = GP_TipoParticula(
        imagenes=["modulos/gestor_particulas/imagenes/luz.png"],
        color="#FFFFFF",
        forma="circulo",
        tamano_min=8, tamano_max=20,
        cantidad=150,
        angulo_base=90, angulo_variacion=20,
        velocidad_min=30, velocidad_max=80,
        ondulado=True, amplitud_ondulado=25, frecuencia_ondulado=0.6,
        opacidad_min=0.5, opacidad_max=1.0,
        zorder=-10,
    )

    GP_LLUVIA = GP_TipoParticula(
        # "gota.png" es una estela ya inclinada ~10 grados, para calzar con
        # el angulo_base de 100.
        imagenes=["modulos/gestor_particulas/imagenes/gota.png"],
        color="#9FC6FF",
        forma="rectangulo",
        tamano_min=14, tamano_max=26,
        ancho_min=1, ancho_max=2,
        cantidad=140,
        angulo_base=100, angulo_variacion=4,
        velocidad_min=650, velocidad_max=950,
        opacidad_min=0.35, opacidad_max=0.7,
        zorder=-10,
    )

    GP_LUCIERNAGAS = GP_TipoParticula(
        # "luz.png" es blanca: se tine de tres tonos de luciernaga.
        imagenes=_gp_imagenes_tenidas(
            ["modulos/gestor_particulas/imagenes/luz.png"],
            ["#F5FF7A", "#CFFF5E", "#FFF1A8"],
        ),
        tamano_min=22, tamano_max=42,
        cantidad=30,
        angulo_variacion=180,
        velocidad_min=15, velocidad_max=40,
        movimiento="aleatorio", vagar_giro=50,
        opacidad_min=0.7, opacidad_max=1.0,
        tiempo_vida_min=3, tiempo_vida_max=6,
        fade_in=1.0, fade_out=1.0,
        zorder=-10,
    )

    # Capa por defecto en la que se muestran los efectos. Se usa
    # "screens" (en vez de "master") para que el efecto NO se borre
    # solo cuando cambies de fondo con la instruccion "scene": se queda
    # prendido hasta que vos lo apagues con gp_terminar_particulas().
    GP_CAPA_POR_DEFECTO = "screens"

    # Contador interno para generar un identificador nuevo cada vez que
    # se crea un efecto con gp_crear_particulas(). Cada efecto activo
    # queda anotado en _gp_activos, con su identificador como clave y
    # la etiqueta/capa de su pantalla como valor (necesario para poder
    # apagarlo despues con gp_terminar_particulas(id)).
    _gp_contador = 0
    _gp_activos = {}

    def gp_crear_particulas(tipo=None, capa=None, **parametros):
        """
        Crea y muestra un efecto de particulas nuevo, armado a partir de
        los parametros que le pases (sin depender de que exista ningun
        efecto predefinido). Devuelve un identificador (un numero) que
        despues usas con gp_terminar_particulas(id) para apagar
        ESE efecto en particular. Podes tener muchos efectos distintos
        activos al mismo tiempo, cada uno con su propio identificador.

        Le podes pasar, con nombre, cualquiera de los parametros que
        recibe GP_TipoParticula (color, imagenes, forma, tamano_min,
        tamano_max, cantidad, angulo_base, angulo_variacion,
        velocidad_min, velocidad_max, ondulado, amplitud_ondulado,
        frecuencia_ondulado, rotar, rotacion_velocidad_min,
        rotacion_velocidad_max, opacidad_min, opacidad_max, origen,
        origen_min, origen_max, tiempo_vida_min, tiempo_vida_max,
        zorder). La explicacion completa de cada uno esta en el
        docstring de la clase GP_TipoParticula, un poco mas arriba en
        este mismo archivo. Los que no le pases quedan con su valor por
        defecto.

        Ejemplo (chispas de fuego, armadas al vuelo, sin ningun efecto
        predefinido ni ninguna imagen):

            $ id_chispas = gp_crear_particulas(
                color=["#FFCC66", "#FF9933", "#FF6600"], forma="circulo",
                tamano_min=2, tamano_max=5, cantidad=25,
                angulo_base=270, angulo_variacion=30,
                velocidad_min=30, velocidad_max=70,
                origen="abajo", tiempo_vida_min=0.8, tiempo_vida_max=1.6,
            )
            ...
            $ gp_terminar_particulas(id_chispas)

        Parametros propios de esta funcion (no de GP_TipoParticula):

            tipo (GP_TipoParticula o None):
                Si ya tenes armado un GP_TipoParticula de antes (por
                ejemplo, uno que queres reutilizar varias veces), se lo
                podes pasar con tipo=...; los parametros con nombre que
                agregues se aplican encima como ajustes puntuales.
                Todo lo que no pongas queda con su valor por defecto.

            capa (str o None):
                En que capa se muestra el efecto. Si se deja en None,
                se usa GP_CAPA_POR_DEFECTO ("screens").
        """
        if tipo is None:
            tipo = GP_TipoParticula(**parametros)
        elif parametros:
            tipo = _gp_tipo_con_cambios(tipo, parametros)

        if capa is None:
            capa = GP_CAPA_POR_DEFECTO

        global _gp_contador
        _gp_contador += 1
        id_efecto = _gp_contador

        etiqueta = "gp_efecto_%d" % id_efecto
        instancia = GestorParticulas(tipo)
        _gp_activos[id_efecto] = (etiqueta, capa)

        # El zorder se pasa como argumento especial "_zorder" (y no como
        # clausula "zorder" dentro del screen) porque esa clausula se
        # evalua antes de que los parametros del screen (en este caso,
        # "instancia") esten disponibles.
        renpy.show_screen(
            "gp_efecto",
            _tag=etiqueta,
            _layer=capa,
            _zorder=tipo.zorder,
            instancia=instancia,
        )

        return id_efecto

    def gp_terminar_particulas(id_efecto):
        """
        Apaga (oculta) el efecto de particulas creado con
        gp_crear_particulas(), a partir del identificador que devolvio
        esa funcion. Si el identificador no corresponde a ningun efecto
        activo (por ejemplo, porque ya se habia apagado antes), no hace
        nada.
        """
        datos = _gp_activos.pop(id_efecto, None)
        if datos is None:
            return
        etiqueta, capa = datos
        renpy.hide_screen(etiqueta, layer=capa)

    def gp_terminar_todas():
        """Apaga todos los efectos de particulas que esten activos."""
        for id_efecto in list(_gp_activos.keys()):
            gp_terminar_particulas(id_efecto)

    def gp_efecto_activo(id_efecto):
        """Devuelve True si ese identificador corresponde a un efecto todavia activo."""
        return id_efecto in _gp_activos

    def _gp_tipo_con_cambios(tipo_base, cambios):
        """
        Devuelve una copia de "tipo_base" (un GP_TipoParticula) con los
        atributos de "cambios" (un diccionario) sobreescritos. Si
        "cambios" esta vacio, devuelve "tipo_base" tal cual, sin copiar.
        La usan gp_nieve() y gp_lluvia() para permitir ajustar la receta
        de nieve/lluvia sin tener que escribirla de nuevo entera.
        """
        if not cambios:
            return tipo_base
        nuevo = _gp_copy.copy(tipo_base)
        cambios = dict(cambios)
        if "tiempo_vida" in cambios:
            valor = cambios.pop("tiempo_vida")
            cambios["tiempo_vida_min"] = valor
            cambios["tiempo_vida_max"] = valor
        for clave, valor in cambios.items():
            if not hasattr(nuevo, clave):
                raise Exception("Parametro de particulas desconocido: %r" % (clave,))
            setattr(nuevo, clave, valor)
        if nuevo.fade_out > 0 and nuevo.tiempo_vida_max is None:
            raise Exception("'fade_out' necesita que definas tiempo_vida")
        return nuevo

    def gp_nieve(capa=None, **cambios):
        """
        Atajo para crear el efecto de nieve de ejemplo (ver GP_NIEVE,
        mas arriba). Devuelve un identificador, igual que
        gp_crear_particulas().

        Le podes pasar, con nombre, cualquier parametro de
        GP_TipoParticula para ajustar solo eso puntualmente. Por
        ejemplo, para una nevada mas densa solo en esta escena:

            $ id_nieve = gp_nieve(cantidad=150)
        """
        return gp_crear_particulas(tipo=_gp_tipo_con_cambios(GP_NIEVE, cambios), capa=capa)

    def gp_lluvia(capa=None, **cambios):
        """
        Atajo para crear el efecto de lluvia de ejemplo (ver GP_LLUVIA).
        Funciona igual que gp_nieve(): devuelve un identificador y acepta
        parametros de GP_TipoParticula para ajustar puntualmente esta
        lluvia.
        """
        return gp_crear_particulas(tipo=_gp_tipo_con_cambios(GP_LLUVIA, cambios), capa=capa)

    def gp_luciernagas(capa=None, **cambios):
        """
        Atajo para crear el efecto de luciernagas de ejemplo (ver
        GP_LUCIERNAGAS). Funciona igual que gp_nieve(): devuelve un
        identificador y acepta parametros de GP_TipoParticula para
        ajustar puntualmente este efecto.
        """
        return gp_crear_particulas(tipo=_gp_tipo_con_cambios(GP_LUCIERNAGAS, cambios), capa=capa)


# Pantalla (screen) interna que efectivamente muestra el efecto en
# pantalla. No se usa directamente: la maneja gp_crear_particulas() /
# gp_terminar_particulas().
screen gp_efecto(instancia):
    add instancia
