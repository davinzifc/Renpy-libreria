# Ruleta Rusa (arma que gira, apunta y dispara, en 2D)

Módulo "copiar y pegar" para proyectos de **Ren'Py**. Agrega un arma con
un tambor de varias recámaras (algunas cargadas con bala) que podés
hacer girar y disparar apuntando hacia el jugador o hacia un NPC, con
animación incluida.

**Importante: esto no usa modelos ni renderizado 3D.** El arma es una
sola imagen 2D que se anima con espejado horizontal (ATL) para apuntar
hacia un lado u otro, como cualquier otro displayable de Ren'Py. Girar
el tambor es un cambio de estado interno, sin ninguna animación
propia. No hace falta saber nada de 3D ni instalar nada extra para
usarlo.

## Qué hay en esta carpeta

```
ruleta_rusa/
├── modulo_ruleta_rusa.rpy   <- el módulo en sí (motor + animación)
├── imagenes/
│   └── arma.png             <- ilustración de revólver de ejemplo
└── README.md                <- este archivo
```

La imagen `arma.png` es un ejemplo listo para probar el módulo sin
necesitar arte propio. Podés reemplazarla por tu propia imagen (ver
"Usar tu propia imagen de arma", más abajo).

**Crédito de la imagen `arma.png`:** ilustración de [Vecteezy.com](https://www.vecteezy.com/),
espejada horizontalmente y reducida de tamaño para usarse como sprite.
Si distribuís tu juego con esta imagen de ejemplo tal cual (sin
reemplazarla por la tuya propia), revisá los términos de la licencia
de Vecteezy para tu caso de uso y mantené este crédito.

## Cómo instalarlo

1. Copiá **toda esta carpeta** (`ruleta_rusa`, con todo lo que tiene
   adentro) dentro de la carpeta `game/modulos/` de tu proyecto de
   Ren'Py. Si tu proyecto no tiene una carpeta `game/modulos/`, creala
   vos mismo y pegá la carpeta del módulo ahí adentro.

   Al final te tiene que quedar así:

   ```
   tu_proyecto/
   └── game/
       └── modulos/
           └── ruleta_rusa/
               ├── modulo_ruleta_rusa.rpy
               ├── imagenes/
               │   └── arma.png
               └── README.md
   ```

2. No hace falta tocar ningún otro archivo del proyecto: Ren'Py carga
   automáticamente todos los archivos `.rpy` que encuentra, sin
   importar en qué subcarpeta estén.

## Uso básico dentro del guión (`script.rpy`)

El módulo agrega una función `arma(...)` que crea un arma nueva. Guardá
lo que te devuelve en una variable propia: como es un objeto de datos
simple (no guarda ninguna pantalla ni imagen "viva" adentro), **viaja
solo con el guardado y la carga de tu partida** — si la historia se
interrumpe a mitad de una ronda y volvés más adelante (incluso cargando
una partida guardada), el arma sigue teniendo las mismas balas y la
misma posición de tambor que cuando la dejaste.

**Crear el arma, con una bala en un tambor de 6:**

```renpy
$ ar = arma(balas=1, recamaras=6)
```

**Disparar, apuntando a la izquierda (por ejemplo, al NPC) o a la
derecha (por ejemplo, al jugador):**

```renpy
label duelo_ruleta_rusa:
    scene bg bar
    show npc normal at left
    show eileen normal at right

    npc "Tu turno primero."
    $ murio_npc = ar.disparar(apuntar_a="izquierda")

    if murio_npc:
        "El disparo resuena en la sala. El NPC cae."
        jump fin_duelo_gano_jugador

    "Click. Nada. Te toca a vos."
    $ murio_jugador = ar.disparar(apuntar_a="derecha")

    if murio_jugador:
        "..."
        jump fin_duelo_gano_npc

    "Otro chasquido en vacío. Seguís con vida, por ahora."
    jump duelo_ruleta_rusa
```

(`fin_duelo_gano_jugador` y `fin_duelo_gano_npc` son las escenas donde
termina el duelo: ahí es donde tenés que llamar a `ar.ocultar()`, ver
más abajo.)

Fijate que **vos decidís qué pasa después de cada disparo** (diálogo,
si alguien "pierde", saltar a otra escena): el módulo solo resuelve la
animación y si salió bala o no.

**El arma queda visible en pantalla entre disparo y disparo:** no se
oculta sola después de cada uno, para que se vea como un elemento fijo
de la escena mientras dura el duelo (y no "parpadeando" cada vez que
alguien tira del gatillo). Llamá a `ar.ocultar()` cuando decidas que la
escena terminó y quieras sacarla de pantalla.

**Dejar que el jugador elija volver a girar el tambor antes de
disparar** (sin que eso cuente como un disparo):

```renpy
menu:
    "¿Querés girar el tambor de nuevo antes de arriesgarte?"

    "Sí, girar":
        $ ar.girar()

    "No, disparar así como está":
        pass

$ murio_jugador = ar.disparar(apuntar_a="derecha")
```

## Cómo funciona la probabilidad

El tambor es, por dentro, un array fijo de recámaras (`[False, True,
False, False, False, False]`, por ejemplo): cada posición dice si esa
recámara tiene bala o no. **Girar el tambor no reparte las balas de
nuevo:** las balas se quedan donde están: girar solo elige al azar
**desde qué recámara arranca el puntero** que se va a ir moviendo con
cada disparo — exactamente como girar el tambor de un revólver real, en
vez de barajar las balas de nuevo cada vez.

Al crear el arma con `arma(balas=..., recamaras=...)`, elegís también
**cómo se comporta el tambor entre disparos** con `girar_siempre`:

```renpy
$ ar = arma(balas=1, recamaras=6, girar_siempre=False)   # por defecto
```

- **`girar_siempre=False`** (por defecto — la ruleta rusa "clásica" de
  las películas): el puntero avanza una recámara por disparo, sin
  volver a girar. La probabilidad del próximo disparo depende de lo que
  ya salió antes (si nadie murió en 5 disparos con 1 bala en 6
  recámaras, el sexto disparo es 100% seguro que sale la bala).
- **`girar_siempre=True`**: cada `disparar()` gira el tambor (puntero a
  una recámara al azar) antes de disparar. La probabilidad de ESE
  disparo es `balas_restantes() / recamaras` en ese momento, sin
  depender de qué recámara tocó la vez anterior.

En los dos modos, una vez que una recámara dispara, esa bala queda
**gastada**: no vuelve a disparar sola si el puntero (girando o no)
vuelve a pasar por ahí, igual que un cartucho real ya percutido. Como
las balas no se reponen solas, si nunca agregás más municion el arma
en algún momento se queda sin balas para siempre (`balas_restantes()`
llega a 0) — usá `ar.agregar_balas(...)` para cargarle más balas a
mitad de partida (ver más abajo).

En cualquiera de los dos modos, podés forzar un giro puntual:

- `ar.girar()` — gira el tambor a mano, en cualquier momento, sin
  disparar.
- `ar.disparar(apuntar_a=..., girar=True)` — gira justo antes de este
  disparo en particular, sin importar el modo del arma.
- `ar.disparar(apuntar_a=..., girar=False)` — fuerza que este disparo
  puntual NO gire, aunque el arma tenga `girar_siempre=True`.

**Agregar balas a mitad de partida**, sin tocar las que ya había (por
ejemplo, un giro más peligroso de la historia: de una bala pasa a
tener dos, en recámaras distintas elegidas al azar):

```renpy
$ ar.agregar_balas(1)
```

Tira una excepción si no quedan recámaras vacías suficientes para esa
cantidad.

## Parámetros de `arma(...)`

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `balas` | `1` | Cuántas balas hay cargadas al crear el arma, repartidas al azar entre las recámaras. |
| `recamaras` | `6` | Cuántas recámaras tiene el tambor. `balas` no puede ser mayor que `recamaras`. |
| `girar_siempre` | `False` | Si el tambor gira (puntero a una recámara al azar) antes de cada disparo (ver "Cómo funciona la probabilidad"). |

## Parámetros de `ar.disparar(...)`

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `apuntar_a` | — (obligatorio) | `"izquierda"` o `"derecha"`: hacia dónde apunta el arma. |
| `girar` | `None` | `None` usa `girar_siempre` del arma; `True`/`False` lo pisa solo para este disparo. |
| `imagen` | `None` | Ruta de imagen propia del arma. Con `None` usa la de ejemplo (`arma.png`). |
| `sonido_disparo` / `sonido_vacio` | `None` | Rutas de sonido para el disparo con bala / el chasquido en vacío. Sin sonido por defecto. |
| `duracion_apuntado` | `0.35` | Segundos que tarda en girar (como imagen) hacia el lado indicado. |

`ar.girar()` no tiene parámetros ni animación: es un cambio de estado
interno (a qué recámara apunta el puntero), sin ningún efecto en
pantalla. No hace falta llamarlo antes de `disparar()` — solo sirve
para el caso de "el jugador elige volver a girar antes de arriesgarse"
(ver más arriba).

`ar.balas_restantes()` devuelve cuántas balas sin disparar quedan en el
tambor actual, por si querés mostrarlo en pantalla (por ejemplo, en una
barra de "tensión").

`ar.agregar_balas(cantidad=1)` carga esa cantidad de balas nuevas en
recámaras vacías elegidas al azar, sin tocar las que ya había ni la
posición del puntero (ver "Cómo funciona la probabilidad").

`ar.ocultar()` saca el arma de pantalla. Llamalo cuando la escena
termine (el arma no se oculta sola entre disparos, ver más arriba).

## Usar tu propia imagen de arma

1. Dibujá o conseguí tu propia imagen de arma, **apuntando hacia la
   derecha** en su versión original (el módulo la espeja
   automáticamente para apuntar a la izquierda: no hace falta que
   dibujes las dos versiones).
2. Copiala dentro de la carpeta `game/` de tu proyecto (por ejemplo
   `game/imagenes/mi_arma.png`), fuera de la carpeta del módulo.
3. Pasala con el parámetro `imagen`:

   ```renpy
   $ murio = ar.disparar(apuntar_a="izquierda", imagen="imagenes/mi_arma.png")
   ```

   Si siempre vas a usar la misma imagen propia, es más cómodo definir
   tu propia constante al lado de tu `script.rpy` (no dentro del
   módulo) y pasarla siempre:

   ```renpy
   define MI_ARMA = "imagenes/mi_arma.png"
   ...
   $ murio = ar.disparar(apuntar_a="izquierda", imagen=MI_ARMA)
   ```

## Por qué no usa 3D

Ren'Py no tiene soporte nativo para renderizar modelos 3D (archivos
`.obj` ni similares): es un motor pensado para escenas 2D. El apuntado
se resuelve con una imagen 2D animada por ATL (espejado horizontal), y
girar el tambor es puro cambio de estado (sin animación), sin salir
del pipeline estándar de Ren'Py, sin depender de librerías externas ni
de OpenGL a mano, y compatible con cualquier plataforma donde corra
Ren'Py.

## Compatibilidad y licencia

- Compatible con Ren'Py 7.x y 8.x.
- Licencia **MIT**, Copyright (c) 2026 davinzifc. Podés usar, copiar,
  modificar y redistribuir este módulo, incluso en juegos comerciales,
  **siempre que des crédito al desarrollador**: mantené el aviso de
  copyright y la licencia (ya están en el encabezado del archivo
  `.rpy`) en todas las copias o partes sustanciales que distribuyas,
  por ejemplo en la carpeta de créditos de tu juego. El texto completo
  está en el archivo `LICENSE` de la raíz del repositorio.
