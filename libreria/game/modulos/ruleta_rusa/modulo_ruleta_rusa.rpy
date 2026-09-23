# ============================================================================
#  MODULO: RULETA RUSA (arma que apunta y dispara)
#  Version: 1.0
#  Compatibilidad: Ren'Py 7.x / 8.x
#  Autor: davinzifc
#  Coautores: popen.queen
#  Licencia: MIT. Copyright (c) 2026 davinzifc y popen.queen.
#            Puedes usar, copiar, modificar y redistribuir este archivo,
#            siempre que mantengas este aviso de copyright y la licencia
#            MIT (ver el archivo LICENSE del repositorio) en las copias.
#            Es decir: hay que dar credito a los desarrolladores.
#
#  Para instrucciones de instalacion, ejemplos de uso dentro del guion y
#  mas detalles, abri el archivo "README.md" que viene junto a este
#  script, en esta misma carpeta.
#
#  Resumen rapido de uso (ver el README para mas ejemplos):
#      $ ar = arma(balas=1, recamaras=6, girar_siempre=False)
#      $ ar.girar()                              # gira el tambor (sonido, sin disparar)
#      $ murio = ar.disparar(apuntar_a="izquierda")
#      $ ar.agregar_balas(1)                     # carga mas municion a mitad de partida
#      $ ar.ocultar()                            # la saca de pantalla al terminar la escena
#      $ RR_DEBUG = True                         # cartel con el estado real del tambor (para probar)
#      $ rr_hit()                                # flash rojo de pantalla completa (por ejemplo, si el jugador se dispara)
#
#  El arma es una sola imagen que se anima con espejado (ATL) para
#  apuntar hacia un lado u otro, igual que cualquier otro displayable
#  de Ren'Py. Girar el tambor NO tiene animacion en pantalla (ver mas
#  abajo), pero si reproduce un sonido y espera a que termine antes de
#  continuar.
# ============================================================================


# ============================================================================
#  CONFIGURACION — esto es lo UNICO que normalmente necesitas tocar
# ----------------------------------------------------------------------------
#  No hace falta saber programar para esta parte: cambia el valor que
#  esta despues del signo "=" en cada linea (dejando las comillas si las
#  tiene) y guarda el archivo.
# ============================================================================

# --- SONIDO DE CHASQUIDO EN VACIO: ACTIVARLO, DESACTIVARLO O CAMBIARLO ----
# Sonido que se escucha cuando disparar() cae en una recamara SIN bala.
#   - Dejalo tal cual esta para usar el sonido de ejemplo ya incluido.
#   - Cambialo a None (sin comillas) para que no suene nada:
#         define RR_SONIDO_VACIO = None
#   - O cambialo por la ruta a tu propio sonido (.mp3, .ogg o .wav),
#     copiado dentro de la carpeta "game/" de tu proyecto.
define RR_SONIDO_VACIO = "modulos/ruleta_rusa/audio/rr_vacio.mp3"

# --- SONIDO DE DISPARO CON BALA -------------------------------------------
# Igual que el de arriba, pero para cuando SI sale la bala.
#   - Dejalo tal cual esta para usar el sonido de ejemplo ya incluido.
#   - Cambialo a None (sin comillas) para que no suene nada.
#   - O cambialo por la ruta a tu propio sonido, copiado dentro de la
#     carpeta "game/" de tu proyecto.
define RR_SONIDO_DISPARO = "modulos/ruleta_rusa/audio/rr_disparo.mp3"

# --- SONIDO DE GIRAR EL TAMBOR ---------------------------------------------
# Sonido que se escucha cada vez que se gira el tambor (con girar(), o con
# disparar() cuando corresponde girar antes de disparar). girar() ESPERA a
# que este sonido termine de sonar antes de seguir, asi que si lo cambias
# por uno mucho mas largo, ese giro va a tardar mas en la practica.
#   - Dejalo tal cual esta para usar el sonido de ejemplo ya incluido.
#   - Cambialo a None (sin comillas) para que no suene nada (y entonces
#     girar() no espera nada: es instantaneo).
#   - O cambialo por la ruta a tu propio sonido, copiado dentro de la
#     carpeta "game/" de tu proyecto.
define RR_SONIDO_GIRAR = "modulos/ruleta_rusa/audio/rr_girar.mp3"

