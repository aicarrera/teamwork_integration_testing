# Taller de Integration Testing — OrderSystem

Bienvenidos al taller práctico de **Pruebas de Integración en Python**. Trabajarán
en **equipos de 5** aplicando las estrategias **Top-Down** y **Bottom-Up** sobre un
sistema de procesamiento de pedidos por capas. Su nota (0–100) se calcula
**automáticamente** con GitHub Actions.

---

## 🚀 EMPIEZA AQUÍ (lo PRIMERO que debe hacer el equipo)

> 🛑 **No hagas _Fork_ ni clones este repositorio directamente.** Sigue estos pasos.

**Paso 1 — UN solo integrante** crea el repositorio del equipo con el botón verde
**"Use this template" → "Create a new repository"**:

![Botón Use this template](docs/usar-plantilla.png)

**Paso 2 —** ese integrante agrega a los otros 4 como colaboradores:
`Settings → Collaborators → Add people`.

**Paso 3 — los 5 integrantes** clonan el repositorio **del equipo** (no este):
usen el botón **"Code" → HTTPS** para copiar la URL y luego:

```bash
git clone https://github.com/EL-EQUIPO/su-repo-del-equipo.git
```


## 📌 Contexto del sistema

`OrderSystem` está dividido en 4 capas:

| Capa | Módulo | Responsabilidad | ¿Existe hoy? |
| :--: | ------ | --------------- | ------------ |
| 1 | `app/cli.py` | Interfaz de línea de comandos (UI) | ✅ Sí |
| 2 | `app/order_service.py` | Lógica de negocio (IVA, stock, pagos) | ✅ Sí |
| 3 | `app/payment_gateway.py` | Pasarela de pagos externa (HTTP) | ❌ **No desplegada** |
| 4 | `app/db_connector.py` | Persistencia / Base de datos | ❌ **No desplegada** |

> ⚠️ **Premisa clave:** la base de datos (Capa 4) y la API de pagos (Capa 3)
> **aún no existen**. Sus métodos lanzan errores de conexión si se ejecutan
> directamente. Deben probar la integración del sistema **antes** de que la
> infraestructura real esté disponible, usando dobles de prueba (mocks, stubs,
> fakes e interceptores HTTP).

**Top-Down** ⬇️ empieza por las capas altas y simula las bajas.
**Bottom-Up** ⬆️ construye y prueba primero las capas base y va integrando hacia arriba.

---

## 👥 Asignación de roles (cada quien trabaja en UN archivo)

| # | Rol | Archivo a completar | Estrategia | Herramienta clave |
| :-: | --- | ------------------- | ---------- | ----------------- |
| 1 | Top-Down · Nivel Superior | `tests/top_down/test_cli.py` | Top-Down | `pytest-mock` (`mocker.patch`) |
| 2 | Top-Down · Nivel Medio | `tests/top_down/test_service.py` | Top-Down | `unittest.mock.MagicMock` |
| 3 | Bottom-Up · Persistencia | `tests/bottom_up/test_db_driver.py` | Bottom-Up | `pytest.fixture` (Fake en memoria) |
| 4 | Bottom-Up · Red/Pagos | `tests/bottom_up/test_payment_driver.py` | Bottom-Up | `requests-mock` |
| 5 | Bottom-Up · Driver Integrador | `tests/bottom_up/test_full_integration.py` | Bottom-Up E2E | Fake (3) + requests-mock (4) + `OrderService` real |

Cada archivo trae un **ejemplo resuelto** y una lista de **`# TODO`** que deben completar.

> 💡 El Integrante 5 **reutiliza** el `FakeDb` del Integrante 3 y la técnica del
> Integrante 4. ¡Coordínense: sus piezas encajan!

---

