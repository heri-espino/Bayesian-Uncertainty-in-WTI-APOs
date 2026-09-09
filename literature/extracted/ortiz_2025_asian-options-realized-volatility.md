---
id: "ortiz_2025_asian-options-realized-volatility"
source_pdf: "../pdf/ortiz_2025_asian-options-realized-volatility.pdf"
source_filename: "ortiz_2025_asian-options-realized-volatility.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "good"
extraction_score: 96.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 2
figures_png: 4
assets_dir: "../assets/ortiz_2025_asian-options-realized-volatility"
references_file: "../references/ortiz_2025_asian-options-realized-volatility.references.md"
---

<!-- p:1 -->

#### Revista Mexicana de Economía y Finanzas, Nueva Época

Volumen 21 Número 1, enero - marzo 2025, pp. 1-12, e1470

DOI: https://doi.org/10.21919/remef.v21i1.1470

(Recibido: 1/julio/2024, aceptado: 26/febrero/2025,

publicado: 7/noviembre/ 2025)

## Valuación de opciones asiáticas con volatilidad realizada y reversión a la media: caso CEMEXCPO

Ambrosio Ortiz Ramírez 1 - Instituto Politécnico Nacional, México Ana Lorena Jiménez Preciado - Instituto Politécnico Nacional, México

El objetivo de este trabajo es valuar opciones asiáticas con volatilidad realizada y reversión a la media sobre precio de CEMEXCPO mediante el método Monte Carlo. La dinámica del activo subyacente y su volatilidad son modelados bajo el enfoque de ecuaciones diferenciales estocásticas (EDE) correlacionadas. La estimación de los parámetros del sistema de  EDE  que  conduce  la  volatilidad  de  acuerdo  con  Bishwal  (2023).  La  aplicación  de  la  metodología  propuesta proporciona resultados suficientemente cercanos a los observados para opciones europeas en el Mercado Mexicano de Derivados (MexDer) para plazos cortos.

Classificación JEL: C63, C15, G13.

Palabras clave: simulación estocástica, método de Monte Carlo, opciones asiáticas.

## Asian options pricing with realized volatility and mean reversion: CEMEXCPO case

The objective of this  work  is  to  value  Asian  options  with  realized  volatility  and  mean  reversion  on  the CEMEXCPO price using the Monte Carlo method. The dynamics of the underlying asset and its volatility are modeled  under  the  correlated  stochastic  differential  equations  (SDE)  approach.  The  estimation  of  EDE system  parameters  drives  volatility  according  to  Bishwal  (2023).  The  application  of  the  proposed methodology provides results sufficiently close to those observed for European options in The Mexican Derivatives Exchange (MexDer) for short terms.

JEL Classification: C63, C15, G13.

Keywords: stochastic simulation, Monte Carlo method, Asian options.

Resumen

Abstract

1  Autor de correspondencia. Email: amortiz@ipn.mx . Instituto Politécnico Nacional, Escuela Superior de Economía

*Sin fuente de financiamiento para el desarrollo de esta investigación.

<!-- p:2 -->


## 1. Introducción

La incertidumbre generada por los mercados financieros en los que interactúan agentes requiere a las ciencias aplicadas metodologías robustas para la valuación de activos. Desde un enfoque teórico y  multidisciplinario  se  han  propuesto  diversas  metodologías  que  coadyuvan  en  el  análisis  y explicación de la aleatoriedad de los acontecimientos inherentes de la interacción de los mercados, con modelos innovadores para la valuación de activos, gestión de riesgos y el crecimiento económico, entre otros. Se puede afirmar que el mercado de capitales y la actividad económica forman parte de una  dinámica  compleja,  ya  que  la  operación  del  mercado  accionario  tiene  una  influencia  en  la actividad  económica  real,  véase  por  ejemplo  Brugger  y  Ortíz  (2012).  El  mercado  de  capitales mexicano aún con la pandemia de COVID19, ha sostenido una trayectoria creciente en los últimos años, sin embargo, se nota una gran diferencia respecto a sus socios comerciales del T-MEC debido al tamaño de sus economías, energéticos como el petróleo y gas, entre otros factores. Con un efecto negativo a nivel mundial está la crisis por la guerra de Ucrania y Rusia en 2022, crisis que ha escalado con  consecuencias  en  la  economía  mundial,  por  ejemplo,  la  demanda  de  gas  natural  en  Europa. (World Economic Forum, 2023).

