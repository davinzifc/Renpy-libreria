# Ejemplo de uso del modulo "ruleta_rusa" (game/modulos/ruleta_rusa/).
# Arma un tambor de 6 con una sola bala, sin re-girar entre disparos (la
# ruleta rusa "clasica"), y alterna turnos entre un desconocido (narrado,
# sin sprite propio) y el jugador, usando ar.disparar().
#
# Este archivo vive en game/vistas/ y NO es parte del modulo: es solo
# una demostracion a la que se llega desde el menu de script.rpy.

label ejemplo_ruleta_rusa:

    scene bg room
    show eileen happy

    e "Che, alguien menciono una ruleta rusa... vamos a probarla (tranquilo, es solo una demo)."

    $ ar = arma(balas=1, recamaras=6, girar_siempre=False)

    e "Un tambor de seis, una sola bala, sin volver a mezclar entre disparo y disparo."

label ejemplo_ruleta_rusa_ronda:

    "El desconocido de la otra punta de la mesa toma el arma primero."
    $ murio_npc = ar.disparar(apuntar_a="izquierda")

    if murio_npc:
        e "..."
        "El arma dispara. Fin de la partida para el desconocido."
        jump ejemplo_ruleta_rusa_fin

    "Click. Nada. Ahora te toca a vos."
    $ murio_jugador = ar.disparar(apuntar_a="derecha")

    if murio_jugador:
        e "..."
        "Esta vez la bala estaba de tu lado."
        jump ejemplo_ruleta_rusa_fin

    $ restantes = ar.balas_restantes()
    e "Otro chasquido en vacio. [restantes] bala en el tambor, seguimos."
    jump ejemplo_ruleta_rusa_ronda

label ejemplo_ruleta_rusa_fin:

    e "Eso es todo: la animacion y la probabilidad las resuelve el modulo, vos decidis que pasa despues de cada disparo."

    $ ar.ocultar()

    return
