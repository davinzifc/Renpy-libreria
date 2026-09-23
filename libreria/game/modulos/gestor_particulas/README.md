# Gestor de Partículas (nieve, lluvia y efectos propios)

Módulo "copiar y pegar" para proyectos de **Ren'Py**. Permite activar y
desactivar efectos de partículas en pantalla (nieve, lluvia, hojas,
chispas, polvo mágico, etc.) con una sola línea de código, en cualquier
punto del guion.

Las partículas se pueden dibujar de dos formas:

- **Con una imagen** (por ejemplo, la imagen de un copo de nieve).
- **Con un color plano** (un círculo o un rectángulo de color, sin
  necesitar ningún archivo de imagen) — funciona perfecto para simular
  nieve (círculos blancos) o lluvia (rayas celestes), como pediste.

No hace falta saber programar para usar los efectos ya armados de nieve
y lluvia: seguí los pasos de más abajo. Si más adelante querés crear tus
propios efectos, en la sección "Cómo crear tu propio efecto" te muestro
cómo, con ejemplos; y en "Cómo armar tus propios 'prefabs'" te muestro
la forma recomendada de guardarlos organizados, en tu propio archivo,
sin tocar el módulo y sin ensuciar el guion de tu historia con
parámetros de configuración.

## Qué hay en esta carpeta

```
gestor_particulas/
├── modulo_gestor_particulas.rpy   <- el módulo en sí (motor + nieve, lluvia y luciérnagas)
├── imagenes/
│   ├── luz.png                    <- círculo con brillo suave (nieve y luciérnagas)
│   └── gota.png                   <- estela de lluvia
└── README.md                      <- este archivo
```

Las dos imágenes de `imagenes/` son las que usan los efectos ya armados
(nieve, lluvia y luciérnagas). Si más adelante querés usar tus propias
imágenes, copialas dentro de la carpeta `game/` de tu proyecto (fuera de
la carpeta del módulo, así no se mezclan) y apuntá a esa ruta.
Si armás un efecto tuyo sin `imagenes`, se dibuja con figuras de color
plano y no necesita ninguna imagen.

## Cómo instalarlo

1. Copiá **toda esta carpeta** (`gestor_particulas`, con todo lo que
   tiene adentro) dentro de la carpeta `game/modulos/` de tu proyecto de
   Ren'Py. Si tu proyecto no tiene una carpeta `game/modulos/`, creala
   vos mismo y pegá la carpeta del módulo ahí adentro.

   Al final te tiene que quedar así:

   ```
   tu_proyecto/
   └── game/
       └── modulos/
           └── gestor_particulas/
               ├── modulo_gestor_particulas.rpy
               ├── imagenes/
               │   ├── luz.png
               │   └── gota.png
               └── README.md
   ```

2. No hace falta tocar ningún otro archivo del proyecto. Ren'Py carga
   automáticamente todos los archivos `.rpy` que encuentra, sin importar
   en qué subcarpeta estén.

3. Abrí el proyecto con el Ren'Py Launcher y ejecutalo. El módulo queda
   listo para usar, pero **no activa ningún efecto solo**: vos decidís
   desde tu guion cuándo prender y apagar cada uno (ver "Uso básico" más
   abajo).

## Uso básico dentro del guión (`script.rpy`)

La función principal del módulo es `gp_crear_particulas(...)`: le pasás
los parámetros que quieras (color, tamaño, ángulo, velocidad, etc.) y te
devuelve un **identificador**. Ese identificador es lo único que
necesitás guardar para poder apagar ese efecto en particular más
adelante, con `gp_terminar_particulas(id)`.

Además, el módulo trae tres efectos de ejemplo ya armados —nieve, lluvia
y luciérnagas— con sus atajos `gp_nieve()`, `gp_lluvia()` y
`gp_luciernagas()`. Funcionan igual: también devuelven un identificador.

**Prender nieve o lluvia con los valores ya configurados:**

```renpy
scene bg pueblo_nevado
$ id_clima = gp_nieve()

e "Está nevando otra vez..."
```

**Apagar ese efecto** (usando el identificador que guardaste):

