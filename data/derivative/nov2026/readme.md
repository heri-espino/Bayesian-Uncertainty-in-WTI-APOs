# Opciones WTI Average Price — noviembre de 2026

## Contenido

Esta carpeta reúne 28 series diarias de opciones de Crude Oil WTI Average Price con vencimiento en noviembre de 2026 (`JAOX6`). Cada archivo corresponde a un strike y derecho específicos:

```text
jaox6_<strike>c_price-history-09-12-2026.csv  # call
jaox6_<strike>p_price-history-09-12-2026.csv  # put
```

En conjunto hay 2,876 observaciones. La cobertura disponible va del **2025-05-21** al **2026-09-11**. Esta ventana está dentro de los últimos dos años; que no llegue a una fecha más antigua refleja el inicio de cotización de cada contrato, no un relleno de datos.

## Formato de los CSV

Todos los archivos usan UTF-8 con BOM y estas columnas:

| Columna | Descripción |
| --- | --- |
| `Time` | Fecha de la sesión, en formato `YYYY-MM-DD`. |
| `Open`, `High`, `Low`, `Latest` | Precios informados por Barchart. |
| `Change`, `%Change` | Cambio absoluto y porcentual de la sesión. |
| `Volume` | Volumen negociado. |
| `Open Int` | Interés abierto. |

## Fuente y reproducibilidad

Los datos provienen de las tablas **Daily Prices / Price History** de Barchart. Las páginas copiadas se conservaron como `.md` y el script de conversión genera los CSV eliminando texto de navegación, notas y pie de página. Revisa siempre el símbolo, strike y derecho antes de combinar series.

## Uso rápido

```python
import pandas as pd

prices = pd.read_csv("jaox6_9000p_price-history-09-12-2026.csv")
prices["Time"] = pd.to_datetime(prices["Time"])
```

## Contexto de derivados: opciones *Average Price* cerca del dinero

Estas son opciones de precio promedio, también llamadas opciones asiáticas. A diferencia de una opción vanilla, el pago al vencimiento depende del promedio del subyacente durante el periodo de promediación. Si `K` es el strike y `S̄` el promedio del subyacente:

- Call: `max(S̄ − K, 0)`.
- Put: `max(K − S̄, 0)`.

El filtro **Near the Money** de Barchart muestra strikes alrededor del precio vigente. En la definición de la página, las calls cercanas al dinero tienen strike menor que el último precio y las puts, strike mayor. La etiqueta no es permanente: cambia cuando cambia el precio del subyacente.

### Prima, liquidez y tamaño del contrato

Cada punto de opción vale **USD 1,000**. La prima en dólares de una cotización se calcula como `Latest × 1,000`; una cotización de `3.22`, por ejemplo, equivale a USD 3,220 por contrato. La prima es el precio de la opción antes del vencimiento y no el payoff final, que depende de `S̄`.

`Volume` es el número de contratos negociados en la sesión para ese strike. `Open Int` es el número de contratos abiertos que no se han liquidado mediante una operación compensatoria. Un `N/A` indica que Barchart no reportó una cotización o el campo; no equivale a cero. Los historiales CSV no contienen bid, ask, volatilidad implícita ni griegas.

### Snapshot de Barchart del 11-sep-2026

La página reporta el subyacente **Crude Oil WTI Nov ’26 (`CLX26`)** en `95.94`, 79 días al vencimiento (30-nov-2026), y punto de opción de USD 1,000. Los totales son:

| Métrica | Valor |
| --- | ---: |
| Prima total de calls | USD 1,510,540 |
| Prima total de puts | USD 33,430 |
| Ratio prima put/call | 0.02 |
| Interés abierto total de calls | 21,444 |
| Interés abierto total de puts | 31,916 |
| Ratio de interés abierto put/call | 1.49 |

Los totales cubren **todos los strikes** mostrados por Barchart, no solo el subconjunto *near the money*. Son una fotografía descriptiva de la fecha indicada y no constituyen por sí solos una recomendación de inversión.
