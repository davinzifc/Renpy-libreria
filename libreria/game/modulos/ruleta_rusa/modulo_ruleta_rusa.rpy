# ============================================================================
#  MODULO: RULETA RUSA (arma que apunta y dispara, en 2D)
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
#      $ ar = arma(balas=1, recamaras=6, girar_siempre=False)
#      $ ar.girar()                              # gira el tambor (sin animacion, sin disparar)
#      $ murio = ar.disparar(apuntar_a="izquierda")
#      $ ar.agregar_balas(1)                     # carga mas municion a mitad de partida
#      $ ar.ocultar()                            # la saca de pantalla al terminar la escena
#
#  IMPORTANTE: esto NO usa modelos ni renderizado 3D. El arma es una
#  sola imagen 2D que se anima con espejado (ATL) para apuntar hacia
#  un lado u otro, igual que cualquier otro displayable de Ren'Py.
#  Girar el tambor es un cambio de estado interno (ver mas abajo): no
#  tiene ninguna animacion propia.
# ============================================================================


# ============================================================================
#  EL "MOTOR" DEL MODULO
# ----------------------------------------------------------------------------
#  No necesitas editar nada de lo que sigue para usar el modulo. La unica
#  funcion que usas desde tu guion es arma(...), y los metodos del objeto
#  que devuelve (girar() y disparar()), explicados en el README.md.
# ============================================================================
init python:

    import random as _rr_random

    # Imagen por defecto (revolver apuntando a la derecha) que se usa
    # si no le pasas la tuya propia con el parametro "imagen" de
    # disparar(). Ilustracion de Vecteezy.com (ver README.md de este
    # modulo para el credito completo), espejada y reducida.
    RR_IMAGEN_POR_DEFECTO = "modulos/ruleta_rusa/imagenes/arma.png"

    def _rr_mostrar_arma(imagen, transformacion):
        """Muestra la pantalla interna del arma con la imagen y la animacion dadas."""
        renpy.show_screen("rr_arma", imagen=(imagen or RR_IMAGEN_POR_DEFECTO), transformacion=transformacion)

    class RR_Arma(object):
        """
        Representa un arma con un tambor de varias recamaras (un array
        de True/False: True = esa recamara tiene bala), y un puntero
        ("posicion") que indica cual recamara esta bajo el martillo.
        Girar el tambor NO cambia donde estan cargadas las balas: solo
        elige al azar desde que recamara arranca el puntero, igual que
        girar un tambor de verdad. Es un objeto de datos simple (no
        guarda ningun displayable ni pantalla adentro), asi que se
        guarda y se carga solo con el sistema de save/load de Ren'Py.

        No se crea directamente: se usa la funcion arma(...), mas abajo
        en este mismo archivo.
        """

        def __init__(self, balas=1, recamaras=6, girar_siempre=False):
            if not isinstance(recamaras, int) or recamaras <= 0:
                raise Exception(
                    "arma(): 'recamaras' tiene que ser un entero mayor a 0 (recibido: %r)" % (recamaras,)
                )
            if not isinstance(balas, int) or balas < 0:
                raise Exception(
                    "arma(): 'balas' tiene que ser un entero mayor o igual a 0 (recibido: %r)" % (balas,)
                )
            if balas > recamaras:
                raise Exception(
                    "arma(): 'balas' (%d) no puede ser mayor que 'recamaras' (%d)" % (balas, recamaras)
                )

            self.recamaras = recamaras
            # Si es True, cada disparar() gira el tambor (puntero a una
            # posicion al azar) antes de disparar. Si es False, el
            # puntero simplemente avanza una recamara por disparo, sin
            # volver a girar (ruleta rusa "clasica"), salvo que se gire
            # a mano con girar() o con el parametro puntual girar= de
            # disparar(). Ver README para más detalle.
            self.girar_siempre = girar_siempre

            # Array fijo de recamaras (True = cargada). Girar el tambor
            # NO reordena este array: solo mueve "posicion" (ver
            # girar()). Se arma una vez aca, con "balas" balas
            # repartidas al azar; para cargar mas balas despues de
            # creada el arma, usa agregar_balas().
            self.camaras = [False] * recamaras
            for indice in _rr_random.sample(range(recamaras), balas):
                self.camaras[indice] = True
            self.posicion = 0

            # Hacia que lado esta apuntando ahora mismo (o apuntaria si
            # se mostrara): punto de partida de la proxima animacion,
            # para que el arma no "salte" de golpe al lado contrario
            # antes de apuntar. Cambia cada vez que disparar() apunta a
            # un lado nuevo.
            self.lado_actual = "derecha"

        def girar(self):
            """
            Gira el tambor: elige al azar desde que recamara arranca el
            puntero (no cambia donde estan cargadas las balas, solo
            desde donde se empieza a recorrer el tambor). Es un cambio
            de estado interno, sin ninguna animacion ni efecto en
            pantalla. Pensado para un momento de la historia donde el
            jugador elige volver a girar el tambor antes de apretar el
            gatillo (por ejemplo, un choice "¿Querés girar el tambor de
            nuevo?").
            """
            self.posicion = _rr_random.randrange(self.recamaras)

        def balas_restantes(self):
            """Cuantas balas sin disparar quedan en el tambor actual."""
            return sum(1 for cargada in self.camaras if cargada)

        def agregar_balas(self, cantidad=1):
            """
            Carga "cantidad" balas nuevas en recamaras vacias elegidas
            al azar, sin tocar las balas ni la posicion que ya habia.
            Pensado para escenas donde, a mitad de la partida, se le
            agrega mas municion al arma. Por ejemplo, con un tambor de
            6 y una sola bala ([][][][v][][]), agregar_balas(1) podria
            dejarlo en [][v][][v][][].

            Tira una excepcion si no quedan suficientes recamaras
            vacias para cargar esa cantidad.
            """
            vacias = [indice for indice, cargada in enumerate(self.camaras) if not cargada]
            if cantidad > len(vacias):
                raise Exception(
                    "arma.agregar_balas(): no hay lugar para %d bala(s): "
                    "quedan %d recamara(s) vacia(s) de %d" % (cantidad, len(vacias), self.recamaras)
                )
            for indice in _rr_random.sample(vacias, cantidad):
                self.camaras[indice] = True

        def ocultar(self):
            """
            Saca el arma de la pantalla. El arma queda visible de forma
            persistente entre disparo y disparo (no se oculta sola
            despues de cada uno): llama a esto cuando la escena termine
            y quieras que desaparezca.
            """
            renpy.hide_screen("rr_arma")

        def disparar(
            self,
            apuntar_a="derecha",
            girar=None,
            imagen=None,
            sonido_disparo=None,
            sonido_vacio=None,
            duracion_apuntado=0.35,
        ):
            """
            Hace la secuencia de un disparo: gira el tambor si
            corresponde (sin animacion propia, ver girar()), apunta
            hacia "izquierda" o "derecha", y "aprieta el gatillo".
            Devuelve True si salio bala, False si fue un chasquido en
            vacio. Las consecuencias de la historia (que pasa despues
            del disparo) las maneja tu propio guion, leyendo el valor
            que devuelve.

            El arma queda visible en pantalla, apuntando hacia
            "apuntar_a", hasta el proximo disparar() o hasta que llames
            a ocultar(): no se oculta sola despues de cada disparo.

            Parametros:
                apuntar_a ("izquierda" o "derecha"):
                    Hacia que lado de la pantalla apunta el arma (donde
                    tipicamente estan posicionados el NPC y el
                    jugador). Usa el mismo lado para el mismo personaje
                    durante toda la escena, para que quede claro a
                    quien le toca.

                girar (bool o None):
                    Si se gira el tambor antes de ESTE disparo en
                    particular. Con None (por defecto), se usa
                    girar_siempre del arma. Pasando True o False acá se
                    lo pisa solo para este llamado puntual.

                imagen (str o None):
                    Ruta de imagen propia del arma (tiene que apuntar
                    hacia la derecha en su version original, sin
                    espejar). Con None usa RR_IMAGEN_POR_DEFECTO.

                sonido_disparo, sonido_vacio (str o None):
                    Rutas de sonido para el disparo con bala y el
                    chasquido en vacio, respectivamente. El modulo no
                    trae sonidos propios (para no depender de efectos
                    con licencia): con None, no suena nada.

                duracion_apuntado (segundos):
                    Cuanto tarda el arma en girar hacia el lado
                    indicado en "apuntar_a".
            """
            if apuntar_a not in ("izquierda", "derecha"):
                raise Exception(
                    "arma.disparar(): 'apuntar_a' tiene que ser 'izquierda' o 'derecha' (recibido: %r)" % (apuntar_a,)
                )

            hubo_giro = self.girar_siempre if girar is None else girar
            if hubo_giro:
                self.posicion = _rr_random.randrange(self.recamaras)

            resultado = self.camaras[self.posicion]
            if resultado:
                # La bala de esta recamara se "gasta": si el puntero
                # sigue avanzando sin volver a girar (girar_siempre=
                # False) y vuelve a pasar por acá en una vuelta
                # siguiente, no vuelve a disparar sola (igual que un
                # cartucho real, que no se dispara dos veces).
                # balas_restantes() tiene que reflejar esto.
                self.camaras[self.posicion] = False
            # El tambor avanza una recamara para el proximo disparo,
            # haya girado o no en este.
            self.posicion = (self.posicion + 1) % self.recamaras

            transformacion = rr_t_apuntar(self.lado_actual, apuntar_a, duracion_apuntado)
            _rr_mostrar_arma(imagen, transformacion)
            self.lado_actual = apuntar_a
            renpy.pause(duracion_apuntado + 0.15)

            sonido = sonido_disparo if resultado else sonido_vacio
            if sonido:
                renpy.play(sonido)
                renpy.pause(0.3)

            return resultado

    def arma(balas=1, recamaras=6, girar_siempre=False):
        """
        Crea y devuelve un arma nueva (un RR_Arma), lista para guardar
        en una variable de tu guion y usar con sus metodos girar() y
        disparar(). Guardala en una variable propia (por ejemplo
        "$ ar = arma(...)") para poder volver a usar la misma más
        adelante: como es un objeto de datos simple, viaja sola con el
        guardado/carga de tu partida.

        Parametros:
            balas (int): cuantas balas hay cargadas, de entrada,
                repartidas al azar entre las recamaras. Podes cargar
                mas balas despues con arma.agregar_balas(...).
            recamaras (int): cuantas recamaras tiene el tambor (6 es lo
                habitual en un revolver).
            girar_siempre (bool): si es True, cada disparar() gira el
                tambor (puntero a una recamara al azar) antes de
                disparar: la probabilidad de ese disparo es
                balas_restantes/recamaras en ese momento, sin depender
                de que recamara toco la vez anterior. Si es False (por
                defecto), el puntero solo avanza una recamara por
                disparo sin volver a girar, como en la ruleta rusa
                "clasica" de las peliculas: la probabilidad del proximo
                disparo depende de lo que ya salio antes. En cualquiera
                de los dos modos, podes forzar un giro puntual con
                arma.girar() o con el parametro girar= de disparar().
        """
        return RR_Arma(balas=balas, recamaras=recamaras, girar_siempre=girar_siempre)