```renpy
$ gp_terminar_particulas(id_clima)
```

**Cambiar de un efecto a otro** (útil cuando la historia salta de
escena y el clima cambia con ella, por ejemplo de nieve a lluvia):

```renpy
scene bg calle_lluviosa
$ gp_terminar_particulas(id_clima)
$ id_clima = gp_lluvia()

e "Uy, empezó a llover."
```

**Crear un efecto propio al vuelo, sin depender de nieve o lluvia**,
pasándole vos mismo todos los parámetros:

```renpy
$ id_chispas = gp_crear_particulas(
      color=["#FFCC66", "#FF9933", "#FF6600"], forma="circulo",
      tamano_min=2, tamano_max=5, cantidad=25,
      angulo_base=270, angulo_variacion=30,
      velocidad_min=30, velocidad_max=70,
      origen="abajo", tiempo_vida_min=0.8, tiempo_vida_max=1.6,
  )
...
$ gp_terminar_particulas(id_chispas)
```

**Apagar todos los efectos activos de una:**

```renpy
$ gp_terminar_todas()
```

**Saber si un efecto sigue activo** (por si necesitás una condición):

```renpy
if gp_efecto_activo(id_clima):
    e "Todavía sigue lloviendo."
```

> El efecto queda prendido hasta que vos lo apagues explícitamente con
> `gp_terminar_particulas()` (o `gp_terminar_todas()`): no se apaga solo
> al cambiar de fondo con `scene` ni al hacer un `jump` a otra etiqueta.
> Esto es a propósito, para que el clima se mantenga mientras avanza la
> historia (por ejemplo, durante varias escenas seguidas bajo la
> lluvia) y para que seas vos quien decide en qué momento exacto empieza
> y termina cada efecto. Por eso es importante que guardes el
> identificador que te devuelve `gp_crear_particulas()` / `gp_nieve()` /
> `gp_lluvia()` en una variable (por ejemplo, guardada con `default` en
> tu guión) si más adelante vas a necesitar apagar ese efecto puntual.

## Parámetros principales

Los efectos de ejemplo (nieve, lluvia y luciérnagas) **no se configuran
editando el módulo**: para uno distinto, se arma con
`gp_crear_particulas(...)` pasando estos parámetros con nombre (o se
ajusta uno de ejemplo, por ejemplo `gp_nieve(cantidad=40)`). Todos son
opcionales: lo que no escribas toma su valor por defecto. La misma
explicación (más detallada) está en el docstring de `GP_TipoParticula`,
dentro de `modulo_gestor_particulas.rpy`.

### Aspecto

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `imagenes` | `None` | Lista de imágenes (rutas o displayables) para usar como partícula; si hay varias, cada una elige una al azar. Con `None` se dibuja una figura de color plano. |
| `color` | `"#FFFFFF"` | Color plano `"#RRGGBB"`. Puede ser una lista (`["#FFF", ...]`) para que cada partícula elija uno. Solo se usa sin `imagenes`. |
| `forma` | `"circulo"` | `"circulo"` o `"rectangulo"`. Solo sin `imagenes`. |
| `tamano_min` / `tamano_max` | `6` / `6` | Rango de tamaño en píxeles (con imagen, su lado más largo; con rectángulo, el largo). Cada partícula elige uno al azar. |
| `ancho_min` / `ancho_max` | `None` | Solo `forma="rectangulo"`: grosor del rectángulo. Con `None` es igual al tamaño (cuadrado). |
| `opacidad_min` / `opacidad_max` | `1.0` / `1.0` | Rango de transparencia (0.0 invisible a 1.0 sólida). Variarla da sensación de profundidad. |
| `rotar` | `False` | Si la partícula gira sobre sí misma. Se nota solo con `imagenes`. |
| `rotacion_velocidad_min` / `rotacion_velocidad_max` | `-60` / `60` | Rango de giro en grados por segundo (negativo = gira al revés). Solo con `rotar=True`. |

