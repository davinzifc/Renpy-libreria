# Ruleta Rusa (arma que gira, apunta y dispara)

Módulo "copiar y pegar" para proyectos de **Ren'Py**. Agrega un arma con
un tambor de varias recámaras (algunas cargadas con bala) que podés
hacer girar y disparar apuntando hacia el jugador o hacia un NPC, con
animación incluida.

El arma es una sola imagen que se anima con espejado horizontal (ATL)
para apuntar hacia un lado u otro, como cualquier otro displayable de
Ren'Py. Girar el tambor es un cambio de estado interno, sin ninguna
animación propia. No hace falta instalar nada extra para usarlo.

## Qué hay en esta carpeta

```
ruleta_rusa/
├── modulo_ruleta_rusa.rpy   <- el módulo en sí (motor + animación)
├── imagenes/
│   └── arma.png             <- ilustración de revólver de ejemplo
├── audio/
│   ├── rr_vacio.mp3         <- chasquido de recámara vacía de ejemplo
│   ├── rr_disparo.mp3       <- disparo con bala de ejemplo
│   ├── rr_girar.mp3         <- sonido de girar el tambor de ejemplo
│   └── rr_recargar.mp3      <- sonido de cargar balas de ejemplo
└── README.md                <- este archivo
```

La imagen `arma.png` y los sonidos `rr_vacio.mp3`/`rr_disparo.mp3`/
`rr_girar.mp3`/`rr_recargar.mp3` son un ejemplo listo para probar el
módulo sin necesitar arte ni audio propio. Podés reemplazarlos por los
tuyos (ver "Usar tu propia imagen de arma" y la sección de
configuración al principio de `modulo_ruleta_rusa.rpy`,
respectivamente).