## 🗂️ Estructura del proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── cli.py                 # Capa 1
│   ├── order_service.py       # Capa 2
│   ├── payment_gateway.py     # Capa 3 (no desplegada)
│   └── db_connector.py        # Capa 4 (no desplegada)
├── tests/
│   ├── top_down/
│   │   ├── test_cli.py            # Integrante 1
│   │   └── test_service.py        # Integrante 2
│   └── bottom_up/
│       ├── test_db_driver.py      # Integrante 3
│       ├── test_payment_driver.py # Integrante 4
│       └── test_full_integration.py # Integrante 5
├── scripts/
│   └── calculate_grade.py     # Motor de autoevaluación (0–100)
├── .github/workflows/
│   └── autograding.yml        # Ejecuta la nota en cada push a main
├── requirements.txt
├── setup.cfg                  # Configuración de mutmut
├── pytest.ini
└── conftest.py
```

---

## 🚀 Puesta en marcha (local)

Requisito: **Python 3.11+**.

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Ejecutar **todas** las pruebas:

```bash
pytest -v
```

Ejecutar **solo tu archivo** mientras trabajas:

```bash
pytest tests/top_down/test_cli.py -v
```

Ver los **`print(...)`** de tu código y tus tests (pytest los oculta por defecto):

```bash
pytest tests/top_down/test_cli.py -v -s
```

Simular **tu nota completa** localmente (igual que en GitHub):

```bash
python scripts/calculate_grade.py
```

---

## 🤖 ¿Cómo se calcula la nota? (0–100)

La calificación se ejecuta con **GitHub Actions** en cada `push` a `main` y se
compone de **dos pasos**:

### 1. PyTest Execution — **20 %**
Verifica que **las pruebas del equipo pasen** sobre el código sano.
Puntos = `20 × (pruebas que pasan / pruebas totales)`.

### 2. Mutation Testing con `mutmut` — **80 %**
Se introducen **mutaciones** en el código de `app/` (cambiar `>` por `>=`,
`+` por `-`, el 16 % del IVA, textos, etc.). Cada mutación crea un "mutante".

- Si **alguna prueba falla** con el código mutado → el mutante fue **detectado (killed)** ✅
- Si **todas las pruebas pasan** con el código mutado → el mutante **sobrevivió** ❌

Puntos = `80 × (mutantes killed / mutantes totales)`.

> 🎯 **La lección:** que tus pruebas "pasen en verde" no basta. Solo unas
> pruebas con **buenas aserciones** matan mutantes. El mutation testing mide la
> **calidad real** de sus pruebas, no solo su existencia.

> 🔎 Nota: `app/db_connector.py` se **excluye** de la mutación a propósito
> (es un stub de una BD que no existe y se reemplaza por un Fake).

**Nota final = Paso 1 + Paso 2** (máximo 100).

---

## 📊 ¿Dónde veo mi nota?

1. Haz `push` a la rama `main` de **su** repositorio (creado desde la plantilla).
2. Entra a la pestaña **Actions** del repo en GitHub.
3. Abre la última ejecución del workflow **“Autograding”**.
4. En la vista de resumen (**Summary**) verás una tabla como esta:

| Paso | Métrica | Detalle | Puntos |
| --- | --- | --- | --- |
| 1. PyTest Execution | 100.0 % pruebas OK | 15/15 pruebas pasan | **20.00 / 20** |
| 2. Mutation Testing | 87.5 % mutantes 💀 | 28/32 mutantes asesinados | **70.00 / 80** |

### 🏆 NOTA FINAL: **90.00 / 100**

La nota se **recalcula en cada push**: mejoren sus aserciones y verán subir el número.

---

## 🧭 Flujo de trabajo recomendado para el equipo

1. Un integrante crea el repositorio del grupo **desde la plantilla**
   (botón _“Use this template”_) y añade a los demás como colaboradores.
2. Cada quien trabaja en **su archivo** de `tests/` (idealmente en su propia rama).
3. Hagan _commits_ pequeños y frecuentes; corran `pytest` en local antes de subir.
4. Integren todo en `main` mediante Pull Requests.
5. Revisen la pestaña **Actions** para ver cómo evoluciona la nota del equipo.

> ✅ **No modifiquen `app/`.** Su trabajo es escribir **pruebas**. Cambiar el
> código de la aplicación para "subir la nota" invalida el ejercicio.

¡Éxitos! 🚀