### Cantidad y origen

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `cantidad` | `60` | Cuántas partículas hay al mismo tiempo. Es lo que más pesa en el rendimiento. |
| `origen` | `"auto"` | De qué borde nacen al reciclarse: `"auto"` (según el ángulo), `"arriba"`, `"abajo"`, `"izquierda"`, `"derecha"` o `"toda_pantalla"`. |
| `origen_min` / `origen_max` | `0.0` / `1.0` | Limita la zona del borde de nacimiento (de 0.0 a 1.0), por ejemplo solo la mitad izquierda. |
| `zorder` | `-10` | Orden de dibujado dentro de su capa. El valor por defecto queda debajo del cuadro de diálogo. |

### Movimiento

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `movimiento` | `"lineal"` | `"lineal"`: recta según ángulo y velocidad. `"aleatorio"`: vaga por toda la pantalla, gira suavemente al azar y rebota en los bordes. |
| `angulo_base` | `90` | Dirección en grados: 0 derecha, 90 abajo, 180 izquierda, 270 arriba (con `"aleatorio"` es solo el rumbo inicial). |
| `angulo_variacion` | `0` | Cuánto varía el ángulo al azar, a cada lado. Con 180 sale en cualquier dirección. |
| `velocidad_min` / `velocidad_max` | `60` / `60` | Rango de velocidad en píxeles por segundo. |
| `ondulado` | `False` | `True` suma un vaivén lateral tipo viento a un movimiento lineal. |
| `amplitud_ondulado` | `15` | Ancho del vaivén, en píxeles. Solo con `ondulado=True`. |
| `frecuencia_ondulado` | `1.0` | Ondas por segundo. Solo con `ondulado=True`. |
| `vagar_giro` | `60` | Solo con `"aleatorio"`: qué tan bruscos son los giros, en grados por segundo (20–40 curvas suaves, 120+ nervioso). |

### Vida y aparición

| Parámetro | Por defecto | Para qué sirve |
|---|---|---|
| `tiempo_vida` | `None` | Atajo: vida exacta en segundos (equivale a poner el mismo valor en `_min` y `_max`). |
| `tiempo_vida_min` / `tiempo_vida_max` | `None` | Rango de vida en segundos. Al cumplirse, la partícula reaparece en otro lugar. Con `None` vive hasta salir de la pantalla. |
| `fade_in` | `0.0` | Segundos que tarda en aparecer (opacidad de 0 a su valor). |
| `fade_out` | `0.0` | Segundos que tarda en apagarse al final de su vida. Requiere `tiempo_vida`. Si `fade_in + fade_out` supera la vida, se acortan proporcionalmente. |

### Del atajo, no de la partícula

`gp_crear_particulas`, `gp_nieve`, `gp_lluvia` y `gp_luciernagas` también
aceptan `capa` (en qué capa se muestra; por defecto `"screens"`, para que
el efecto no se borre con `scene`), y `gp_crear_particulas` acepta
`tipo=` (un prefab ya armado, al que se le pueden sumar ajustes por
nombre).

### Cómo funciona el ángulo

El ángulo se mide en grados, igual que las agujas de un reloj pero
empezando desde la derecha:

```
              270 (arriba)
                  |
  180 (izq.) ---- + ---- 0 (derecha)
                  |
              90 (abajo)
```

La nieve y la lluvia usan un ángulo cercano a 90 (hacia abajo). Si
quisieras, por ejemplo, chispas que suben desde una fogata, usarías un
ángulo cercano a 270 (hacia arriba).

### Usar tus propias imágenes en vez de color plano

1. Copiá tu imagen (por ejemplo `copo.png`) dentro de la carpeta
   `game/` de tu proyecto, en tu propia carpeta de imágenes (por
   ejemplo `game/imagenes/`), fuera de la carpeta del módulo.
2. Pasá esa ruta en el parámetro `imagenes`:

   ```renpy
   $ id = gp_crear_particulas(imagenes=["imagenes/copo.png"], cantidad=50)
   ```

3. Si le pasás más de una imagen en la lista, cada partícula elige una
   al azar — útil para mezclar, por ejemplo, dos o tres formas de copo
   distintas.

## Cómo crear tu propio efecto

