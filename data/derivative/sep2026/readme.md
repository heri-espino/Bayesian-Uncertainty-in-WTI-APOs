# Opciones WTI Average Price — septiembre de 2026

## Contenido

Esta carpeta reúne 30 series diarias de opciones de Crude Oil WTI Average Price con vencimiento en septiembre de 2026 (`JAOU6`). Los archivos se nombran por contrato:

```text
jaou6_<strike>c_price-history-09-12-2026.csv  # call
jaou6_<strike>p_price-history-09-12-2026.csv  # put
```

En conjunto contienen 2,963 observaciones, desde **2025-11-06** hasta **2026-09-11**. La cobertura está dentro de una consulta de hasta dos años; una historia menor para alguna opción puede deberse a la fecha en que comenzó a cotizar.

## Formato de los CSV

| Columna | Descripción |
| --- | --- |
| `Time` | Fecha de sesión, en formato `YYYY-MM-DD`. |
| `Open`, `High`, `Low`, `Latest` | Precios informados por Barchart. |
| `Change`, `%Change` | Cambio absoluto y porcentual diario. |
| `Volume` | Volumen negociado. |
| `Open Int` | Interés abierto. |

Todos los CSV usan UTF-8 con BOM y nueve columnas homogéneas, por lo que se pueden cargar directamente con Excel, pandas o R.

## Fuente y buenas prácticas

La fuente es Barchart Price History. Cada serie representa un contrato distinto: no combines calls, puts ni strikes sin añadir identificadores de contrato. Conserva este README junto con los datos para mantener la procedencia, la cobertura y la convención de nombres.

## Contexto de derivados: opciones *Average Price* cerca del dinero

Estas son opciones de precio promedio, también llamadas opciones asiáticas. A diferencia de una opción vanilla, su pago al vencimiento depende del promedio del subyacente durante el periodo de promediación, no únicamente del precio final. Si `K` es el strike y `S̄` el precio promedio del subyacente:

- Call: `max(S̄ − K, 0)`.
- Put: `max(K − S̄, 0)`.

El filtro **Near the Money** de Barchart muestra strikes alrededor del precio vigente del subyacente. En la definición de la página, las calls cercanas al dinero tienen strike menor que el último precio y las puts, strike mayor. Es un filtro de pantalla, no una clasificación fija: puede cambiar cuando se mueve el subyacente.

### Prima, liquidez y tamaño del contrato

El valor de un punto de opción es **USD 1,000**. Por eso, la prima en dólares de una cotización se obtiene como `Latest × 1,000`; por ejemplo, una cotización de `2.50` equivale a una prima de USD 2,500 por contrato. La prima es el precio de la opción antes del vencimiento; no debe confundirse con el payoff final, que depende de `S̄`.

`Volume` mide contratos negociados durante la sesión para ese strike; `Open Int` mide contratos abiertos que siguen vigentes. Un valor `N/A` significa que Barchart no reportó la cotización o el campo, no que el valor económico sea cero. Estos CSV contienen el historial diario; bid, ask, prima agregada, volatilidad implícita y griegas no están en las columnas descargadas.

### Snapshot de Barchart del 11-sep-2026

La página de opciones reporta el subyacente **Crude Oil WTI Oct ’26 (`CLV26`)** en `100.05`, 18 días al vencimiento (30-sep-2026), y punto de opción de USD 1,000. Los totales reportados son:

| Métrica | Valor |
| --- | ---: |
| Prima total de calls | USD 2,144,490 |
| Prima total de puts | USD 470 |
| Ratio prima put/call | 0.00 |
| Interés abierto total de calls | 20,246 |
| Interés abierto total de puts | 29,805 |
| Ratio de interés abierto put/call | 1.47 |

Estos totales se calculan sobre **todos los strikes** de la página, no solo los contratos *near the money* guardados aquí. Son una fotografía de una fecha y no una señal de trading por sí misma.