En este contexto, los agentes asumen riesgos que proceden de las variaciones en precios de activos financieros. Tales variaciones pueden generar grandes pérdidas con efectos significativos. Una propuesta de solución a esto es el desarrollo y aplicación de derivados financieros. Un derivado se define como un instrumento financiero cuyo valor depende (o se deriva) de los valores de otras variables subyacentes más simples. Por lo general, tales variables subyacentes son precios de activos negociados  en  mercados  financieros.  La  negociación  de  opciones  asiáticas  en  un  mercado  de derivados es importante debido a sus beneficios para los participantes y su impacto en la economía en  sectores  clave  como  materias  primas  y  farmacéuticos  en  los  que  aranceles  pueden  afectar significativamente  los  costos  y  la  cadena  de  suministro,  estas  opciones  permiten  cubrir  riesgos asociados a cambios imprevistos en los precios de insumos o productos terminados.

En lo que respecta la utilización de derivados se encuentran las opciones financieras y para su valuación debe tenerse en cuenta los puntos siguientes: 1. Las opciones típicas o plain vanilla pueden ser de compra (call) o de venta (put),  que  también  se  distinguen  por  su  manera  de  ser ejercida, es decir: estilo europeo o americano, son listadas tanto en mercados de valores regulados como en mercados sobre mostrador o mercados Over The Counter (OTC). 2. Las opciones exóticas o de segunda generación, son las que impliquen una modificación a una o más variables de las opciones típicas y se negocian fundamentalmente en mercados OTC, estas surgen para atender requerimientos concretos de los agentes, en gran medida son acuerdos diseñados a la medida en cuanto a cantidad, calidad y tipo de subyacente, entre otros.

Las opciones asiáticas son de opciones de segunda generación, se negociaron en 1987 en Tokio, de ahí su nomenclatura. Su denominación proviene del hecho que su precio se determina en función de la dinámica del subyacente durante la vigencia del contrato. En particular, la valoración de  opciones  asiáticas  con  media  aritmética  es  una  línea  de  investigación  aún  por  explorar.  Por ejemplo, el promedio geométrico del precio es exactamente lognormal y el promedio aritmético es aproximadamente  lognormal  y  representa  un  problema  llegar  a  una  distribución  tratable  con procesos estocásticos usuales.


<!-- p:3 -->


En  general,  los  métodos  para  la  valoración  de  derivados  se  clasifican  en  analíticos  y numéricos. El primer enfoque es extenso para modelar funciones de pago de opciones con ecuaciones diferenciales  parciales  (EDP),  en  Pirjol  y  Zhu  (2017)  se  obtienen  aproximaciones  a  precios  de opciones asiáticas con ejercicio tanto fijo como flotante en el modelo de Black y Scholes. Asimismo, en  Koh  et  al.  (2019)  presentan  ejemplos  numéricos  con  diferencias  finitas.    En  el  trabajo  de Pergamenchtchikov y Shishkova (2020) se aborda el problema de cobertura de opciones asiáticas con costos de transacción al compensar los pagos de todas las transacciones, incluso si su número aumenta de forma ilimitada. En Bernal (2020) et al, se examina el efecto de los derivados sobre la relación  entre  el  tipo  de  cambio  y  el  mercado  de  valores  con  un  análisis  empírico  utilizando  la estrategia GMM para los mercados bursátiles de México y Brasil para el periodo 2007 a 2019. El resultado más importante es que además del tipo de cambio spot, los futuros de tipo de cambio explican la exposición cambiaria. En Gan, Wang y Yang (2020) se discuten las ventajas de las opciones asiáticas  con  subyacente  promedio  y  proponen  un  método  robusto  basado  en  aprendizaje automático  para  valuar  opciones  asiáticas  con  promedio  aritmético  y  geométrico  de  manera eficiente. Anceschi, et al (2021) prueban la existencia y unicidad de la solución fundamental para los operadores de Kolmogorov asociados a algunos procesos estocásticos que surgen en el método de portafolios replicantes en la determinación de precios en opciones dependientes de la trayectoria. Roul  (2022)  se  propone  un  enfoque  alternativo  basado  en  B-splines  exponenciales,  analizan  la volatilidad, la tasa y vigencia, y los valores delta relacionados con la aproximación al derivado.  En Alsenafi, Alazemi y Alavi (2025) valoran opciones asiáticas con promedio geométrico al plantear y resolver la ecuación diferencial parcial asociada que caracteriza el precio de la opción mediante la implementación de un algoritmo en tiempo semi discreto combinado con diferencias forward y Bsplines cúbicos.

