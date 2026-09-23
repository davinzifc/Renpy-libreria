# Ejemplo de uso del modulo "efecto_maquina_de_escribir"
# (game/modulos/efecto_maquina_de_escribir/).
# El efecto letra por letra ya queda activo solo, para todos los
# dialogos, apenas se copia el modulo. Este ejemplo muestra ademas los
# tres puntos de control que ofrece: velocidad por personaje, velocidad
# puntual con {cps=...} y el cambio de velocidad global en tiempo real
# con mme_definir_velocidad().
#
# Este archivo vive en game/vistas/ y NO es parte del modulo: es solo
# una demostracion a la que se llega desde el menu de script.rpy.

define ej_mme_narrador = Character("Narrador", cps=40)

label ejemplo_efecto_maquina_de_escribir:

    scene bg room

    show eileen happy

    e "Esto ya se escribe solo, letra por letra, con la velocidad por defecto del modulo."

    # ------------------------------------------------------------------
    # 1) VELOCIDAD POR PERSONAJE: un Character con su propio "cps".
    # ------------------------------------------------------------------
    ej_mme_narrador "Y yo soy un personaje aparte, definido con cps=40: escribo mas rapido que Eileen."

    # ------------------------------------------------------------------
    # 2) VELOCIDAD PUNTUAL con la etiqueta {cps=...} dentro del texto.
    # ------------------------------------------------------------------
    e "Esto se lee normal, pero {cps=5}esto se escribe muy despacio{/cps} y esto vuelve a la velocidad normal."

    # ------------------------------------------------------------------
    # 3) VELOCIDAD GLOBAL en tiempo real con mme_definir_velocidad().
    # ------------------------------------------------------------------
    $ mme_definir_velocidad(5)

    e "Esto... se... escribe... despacio... para todo lo que sigue, no solo esta linea."

    $ mme_definir_velocidad(0)

    e "Y esto aparece todo de golpe, con cps en cero."

    $ mme_definir_velocidad(MME_VELOCIDAD_CPS)

    e "Y esto vuelve a la velocidad normal configurada en el modulo. Fin del ejemplo."

    return