Además de la nieve y la lluvia, podés crear cualquier otro efecto
(hojas cayendo, chispas de fuego, pétalos, polvo mágico, luciérnagas,
etc.) sin tocar el archivo del módulo, llamando directamente a
`gp_crear_particulas(...)` con los parámetros que quieras desde tu
propio `script.rpy` (o mejor, desde un archivo `.rpy` nuevo tuyo). No
hace falta que el efecto exista de antemano: vos decidís todos sus
parámetros en el momento de crearlo.

**Ejemplo: hojas cayendo, girando, con imagen propia:**

```renpy
label bosque_otonal:
    scene bg bosque
    $ id_hojas = gp_crear_particulas(
          imagenes=["imagenes/hoja1.png", "imagenes/hoja2.png"],
          tamano_min=16, tamano_max=28,
          cantidad=40,
          angulo_base=100, angulo_variacion=25,
          velocidad_min=40, velocidad_max=90,
          ondulado=True, amplitud_ondulado=40, frecuencia_ondulado=0.4,
          rotar=True, rotacion_velocidad_min=-90, rotacion_velocidad_max=90,
          opacidad_min=0.7, opacidad_max=1.0,
      )
    e "Las hojas caen sin parar por acá."
    ...
    $ gp_terminar_particulas(id_hojas)
```

**Ejemplo: chispas de fuego que suben y se apagan solas (sin imagen,
solo color), usando `tiempo_vida` en vez de reciclado por pantalla:**

```renpy
$ id_chispas = gp_crear_particulas(
      color=["#FFCC66", "#FF9933", "#FF6600"],
      forma="circulo",
      tamano_min=2, tamano_max=5,
      cantidad=25,
      angulo_base=270, angulo_variacion=30,
      velocidad_min=30, velocidad_max=70,
      origen="abajo", origen_min=0.4, origen_max=0.6,
      opacidad_min=0.4, opacidad_max=0.9,
      tiempo_vida_min=0.8, tiempo_vida_max=1.6,
  )
```

**Si vas a reutilizar el mismo efecto muchas veces** (por ejemplo, en
varias etiquetas distintas), armá la receta una sola vez con
`GP_TipoParticula(...)` guardada en un `define`, y pasásela a
`gp_crear_particulas()` con `tipo=...` cada vez que la necesites, en vez
de repetir todos los parámetros cada vez. A esa receta ya armada y
guardada le podemos decir un **"prefab"**: la sección siguiente explica
dónde conviene guardarla.

## Cómo armar tus propios "prefabs" (sin tocar el módulo)

Un "prefab" es simplemente un `GP_TipoParticula(...)` guardado en un
`define`, con un nombre, listo para usar en cualquier parte de tu juego
con `gp_crear_particulas(tipo=TU_PREFAB)`. `gp_nieve()` y `gp_lluvia()`
son, por dentro, exactamente eso: dos prefabs que ya vienen armados con
el módulo.

**Importante: tus propios prefabs NO van dentro del archivo del
módulo** (`modulo_gestor_particulas.rpy`). Se guardan en un archivo
`.rpy` **aparte**, en cualquier otro lugar de tu carpeta `game/`. Por
ejemplo, uno tuyo llamado `prefab_particulas.rpy`, junto a tu
`script.rpy`:

```
tu_proyecto/
└── game/
    ├── modulos/
    │   └── gestor_particulas/       <- el módulo: no lo edites
    │       ├── modulo_gestor_particulas.rpy
    │       └── README.md
    ├── prefab_particulas.rpy        <- tus prefabs, en tu propio archivo
    └── script.rpy
```

¿Por qué conviene un archivo aparte, con TODOS tus prefabs juntos, en
vez de escribirlos sueltos donde los vayas necesitando? Por dos
motivos:

- **El módulo queda intacto.** Está pensado para copiarse y pegarse tal
  cual entre proyectos (o reemplazarse por una versión más nueva el día
  de mañana) sin arrastrar contenido específico de tu juego. Si guardás
  tus prefabs en su propio archivo, podés actualizar o volver a copiar
  la carpeta `gestor_particulas/` sin miedo a perder nada tuyo, porque
  nunca la tocaste.

