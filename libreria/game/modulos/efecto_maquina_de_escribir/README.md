# Efecto Máquina de Escribir (texto letra por letra)

Módulo "copiar y pegar" para proyectos de **Ren'Py**. Hace que el texto de
los diálogos aparezca **letra por letra**, como si un personaje lo
estuviera escribiendo en tiempo real, con un sonido de tecleo opcional.

No hace falta saber programar para usarlo: seguí los pasos de más abajo.

## Qué hay en esta carpeta

```
efecto_maquina_de_escribir/
├── modulo_efecto_maquina_de_escribir.rpy   <- el módulo en sí
├── audio/
│   └── mme_tecleo.mp3                      <- sonido de tecleo de ejemplo
└── README.md                               <- este archivo
```

Los tres archivos van siempre juntos, en la misma carpeta.

## Cómo instalarlo

1. Copiá **toda esta carpeta** (`efecto_maquina_de_escribir`, con todo lo
   que tiene adentro) dentro de la carpeta `game/modulos/` de tu proyecto
   de Ren'Py. Si tu proyecto no tiene una carpeta `game/modulos/`, creala
   vos mismo y pegá la carpeta del módulo ahí adentro.

   Al final te tiene que quedar así:

   ```
   tu_proyecto/
   └── game/
       └── modulos/
           └── efecto_maquina_de_escribir/
               ├── modulo_efecto_maquina_de_escribir.rpy
               ├── audio/
               │   └── mme_tecleo.mp3
               └── README.md
   ```

2. No hace falta tocar ningún otro archivo del proyecto (ni `options.rpy`,
   ni `script.rpy`). Ren'Py carga automáticamente todos los archivos
   `.rpy` que encuentra, sin importar en qué subcarpeta estén.

3. Abrí el proyecto con el Ren'Py Launcher y ejecutalo. Listo — el efecto
   ya está activo en todos los diálogos del juego.

> **¿Querés ponerlo en otra carpeta** (por ejemplo `game/components/` en
> vez de `game/modulos/`)? Podés hacerlo, pero después tenés que abrir
> `modulo_efecto_maquina_de_escribir.rpy` y ajustar la línea de
> `MME_SONIDO_TECLEO` para que la ruta coincida con la carpeta nueva
> (ver más abajo).

## Cómo configurarlo

Todo lo que podés cambiar está junto, arriba del todo del archivo
`modulo_efecto_maquina_de_escribir.rpy`, en la sección que dice
**"CONFIGURACION"**. Cada línea tiene una explicación en español simple
arriba. En resumen:

| Variable | Para qué sirve |
|---|---|
| `MME_VELOCIDAD_CPS` | Qué tan rápido aparece el texto (0 = de golpe, 20-35 = cómodo, 60 = muy rápido). |
| `MME_SONIDO_TECLEO` | Sonido de tecleo a usar. Poné `None` para que no suene nada. |
| `MME_SONIDO_TECLEO_VOLUMEN` | Volumen del sonido, de `0.0` (silencio) a `1.0` (máximo). |
| `MME_SONIDO_TECLEO_SINCRONIZAR_CON_VELOCIDAD` | Si el sonido acompaña la velocidad del texto (`True`) o suena siempre igual (`False`). |
| `MME_SONIDO_TECLEO_DURACION_MINIMA` | Límite de qué tan rápido puede sonar el tecleo cuando está sincronizado. No lo toques si no estás seguro. |
| `MME_SONIDO_TECLEO_DURACION` | Ritmo fijo del sonido, cuando NO está sincronizado con la velocidad. |

Para cambiar cualquier cosa: abrí el archivo con un editor de texto
(el mismo Ren'Py Launcher trae uno), cambiá el valor después del `=` en
la línea que te interese, y guardá.

### Usar tu propio sonido de tecleo

1. Copiá tu archivo de sonido (`.mp3`, `.ogg` o `.wav`) dentro de la
   carpeta `game/` de tu proyecto (podés crear una carpeta `game/audio/`
   para ordenarlo, por ejemplo).
2. Cambiá la línea `MME_SONIDO_TECLEO` para que apunte a esa ruta, por
   ejemplo:

   ```
   define MME_SONIDO_TECLEO = "audio/mi_sonido.ogg"
   ```

## Uso avanzado dentro del guión (`script.rpy`)

El efecto se aplica solo, no hace falta escribir nada especial. Pero si
querés más control:

**A) Un personaje con su propia velocidad** (por ejemplo un narrador más
rápido, o un personaje nervioso):

```renpy
define e = Character("Eileen", cps=25)
define n = Character("Narrador", cps=40)
```

**B) Cambiar la velocidad en un punto puntual del diálogo**, con la
etiqueta `{cps=...}`:

```renpy
e "Esto se lee normal, pero {cps=5}esto se escribe muy
despacio{/cps} y esto vuelve a la velocidad normal."
```

**C) Cambiar la velocidad general para todo lo que sigue** (útil para
efectos dramáticos), con la función que trae el módulo:

```renpy
$ mme_definir_velocidad(5)      # muy lento
e "Esto... se... escribe... despacio..."
$ mme_definir_velocidad(25)     # vuelve a la velocidad normal
```

## Nota para el jugador

Mientras el texto se está "escribiendo", un clic o tecla completa esa
línea de inmediato; otro clic avanza a la siguiente. Esto ya lo maneja
Ren'Py automáticamente. Además, el menú de "Preferencias" de Ren'Py ya
trae un control deslizante de "Velocidad de texto" para que el jugador lo
ajuste a su gusto.

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