# ============================================================================
#  ANIMACION (ATL puro, sin ningun modelo ni renderizado 3D)
# ----------------------------------------------------------------------------
#  rr_t_apuntar: espejado horizontal (NO una rotacion de 180, para que
#  no quede "boca abajo") hacia el lado indicado, y un pequeño golpe de
#  retroceso al final. Es la UNICA animacion del modulo: girar el
#  tambor (ver girar() y disparar(), mas arriba) no tiene animacion
#  propia, es solo un cambio de estado interno.
# ============================================================================
transform rr_t_apuntar(lado_inicial, lado, duracion=0.35):
    xalign 0.5 yalign 0.6
    xanchor 0.5 yanchor 0.5
    xzoom (-1.0 if lado_inicial == "izquierda" else 1.0)
    zoom 1.0
    linear duracion xzoom (-1.0 if lado == "izquierda" else 1.0)
    linear 0.05 zoom 0.92
    linear 0.1 zoom 1.0


# Pantalla interna que muestra el arma animandose. No se usa
# directamente: la maneja disparar(), mas arriba, llamando
# renpy.show_screen()/renpy.pause()/renpy.hide_screen() directamente
# desde Python (NO con la sentencia "call": renpy.call() corta la
# sentencia "$" que lo invoca y no puede devolver un valor a quien lo
# llamo, asi que no sirve para esto).
screen rr_arma(imagen, transformacion):
    add imagen at transformacion
