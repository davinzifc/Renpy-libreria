# ============================================================================
#  MODULO: EFECTO MAQUINA DE ESCRIBIR (TEXTO LETRA POR LETRA)
#  Version: 1.1
#  Compatibilidad: Ren'Py 7.x / 8.x
#  Autor: davinzifc
#  Licencia: MIT. Copyright (c) 2026 davinzifc.
#            Puedes usar, copiar, modificar y redistribuir este archivo,
#            siempre que mantengas este aviso de copyright y la licencia
#            MIT (ver el archivo LICENSE del repositorio) en las copias.
#            Es decir: hay que dar crédito al desarrollador.
#
#  Para instrucciones de instalacion, ejemplos de uso dentro del guion y
#  mas detalles, abri el archivo "README.md" que viene junto a este
#  script, en esta misma carpeta.
# ============================================================================


# ============================================================================
#  CONFIGURACION — esto es lo UNICO que normalmente necesitas tocar
# ----------------------------------------------------------------------------
#  No hace falta saber programar para esta parte: cambia el valor que
#  esta despues del signo "=" en cada linea (dejando las comillas si las
#  tiene) y guarda el archivo.
# ============================================================================

# --- VELOCIDAD DEL TEXTO --------------------------------------------------
# Que tan rapido aparece el texto de los dialogos, letra por letra.
#   0      = el texto aparece todo de golpe (sin efecto de "escritura")
#   20-35  = velocidad comoda para leer (recomendado)
#   60     = muy rapido
define MME_VELOCIDAD_CPS = 25

# --- SONIDO DE TECLEO: ACTIVARLO, DESACTIVARLO O CAMBIARLO ---------------
# Sonido que se escucha mientras el texto va apareciendo, como si alguien
# estuviera tecleando en una maquina de escribir.
#   - Dejalo tal cual esta para usar el sonido de ejemplo ya incluido.
#   - Cambialo a None (sin comillas) para que no suene nada:
#         define MME_SONIDO_TECLEO = None
#   - O cambialo por la ruta a tu propio sonido (.mp3, .ogg o .wav),
#     copiado dentro de la carpeta "game/" de tu proyecto.
define MME_SONIDO_TECLEO = "modulos/efecto_maquina_de_escribir/audio/mme_tecleo.mp3"

# --- VOLUMEN DEL SONIDO DE TECLEO -----------------------------------------
# 0.0 = silencio, 1.0 = volumen normal (el maximo) del archivo de sonido.
# Bajalo si el sonido se escucha muy fuerte comparado con el resto del
# audio del juego.
define MME_SONIDO_TECLEO_VOLUMEN = 0.2

# --- ¿EL SONIDO ACOMPAÑA LA VELOCIDAD DEL TEXTO? --------------------------
#   True  = el sonido va mas rapido o mas lento segun la velocidad del
#           texto (MME_VELOCIDAD_CPS, arriba). Recomendado.
#   False = el sonido siempre suena al mismo ritmo fijo, sin importar la
#           velocidad del texto (ver MME_SONIDO_TECLEO_DURACION mas abajo).
define MME_SONIDO_TECLEO_SINCRONIZAR_CON_VELOCIDAD = True

# --- LIMITE DE VELOCIDAD DEL SONIDO (solo se usa si lo de arriba es True) -
# Por mas rapido que vaya el texto, el sonido nunca va a repetirse mas
# seguido que este numero (en segundos). Esto evita que, con velocidades
# de texto muy altas, el sonido se corte tanto que deje de escucharse. Si
# no estas seguro, dejalo como esta.
define MME_SONIDO_TECLEO_DURACION_MINIMA = 0.12

# --- RITMO FIJO DEL SONIDO (solo se usa si lo de arriba es False) --------
# Cuanto dura cada "clic" del sonido antes de repetirse, en segundos. Un
# numero mas chico = tecleo mas rapido. Ponelo en None para reproducir el
# sonido completo cada vez, sin recortarlo.
define MME_SONIDO_TECLEO_DURACION = 0.12


