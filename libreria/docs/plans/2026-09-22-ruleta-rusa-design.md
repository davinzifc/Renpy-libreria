# Diseño: módulo "Ruleta Rusa" (2D, sin 3D)

## Contexto

Un miembro de la comunidad de Ren'Py del dev pidió un minijuego de ruleta
rusa (arma que apunta a NPC o jugador según el turno, tambor que gira,
cantidad de balas configurable). Se pensó inicialmente en 3D por la
cantidad de partes en movimiento, pero se descarta: Ren'Py no tiene
soporte nativo de mallas 3D, y la comunidad del dev no es técnica. Se
resuelve igual que el resto de la librería (`gestor_particulas`,
`efecto_maquina_de_escribir`): un módulo "copiar y pegar" en
`game/modulos/`, con arte 2D animado por ATL (rotación/espejado), sin
salir del pipeline estándar de Ren'Py.

## Alcance

Minijuego completo: el módulo resuelve tanto la animación (giro,
apuntado, gatillo) como la lógica de probabilidad de las balas. El dev
que instale el módulo solo llama a los métodos del arma desde su propio
guion y decide las consecuencias narrativas (diálogo, muerte de un
personaje, fin de la partida) — el módulo no impone flujo de historia.

## 1) El arma como objeto persistente

```renpy
$ ar = arma(balas=1, recamaras=6, girar_siempre=False)
```

- `arma(...)` es una función atajo que crea una instancia de la clase
  interna `RR_Arma` (prefijo `RR_`, igual convención que
  `GP_TipoParticula` en el módulo de partículas).
- `RR_Arma` es un objeto de datos simple: una lista de booleanos
  (`camaras`, una por recámara, marcando dónde hay bala), un entero
  (`posicion`, la cámara actual bajo el martillo) y dos parámetros de
  configuración (`recamaras`, `girar_siempre`). No contiene
  displayables, pantallas ni referencias no serializables.
- Al ser un objeto de datos plano, **se guarda y se carga solo** con el
  sistema estándar de save/load de Ren'Py: si la historia interrumpe la
  partida y se retoma más adelante (incluso cargando una partida
  guardada), el arma conserva exactamente el mismo estado de balas y
  posición sin que el dev tenga que persistir nada a mano.
- Validaciones al crear el arma (siguiendo el estilo del resto de la
  librería): `balas` no puede ser mayor que `recamaras`, `recamaras`
  tiene que ser un entero positivo. Errores claros con `raise
  Exception(...)`, no fallos silenciosos.

## 2) Métodos del arma

- `ar.girar()` — remezcla al azar las balas entre las recámaras (nueva
  distribución) y resetea la posición. Reproduce su propia animación de
  giro. Pensado para exponer un re-giro manual elegido por el jugador
  (por ejemplo, un choice "¿Querés volver a girar el tambor?") sin
  disparar todavía — esto es lo que pedía el dev: "que gire una vez si
  el usuario lo quiere", como acción explícita y separada de disparar.

- `ar.disparar(apuntar_a="izquierda")` — hace la secuencia completa:
  1. Si corresponde re-girar antes de este disparo (según
     `girar_siempre` del arma, salvo que se pase `girar=True/False`
     puntual a este llamado), remezcla las balas.
  2. Reproduce la animación de giro (si se remezcló) y de apuntado
     hacia `"izquierda"` o `"derecha"`.
  3. Determina el resultado (`camaras[posicion]`) y avanza `posicion`
     una cámara para el próximo disparo (haya girado o no).
  4. Reproduce la animación/sonido de gatillo (bang o click).
  5. Devuelve `True` (salió bala) o `False` (chasquido en vacío).

  Por dentro, `disparar()` usa `renpy.call(...)` a un label interno del
  módulo, así el método puede mostrar pantallas y animar aunque se
  invoque como un método Python normal (`$ murio = ar.disparar(...)`).
  El dev maneja lo que pasa después del `return` en su propio guion.

- `ar.balas_restantes()` — cuántas balas sin disparar quedan en el
  tambor actual (para mostrar en pantalla, opcional).

### Mecánica de probabilidad (repaso de la decisión ya tomada)

- `girar_siempre=True`: cada disparo es independiente (probabilidad
  fija `balas/recamaras` en todo momento).
- `girar_siempre=False` (default, ruleta rusa "clásica" de película): el
  tambor avanza una posición por disparo sin volver a mezclar; la
  probabilidad de la próxima cámara depende de lo que ya salió.
- `ar.girar()` y el parámetro puntual `girar=` de `disparar()` permiten
  saltarse el modo por defecto del arma para un disparo/momento
  específico.

## 3) Visual (2D, sin 3D)

- Una sola imagen `arma.png` (silueta simple de revólver, generada como
  placeholder con PIL, apuntando a la derecha por defecto). El dev la
  reemplaza pasando su propia ruta de imagen.
- Animación 100% ATL, sin segunda imagen que alinear:
  1. **Giro**: rotación rápida con desaceleración (cantidad de vueltas y
     velocidad configurables) — simula el tambor girando.
  2. **Apuntado**: transición suave a la posición de descanso (derecha)
     o espejada horizontalmente (`xzoom=-1`, NO rotación de 180°, para
     que no quede "boca abajo") hacia la izquierda.
  3. **Gatillo**: pequeño golpe/recoil. Sonido opcional si el dev pasa
     `sonido_disparo=`/`sonido_vacio=` (sin audio por defecto, para no
     depender de efectos de sonido con licencia).

## 4) Archivos

```
game/modulos/ruleta_rusa/
├── modulo_ruleta_rusa.rpy
├── imagenes/arma.png
└── README.md
game/vistas/ejemplo_ruleta_rusa.rpy   <- demo (turnos NPC/jugador alternados)
```

Más una entrada nueva en el menú de `game/script.rpy`, igual que los
demás módulos de la librería.

## Fuera de alcance

- Apuntado a posiciones arbitrarias (x, y) o a más de dos lados: se deja
  fijo a `"izquierda"`/`"derecha"`, como en una VN estándar de dos
  personajes.
- Flujo de turnos automático o pantalla de "game over": el dev arma su
  propio label/menú alrededor de `ar.disparar()`, igual que con el resto
  de la librería.
- Efectos de sonido incluidos por defecto (licencias).