- **El guión de tu novela visual queda limpio.** Si cada vez que
  necesitás un efecto escribís `gp_crear_particulas(...)` con quince
  parámetros directamente en medio de un label, tu `script.rpy` (o el
  capítulo que estés escribiendo) se llena de números y configuración
  que no tienen nada que ver con la historia, y se vuelve más difícil
  de leer. Definiendo cada efecto UNA vez como prefab, en su propio
  archivo, el guión de la historia queda enfocado en la historia: en
  el label solo aparece un `gp_crear_particulas(tipo=PREFAB_LLUVIA)`,
  una línea corta y fácil de entender de un vistazo, sin tener que
  bucear entre parámetros para saber qué está pasando en esa escena.
  Además, si más adelante querés ajustar cómo se ve la lluvia en TODO
  el juego, lo cambiás en un solo lugar (el prefab) en vez de buscar y
  editar cada label donde la usaste.

Ren'Py no necesita que le digas nada especial para que ese archivo se
cargue: como pasa con cualquier `.rpy` dentro de `game/`, se carga solo,
sin importar el nombre que le pongas ni en qué subcarpeta esté. Lo único
que importa es que se cargue DESPUÉS del módulo — y eso también pasa
solo, porque Ren'Py carga primero por orden alfabético de carpeta y acá
`modulos/` va antes que un archivo suelto en `game/`. Si igual preferís
ordenarlo distinto (por ejemplo, un prefab por capítulo del juego,
dentro de una carpeta `game/particulas/`), también funciona igual.

**Ejemplo de `prefab_particulas.rpy`**, con tres prefabs propios:

```renpy
# prefab_particulas.rpy
# Prefabs de partículas propios de este juego. Este archivo NO es parte
# del módulo "gestor_particulas": es tuyo, y podés editarlo, renombrarlo
# o borrar prefabs sin afectar al módulo en absoluto.

define PREFAB_HOJAS = GP_TipoParticula(
    imagenes=["imagenes/hoja1.png", "imagenes/hoja2.png"],
    tamano_min=16, tamano_max=28,
    cantidad=40,
    angulo_base=100, angulo_variacion=25,
    velocidad_min=40, velocidad_max=90,
    ondulado=True, amplitud_ondulado=40, frecuencia_ondulado=0.4,
    rotar=True, rotacion_velocidad_min=-90, rotacion_velocidad_max=90,
    opacidad_min=0.7, opacidad_max=1.0,
)

define PREFAB_CHISPAS = GP_TipoParticula(
    color=["#FFCC66", "#FF9933", "#FF6600"],
    forma="circulo",
    tamano_min=2, tamano_max=5,
    cantidad=25,
    angulo_base=270, angulo_variacion=30,
    velocidad_min=30, velocidad_max=70,
    origen="abajo", origen_min=0.4, origen_max=0.6,
    opacidad_min=0.4, opacidad_max=0.9,
    tiempo_vida_min=0.8, tiempo_vida_max=1.6,
)

define PREFAB_POLVO_MAGICO = GP_TipoParticula(
    color=["#E0AAFF", "#C77DFF", "#FFFFFF"],
    forma="circulo",
    tamano_min=1, tamano_max=3,
    cantidad=35,
    angulo_base=270, angulo_variacion=180,
    velocidad_min=10, velocidad_max=35,
    origen="toda_pantalla",
    opacidad_min=0.3, opacidad_max=0.8,
    tiempo_vida_min=1.0, tiempo_vida_max=2.5,
)
```

Y despues, en `script.rpy` (o en cualquier otro label), los usás igual
que a `gp_nieve()` o `gp_lluvia()`, pasándoselos a
`gp_crear_particulas()` con `tipo=...`:

```renpy
label bosque_otonal:
    scene bg bosque
    $ id_hojas = gp_crear_particulas(tipo=PREFAB_HOJAS)
    e "Las hojas caen sin parar por acá."
    ...
    $ gp_terminar_particulas(id_hojas)

label cueva_magica:
    scene bg cueva
    $ id_polvo = gp_crear_particulas(tipo=PREFAB_POLVO_MAGICO)
    e "Este lugar brilla solo..."
    ...
    $ gp_terminar_particulas(id_polvo)
```

