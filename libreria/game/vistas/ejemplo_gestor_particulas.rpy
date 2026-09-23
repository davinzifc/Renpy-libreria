# Ejemplo de uso del modulo "gestor_particulas" (game/modulos/gestor_particulas/).
# Todos los efectos se arman "a mano" con parametros con nombre, sin
# prefabs ni atajos: solo se escribe lo que se quiere cambiar y el resto
# queda con su valor por defecto.
#
# Este archivo vive en game/vistas/ y NO es parte del modulo: es solo
# una demostracion a la que se llega desde el menu de script.rpy.

label ejemplo_gestor_particulas:

    scene bg room

    show eileen happy

    e "Tour de particulas: todo se arma solo con parametros."

    # ------------------------------------------------------------------
    # 1) NIEVE: cae en diagonal suave, con vaiven lateral tipo viento.
    # ------------------------------------------------------------------
    $ id_efecto = gp_crear_particulas(
        color="#FFFFFF",
        tamano_min=3, tamano_max=8,
        cantidad=150,
        angulo_base=90, angulo_variacion=20,
        velocidad_min=30, velocidad_max=80,
        ondulado=True, amplitud_ondulado=25, frecuencia_ondulado=0.6,
        opacidad_min=0.5, opacidad_max=1.0,
    )

    e "Primero, nieve: caida lenta con vaiven lateral."

    $ gp_terminar_particulas(id_efecto)

    # ------------------------------------------------------------------
    # 2) LLUVIA: rayitas rapidas y casi rectas.
    # ------------------------------------------------------------------
    $ id_efecto = gp_crear_particulas(
        color="#9FC6FF",
        forma="rectangulo",
        tamano_min=14, tamano_max=26,
        ancho_min=1, ancho_max=2,
        cantidad=140,
        angulo_base=100, angulo_variacion=4,
        velocidad_min=650, velocidad_max=950,
        opacidad_min=0.35, opacidad_max=0.7,
    )

    e "Ahora lluvia: rectangulos finos, rapidos y un poco inclinados."

    $ gp_terminar_particulas(id_efecto)

    # ------------------------------------------------------------------
    # 3) LUCIERNAGAS: vagan por toda la pantalla, se prenden y se apagan
    #    suavemente (fade in / fade out) y viven pocos segundos.
    #    Ahora con IMAGEN: luz.png es un circulo con brillo suave (centro
    #    intenso y halo que se desvanece), sin bordes pixelados. Es
    #    blanca y se tine de tres tonos de luciernaga.
    # ------------------------------------------------------------------
    $ luz_png = "modulos/gestor_particulas/imagenes/luz.png"
    $ luces_luciernaga = [
        im.MatrixColor(luz_png, im.matrix.colorize(tono, tono))
        for tono in ("#F5FF7A", "#CFFF5E", "#FFF1A8")
    ]

    $ id_efecto = gp_crear_particulas(
        imagenes=luces_luciernaga,
        tamano_min=22, tamano_max=42,
        cantidad=30,
        movimiento="aleatorio", vagar_giro=50,
        angulo_variacion=180,
        velocidad_min=15, velocidad_max=40,
        opacidad_min=0.7, opacidad_max=1.0,
        tiempo_vida_min=2, tiempo_vida_max=4,
        fade_in=0.5, fade_out=0.5,
    )

    e "Luciernagas: andan al azar por toda la pantalla y se prenden y apagan suave."

    $ gp_terminar_particulas(id_efecto)

    # ------------------------------------------------------------------
    # 4) ALGO LOCO: dos efectos a la vez, ambos solo con parametros.
    #    - Pelotas de neon multicolor que rebotan rapido por toda la
    #      pantalla (movimiento aleatorio casi recto = rebote tipo DVD),
    #      de tamanos muy distintos y con fade.
    #    - Burbujas que suben ondulando, aparecen y desaparecen solas.
    # ------------------------------------------------------------------
    $ id_pelotas = gp_crear_particulas(
        color=["#FF2E93", "#00F0FF", "#B6FF00", "#FFB300", "#9D4DFF"],
        tamano_min=10, tamano_max=45,
        cantidad=18,
        movimiento="aleatorio", vagar_giro=8,
        angulo_variacion=180,
        velocidad_min=180, velocidad_max=420,
        opacidad_min=0.5, opacidad_max=0.95,
        tiempo_vida_min=6, tiempo_vida_max=12,
        fade_in=0.8, fade_out=2.0,
    )

    $ id_burbujas = gp_crear_particulas(
        color=["#BDEBFF", "#FFFFFF"],
        tamano_min=6, tamano_max=22,
        cantidad=40,
        angulo_base=270, angulo_variacion=12,
        velocidad_min=40, velocidad_max=110,
        ondulado=True, amplitud_ondulado=35, frecuencia_ondulado=0.8,
        opacidad_min=0.25, opacidad_max=0.7,
        tiempo_vida_min=3, tiempo_vida_max=7,
        fade_in=1.0, fade_out=1.5,
        origen="abajo",
    )

    e "Y para cerrar, algo loco: pelotas de neon rebotando y burbujas que suben, todo a la vez."

    $ gp_terminar_todas()

    # ------------------------------------------------------------------
    # 5) PARTICULA CON IMAGEN: copos de nieve dibujados (PNG), que giran
    #    mientras caen. La imagen esta en
    #    game/imagenes/copo.png (Snowflake 01,
    #    de Wikimedia Commons, dominio publico). Viene en negro, asi que
    #    se tine de celeste claro con im.MatrixColor: "imagenes" acepta
    #    tanto rutas como displayables ya armados.
    # ------------------------------------------------------------------
    $ copo_celeste = im.MatrixColor(
        "imagenes/copo.png",
        im.matrix.colorize("#DDF0FF", "#DDF0FF"),
    )

    $ id_efecto = gp_crear_particulas(
        imagenes=[copo_celeste],
        tamano_min=14, tamano_max=40,
        cantidad=50,
        angulo_base=90, angulo_variacion=25,
        velocidad_min=40, velocidad_max=100,
        ondulado=True, amplitud_ondulado=30, frecuencia_ondulado=0.5,
        rotar=True, rotacion_velocidad_min=-90, rotacion_velocidad_max=90,
        opacidad_min=0.6, opacidad_max=1.0,
    )

    e "Y esto es una particula con imagen: copos dibujados que giran mientras caen."

    $ gp_terminar_particulas(id_efecto)

    # ------------------------------------------------------------------
    # 6) TORMENTA DE ARENA: cuatro capas superpuestas, todas con
    #    parametros. Cada capa devuelve su propio id y se apaga junto
    #    con las demas usando gp_terminar_todas().
    # ------------------------------------------------------------------

    # Las imagenes (polvo1-3.png y rafaga.png, en
    # game/imagenes/) son blancas con bordes
    # suaves: se tinen de arena aca con im.MatrixColor, y de cada nube
    # se hacen dos tonos para que no se vean todas iguales.
    $ dir_img = "imagenes/"
    $ tono_claro = im.matrix.colorize("#D8B980", "#D8B980")
    $ tono_oscuro = im.matrix.colorize("#B8925A", "#B8925A")
    $ nubes_polvo = [
        im.MatrixColor(dir_img + nombre, tono)
        for nombre in ("polvo1.png", "polvo2.png", "polvo3.png")
        for tono in (tono_claro, tono_oscuro)
    ]
    $ rafaga_arena = im.MatrixColor(dir_img + "rafaga.png", im.matrix.colorize("#F5E3BE", "#F5E3BE"))

    # Capa 1 - neblina de polvo: nubes de polvo de borde suave (imagen),
    # enormes y lentas, que se prenden y se apagan (fade) y dan el
    # "cuerpo" de la tormenta. Giran muy despacio para no verse repetidas.
    $ id_neblina = gp_crear_particulas(
        imagenes=nubes_polvo,
        tamano_min=250, tamano_max=520,
        cantidad=12,
        angulo_base=0, angulo_variacion=8,
        velocidad_min=90, velocidad_max=180,
        ondulado=True, amplitud_ondulado=40, frecuencia_ondulado=0.3,
        rotar=True, rotacion_velocidad_min=-6, rotacion_velocidad_max=6,
        opacidad_min=0.15, opacidad_max=0.4,
        tiempo_vida_min=6, tiempo_vida_max=11,
        fade_in=2.5, fade_out=2.5,
        origen="izquierda",
    )

    # Capa 2 - granos de arena: cientos de puntitos rapidos con
    # turbulencia (ondulado corto y rapido = el viento los sacude).
    $ id_granos = gp_crear_particulas(
        color=["#E2C08A", "#C9A66B", "#F0D9A8", "#A8824A"],
        tamano_min=1, tamano_max=4,
        cantidad=320,
        angulo_base=8, angulo_variacion=14,
        velocidad_min=500, velocidad_max=1000,
        ondulado=True, amplitud_ondulado=14, frecuencia_ondulado=2.2,
        opacidad_min=0.35, opacidad_max=0.95,
    )

    # Capa 3 - rafagas de viento: estelas horizontales de puntas
    # difuminadas (imagen), las mas rapidas de todas. "tamano" es el
    # largo de la estela; el grosor sale proporcional.
    $ id_rafagas = gp_crear_particulas(
        imagenes=[rafaga_arena],
        tamano_min=80, tamano_max=320,
        cantidad=22,
        angulo_base=3, angulo_variacion=4,
        velocidad_min=1100, velocidad_max=1700,
        opacidad_min=0.2, opacidad_max=0.5,
        tiempo_vida_min=1.5, tiempo_vida_max=3,
        fade_in=0.4, fade_out=0.6,
        origen="izquierda",
    )

    # Capa 4 - remolinos: granos que NO siguen el viento sino que
    # vagan con giros bruscos por toda la pantalla, como arena
    # arremolinada. Aparecen y desaparecen con fade.
    $ id_remolinos = gp_crear_particulas(
        color=["#D8B980", "#B8925A"],
        tamano_min=2, tamano_max=5,
        cantidad=70,
        movimiento="aleatorio", vagar_giro=220,
        angulo_variacion=180,
        velocidad_min=120, velocidad_max=320,
        opacidad_min=0.3, opacidad_max=0.8,
        tiempo_vida_min=1.5, tiempo_vida_max=4,
        fade_in=0.5, fade_out=0.8,
    )

    e "Y la prueba dificil: una tormenta de arena, con cuatro capas a la vez."

    $ gp_terminar_todas()

    e "Todo eso salio solo de parametros. Fin del tour."

    return
