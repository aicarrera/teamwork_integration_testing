"""INTEGRANTE 3 — Bottom-Up · Nivel Base (Persistencia)
================================================================

OBJETIVO
    La base de datos real (Capa 4) AÚN NO EXISTE. Debes construir un
    "Fake State Driver": un doble de prueba EN MEMORIA que implemente el mismo
    contrato que `app.db_connector.DbConnector` y que, a diferencia de un Mock,
    MANTENGA ESTADO (el stock baja cuando se descuenta, los pedidos se guardan).

    Este Fake será la pieza base sobre la que el Integrante 5 montará el test
    de integración ascendente.

TÉCNICA
    - Estrategia: Bottom-Up (construyes primero lo de abajo).
    - Herramienta: `pytest.fixture` que provee el Fake con estado inicial.

CONTRATO A IMPLEMENTAR (igual que DbConnector):
    - get_stock(product_id) -> int
    - get_price(product_id) -> float
    - save_order(order) -> str
    - update_stock(product_id, new_stock) -> None
"""

import pytest


class FakeDb:
    """Driver de BD EN MEMORIA (mantiene estado real entre llamadas)."""

    def __init__(self, stock: dict[str, int], prices: dict[str, float]):
        self._stock = dict(stock)
        self._prices = dict(prices)
        self._orders: dict[str, dict] = {}
        self._seq = 0

    def get_stock(self, product_id: str) -> int:
        return self._stock[product_id]

    def get_price(self, product_id: str) -> float:
        return self._prices[product_id]

    def save_order(self, order: dict) -> str:
        self._seq += 1
        order_id = f"ORD-{self._seq}"
        self._orders[order_id] = dict(order)
        return order_id

    def update_stock(self, product_id: str, new_stock: int) -> None:
        self._stock[product_id] = new_stock

    # Ayudas para las aserciones de las pruebas.
    @property
    def orders(self) -> dict[str, dict]:
        return self._orders


@pytest.fixture
def fake_db():
    """Fixture reutilizable: BD en memoria con datos de arranque conocidos."""
    return FakeDb(
        stock={"SKU-1": 10, "SKU-2": 0},
        prices={"SKU-1": 100.0, "SKU-2": 50.0},
    )


# --- EJEMPLO RESUELTO ------------------------------------------------------
def test_fake_db_lee_estado_inicial(fake_db):
    assert fake_db.get_stock("SKU-1") == 10
    assert fake_db.get_price("SKU-1") == 100.0


# --- TODO INTEGRANTE 3 -----------------------------------------------------
# TODO 1: El estado cambia de verdad.
#   - Llama a `fake_db.update_stock("SKU-1", 7)` y verifica que
#     `fake_db.get_stock("SKU-1") == 7`. (Un Mock no haría esto solo.)
def test_fake_db_actualiza_stock(fake_db):
    pytest.skip("TODO pendiente: completa este test (Integrante responsable).")


# TODO 2: Guardado de pedidos.
#   - Guarda un pedido con `save_order({...})` y verifica que:
#       * devuelve un id no vacío,
#       * ese id aparece en `fake_db.orders`,
#       * dos pedidos guardados reciben ids DISTINTOS.
def test_fake_db_guarda_pedidos_con_id_unico(fake_db):
    pytest.skip("TODO pendiente: completa este test (Integrante responsable).")


# TODO 3 (opcional): decide qué hacer ante un producto inexistente.
#   - Documenta y prueba el comportamiento (p. ej. `KeyError`) para dejar
#     claro el contrato del Fake al resto del equipo.
def test_fake_db_producto_inexistente(fake_db):
    pytest.skip("TODO pendiente: completa este test (Integrante responsable).")