En el caso de métodos numéricos se tiene al método de Monte Carlo, su amplio uso se debe a que permite encontrar soluciones aproximadas en modelación matemática que involucran procesos estocásticos.  Sin duda, el trabajo pionero de Boyle (1977) es el referente principal, así como Boyle et al. (1997).  En Larcher (2022) se desarrollan métodos de valuación de opciones asiáticas mediante simulación Monte Carlo con promedio geométrico y opciones de barrera con reducción de varianza con  varios  ejemplos  aplicados  a  diferentes  subyacentes.  En  Ewald,  Wu  y  Zhang  (2023)  obtienen fórmulas cerradas para el precio de opciones asiáticas sobre futuros de materias primas con los supuestos  de  tasas  de  conveniencia  y  tasa  de  interés  estocásticas  con  saltos.  Si  el  promedio  es geométrico y sin saltos hay una expresión analítica, en otros se toma tal resultado como variable de control para el precio de la opción asiática con promedio aritmético. En el caso de saltos primero condicionan los tiempos de salto y luego promedian las secuencias de saltos. En Abbasi y Nouri (2025) proponen la valuación de opciones asiáticas en un entorno de incertidumbre cuando el precio del subyacente es conducido por un modelo exponencial de Ornstein-Uhlenbeck y obtienen fórmulas cerradas  para  opciones  asiáticas  con  barrera  del  tipo  knock-in  y  knock-out  utilizando  alpha trayectorias de ecuaciones diferenciales. Algunas innovaciones en este enfoque extienden el método de Monte Carlo con modificaciones en la estructura de dependencia, véanse Kahalé (2021), Cruz-Aké, et al (2021), Alaya, et al. (2022) y Brignone et al. (2024) por mencionar algunos.

El presente trabajo difiere de otros en cuanto a que propone un procedimiento por simulación Monte Carlo para la valuación de opciones asiáticas con subyacente promedio en un sistema de EDE correlacionadas, en el cual la volatilidad se calibra con una adaptación del modelo CIR a volatilidad realizada, el procedimiento propuesto contrasta precios obtenidos con los publicados en el boletín de MexDer. Es importante señalar que hasta donde se conoce, no se cotizan este tipo de derivados en el MexDer, por lo que la metodología propuesta puede ser de utilidad para que en un futuro se listen este tipo de opciones como una alternativa de cobertura sobre otros subyacentes, tal y como sucede, por ejemplo, en el CBOE. Uno de los resultados interesantes que se obtienen, es que en el corto plazo los precios de opciones asiáticas y europeas son similares cuantitativamente, este hecho se explica porque el spot no difiere tanto del promedio, excepto en los extremos y plazos más largos.


<!-- p:4 -->