# --- SONIDO DE CARGAR BALAS -------------------------------------------
# Sonido que se escucha al agregar balas con agregar_balas(). Igual que
# RR_SONIDO_GIRAR, agregar_balas() ESPERA a que este sonido termine de
# sonar antes de seguir.
#   - Dejalo tal cual esta para usar el sonido de ejemplo ya incluido.
#   - Cambialo a None (sin comillas) para que no suene nada (y entonces
#     agregar_balas() no espera nada: es instantaneo).
#   - O cambialo por la ruta a tu propio sonido, copiado dentro de la
#     carpeta "game/" de tu proyecto.
define RR_SONIDO_RECARGAR = "modulos/ruleta_rusa/audio/rr_recargar.mp3"

# --- MODO DEBUG -------------------------------------------------------
# Con True, muestra un cartel en pantalla con el estado REAL del tambor:
# que recamaras tienen bala y donde apunta el puntero ahora mismo. Util
# para probar tu guion, pero es "hacer trampa" para jugar de verdad (le
# muestra al jugador donde esta la bala), asi que se recomienda dejarlo
# en False para la version final de tu juego.
#   $ RR_DEBUG = True    # tambien lo podes prender/apagar desde tu guion
define RR_DEBUG = False

# --- FLASH DE GOLPE (rr_hit) ----------------------------------------------
# Color y tiempos del flash de pantalla completa que hace rr_hit(), pensado
# para marcar el momento en que alguien "recibe" el disparo (por ejemplo,
# el jugador). El modulo NO lo llama solo en ningun momento: vos decidis
# cuando pasa eso en tu guion (ver README para un ejemplo) y ahi llamas a
# rr_hit().
define RR_HIT_COLOR = "#FF0000"
define RR_HIT_ALPHA_MAXIMO = 0.6
define RR_HIT_DURACION_SUBIDA = 0.05
define RR_HIT_DURACION_BAJADA = 0.4


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

    # Duracion del pequeño "golpe" del gatillo al final de rr_t_apuntar
    # (mas abajo): un recorte rapido de zoom y la vuelta a su tamano
    # normal. Se nota en CUALQUIER disparo, haya salido bala o no (es
    # el gatillo, no el disparo en si). Definida UNA sola vez aca (no
    # como numeros sueltos en dos lugares distintos) para que
    # disparar() siempre espere exactamente lo que tarda la animacion,
    # sin que se puedan desincronizar.
    RR_DURACION_GOLPE_RECORTE = 0.08
    RR_DURACION_GOLPE_VUELTA = 0.15

    # Duracion del culatazo (rr_t_retroceso, mas abajo): SOLO se juega
    # cuando sale bala de verdad (no en un chasquido en vacio). Mismo
    # motivo que arriba: una sola definicion para que no se desincronice.
    RR_DURACION_RETROCESO_GOLPE = 0.05
    RR_DURACION_RETROCESO_VUELTA = 0.25

    # Canales de audio propios para los sonidos que hay que esperar a que
    # terminen (girar y recargar), separados del canal "sound" general (el
    # que usa renpy.play() para disparo/vacio), para poder preguntarles
    # "¿todavia estas sonando?" sin que otro efecto de sonido del juego los
    # interrumpa ni sea interrumpido por ellos. Usan el mixer "sound" para
    # que el jugador los controle con el control deslizante "Sonido" de
    # siempre.
    renpy.music.register_channel("rr_girar", mixer="sound", loop=False, tight=True)
    renpy.music.register_channel("rr_recargar", mixer="sound", loop=False, tight=True)

    def _rr_reproducir_y_esperar(sonido, canal):
        """Reproduce "sonido" en "canal" y no vuelve hasta que termina de sonar."""
        if not sonido:
            return
        renpy.music.play(sonido, channel=canal)
        while renpy.music.is_playing(channel=canal):
            renpy.pause(0.05)

    def _rr_validar_posiciones(quien, nombre_parametro, posiciones, recamaras):
        """
        Valida una lista de indices de recamara (0 a recamaras-1, sin
        repetidos) para arma(posiciones_balas=...) y
        arma.agregar_balas(posiciones=...). Devuelve la lista ya
        convertida (por si "posiciones" era otra cosa iterable, como
        una tupla), o tira una excepcion clara si algo esta mal.
        """
        posiciones = list(posiciones)
        for indice in posiciones:
            if not isinstance(indice, int) or not (0 <= indice < recamaras):
                raise Exception(
                    "%s: '%s' tiene una recamara invalida (%r): tiene que ser un entero "
                    "entre 0 y %d (recamaras=%d)" % (quien, nombre_parametro, indice, recamaras - 1, recamaras)
                )
        if len(set(posiciones)) != len(posiciones):
            raise Exception(
                "%s: '%s' no puede repetir la misma recamara (recibido: %r)" % (quien, nombre_parametro, posiciones)
            )
        return posiciones

    def _rr_mostrar_arma(imagen, transformacion):
        """Muestra la pantalla interna del arma con la imagen y la animacion dadas."""
        renpy.show_screen("rr_arma", imagen=(imagen or RR_IMAGEN_POR_DEFECTO), transformacion=transformacion)

    def _rr_texto_debug(arma_obj):
        """
        Arma una linea de texto tipo " _  _ [v] _  _  _ " con una
        posicion por recamara: "v" = tiene bala, "_" = vacia, y la
        recamara entre corchetes es donde esta el puntero ahora mismo
        (la que va a leer el proximo disparar()).
        """
        partes = []
        for indice, cargada in enumerate(arma_obj.camaras):
            marca = "v" if cargada else "_"
            if indice == arma_obj.posicion:
                marca = "[%s]" % marca
            else:
                marca = " %s " % marca
            partes.append(marca)
        return "".join(partes)

    def _rr_actualizar_debug(arma_obj):
        """Muestra (o actualiza) el cartel de RR_DEBUG para "arma_obj", o lo oculta si RR_DEBUG es False."""
        if RR_DEBUG:
            renpy.show_screen("rr_debug", arma_obj=arma_obj)
        else:
            renpy.hide_screen("rr_debug")

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

        def __init__(self, balas=1, recamaras=6, girar_siempre=False, posiciones_balas=None):
            if not isinstance(recamaras, int) or recamaras <= 0:
                raise Exception(
                    "arma(): 'recamaras' tiene que ser un entero mayor a 0 (recibido: %r)" % (recamaras,)
                )

            if posiciones_balas is not None:
                posiciones_balas = _rr_validar_posiciones("arma()", "posiciones_balas", posiciones_balas, recamaras)
            else:
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
            # girar()). Se arma una vez aca: en recamaras exactas si te
            # pasaron "posiciones_balas", o si no, con "balas" balas
            # repartidas al azar. Para cargar mas balas despues de
            # creada el arma, usa agregar_balas().
            self.camaras = [False] * recamaras
            if posiciones_balas is not None:
                for indice in posiciones_balas:
                    self.camaras[indice] = True
            else:
                for indice in _rr_random.sample(range(recamaras), balas):
                    self.camaras[indice] = True
            self.posicion = 0

            # Hacia que lado esta apuntando ahora mismo (o apuntaria si
            # se mostrara): punto de partida de la proxima animacion,
            # para que el arma no "salte" de golpe al lado contrario
            # antes de apuntar. Cambia cada vez que disparar() apunta a
            # un lado nuevo.
            self.lado_actual = "derecha"

            _rr_actualizar_debug(self)

        def girar(self):
            """
            Gira el tambor: elige al azar desde que recamara arranca el
            puntero (no cambia donde estan cargadas las balas, solo
            desde donde se empieza a recorrer el tambor). No tiene
            ninguna animacion en pantalla, pero SI reproduce
            RR_SONIDO_GIRAR (configurable al principio de este archivo)
            y espera a que termine de sonar antes de devolver el
            control a tu guion. Con RR_SONIDO_GIRAR en None, es
            instantaneo. Pensado para un momento de la historia donde
            el jugador elige volver a girar el tambor antes de apretar
            el gatillo (por ejemplo, un choice "¿Querés girar el tambor
            de nuevo?"); disparar() tambien lo usa por dentro cuando
            corresponde girar antes de disparar.
            """
            self.posicion = _rr_random.randrange(self.recamaras)
            _rr_actualizar_debug(self)
            _rr_reproducir_y_esperar(RR_SONIDO_GIRAR, "rr_girar")

        def balas_restantes(self):
            """Cuantas balas sin disparar quedan en el tambor actual."""
            return sum(1 for cargada in self.camaras if cargada)

        def agregar_balas(self, cantidad=1, posiciones=None):
            """
            Carga balas nuevas sin tocar las balas ni la posicion del
            puntero que ya habia. Pensado para escenas donde, a mitad
            de la partida, se le agrega mas municion al arma. Por
            ejemplo, con un tambor de 6 y una sola bala ([][][][v][][],
            puntero en la recamara 1), agregar_balas(1) la carga ahi
            mismo: [][v][][v][][].

            No tiene ninguna animacion en pantalla, pero SI reproduce
            RR_SONIDO_RECARGAR (configurable al principio de este
            archivo) y espera a que termine de sonar antes de devolver
            el control a tu guion. Con RR_SONIDO_RECARGAR en None, es
            instantaneo.

            Parametros:
                cantidad (int):
                    Cuantas balas cargar. No es al azar: arranca en la
                    recamara donde esta el puntero AHORA (la que va a
                    leer el proximo disparar() si no se vuelve a
                    girar); si esa ya tiene bala, sigue avanzando
                    recamara por recamara (dando la vuelta al tambor si
                    hace falta) hasta cargar tantas balas como
                    "cantidad". No se usa si le pasas "posiciones".

                posiciones (lista de int, o None):
                    En vez de al azar, elegi vos mismo en que recamaras
                    exactas cargar bala (indices de 0 a recamaras-1).
                    Por ejemplo, posiciones=[0, 3] carga dos balas, en
                    la primera y la cuarta recamara. Si lo usas, "cantidad"
                    se ignora (la cantidad cargada es la cantidad de
                    posiciones que le pases).

            Tira una excepcion si no quedan suficientes recamaras
            vacias para "cantidad" (o si alguna de "posiciones" es
            invalida o ya tenia bala), antes de reproducir nada.
            """
            if posiciones is not None:
                posiciones = _rr_validar_posiciones("arma.agregar_balas()", "posiciones", posiciones, self.recamaras)
                ocupadas = [indice for indice in posiciones if self.camaras[indice]]
                if ocupadas:
                    raise Exception(
                        "arma.agregar_balas(): la(s) recamara(s) %r ya tenian bala cargada" % (ocupadas,)
                    )
                for indice in posiciones:
                    self.camaras[indice] = True
            else:
                vacias_totales = [indice for indice, cargada in enumerate(self.camaras) if not cargada]
                if cantidad > len(vacias_totales):
                    raise Exception(
                        "arma.agregar_balas(): no hay lugar para %d bala(s): "
                        "quedan %d recamara(s) vacia(s) de %d" % (cantidad, len(vacias_totales), self.recamaras)
                    )
                # No es al azar: arranca en la posicion ACTUAL del
                # puntero (la que va a leer el proximo disparar() si no
                # se vuelve a girar) y, si ya tiene bala, sigue
                # avanzando recamara por recamara (dando la vuelta al
                # tambor si hace falta) hasta encontrar tantas vacias
                # como "cantidad".
                elegidas = []
                indice = self.posicion
                for _ in range(self.recamaras):
                    if not self.camaras[indice]:
                        elegidas.append(indice)
                        if len(elegidas) == cantidad:
                            break
                    indice = (indice + 1) % self.recamaras
                for indice in elegidas:
                    self.camaras[indice] = True

            _rr_actualizar_debug(self)
            _rr_reproducir_y_esperar(RR_SONIDO_RECARGAR, "rr_recargar")

        def ocultar(self):
            """
            Saca el arma de la pantalla. El arma queda visible de forma
            persistente entre disparo y disparo (no se oculta sola
            despues de cada uno): llama a esto cuando la escena termine
            y quieras que desaparezca.
            """
            renpy.hide_screen("rr_arma")
            renpy.hide_screen("rr_debug")

        def disparar(
            self,
            apuntar_a="derecha",
            girar=None,
            imagen=None,
            sonido_disparo=None,
            sonido_vacio=None,
            duracion_apuntado=0.6,
        ):
            """
            Hace la secuencia de un disparo: gira el tambor si
            corresponde (sin animacion propia, ver girar()), apunta
            hacia "izquierda" o "derecha", y "aprieta el gatillo".
            Devuelve True si salio bala, False si fue un chasquido en
            vacio. Las consecuencias de la historia (que pasa despues
            del disparo) las maneja tu propio guion, leyendo el valor
            que devuelve. Si te interesa un flash rojo de pantalla
            completa para cuando alguien "recibe" el disparo, ver
            rr_hit(), mas abajo (es una funcion aparte: no se llama
            sola desde aca).

            Cada vez que el arma cambia de lado, ESPERA a que termine
            de moverse del todo (el giro hacia el lado nuevo mas el
            golpe del gatillo) antes de seguir. Si salio bala, despues
            de eso TAMBIEN espera al culatazo completo (el retroceso de
            verdad, mas fuerte que el golpe del gatillo) antes de
            devolver el control a tu guion.

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
                    particular (con el sonido y la espera de girar(),
                    ver mas arriba). Con None (por defecto), se usa
                    girar_siempre del arma. Pasando True o False acá se
                    lo pisa solo para este llamado puntual.

                imagen (str o None):
                    Ruta de imagen propia del arma (tiene que apuntar
                    hacia la derecha en su version original, sin
                    espejar). Con None usa RR_IMAGEN_POR_DEFECTO.

                sonido_disparo, sonido_vacio (str o None):
                    Rutas de sonido para el disparo con bala y el
                    chasquido en vacio, respectivamente. Con None (por
                    defecto), usa RR_SONIDO_DISPARO / RR_SONIDO_VACIO
                    (configurables al principio de este archivo). Pasa
                    una ruta propia para pisarlo solo en este llamado.

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
                self.girar()

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
            _rr_actualizar_debug(self)

            transformacion = rr_t_apuntar(self.lado_actual, apuntar_a, duracion_apuntado)
            _rr_mostrar_arma(imagen, transformacion)
            self.lado_actual = apuntar_a
            # Espera a que el arma termine de moverse del todo (el giro
            # hacia el lado nuevo MAS el golpe de retroceso) antes de
            # seguir con el sonido del disparo o devolver el control.
            renpy.pause(duracion_apuntado + RR_DURACION_GOLPE_RECORTE + RR_DURACION_GOLPE_VUELTA)

            sonido_disparo_final = RR_SONIDO_DISPARO if sonido_disparo is None else sonido_disparo
            sonido_vacio_final = RR_SONIDO_VACIO if sonido_vacio is None else sonido_vacio
            sonido = sonido_disparo_final if resultado else sonido_vacio_final

            if resultado:
                # Culatazo: solo cuando sale bala de verdad (un
                # chasquido en vacio no tiene retroceso). Reemplaza la
                # pose quieta por la animacion de retroceso, arrancando
                # exactamente desde donde quedo (mismo lado, sin salto).
                _rr_mostrar_arma(imagen, rr_t_retroceso(apuntar_a, RR_DURACION_RETROCESO_GOLPE, RR_DURACION_RETROCESO_VUELTA))
                if sonido:
                    renpy.play(sonido)
                # Espera a que el culatazo termine del todo antes de
                # devolver el control a tu guion.
                renpy.pause(RR_DURACION_RETROCESO_GOLPE + RR_DURACION_RETROCESO_VUELTA)
            elif sonido:
                renpy.play(sonido)
                renpy.pause(0.3)

            return resultado

    def arma(balas=1, recamaras=6, girar_siempre=False, posiciones_balas=None):
        """
        Crea y devuelve un arma nueva (un RR_Arma), lista para guardar
        en una variable de tu guion y usar con sus metodos girar() y
        disparar(). Guardala en una variable propia (por ejemplo
        "$ ar = arma(...)") para poder volver a usar la misma más
        adelante: como es un objeto de datos simple, viaja sola con el
        guardado/carga de tu partida.

        Parametros:
            balas (int): cuantas balas hay cargadas, de entrada,
                repartidas al azar entre las recamaras. No se usa si le
                pasas "posiciones_balas". Podes cargar mas balas
                despues con arma.agregar_balas(...).
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
            posiciones_balas (lista de int, o None):
                En vez de repartir "balas" al azar, elegi vos mismo en
                que recamaras exactas van cargadas (indices de 0 a
                recamaras-1). Por ejemplo, posiciones_balas=[0, 3] en
                un tambor de 6 dejaria las balas en la primera y la
                cuarta recamara, con el resto vacias. Si lo usas,
                "balas" se ignora (la cantidad cargada es la cantidad
                de posiciones que le pases). Pensado para cuando la
                historia necesita un resultado exacto y no al azar (por
                ejemplo, un truco o una trampa que hace un personaje).
        """
        return RR_Arma(balas=balas, recamaras=recamaras, girar_siempre=girar_siempre, posiciones_balas=posiciones_balas)

    def rr_hit(color=None, alpha_maximo=None, duracion_subida=None, duracion_bajada=None):
        """
        Flash de pantalla completa (por defecto, rojo): una pantalla de
        color que aparece de golpe y se desvanece. Pensado para marcar
        el momento en que alguien "recibe" el disparo (por ejemplo, el
        jugador se dispara a si mismo y pierde). El modulo NO lo llama
        solo en ningun momento: es una funcion aparte que vos llamas
        desde tu guion, en el momento exacto que decidas (por ejemplo,
        justo despues de un disparar() que devolvio True), asi que
        funciona igual de bien con o sin arma() (no depende de ninguna
        en particular).

        Esta funcion ESPERA a que el flash termine del todo (subida y
        bajada) antes de devolver el control a tu guion.

        Parametros (todos opcionales; con None usan las constantes
        configurables al principio de este archivo):
            color (str): color del flash, en formato "#RRGGBB". Por
                defecto RR_HIT_COLOR ("#FF0000", rojo).
            alpha_maximo (0.0 a 1.0): que tan opaco se pone el flash en
                su punto mas fuerte. Por defecto RR_HIT_ALPHA_MAXIMO.
            duracion_subida, duracion_bajada (segundos): cuanto tarda
                en aparecer y en desvanecerse. Por defecto
                RR_HIT_DURACION_SUBIDA / RR_HIT_DURACION_BAJADA.
        """
        color_final = RR_HIT_COLOR if color is None else color
        alpha_final = RR_HIT_ALPHA_MAXIMO if alpha_maximo is None else alpha_maximo
        subida_final = RR_HIT_DURACION_SUBIDA if duracion_subida is None else duracion_subida
        bajada_final = RR_HIT_DURACION_BAJADA if duracion_bajada is None else duracion_bajada

        renpy.show_screen("rr_flash", color=color_final, transformacion=rr_t_flash(subida_final, bajada_final, alpha_final))
        renpy.pause(subida_final + bajada_final)
        renpy.hide_screen("rr_flash")


# ============================================================================
#  ANIMACION (ATL puro)
# ----------------------------------------------------------------------------
#  rr_t_apuntar: espejado horizontal (NO una rotacion de 180, para que
#  no quede "boca abajo") hacia el lado indicado, y un pequeño golpe del
#  gatillo al final (se nota en CUALQUIER disparo, haya salido bala o
#  no). rr_t_retroceso: el culatazo de verdad, SOLO para cuando sale
#  bala (tira el arma hacia atras, en el sentido contrario a donde
#  apunta, y la levanta un poco). rr_t_flash: la usa rr_hit(), mas
#  arriba, para el flash de pantalla completa.
# ============================================================================
transform rr_t_apuntar(lado_inicial, lado, duracion=0.6):
    xalign 0.5 yalign 0.6
    xanchor 0.5 yanchor 0.5
    xzoom (-1.0 if lado_inicial == "izquierda" else 1.0)
    zoom 1.0
    linear duracion xzoom (-1.0 if lado == "izquierda" else 1.0)
    linear RR_DURACION_GOLPE_RECORTE zoom 0.92
    linear RR_DURACION_GOLPE_VUELTA zoom 1.0

transform rr_t_retroceso(lado, duracion_golpe=0.05, duracion_vuelta=0.25):
    xalign 0.5 yalign 0.6
    xanchor 0.5 yanchor 0.5
    xzoom (-1.0 if lado == "izquierda" else 1.0)
    xoffset 0
    yoffset 0
    zoom 1.0
    linear duracion_golpe xoffset (24 if lado == "izquierda" else -24) yoffset -14 zoom 1.06
    linear duracion_vuelta xoffset 0 yoffset 0 zoom 1.0

transform rr_t_flash(duracion_subida, duracion_bajada, alpha_maximo):
    alpha 0.0
    linear duracion_subida alpha alpha_maximo
    linear duracion_bajada alpha 0.0


# Pantalla interna que muestra el arma animandose. No se usa
# directamente: la maneja disparar(), mas arriba, llamando
# renpy.show_screen()/renpy.pause()/renpy.hide_screen() directamente
# desde Python (NO con la sentencia "call": renpy.call() corta la
# sentencia "$" que lo invoca y no puede devolver un valor a quien lo
# llamo, asi que no sirve para esto).
screen rr_arma(imagen, transformacion):
    add imagen at transformacion


# Cartel de RR_DEBUG (ver la seccion de configuracion, al principio del
# archivo): muestra el estado real del tambor. Se actualiza solo,
# porque el texto se vuelve a calcular en cada interaccion mientras la
# pantalla sigue mostrada. No se usa directamente: la muestran/ocultan
# _rr_actualizar_debug() y ocultar(), mas arriba.
screen rr_debug(arma_obj):
    zorder 100
    frame:
        xalign 0.0 yalign 0.0
        xpadding 10
        ypadding 6
        background "#000000AA"
        vbox:
            text "[[RR_DEBUG] tambor: [_rr_texto_debug(arma_obj)]" size 16 color "#6f6"
            text "[[RR_DEBUG] balas restantes: [arma_obj.balas_restantes()]" size 16 color "#6f6"


# Pantalla de flash de pantalla completa. No se usa directamente: la
# maneja rr_hit(), mas arriba.
screen rr_flash(color, transformacion):
    zorder 200
    add Solid(color) at transformacion