# ============================================================================
#  A PARTIR DE ACA: EL "MOTOR" DEL MODULO
# ----------------------------------------------------------------------------
#  No necesitas editar nada de lo que sigue para usar el modulo. Si no
#  sabes programar, es mejor que no lo toques.
# ============================================================================
init python:

    def mme_definir_velocidad(cps):
        """
        Cambia la velocidad de escritura (en caracteres por segundo) para
        todo el dialogo que se muestre a partir de este punto del guion.

        Parametros:
            cps (int): caracteres por segundo.
                0 = instantaneo (efecto desactivado)
                1 a 60 = velocidad tipica de dialogo (20-35 recomendado)
        """
        preferences.text_cps = cps

    # Aplica la velocidad configurada arriba como punto de partida del
    # juego. Se usa una asignacion directa (no "default") para que este
    # modulo funcione sin importar lo que ya tenga definido options.rpy
    # en el proyecto donde se copie.
    preferences.text_cps = MME_VELOCIDAD_CPS

    # Canal de audio propio para el sonido de tecleo, separado del canal
    # "sound" general, para que no interrumpa (ni sea interrumpido por)
    # otros efectos de sonido del juego. Usa el mixer "sound" para que el
    # jugador lo controle con el control deslizante "Sonido" de siempre.
    renpy.music.register_channel("mme_teclado", mixer="sound", loop=False, tight=True)

    # "config.character_callback" es UNA sola funcion (no una lista). Si el
    # proyecto donde se copia este modulo ya tenia una propia configurada,
    # la guardamos para seguir llamandola y no romper lo que ya existia.
    _mme_callback_previo = config.character_callback

    # Ren'Py no ofrece un evento por cada letra individual, asi que este
    # sonido se reproduce en bucle (loop) mientras el texto se esta
    # "escribiendo" y se corta apenas termina de aparecer (o el jugador lo
    # salta con un clic). Con un sonido corto de una sola tecla, el bucle
    # suena como un traqueteo continuo.
    def mme_sonido_de_tecleo(event, **kwargs):
        """
        "show" marca el instante en que aparece el cuadro de dialogo
        (arranca el bucle); "slow_done" marca cuando termina la animacion
        letra por letra (corta el bucle); "end" es un respaldo por si
        "slow_done" no llega a dispararse (por ejemplo con el texto
        instantaneo o en modo "saltar"). Si MME_SONIDO_TECLEO esta en None,
        no hace nada.
        """
        if _mme_callback_previo is not None:
            _mme_callback_previo(event, **kwargs)

        if not MME_SONIDO_TECLEO:
            return

        # "interact" viene en False en casos donde el dialogo no genera una
        # interaccion real (por ejemplo durante un rollback); en esos casos
        # no queremos reproducir sonido.
        if not kwargs.get("interact", True):
            return

        if event == "show" and preferences.text_cps != 0:
            renpy.sound.set_volume(MME_SONIDO_TECLEO_VOLUMEN, channel="mme_teclado")

            if MME_SONIDO_TECLEO_SINCRONIZAR_CON_VELOCIDAD:
                _mme_duracion = max(1.0 / preferences.text_cps, MME_SONIDO_TECLEO_DURACION_MINIMA)
            else:
                _mme_duracion = MME_SONIDO_TECLEO_DURACION

            _mme_sonido = MME_SONIDO_TECLEO
            if _mme_duracion:
                _mme_sonido = "<from 0 to %s>%s" % (_mme_duracion, MME_SONIDO_TECLEO)

            renpy.sound.play(_mme_sonido, channel="mme_teclado", loop=True)
        elif event in ("slow_done", "end"):
            renpy.sound.stop(channel="mme_teclado")

    # Se registra como el callback global de personaje para que el sonido
    # suene en TODOS los dialogos, sin tener que modificar cada Character()
    # del proyecto donde se copie este modulo.
    config.character_callback = mme_sonido_de_tecleo