El resto de esta investigación se compone de la siguiente manera, en la siguiente sección se presenta la definición de opción asiática, la clasificación del promedio en tiempo discreto y continuo, luego, se describe el método para cuantificar calls y puts asiáticas con volatilidad dinámica en un sistema de EDE ́s con correlación. Se estiman los parámetros con una serie histórica de volatilidad realizada del subyacente y el modelo de Cox, Ingersoll y Ross, 1985 (CIR) según Bishwal (2023). En la tercera sección se presenta y discute la evidencia empírica del método propuesto, en esa parte los precios  calculados  son  comparados  con  los  del  boletín  del  portal  de  internet  del  Mexicano  de Derivados al 10 de julio 2023 para CEMEXCPO, en este caso para la tasa de interés se ocupa CETES que se recaba del portal de Banco de México. Se concluye con la cuarta sección.

## 2. Metodología

Como ya se ha comentado una clasificación de las opciones que depende de su estructura es opciones plain vanilla y opciones exóticas. En el segundo caso existe una gran variedad de tipos y su precio depende tanto de su precio final como de sus cambios en la temporalidad del contrato, por ejemplo, opciones asiáticas, con barrera y/o doble barrera tipo knock-in, knock-out (muy dependientes de la trayectoria), opciones bermuda pertenecen a esta clasificación.

Una  opción  asiática  es  aquella  en  la  que  el  pago  está  sujeto  al  promedio  aritmético  o geométrico del activo a lo largo de su vigencia. Por consiguiente, el pago de una opción asiática que vence en T está en función de una serie de observaciones X1, ... , Xn hechas fechas predefinidas 0 &lt; t 1 &lt; t2 &lt; ⋯ &lt; tn = T . Por  ejemplo,  se  puede  elegir  alguna  de  las  definiciones  de  promedio: aritmético Ma o geométrico Mg para caracterizar la función de pago de una opción asiática:

$$M _ { \alpha } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } X _ { i } \, ; \, M _ { g } = \left ( \prod _ { i = 1 } ^ { n } X _ { i } \right ) ^ { 1 / n } .$$

Asimismo, si se modela en tiempo discreto o continuo la media y se atribuyen pesos equitativos en su cálculo como se muestra en el Cuadro 1.

Cuadro 1 . Definición de la media.

| Media      | Tiempo discreto            | Tiempo continuo           |
|------------|----------------------------|---------------------------|
| Aritmética | 1 n ∑X t i n i=1           | 1 T ∫ X t T 0 dt          |
| Geométrica | (X t 1 , . . .,X t n ) 1/n | exp( 1 T ∫ ln T 0 X t dt) |

Fuente: elaboración propia.


<!-- p:5 -->


Existen varias  investigaciones  que  contemplan  alguno  de  los  casos  del  Cuadro  1  con  su correspondiente complejidad, véase el documento de Gan et al. (2020).

### 2.1. Estimación de parámetros y valoración de opciones con subyacente promedio

Un hecho empírico de varias variables económicas, como las tasas de interés, las tasas de inflación, volatilidad e incluso precios de materias primas, es que muestran una tendencia hacia niveles más bajos (niveles más altos), cuando son demasiado altos (bajos). Esta propiedad se denomina reversión a la media y se puede modelar utilizando un proceso estocástico, como en Hull y White (1987), Heston (1993),  Stojkoski  et  al.  (2020)  entre  otros.  En  la  práctica  sigue  representando  un  tópico  tanto numérico como computacional.

Considere  un  sistema  de  dos  EDE  para  calcular  el  precio  de  una  opción  asiática  con subyacente promedio, la primera modela el precio X t y la segunda la volatilidad σ t 2 = εt .

$$\begin{array} { c } \ m a t h s c r { D } _ { 0 } , \bar { a } \ p r i m a l { a } \ m o d e a l { e } \ p r i c { 0 } { \lambda _ { t } } \ y a l s e g n u d a l { a } \ v o l a c t { a } \ m a t h s c r { O } _ { t } - \varepsilon _ { t } . \\ \frac { d X _ { t } } { X _ { t } } = r d t + \sqrt { \eta _ { t } } d B _ { X _ { t } } \\ \quad d \varepsilon _ { t } = a ( b - \varepsilon _ { t } ) d t + \eta _ { t } \sqrt { \varepsilon _ { t } } d B _ { \varepsilon _ { t } } \end{array}$$

