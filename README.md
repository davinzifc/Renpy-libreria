# Librería de Módulos para Ren'Py

Proyecto **gratuito y de código abierto para la comunidad de Ren'Py**.
Acá vas a encontrar módulos "copiar y pegar": cada uno agrega una
funcionalidad a tu juego (por ejemplo, un efecto de texto) sin que
tengas que programarla desde cero. Están pensados para poder usarse
aunque no sepas programar.

Este proyecto existe gracias a la comunidad de **[Venus Tuto](https://www.youtube.com/@VenusTuto)**,
un canal de YouTube dedicado a enseñar Ren'Py. 💜

## Índice de módulos

| Módulo | Qué hace |
|---|---|
| [Efecto Máquina de Escribir](libreria/game/modulos/efecto_maquina_de_escribir/README.md) | El texto de los diálogos aparece letra por letra, con un sonido de tecleo opcional y configurable. |
| [Gestor de Partículas](libreria/game/modulos/gestor_particulas/README.md) | Efectos de partículas en pantalla (nieve, lluvia y cualquier efecto propio), con color plano o imagen, totalmente configurables: ángulo, velocidad, tamaño, rotación, etc. |
| [Ruleta Rusa](libreria/game/modulos/ruleta_rusa/README.md) | Arma 2D (sin 3D) que apunta y dispara: tambor con recámaras reales, control exacto o al azar de dónde van las balas, sonidos configurables, culatazo, modo debug y flash de pantalla al recibir un disparo. |

*(A medida que se agreguen más módulos, van a aparecer acá.)*

## Cómo usar un módulo

1. Entrá a la carpeta del módulo que te interese (link en el índice de
   arriba) y leé su propio `README.md`: ahí están los pasos exactos de
   instalación y configuración de ESE módulo en particular.
2. En general, la idea es siempre la misma: copiás la carpeta completa
   del módulo dentro de `game/modulos/` en tu propio proyecto de Ren'Py,
   y listo — no hace falta tocar ningún otro archivo.

## Cómo ver los ejemplos en acción

Este mismo proyecto (`libreria/`) trae, además de los módulos, una
demostración jugable de cada uno. Si abrís el proyecto con el Ren'Py
Launcher y le das a "Ejecutar", `game/script.rpy` te muestra un menú
para elegir qué módulo querés ver funcionando:

```
Elegí qué módulo querés ver en acción.

Gestor de partículas (nieve, lluvia, luciérnagas...)
Efecto máquina de escribir (texto letra por letra)
Ruleta rusa (arma que gira, apunta y dispara)
Salir
```

`game/script.rpy` actúa solo como **handler**: no tiene la lógica de
ningún efecto, solo llama (`call`) a la vista de ejemplo de cada módulo
y, al volver, muestra el menú de nuevo. Cada vista de ejemplo vive en su
propio archivo dentro de `game/vistas/`, con el nombre
`ejemplo_<nombre_del_modulo>.rpy`. Esto mantiene tres cosas bien
separadas:

- `game/modulos/` — el código de cada módulo, autocontenido, listo para
  copiarse a otro proyecto tal cual está.
- `game/vistas/` — un ejemplo de uso por módulo (uno o varios `label` con
  diálogo de Eileen probando el módulo), que **no** se copia a otro
  proyecto: es solo la demo de esta librería.
- `game/script.rpy` — el punto de entrada, que arma el menú y deriva a
  cada vista.

Si agregás un módulo nuevo a `game/modulos/`, la idea es sumar su vista
correspondiente en `game/vistas/ejemplo_<nombre_del_modulo>.rpy` y una
opción más en el menú de `game/script.rpy` que haga `call` a esa vista.

## Estructura del proyecto

```
libreria/                          <- proyecto de Ren'Py (podés abrirlo con el Launcher)
└── game/
    ├── script.rpy                      <- handler: arma el menú y llama a cada vista
    ├── modulos/
    │   ├── efecto_maquina_de_escribir/   <- un módulo, autocontenido en su carpeta
    │   │   ├── modulo_efecto_maquina_de_escribir.rpy
    │   │   ├── audio/
    │   │   └── README.md
    │   ├── gestor_particulas/            <- otro módulo, autocontenido en su carpeta
    │   │   ├── modulo_gestor_particulas.rpy
    │   │   └── README.md
    │   └── ruleta_rusa/                  <- otro módulo, autocontenido en su carpeta
    │       ├── modulo_ruleta_rusa.rpy
    │       ├── imagenes/
    │       ├── audio/
    │       └── README.md
    └── vistas/                         <- ejemplos de uso, uno por módulo
        ├── ejemplo_efecto_maquina_de_escribir.rpy
        ├── ejemplo_gestor_particulas.rpy
        └── ejemplo_ruleta_rusa.rpy
```

Cada módulo vive en su propia carpeta, con todo lo que necesita adentro
(script, sonidos u otros archivos, y su propio `README.md`), para que
copiarlo a otro proyecto sea tan simple como copiar esa carpeta. Las
vistas de `game/vistas/` son aparte, y solo sirven para probar los
módulos dentro de este mismo repositorio.

## Licencia

Licencia **MIT** (ver el archivo [`LICENSE`](LICENSE)), Copyright (c) 2026
davinzifc.

Podés usar, copiar, modificar y redistribuir cualquiera de estos
módulos, en proyectos personales o comerciales, **con la condición de
dar crédito al desarrollador**: en todas las copias o partes
sustanciales que distribuyas tenés que mantener el aviso de copyright y
el texto de la licencia. Con un juego, lo más simple es incluirlos en tu
carpeta de créditos/licencias (o conservarlos en el encabezado del
archivo `.rpy` del módulo, que ya los trae).

Algunos módulos tienen coautores propios además de davinzifc (por
ejemplo, Ruleta Rusa suma a popen.queen): fijate el apartado "Autor" del
`README.md` y el encabezado del `.rpy` de cada módulo para el crédito
exacto de ese módulo en particular.

Ejemplo de crédito para pegar:

> Módulos de Ren'Py por davinzifc (MIT License).