**Crédito de la imagen `arma.png`:** ilustración de [Vecteezy.com](https://www.vecteezy.com/),
espejada horizontalmente y reducida de tamaño para usarse como sprite.

**Crédito de los sonidos `rr_vacio.mp3`, `rr_disparo.mp3`,
`rr_girar.mp3` y `rr_recargar.mp3`:** efectos de sonido de la
comunidad de [Freesound](https://freesound.org/). Si distribuís
vuestro juego con estos archivos de ejemplo tal cual (sin
reemplazarlos por los propios), revisá los términos de licencia de
cada fuente para su caso de uso y mantengan el crédito correspondiente.

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
               ├── audio/
               │   ├── rr_vacio.mp3
               │   ├── rr_disparo.mp3
               │   ├── rr_girar.mp3
               │   └── rr_recargar.mp3
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
tener dos):

```renpy
$ ar.agregar_balas(1)
```

**No es al azar:** la bala nueva va a la recámara donde está el
puntero *ahora mismo* (la que va a leer el próximo `disparar()` si no
se vuelve a girar); si esa ya tenía bala, sigue probando la siguiente
recámara (dando la vuelta al tambor si hace falta) hasta encontrar una
vacía. Con más de una bala, se van cargando así, en secuencia, hacia
adelante desde el puntero. Tira una excepción si no quedan recámaras
vacías suficientes para esa cantidad.

**Elegir vos mismo en qué recámaras exactas van las balas**, en vez de
al azar (por ejemplo, para un truco o una trampa de la historia donde
el resultado no puede ser aleatorio):

```renpy
$ ar = arma(recamaras=6, posiciones_balas=[0, 3])   # balas en la 1ra y la 4ta recámara
...
$ ar.agregar_balas(posiciones=[5])                  # agrega una bala en la última recámara
```

Con `posiciones_balas`/`posiciones`, el parámetro `balas`/`cantidad`
correspondiente se ignora (la cantidad cargada es la cantidad de
posiciones que le pasás). Tira una excepción si alguna posición está
fuera de rango, repetida, o (en `agregar_balas`) ya tenía bala.

## Parámetros de `arma(...)`

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `balas` | `1` | Cuántas balas hay cargadas al crear el arma, repartidas al azar entre las recámaras. Se ignora si pasás `posiciones_balas`. |
| `recamaras` | `6` | Cuántas recámaras tiene el tambor. `balas` no puede ser mayor que `recamaras`. |
| `girar_siempre` | `False` | Si el tambor gira (puntero a una recámara al azar) antes de cada disparo (ver "Cómo funciona la probabilidad"). |
| `posiciones_balas` | `None` | Lista de índices de recámara (0 a `recamaras - 1`) donde cargar bala, en vez de al azar. Ver más arriba. |

## Parámetros de `ar.disparar(...)`

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `apuntar_a` | — (obligatorio) | `"izquierda"` o `"derecha"`: hacia dónde apunta el arma. |
| `girar` | `None` | `None` usa `girar_siempre` del arma; `True`/`False` lo pisa solo para este disparo. |
| `imagen` | `None` | Ruta de imagen propia del arma. Con `None` usa la de ejemplo (`arma.png`). |
| `sonido_disparo` / `sonido_vacio` | `None` | Rutas de sonido para el disparo con bala / el chasquido en vacío. Con `None`, usa `RR_SONIDO_DISPARO` / `RR_SONIDO_VACIO` (configurables al principio de `modulo_ruleta_rusa.rpy`, ambos con un sonido de ejemplo ya cargado). |
| `duracion_apuntado` | `0.6` | Segundos que tarda en girar (como imagen) hacia el lado indicado. |

Además del apuntado, cada disparo tiene un pequeño "golpe" del gatillo
(se nota siempre, haya salido bala o no). **Si salió bala**, después de
eso se juega también un culatazo más fuerte (retroceso real, tirando el
arma hacia atrás y arriba): las duraciones de ambos golpes son
`RR_DURACION_GOLPE_RECORTE`/`RR_DURACION_GOLPE_VUELTA` y
`RR_DURACION_RETROCESO_GOLPE`/`RR_DURACION_RETROCESO_VUELTA`,
configurables al principio de `modulo_ruleta_rusa.rpy`. `disparar()`
espera a que termine el que corresponda antes de devolver el control a
tu guion.

`ar.girar()` no tiene parámetros ni animación en pantalla: es un cambio
de estado interno (a qué recámara apunta el puntero). Sí reproduce
`RR_SONIDO_GIRAR` (configurable al principio de `modulo_ruleta_rusa.rpy`,
con un sonido de ejemplo ya cargado) y **espera a que termine de sonar**
antes de devolver el control a tu guion — así que si lo cambiás por un
sonido más largo, ese giro va a tardar más en la práctica. Con
`RR_SONIDO_GIRAR = None`, es instantáneo. `disparar()` también lo usa
por dentro cuando corresponde girar antes de disparar. No hace falta
llamarlo antes de `disparar()` — solo sirve para el caso de "el jugador
elige volver a girar antes de arriesgarse" (ver más arriba).

`ar.balas_restantes()` devuelve cuántas balas sin disparar quedan en el
tambor actual, por si querés mostrarlo en pantalla (por ejemplo, en una
barra de "tensión").

`ar.agregar_balas(cantidad=1, posiciones=None)` carga esa cantidad de
balas nuevas empezando en la recámara del puntero y avanzando hasta
encontrar vacías (o en las recámaras exactas de `posiciones`, ver más
arriba), sin tocar las que ya había ni la posición del puntero (ver
"Cómo funciona la probabilidad"). No tiene
animación en pantalla, pero sí reproduce `RR_SONIDO_RECARGAR`
(configurable al principio de `modulo_ruleta_rusa.rpy`, con un sonido
de ejemplo ya cargado) y **espera a que termine de sonar** antes de
devolver el control a tu guion. Con `RR_SONIDO_RECARGAR = None`, es
instantáneo.

`ar.ocultar()` saca el arma de pantalla (y el cartel de `RR_DEBUG`, si
estaba prendido). Llamalo cuando la escena termine (el arma no se
oculta sola entre disparos, ver más arriba).

## Modo debug (ver el estado real del tambor)

Para probar tu guion (o el módulo mismo) sin depender de la suerte,
activá `RR_DEBUG`:

```renpy
$ RR_DEBUG = True
```

Con esto prendido, mientras el arma esté visible aparece un cartel en
la esquina superior izquierda con el estado real del tambor, por
ejemplo:

```
[RR_DEBUG] tambor:  _  _ [v] _  _  _
[RR_DEBUG] balas restantes: 1
```

Cada posición es una recámara (`v` = tiene bala, `_` = vacía), y la que
está entre corchetes es donde apunta el puntero ahora mismo (la que va
a leer el próximo `disparar()`). El cartel se actualiza solo en cada
`girar()`/`disparar()`/`agregar_balas()`.

**Esto es "hacer trampa"**: le muestra a quien esté jugando dónde está
la bala, así que es solo para desarrollo. Por defecto viene en
`False`; dejalo así (o volvé a ponerlo en `False`) para la versión
final de tu juego. Se puede prender/apagar en cualquier momento desde
tu guion (no hace falta tocar el módulo), como en el ejemplo de arriba.

## Flash de golpe (`rr_hit()`)

Función aparte del módulo (no es un método de `arma()`, no depende de
ninguna en particular): hace un flash de pantalla completa, rojo por
defecto, pensado para marcar el momento en que alguien "recibe" el
disparo. El módulo **no la llama solo en ningún momento** — vos
decidís cuándo, en tu propio guion:

```renpy
$ murio_jugador = ar.disparar(apuntar_a="derecha")
if murio_jugador:
    $ rr_hit()
    "..."
```

`rr_hit(color=None, alpha_maximo=None, duracion_subida=None,
duracion_bajada=None)` — con todo en `None` (por defecto) usa las
constantes configurables al principio de `modulo_ruleta_rusa.rpy`:

| Parámetro | Constante | Por defecto | Para qué sirve |
|---|---|---|---|
| `color` | `RR_HIT_COLOR` | `"#FF0000"` | Color del flash, en formato `"#RRGGBB"`. |
| `alpha_maximo` | `RR_HIT_ALPHA_MAXIMO` | `0.6` | Qué tan opaco se pone en su punto más fuerte (0.0 a 1.0). |
| `duracion_subida` | `RR_HIT_DURACION_SUBIDA` | `0.05` | Segundos que tarda en aparecer. |
| `duracion_bajada` | `RR_HIT_DURACION_BAJADA` | `0.4` | Segundos que tarda en desvanecerse. |

Espera a que el flash termine del todo (subida y bajada) antes de
devolver el control a tu guion. Le podés pasar cualquiera de estos
parámetros para pisar el valor configurado, solo para ese llamado.

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

## Autor

- **Autor:** davinzifc
- **Coautores:** popen.queen

## Compatibilidad y licencia

- Compatible con Ren'Py 7.x y 8.x.
- Licencia **MIT**, Copyright (c) 2026 davinzifc y popen.queen. Podés
  usar, copiar, modificar y redistribuir este módulo, incluso en
  juegos comerciales, **siempre que des crédito a los desarrolladores**:
  mantené el aviso de
  copyright y la licencia (ya están en el encabezado del archivo
  `.rpy`) en todas las copias o partes sustanciales que distribuyas,
  por ejemplo en la carpeta de créditos de tu juego. El texto completo
  está en el archivo `LICENSE` de la raíz del repositorio.