aquí BXt es  un  movimiento browniano correlacionado con Bvt ,  es  decir Cov (dBXt , dB εt ) = ρdt, a &gt; 0,  b &gt; 0 y ηt &gt; 0 con valores constantes. Se dice que la segunda EDE tiene reversión a la media puesto que si εt &lt; b , entonces la parte determinista a(b - εt ) &gt; 0 y se anticipa una subida de volatilidad o si εt &gt; b entonces a(b - εt ) &lt; 0 y  se  espera  una  bajada.  Para  simular  el  sistema se plantea una dependencia:

$$d \tilde { B } = \begin{pmatrix} d B _ { X _ { t } } \\ d B _ { \varepsilon _ { t } } \end{pmatrix} \sim \mathcal { N } ( 0 , \Sigma ) ,$$

con la descomposición de Choleski en

$$\Sigma = \begin{pmatrix} \Delta t & \rho _ { \varepsilon _ { t } , X _ { t } } \Delta t \\ \rho _ { X _ { t } , \varepsilon _ { t } } \Delta t & \Delta t \end{pmatrix} .$$

Para ello en primero lugar se calcula S dado  que Σ = SS ⊤ y  plantear  la  distribución  de dW~N(0,IW 2 ) para obtener dB ̃ = XdW , como se muestra más adelante en la discretización de (1) por lo regular se elige a Δt = T/M con M = 252, luego se aplica con el método de Barraquand (1995) generar  muestras  de dW ,  que  incorpora  a dB ̃ implícitamente.  Sean  las  matrices  de  media  y covarianzas de dW :

$$\mu _ { W } = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \ y \ \Sigma _ { W } = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$$

Al discretizar el sistema dado en (14) y por el método Monte Carlo se ejecuta la valoración de opciones.  Bajo  esas  condiciones  si c XT denota  el  precio  del  call  y pXT el  del  put  con  subyacente promedio y precio de ejercicio E:

$$c _ { X _ { T } } = \max \left ( \frac { 1 } { T } \int _ { 0 } ^ { T } X _ { \tau } d \tau - E , 0 \right ) \quad y \quad p _ { X _ { T } } = \max \left ( E - \frac { 1 } { T } \int _ { 0 } ^ { T } X _ { \tau } \, d \tau , 0 \right ) .$$


<!-- p:6 -->


En concreto, el procedimiento para la valoración de las opciones se presenta a continuación:

- 1) Se definen dBXt y dBεt como:

$$d B _ { X _ { t } } ^ { ( k ) } & = W _ { X _ { t } } ^ { ( k ) } \sqrt { \Delta t } \\ d B _ { \varepsilon _ { t } } ^ { ( k ) } & = \rho W _ { \varepsilon _ { t } } ^ { ( k ) } \sqrt { \Delta t } + \sqrt { 1 - \rho ^ { 2 } } W _ { \varepsilon _ { t } } ^ { ( k ) } \sqrt { \Delta t }$$

- 2) Estimar los parámetros: a, b and η .
- 3) Discretizar el sistema de EDE en un esquema de Euler (Venegas, 2008, p. 856):

$$\varepsilon ( t _ { i + 1 } ) ^ { ( q ) } & = a _ { i } ^ { ( q ) } + b \left ( \theta - \varepsilon ( t _ { i } ) ^ { ( q ) } \right ) \Delta t + \eta \sqrt { \varepsilon ( t _ { i } ) ^ { ( q ) } } \Delta B _ { \varepsilon _ { t } } ^ { ( q ) } \\ X _ { i + 1 } ^ { ( q ) } & = X _ { i } ^ { ( q ) } \left ( 1 + \varepsilon ( t _ { i } ) ^ { ( q ) } \Delta t + \varepsilon ( t _ { i } ) ^ { ( q ) } \Delta B _ { X _ { t } ^ { ( q ) } } ^ { ( q ) } \right ) , \ \ i = 1 , \dots , p - 1 .$$

- 4) Calcular el promedio X ̄ (q) de los valores finales de cada trayectoria:

$$\ e d i o { X } ^ { ( n ) } \det \text {ios valences in matrices of } c a d a \text { rayectura} \colon \\ \bar { X } ^ { ( q ) } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } X _ { i } ^ { ( q ) } .$$

- 5) Calcular precios de las opciones call y put:

y

$$\hat { c } = e ^ { - r T } \frac { 1 } { j } \sum _ { k = 1 } ^ { j } \max ( \bar { X } ^ { ( q ) } - E , 0 )$$

$$\hat { p } = e ^ { - r T } \frac { 1 } { j } \sum _ { k = 1 } ^ { j } \max ( E - \bar { X } ^ { ( q ) } , 0 )$$

donde j se ocupa en un ciclo de la simulación para generar q precios asociados a (4). El procedimiento anterior puede configurarse tal que es factible modificar la función de pago a otro tipo de derivado.

## 3. Aplicación de la metodología

Con los pasos descritos en la sección anterior se ejecutan simulaciones en Matlab (c) para valorar opciones asiáticas con subyacente promedio sobre CEMEXCPO. Se contrastan los resultados con la información del boletín de MexDer del 10 de julio de 2023. La tasa CETES se recaba de la página de Banco de México y se ejecuta interpolación donde se requiere. Los coeficientes de modelo CIR a volatilidad realizada se estiman según Bishwal (2023). El periodo de estudio de volatilidad realizada del subyacente es del 3 de enero de 2022 al 10 de julio de 2023 con 383 observaciones. La Gráfica 1 exhibe  variaciones  logarítmicas  de  CEMEXCPO  y  la  serie  de  volatilidad  diaria.  Se  observan variaciones importantes con ascensos y descensos en el periodo de la muestra.


<!-- p:7 -->


Gráfica 1 . Variaciones logarítmicas diarias de CEMEXCPO y volatilidad realizada.

Fuente: elaboración propia.

Los coeficientes estimados con el método de Overbeck y Rydén (1997) y su extensión en Bishwal (2023) para el modelo CIR dados en el Cuadro 2.

Cuadro 2 . Coeficientes estimados.

| Coeficiente   |        a |        b |        η |   No. Obs. |   Cociente de verosimilitud |
|---------------|----------|----------|----------|------------|-----------------------------|
| valor         | 2.222742 | 0.028964 | 0.008282 |        383 |                    7.928659 |

Fuente: Elaboración propia.

Gráfica 2 . Trayectorias simuladas.

Fuente: elaboración propia.

400


<!-- p:8 -->


Con los coeficientes en el Cuadro 2, el lector puede comprobar que 2ab ≥ η 2 , que se conoce como propiedad de positividad de Feller, que asegura que la primera EDE en (1) no tocará el cero. La Gráfica 2 presenta trayectorias con la segunda EDE en (1) y la serie original de volatilidad. Se observa que las trayectorias son consistentes con la tendencia alcista que proviene de la inercia del precio del activo.  En  la  Gráfica  3  se  exhiben  precios  de  calls  y  puts  de  tipo  europeo,  y  precios  de  opciones asiáticas con la metodología descrita anteriormente, los plazos que se obtienen del boletín son T = 70, 161, 252 y 343 días, los precios de ejercicio comienzan en $10 a $23 con variaciones uniformes de $0.50.  Los precios calculados se contrastan con los del boletín del 10/07/2023, en ese día el precio de cierre de CEMEXCPO fue de $16.71. La simulación Monte Carlo es con m = 50,000 trayectorias y una correlación inicial de ρ = -0.5.

Gráfica 3 . Precios de opciones europeas reportados por MexDer a cuatro plazos comparados con las opciones asiáticas obtenidos por simulación Monte Carlo.

Fuente: elaboración propia.