> **Tip de nombres:** evitá que tus propios prefabs empiecen con `GP_`
> (ese prefijo lo usa el módulo para sus propios nombres internos, como
> `GP_NIEVE` o `GP_TipoParticula`). Usar otro prefijo propio — en el
> ejemplo de arriba, `PREFAB_` — evita cualquier confusión o choque de
> nombres, y además deja bien claro, con solo mirar el nombre, que es
> algo tuyo y no parte del módulo.

Esto es exactamente lo mismo que hace el módulo con sus efectos de
ejemplo: `GP_NIEVE`, `GP_LLUVIA` y `GP_LUCIERNAGAS` son prefabs armados
con `GP_TipoParticula(...)` con los valores escritos directamente, y
`gp_nieve()`, `gp_lluvia()` y `gp_luciernagas()` se los pasan a
`gp_crear_particulas()`. Podés ajustarles algún parámetro puntual, por
ejemplo `gp_nieve(cantidad=150)` para una nevada más densa solo en una
escena puntual.

La lista completa de parámetros disponibles para `gp_crear_particulas()`
(con la explicación de cada uno en español) está en el docstring de la
clase `GP_TipoParticula`, dentro de `modulo_gestor_particulas.rpy`, en
la sección "MOTOR". Ahí también podés ver `origen`,
`origen_min`/`origen_max`, `ancho_min`/`ancho_max` y `zorder`, que no
hicieron falta en los ejemplos de arriba pero están disponibles para
casos más específicos.

## Efectos ya armados: nieve, lluvia y luciérnagas

Los tres vienen con imágenes de bordes suaves (sin el pixelado de los
círculos planos), guardadas en la carpeta `imagenes/` del módulo:

| Efecto | Atajo | Imagen por defecto |
|---|---|---|
| Nieve | `gp_nieve()` | `luz.png` (círculo blanco con brillo suave) |
| Lluvia | `gp_lluvia()` | `gota.png` (estela celeste inclinada ~10°) |
| Luciérnagas | `gp_luciernagas()` | `luz.png`, teñida de tres tonos de luciérnaga |

Son **ejemplos listos para usar**, no configuraciones que se editen en el
módulo. Para cambiar algo puntual, pasale el parámetro con nombre al atajo
(`gp_nieve(cantidad=40)`, `gp_lluvia(opacidad_max=0.9)`). Para uno
distinto, usá `gp_crear_particulas(...)`; por ejemplo, para volver a
formas planas (más livianas) sin imagen:

```renpy
$ id = gp_nieve(imagenes=None, tamano_min=3, tamano_max=8)
```

Las imágenes que se tiñen (como la luz de las luciérnagas) tienen que ser
**blancas sobre transparente**.

## Configurar solo lo que quieras cambiar

No hace falta pasar parámetros en orden ni escribir `None` en los que no
querés tocar: todo parámetro tiene un valor por defecto y se indica por
nombre (`nombre=valor`), así que solo escribís lo que te interesa:

```renpy
$ id = gp_crear_particulas(color="#FFFF88", tiempo_vida=4, fade_in=1)
```

Sirve también para ajustar nieve, lluvia, luciérnagas o un prefab ya
armado:

```renpy
$ id = gp_nieve(cantidad=40)
$ id = gp_crear_particulas(tipo=PREFAB_HOJAS, cantidad=20)
```

Un parámetro mal escrito da un error claro en vez de ignorarse en
silencio.

## Tiempo de vida y fade (aparición/desaparición suave)

| Parámetro | Para qué sirve |
|---|---|
| `tiempo_vida` | Cuántos segundos vive cada partícula (atajo de `tiempo_vida_min` = `tiempo_vida_max`). Pasado ese tiempo, reaparece en otro lugar. |
| `tiempo_vida_min` / `tiempo_vida_max` | Lo mismo, pero con un rango al azar por partícula. |
| `fade_in` | Segundos que tarda en aparecer (opacidad de 0 a su valor). |
| `fade_out` | Segundos que tarda en apagarse al final de su vida. Necesita `tiempo_vida`. |

