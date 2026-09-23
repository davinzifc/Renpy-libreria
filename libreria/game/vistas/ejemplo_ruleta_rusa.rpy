# Ejemplo de uso del modulo "ruleta_rusa" (game/modulos/ruleta_rusa/).
# Arma un tambor de 6 con la bala en una recamara elegida a mano (con
# posiciones_balas, en vez de al azar), sin re-girar entre disparos (la
# ruleta rusa "clasica"), y alterna turnos entre un desconocido (narrado,
# sin sprite propio) y el jugador, usando ar.disparar(). En el turno del
# jugador, un menu deja elegir entre gatillar así como esta, girar el
# tambor primero y despues gatillar, o agregar una bala antes de decidir.
#
# Este archivo vive en game/vistas/ y NO es parte del modulo: es solo
# una demostracion a la que se llega desde el menu de script.rpy.

label ejemplo_ruleta_rusa:

    scene bg room
    show eileen happy

    e "Che, alguien menciono una ruleta rusa... vamos a probarla (tranquilo, es solo una demo)."

    # RR_DEBUG es del propio modulo (ver la seccion de configuracion en
    # modulo_ruleta_rusa.rpy): con True, muestra un cartel con el estado
    # real del tambor. Lo prendemos aca solo para esta demo.
    $ RR_DEBUG = True

    # posiciones_balas=[2] carga la bala a mano en la recamara de indice
    # 2 (la tercera), en vez de repartirla al azar con "balas".
    $ ar = arma(recamaras=6, girar_siempre=False, posiciones_balas=[2])

    e "Un tambor de seis, con la bala puesta a mano en una recamara fija, sin volver a mezclar entre disparo y disparo."

label ejemplo_ruleta_rusa_ronda:

    "El desconocido de la otra punta de la mesa toma el arma primero."
    $ murio_npc = ar.disparar(apuntar_a="izquierda")

    if murio_npc:
        e "..."
        "El arma dispara. Fin de la partida para el desconocido."
        jump ejemplo_ruleta_rusa_fin

    "Click. Nada. Ahora te toca a vos."
    call ejemplo_ruleta_rusa_turno_jugador
    $ murio_jugador = _return

    if murio_jugador:
        $ rr_hit()
        e "..."
        "Esta vez la bala estaba de tu lado."
        jump ejemplo_ruleta_rusa_fin

    $ restantes = ar.balas_restantes()
    e "Otro chasquido en vacio. [restantes] bala en el tambor, seguimos."
    jump ejemplo_ruleta_rusa_ronda

label ejemplo_ruleta_rusa_turno_jugador:

    $ restantes = ar.balas_restantes()

    menu:
        "Te toca a vos. Quedan [restantes] bala(s) en el tambor. ¿Qué hacés?"

        "Gatillar así como está":
            $ murio = ar.disparar(apuntar_a="derecha")
            return murio

        "Girar el tambor y después gatillar":
            $ ar.girar()
            $ murio = ar.disparar(apuntar_a="derecha")
            return murio

        "Agregar una bala y girar el tambor":
            if ar.balas_restantes() >= ar.recamaras:
                e "El tambor ya está lleno, no hay lugar para más balas."
                jump ejemplo_ruleta_rusa_turno_jugador
            $ ar.agregar_balas(1)
            e "Una bala más en el tambor. Ahora a girar y gatillar."
            $ ar.girar()
            $ murio = ar.disparar(apuntar_a="derecha")
            return murio

label ejemplo_ruleta_rusa_fin:

    e "Eso es todo: la animacion y la probabilidad las resuelve el modulo, vos decidis que pasa despues de cada disparo."

    $ ar.ocultar()

    return
