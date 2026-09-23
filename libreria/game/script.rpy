# script.rpy — handler de entrada del proyecto.
# No contiene demostraciones: solo un menu que llama a la vista de
# ejemplo de cada modulo, guardada en game/vistas/. Los modulos en si
# (game/modulos/) no se tocan desde aca.

define e = Character("Eileen")


label start:

    jump menu_principal


label menu_principal:

    scene bg room
    show eileen happy

    menu:
        "Elegi que modulo queres ver en accion."

        "Gestor de particulas (nieve, lluvia, luciernagas...)":
            call ejemplo_gestor_particulas
            jump menu_principal

        "Efecto maquina de escribir (texto letra por letra)":
            call ejemplo_efecto_maquina_de_escribir
            jump menu_principal

        "Ruleta rusa (arma que gira, apunta y dispara)":
            call ejemplo_ruleta_rusa
            jump menu_principal

        "Salir":
            return