La partícula queda con opacidad completa entre el fade in y el fade out.
Si `fade_in + fade_out` es más largo que la vida, se acortan
proporcionalmente. Al arrancar el efecto, cada partícula empieza en un
punto distinto de su ciclo, así no parpadean todas a la vez.

## Movimiento aleatorio (luciérnagas, polvo, burbujas)

Con `movimiento="aleatorio"` las partículas **vagan por toda la
pantalla**: cambian de rumbo suavemente al azar y rebotan en los bordes
(nunca salen). Nacen en cualquier punto de la pantalla.
`vagar_giro` (grados por segundo) controla qué tan bruscos son los giros:
20-40 = curvas suaves, 120+ = nervioso. `velocidad_min/max` fija qué tan
rápido andan.

**Ejemplo: luciérnagas**

```renpy
define PREFAB_LUCIERNAGAS = GP_TipoParticula(
    color=["#F5FF7A", "#CFFF5E"], forma="circulo",
    tamano_min=3, tamano_max=6, cantidad=30,
    movimiento="aleatorio", vagar_giro=50,
    angulo_variacion=180,
    velocidad_min=15, velocidad_max=40,
    opacidad_min=0.7, opacidad_max=1.0,
    tiempo_vida_min=4, tiempo_vida_max=8,
    fade_in=1.5, fade_out=1.5,
)
```

Sin `tiempo_vida`, las partículas vagan para siempre sin apagarse.

## Notas de rendimiento

Ren'Py mueve las partículas con Python "a mano", cuadro a cuadro: no hay
forma de que esto lo acelere la placa de video (GPU), todo el trabajo
lo hace el procesador (CPU). Por eso `cantidad` es el parámetro que más
impacta en el rendimiento, y conviene tenerlo en cuenta:

- **Color plano (`imagenes=None`), que es lo que usan nieve y lluvia
  por defecto:** es la opción más liviana, porque cada partícula se
  dibuja con una sola instrucción directa (un círculo o un rectángulo),
  sin pasar por el sistema de imágenes de Ren'Py. En una PC de gama
  media hoy en día, andar con 200-400 partículas de este tipo al mismo
  tiempo no debería notarse. En celulares o PCs más limitadas, convine
  quedarse más cerca de 80-150.
- **Con `imagenes`:** cada partícula se escala (y, si `rotar=True`, se
  rota) como una imagen aparte en cada cuadro, pasando por el sistema
  de renderizado completo de Ren'Py — mucho más costoso que dibujar un
  color plano. Con imágenes conviene quedarse en un rango más chico,
  como 60-120 partículas, sobre todo si además rotan.
- Si necesitás un efecto muy denso y notás que se pone lento, primero
  probá bajar `cantidad` antes que cualquier otro parámetro: es el que
  tiene el impacto más directo en el rendimiento. Combinar varios
  efectos activos al mismo tiempo (por ejemplo nieve + niebla + polvo)
  también suma: la cantidad total de partículas en pantalla es lo que
  importa, sin importar en cuántos `gp_crear_particulas()` distintos
  estén repartidas.
- El módulo ya evita todo el trabajo que se pueda calcular una sola vez
  por partícula (por ejemplo, el color exacto con su transparencia) en
  vez de recalcularlo en cada cuadro, así que no hace falta que hagas
  nada extra para aprovechar eso: viene optimizado así desde la propia
  función que crea cada partícula.

## Autor

- **Autor:** davinzifc

## Compatibilidad y licencia

- Compatible con Ren'Py 7.x y 8.x.
- Licencia **MIT**, Copyright (c) 2026 davinzifc. Podés usar, copiar,
  modificar y redistribuir este módulo, incluso en juegos comerciales,
  **siempre que des crédito al desarrollador**: mantené el aviso de
  copyright y la licencia (ya están en el encabezado del archivo
  `.rpy`) en todas las copias o partes sustanciales que distribuyas, por
  ejemplo en la carpeta de créditos de tu juego. El texto completo está
  en el archivo `LICENSE` de la raíz del repositorio.
