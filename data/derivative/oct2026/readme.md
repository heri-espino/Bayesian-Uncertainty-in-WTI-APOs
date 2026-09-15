# Opciones WTI Average Price — octubre de 2026

## Contenido

Esta carpeta contiene 31 series diarias de opciones de Crude Oil WTI Average Price con vencimiento en octubre de 2026 (`JAOV6`):

```text
jaov6_<strike>c_price-history-09-12-2026.csv  # call
jaov6_<strike>p_price-history-09-12-2026.csv  # put
```

Los archivos suman 356 observaciones, con fechas disponibles entre **2026-08-18** y **2026-09-11**. Son contratos recientes; por ello, aunque la consulta se configuró para buscar hasta dos años, no existe historia anterior para la mayoría de las series.

## Verificación de la ventana de dos años

De las 31 páginas fuente, 28 muestran explícitamente `Select History: 2 Years`. Los archivos `18.md`, `26.md` y `30.md` no muestran esa selección y solo aportan 1, 1 y 5 sesiones, respectivamente. La trazabilidad completa está en [coverage_report.csv](coverage_report.csv); no se debe interpretar que esos tres contratos tengan un historial completo de dos años.

## Formato de los CSV

| Columna | Descripción |
| --- | --- |
| `Time` | Fecha de sesión en formato `YYYY-MM-DD`. |
| `Open`, `High`, `Low`, `Latest` | Precios de Barchart. |
| `Change`, `%Change` | Variación diaria absoluta y porcentual. |
| `Volume` | Volumen negociado. |
| `Open Int` | Interés abierto. |

Los CSV están en UTF-8 con BOM, tienen exactamente nueve columnas y no incluyen textos de navegación de Barchart. Cuando Barchart registra `unch`, se normaliza a `0` y `0.00%` para mantener columnas analizables.

## Reproducibilidad

Las páginas originales están en `01.md`–`31.md`. Ejecuta `python convert_oct2026_barchart.py` desde esta carpeta para regenerar los CSV y el reporte de cobertura. Comprueba el símbolo, strike y derecho antes de mezclar contratos.

## Contexto de derivados: opciones *Average Price* cerca del dinero

Estas son opciones de precio promedio, también llamadas opciones asiáticas. Su pago al vencimiento depende del promedio del subyacente durante el periodo de promediación, no únicamente del precio final. Si `K` es el strike y `S̄` el precio promedio del subyacente:

- Call: `max(S̄ − K, 0)`.
- Put: `max(K − S̄, 0)`.

El filtro **Near the Money** de Barchart muestra strikes alrededor del precio vigente del subyacente. En la definición de la página, las calls cercanas al dinero tienen strike menor que el último precio y las puts, strike mayor. Es un filtro de pantalla, no una clasificación fija: se mueve con el precio del subyacente.

### Prima, liquidez y tamaño del contrato

El valor de un punto de opción es **USD 1,000**. La prima en dólares se obtiene como `Latest × 1,000`; por ejemplo, `6.72` corresponde a USD 6,720 por contrato. La prima es el valor de la opción antes del vencimiento; no es el payoff final, que depende de `S̄`.

`Volume` representa contratos negociados durante la sesión en un strike; `Open Int`, contratos abiertos que siguen vigentes. Un `N/A` indica ausencia de cotización o de dato reportado, no un valor económico de cero. Los CSV son historiales diarios por contrato y no incluyen bid, ask, volatilidad implícita ni griegas.

### Snapshot de Barchart del 11-sep-2026

La página reporta el subyacente **Crude Oil WTI Oct ’26 (`CLV26`)** en `100.05`, 48 días al vencimiento (30-oct-2026), y punto de opción de USD 1,000. Los totales de la página son:

| Métrica | Valor |
| --- | ---: |
| Prima total de calls | USD 1,883,580 |
| Prima total de puts | USD 11,170 |
| Ratio prima put/call | 0.01 |
| Interés abierto total de calls | 22,379 |
| Interés abierto total de puts | 32,152 |
| Ratio de interés abierto put/call | 1.44 |

Los totales se calculan sobre **todos los strikes** de Barchart, no únicamente sobre el filtro *near the money*. Son una fotografía de una fecha, útil como contexto descriptivo pero no como señal de trading aislada.