La información del boletín señala que son veintisiete precios de ejercicio, en catorce de ellos el precio de CEMEXCPO es mayor que el precio de ejercicio para opciones de compra; para opciones de venta solo en trece. Con el propósito de observar la diferencia de precios entre los publicados por MexDer y los obtenidos con la metodología propuesta se muestran en la Gráfica 4, al compararlos se observa que conforme el plazo aumenta la diferencia se incrementa. Esto se debe a que en el corto plazo  el  precio  spot  del  subyacente  no  difiere  significativamente  del  promedio,  por  ello  en  para opciones de compra con subyacente promedio in the money son cero, mientras que para opciones de venta con subyacente promedio out of the money ocurre lo mismo.


<!-- p:9 -->


Gráfica 4. Diferencias de precios publicados por MexDer y los calculados de opciones asiáticas con promedio del subyacente, tanto de compra como de venta a los cuatro plazos

Fuente: elaboración propia.

Al contrastar los calls y puts de tipo europeo a plazo de 70 días y la información del portal de internet  de  MexDer  el  10  de  julio  2023  con  los  precios  simulados  para  asiáticas,  resultan  ser semejantes, sin embargo, para los otros vencimientos de 161, 252 y 353, la distancia de precios es notoria. Una posible explicación de este hecho es que la volatilidad del promedio aritmético muestra poca variación.  En resumen, la evidencia empírica permite inferir que en el corto plazo los precios de opciones asiáticas y europeas son similares cuantitativamente, que se explica debido a que el spot es cercano al promedio aritmético, excepto en los extremos y plazo al vencimiento mayores.

## 4. Conclusiones

Las opciones asiáticas son derivados cuyos pagos dependen del valor promedio del precio del activo subyacente durante un período de tiempo establecido previamente. La gran mayoría de las funciones de pago asociadas a este tipo de instrumentos no permiten una solución analítica y, por lo tanto, con frecuencia se encuentran soluciones aproximadas dependiendo del enfoque con el que se aborde el problema. En esta investigación se ha propuesto una metodología basada en simulación Monte Carlo para la valuación de opciones asiáticas con volatilidad realizada y reversión a la media.


<!-- p:10 -->


En este trabajo se valúan calls y puts de tipo europeo, y con precio promedio (asiática) con media aritmética sobre CEMEXCPO con el método de Monte Carlo. Una estructura de dos EDE ́s modela precios y su volatilidad con correlación arbitraria. Se estiman los parámetros de la EDE que conduce  la  volatilidad  de  acuerdo  con  Overbeck  y  Rydén  (1997)  y,  más  recientemente,  Bishwal (2023) en tiempo discreto al modelo CIR con volatilidad realizada. Se usa el método propuesto en Barraquand (1995) en el esquema de discretización de Euler. La evidencia empírica muestra que en el  corto  plazo  los  precios  de  opciones  asiáticas  y  europeas  son  muy  cercanos,  este  hecho  puede explicarse porque el spot no difiere tanto del promedio, excepto en los extremos y plazos más largos. Estos resultados pueden ser útiles para un agente que busca una cobertura con costos más asequibles o incluso podría formar parte de la oferta de contratos de opciones en MexDer como se estila en otros mercados  organizados.  A  nivel  macroeconómico,  la  adopción  de  este  tipo  de  instrumentos financieros  fomenta  la  estabilidad  del  mercado,  atrae  inversiones  y  promueve  el  crecimiento económico.  Además,  al  mitigar  los  riesgos  asociados  a  los  aranceles,  se  facilita  el  comercio internacional y se protege la competitividad de sectores estratégicos, contribuyendo al desarrollo sostenible de la economía.

No obstante, los supuestos parsimoniosos de la metodología propuesta en este trabajo los resultados son enriquecedores en el sentido que un contrato con opciones asiáticas representaría una recomendación para un agente que prefiere un riesgo moderado sobre un subyacente como puede ser el precio de la mezcla mexicana de exportación u otras materias primas, bonos cupón cero y con cupón, en los mercados de: divisas, criptomonedas, energía o en el mercado OTC.  En lo que se refiere  a  la  metodología  se  puede  ampliar  al  planteamiento  y  solución  de la  ecuación  diferencial parcial con los supuestos del modelo o al uso de variables antitéticas en la simulación Monte Carlo o añadir la presencia de saltos en tiempo discreto o continuo.
