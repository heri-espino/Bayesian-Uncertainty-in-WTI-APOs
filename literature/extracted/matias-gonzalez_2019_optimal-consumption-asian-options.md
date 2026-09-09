---
id: "matias-gonzalez_2019_optimal-consumption-asian-options"
source_pdf: "../pdf/matias-gonzalez_2019_optimal-consumption-asian-options.pdf"
source_filename: "matias-gonzalez_2019_optimal-consumption-asian-options.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "good"
extraction_score: 88.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 2
figures_png: 3
assets_dir: "../assets/matias-gonzalez_2019_optimal-consumption-asian-options"
references_file: "../references/matias-gonzalez_2019_optimal-consumption-asian-options.references.md"
---

<!-- p:1 -->

#### Resumen

En esta investigación se presenta un modelo alternativo que caracteriza el precio de una opción asiática de venta del tipo europeo con precio de ejercicio variable con media aritmética suscrita sobre una acción cuya volatilidad es estocástica; mediante un sistema de ecuaciones diferenciales que proviene de un modelo de control óptimo estocástico en tiempo continuo. Para tal efecto se desarrolla un modelo de un agente racional que dispone de una riqueza inicial y enfrenta la decisión de distribuir su riqueza entre consumo e inversión en un portafolio de activos, que incluye una opción asiática de venta y europea con precio de ejercicio con media aritmética, en un horizonte temporal finito. La valuación se lleva a cabo en términos del monto que el consumidor está dispuesto a pagar por mantener su contrato de opción asiática a fin de cubrirse contra riesgo de mercado. Asimismo, se aproximan los precios de opciones europeas y asiáticas de compra y venta por simulación Monte Carlo con parámetros calibrados adaptando el modelo de CoxIngersoll-Ross con volatilidad realizada. La fórmula de valuación obtenida no se había determinado mediante fundamentos de racionalidad económica. La evidencia empírica señala que los precios son muy cercanos en el corto plazo, pero a largo plazo, la diferencia entre las europeas y las asiáticas aumenta.

Clasificación JEL: C15, C61, G11, G13, G17

Palabras clave: Método de Monte Carlo, control óptimo estocástico, selección de portafolio, valuación de opciones asiáticas, volatilidad estocástica

Optimal consumption and investment and Asian option pricing in a stochastic environment with microeconomic foundations and Monte Carlo simulation

#### Abstract

This research presents an alternative model that characterizes the price of an Europeanstyle Asian put option with variable exercise price with arithmetic average subscribed on an stock whose volatility is stochastic, through a system of differential equations that comes from a model of stochastic optimal control in continuous time. For this purpose, a model of a rational agent is developed that has an initial wealth and faces the decision of distributing its wealth between consumption and investment in a portfolio of assets, which includes an European-style Asian put option with exercise price with arithmetic

1 Sección de Estudios de Posgrado e Investigación de la Escuela Superior de Economia del IPN. Plan de Agua Prieta 66, Plutarco Elias Calles, 11350 Ciudad de México, CDMX. Tel. 57296000 ext. 62036, amortiz@ipn.mx.

Revista Mexicana de Economía y Finanzas Nueva Época Volumen 14 Número 3, Julio-Septiembre 2019, pp. 397-414

DOI: https://doi.org/10.21919/remef.v14i3.408

### Consumo e inversión óptimos y valuación de opciones asiáticas en un entorno estocástico con fundamentos microeconómicos y simulación Monte Carlo

Araceli Matías González Instituto Politécnico Nacional, México María Teresa Verónica Martínez-Palacios Instituto Politécnico Nacional, México Ambrosio Ortiz-Ramírez 1

Instituto Politécnico Nacional, México

(Recepción: 30/noviembre/2018, aceptado: 26/marzo/2019)


<!-- p:2 -->


#### Abstract

average, in a finite temporal horizon. The valuation is carried out in terms of the amount that the consumer is willing to pay to maintain its Asian option contract in order to hedge against market risk. Also, prices of European and Asian call and put options are approximated by Monte Carlo simulation with calibrated parameters adapting the CoxIngersoll-Ross model with realized volatility. The valuation formula obtained was not determined by fundamentals of economic rationality. The empirical evidence indicates that prices are very close in the short term, but in the long term, the difference between European and Asian prices increases.

JEL Classification: C15, C61, G11, G13, G17

Keywords: Monte Carlo method, stochastic optimal control, portfolio choice, Asian option pricing, stochastic volatility

## 1. Introducción

Las empresas están expuestas a riesgos que se derivan de las fluctuaciones de los mercados económicos y financieros, ya que influyen directamente en los precios de activos financieros. El cambio generado en estos, puede conducir a ganancias o pérdidas increíblemente altas (Oro, 2004). Una propuesta para la administración de tales riesgos ha sido la creación y el desarrollo de instrumentos derivados. Un derivado es un instrumento financiero cuyo valor depende de otro activo llamado subyacente, su uso permite, entre otros, asegurar precios futuros y cubrirse contra potenciales pérdidas.

Las opciones plain vanilla son derivados que han alcanzado un gran desarrollo en los mercados estandarizados. La variedad de subyacentes sobre los que se suscribe este tipo de contratos es extensa, a saber, divisas, acciones, índices bursátiles, tasa de interés, commodities, seguros y energía. Las opciones suelen clasificarse de distintas formas, una de ellas es por el derecho que dan al poseedor del contrato: si el contrato confiere al poseedor de la opción el derecho a comprar el activo subyacente, será una opción de compra también llamada call, pero si el contrato le confiere el derecho a vender el activo subyacente, será una opción de venta también llamada put. Otra clasificación es de acuerdo a la fecha de ejercicio del contrato, es europea si el contrato se ejerce justo al vencimiento de este y americana cuando se puede ejercer en cualquier momento durante la vida del contrato.

Sin embargo, las necesidades específicas de los inversionistas, dieron origen a la creación de las opciones de segunda generación, también conocidas como opciones exóticas, las cuales se negocian principalmente en mercados Over The Counter (OTC). Las opciones asiáticas pertenecen al grupo de las llamadas opciones exóticas, su nombre se debe a que se comercializaron por primera vez en Tokio en 1987 (Venezia, 2010). La principal característica de este tipo de opciones es que para calcular su prima se toma en consideración el promedio de la evolución de precios del activo subyacente durante la vida del contrato, haciendo que su valuación sea menos vulnerable a la manipulación de precios; lo que las hace bastante competitivas como instrumento de especulación y arbitraje, y motiva su uso en portafolios de inversión. Por ejemplo Arregui y Vallejo (2001) muestran la relevancia de la valuación de opciones asiáticas que forman parte de un portafolio de inversión para calcular la rentabilidad que se puede garantizar además de valorar la situación patrimonial de un fondo de inversión garantizado de renta variable en cualquier momento.

Las opciones asiáticas además de ser de compra o venta, europea o americana, tienen su propia clasificación y esta se da por el tipo de promedio, aritmético o geométrico. Para un análisis de la valuación de opciones asiáticas con promedio geométrico pueden leerse los trabajos de Wang, Wang, Wang, y Jin, (2014), Zhang y Liu (2014), Kim y Wee (2014), Prakasa (2016), Jeon, Yoon, y Kang (2016), Zhang, Xiao, Kong y Zhang


<!-- p:3 -->


(2015) y Hubalek, Keller-Ressel y Sgarra (2017). Mientras que para opciones asiáticas con promedio aritmético refiérase a Sengupta (2014), Chung y Wong (2014), Mehrdoust y Saber (2015), Zeng y Kwok (2016), Hozman, Tichý y Cvejnová (2016) y Huang, O'Hara y Mataramvura (2017), por mencionar solo algunos. Es necesario precisar, que si el precio de ejercicio de una opción asiática depende de una cantidad fija, la opción se conoce como una opción asiática con precio de ejercicio constante. Pero si el precio de ejercicio es proporcional al precio del activo subyacente, entonces es una opción asiática con precio de ejercicio flotante o promedio.

En lo que concierne a métodos de valuación, se encuentran disponibles en la literatura métodos tanto numéricos como analíticos. Respecto a métodos numéricos, pueden leerse los trabajos de: Yor (1992), en donde expresa el valor de la opción como una integral triple difícil de evaluar numéricamente, Dufresne (2000) quien obtiene una fórmula que expresa el valor de la opción asiática como una serie infinita de polinomios de Laguerre con cada coeficiente en la serie dada por una única integral que necesita ser calculada numéricamente, la limitación que encontró es que solo aplica a promedios continuos con ponderaciones iguales además de que no hay límite en el error que se produce al truncar la serie. Linetsky (2004) desarrolla dos representaciones, la primera es una serie infinita de términos relacionados con las funciones de Whittaker M y W. y la segunda es una integral real única de una expresión que involucra la función Whittaker W. plus y funciones gamma incompletas, así como polinomios de Laguerre encontrando una precisión de 6 decimales al comparar con Vecer (2002). Autores como Turnbull y Wakeman (1991) encuentran la aproximación lognormal con los primeros y segundos momentos combinados obteniendo el precio de una opción con media aritmética.

Particularmente, el método de simulación de Monte Carlo es utilizado frecuentemente en Finanzas, porque permite encontrar soluciones aproximadas de problemas matemáticos que involucran variables aleatorias dependientes del tiempo (Venegas-Martínez, 2008), al respecto se puede consultar a: Boyle (1977), quien usa el método de simulación de Monte Carlo para resolver problemas de valoración de opciones, simula el proceso que generan los rendimientos en el activo subyacente suponiendo neutralidad de riesgo para derivar el valor de la opción e introduce una variable de control apropiada con la cual se aumenta significativamente la precisión de los resultados, Kemna y Vorst (1990) ofrecen un método de precios mejorado incluyendo la simulación de Monte Carlo con elementos de reducción de varianza. Por su parte Levy (1992), proporciona aproximaciones analíticas de forma cerrada para valuar opciones europeas que involucran el promedio aritmético de las tasas de cambio futuras. Asimismo se han desarrollado investigaciones cuya característica es utilizar el método de Monte Carlo con variables de control, por ejemplo, Fu, Madan y Wang (1999) utilizan variables de control para corregir el sesgo de discretización inherente a la simulación, también pueden consultarse: Datey, Gauthier y Simonato(2003), Ben y Kebaier (2014), Mehrdoust (2015), Shiraya y Takahashi (2017), entre otros.

En lo que a métodos analíticos compete, el enfoque de ecuaciones diferenciales parciales ha sido recurrentemente utilizado para valuar instrumentos derivados, particularmente opciones. Véanse los trabajos de Zvan et al. (1997), Rogers y Shi (1995) quienes realizan la valuación de la opción asiática resolviendo una ecuación diferencial parcial parabólica en dos variables además de proporcionar un límite inferior que es tan preciso que es esencialmente el precio real. Por otra parte, Vecer (2001 y 2002), Marcozzi (2003), Foufas y Larson (2008) obtienen el precio de la opción asiática con el modelo de Black-Scholes, las ecuaciones diferenciales parciales resultantes son de tipo parabólico en una dimensión espacial y el cálculo numérico se realiza mediante el uso de un método de elementos finitos adaptativos.

De particular mención para esta investigación son los modelos que utilizan métodos mixtos, en la búsqueda de valuación de derivados en escenarios más apegados a la realidad. Un instrumento muy valioso en este rubro es la Teoría de Control Óptimo Estocástico en Optimización Dinámica en tiempo continuo, en este contexto existen modelos Microeconómicos o Macroeconómicos disponibles en la literatura, en los que realizan la valuación de activos financieros y/o instrumentos derivados. Véanse por ejemplo Sierra (2007), Cruz-Aké y Venegas-Martínez (2010), Martínez-Palacios, Sánchez-Daza y Venegas-Martínez (2012), Cai, Song y Kou (2015), Venegas-Martínez y Aguilar-Sánchez (2005) y Martínez-Palacios, Venegas-Martínez y Martínez-Sánchez (2015), quienes modelan en tiempo continuo la toma de decisiones óptima de consumo y una cartera de activos en un horizonte temporal finito, de longitud estocástica, y en el proceso de solución, obtienen el modelo equivalente a Black-Scholes-Merton para valuar una opción de venta de tipo americano; Sierra (2007) mediante un modelo de agente representativo y suponiendo la distribución de activos modelados mediante Brownianos fraccionales, obtiene el precio de una opción europea de compra. Por su parte Cai, Song y Kou (2015) propusieron fórmulas de aproximación de doble transformación de forma cerrada para los precios de las opciones asiáticas controladas de forma discreta y continúa estableciendo una cadena general de Markov de tiempo continuo.


<!-- p:4 -->


En la presente investigación el marco de la Teoría de Control Óptimo Estocástico en Optimización Dinámica en tiempo continuo, y en un ambiente de riesgos de mercado, se desarrolla un modelo de un agente económico racional que dispone de una riqueza inicial y enfrenta la decisión de cómo distribuir su riqueza entre consumo e inversión en portafolio de activos, uno de ellos una opción asiática de venta suscrita sobre una acción que tiene volatilidad estocástica, de forma tal que maximice su utilidad total esperada por el consumo e inversión, en un horizonte de planeación temporal finito. En el proceso de solución, mediante un sistema de ecuaciones diferenciales se deduce el modelo para valuar la opción asiática de venta de tipo europeo que tiene precio de ejercicio variable igual a la media aritmética. Para dar solución al modelo, y con el objetivo de un análisis profundo de solución, se establece una metodología mediante simulación Montecarlo en la que se supone que las distribuciones de los precios del subyacente y la volatilidad son conducidos por un movimiento geométrico browniano, la volatilidad del subyacente y sus parámetros se calibran mediante una adaptación del modelo de tasa corta de Cox, Ingersoll y Ross (1985) (CIR) a volatilidad realizada, la tasa de interés libre de riesgo se obtiene de la página de Banxico para los cuatro plazos de las opciones del boletín que se publica en la página web del Mercado Mexicano de Derivados (MexDer).

En el contexto de las investigaciones mencionadas, las características distintivas del presente trabajo son: 1) Se obtiene una ecuación diferencial parcial equivalente a la ecuación obtenida por Black-Scholes-Merton introduciendo el supuesto de volatilidad estocástica conducida por un movimiento geométrico browniano, 2) La valuación de la opción asiática de venta con promedio aritmético y europea se establece mediante micro fundamentos y 3) Se desarrolla una metodología mediante Simulación Monte Carlo para la valuación de opciones asiáticas de compra y de venta con el supuesto de que la volatilidad es estocástica y conducida por una ecuación diferencial estocástica con reversión a la media, con parámetros calibrados a partir de información de mercado.

Este trabajo está organizado de la siguiente forma, en la siguiente sección se definen los activos de inversión a los que tiene acceso el agente y se establece su representación analítica en el modelo, en la sección 3 se establece la ecuación de riqueza del agente representativo de esta economía, así como el modelo de Control Óptimo Estocástico por resolver. En el transcurso de la sección 4 se proporciona el proceso de solución al problema planteado utilizando programación dinámica estocástica en tiempo continuo y en la cual se obtiene los resultados centrales: i) ecuación diferencial parcial de Hamilton-JacobiBellman y ii) las condiciones de primer orden, que conducen a las trayectorias óptimas. En la sección 5 se propone una función HARA y se da la solución del problema planteado, obteniendo las proporciones óptimas de consumo e inversión. En la sección 6, se deduce la ecuación diferencial parcial lineal de segundo orden equivalente a la de Black-Sholes- Merton, la cual es el modelo mediante el que se valuara una opción asiática de venta del tipo europeo con precio de ejercicio variable media aritmética suscrita sobre una acción cuya volatilidad. En la sección 7 se aproximan los precios de opciones europeas y asiáticas de compra y venta por simulación Monte Carlo con parámetros calibrados adaptando el modelo de Cox-Ingersoll-Ross con volatilidad realizada y su correspondiente análisis de resultados. En la sección 8 se presentan las conclusiones de la presente investigación indicando aquellas extensiones previstas en la agenda futura de trabajo. Por último, se presentan las referencias bibliográficas utilizadas y un Apéndice en el que se dispone en un cuadro los precios obtenidos de opciones europeas de compra y de venta sobre WALMEXV.


<!-- p:5 -->


## 2. Descripción del marco teórico

Se supone una economía pequeña y cerrada, en la que se comercializa un solo bien de consumo de carácter perecedero. En esta economía existe un sistema bancario o mercado de crédito en el que son posibles las negociaciones de forma continua, es decir, se opera los 365 días del año, las 24 horas del día. En este sistema, las ventas en corto son permitidas e ilimitadas.

### 2.1 Descripción analítica de los supuestos

Considere a un agente económico racional que desea maximizar el valor presente y futuro esperado por consumo e inversión en una cartera de activos, en un horizonte temporal finito, representado por el intervalo [0 , T ] . En el tiempo t = 0 el agente económico es dotado con una riqueza inicial z 0 y enfrenta el problema de cómo distribuirla en consumo de un bien genérico y proporciones de inversión en un portafolio de activos.

Se supone que el agente tiene permitido invertir en 3 activos:

1. Un bono cupón cero de precio B 0 (en t = 0 ), que otorga una tasa de interés r &gt; 0 , libre de riesgo de incumplimiento y constante a todos los plazos. En el tiempo t el saldo de la inversión está dado por B = B 0 e rt , y sus rendimientos, están dados por,

$$d R _ { B } = \frac { d B _ { t } } { B _ { t } } = r d t$$

2. Una acción cuyo proceso de precios es conducido por la ecuación diferencial estocástica,

$$d Y _ { t } = \mu Y _ { t } d t + \sigma Y _ { t } d W _ { t }$$

$$d R _ { Y _ { t } } = \frac { d Y _ { t } } { Y _ { t } } = \mu d t + \sigma d W _ { t } ,$$

donde μ representa la tendencia del precio del activo y dW t es un movimiento geométrico browniano definido en un espacio de probabilidad con su filtración aumentada ( Ω , F, ( F w t t ∈ N ) t ∈ [0 ,T ] , P ) .

Se observa que σ 2 = V t es la varianza o volatilidad al cuadrado y esta se modela mediante un movimiento geométrico browniano en su forma diferencial,

$$d V _ { t } = \gamma \left ( V - \theta \right ) _ { t } d t + \delta V _ { t } d U _ { t }$$

donde γ es la tendencia del precio de la volatilidad, dU t es un movimiento geométrico browniano definido en un espacio de probabilidad con su filtración aumentada ( Ω , F, ( F U t t ∈ N ) t ∈ [0 ,T ] , P ) y δ &gt; 0 es la volatilidad de la varianza. Así, los rendi-

mientos de la varianza están dados por:

que tiene rendimientos,


<!-- p:6 -->


$$d R _ { V _ { t } } = \frac { d V _ { t } } { V _ { t } } = \gamma \left ( 1 - \frac { \theta } { V _ { t } } \right ) d t + \delta d U _ { t }$$

Con el objetivo de no complicar los cálculos, se supondrá que:

$$c o v ( d W _ { t } , d U _ { t } ) = 0$$

3. El tercer activo es una opción asiática de venta del tipo europeo suscrita sobre la acción dada en la ecuación (2) y tiene precio de ejercicio variable igual a la media aritmética. El pago del contrato en la fecha del vencimiento es el max ( K t,T - Y T , 0) , en donde K t,T = 1 T - t ∫ T t S u du ,

Se define:

$$\mu _ { A _ { t } } = \int _ { 0 } ^ { t } S _ { u } d u$$

En la ecuación (2) se observa que la historia de precios del activo subyacente es independiente del precio actual. Por lo anterior μ A t y Y t pueden ser tratadas como variables de estado independientes. Además, se tiene que

$$d \mu _ { A _ { t } } = Y _ { t } d t$$

El precio de la opción es la función de C A t = C A t ( Y t , μ A t , V t , t ) , y tiene rendimientos,

$$d R _ { C _ { t } ^ { A } } = \frac { d C _ { t } ^ { A } } { C _ { t } ^ { A } }$$

la diferencial estocástica dC A t se obtiene mediante el Lema de Itô, de donde

$$d R _ { C _ { t } ^ { A } } = \frac { d C _ { t } ^ { A } } { C _ { t } ^ { A } } = \mu _ { C _ { t } ^ { A } } d t + \sigma _ { 1 C _ { t } ^ { A } } d W _ { t } + \sigma _ { 2 C _ { t } ^ { A } } d U _ { t }$$

con

$$\mu _ { C _ { t } ^ { A } } = C _ { t } ^ { A } + C _ { t Y _ { t } } ^ { A } \mu Y _ { t } + C _ { t \mu _ { A _ { t } } } ^ { A } Y _ { t } + C _ { t } ^ { A } \gamma \, \gamma V _ { t } + \frac { 1 } { 2 } \left [ C _ { t Y _ { t } } ^ { A } Y _ { t } \sigma ^ { 2 } Y _ { t } ^ { 2 } + C _ { t V _ { t } } ^ { A } \delta ^ { 2 } V _ { t } ^ { 2 } \right ] \\ \sigma _ { 1 C _ { t } ^ { A } } = C _ { t } ^ { A } \sigma Y _ { t } \quad Y \quad \sigma _ { 2 C _ { t } ^ { A } } = C _ { t V _ { t } } ^ { A } \delta V _ { t }$$

## 3. Ecuación de riqueza y planteamiento del Modelo

### 3.1 Ecuación de riqueza

Las proporciones de riqueza que se destinan en inversión a los activos riesgosos acción y opción, se denotan mediante α 1 t y α 2 t respectivamente, de tal forma que la proporción que se destina al bono o activo sin riesgo es (1 - α 1 t - α 2 t ) y c t denota la tasa de consumo. También se supone que no se incurre en pagos por transacción a agentes de casa de bolsa y/o pagos por impuestos a autoridades fiscales.

Se supone ahora, que Z t representa la riqueza del agente en el tiempo t, por lo que se define la dinámica del proceso de riqueza o restricción presupuestal intertemporal del agente representativo como:

$$d Z _ { t } = \alpha _ { 1 t } Y _ { t } d R _ { Y _ { t } } + \alpha _ { 2 t } Z _ { t } d R _ { C _ { t } ^ { A } } + ( 1 - \alpha _ { 1 t } - \alpha _ { 2 t } ) Z _ { t } d R _ { B } - c _ { t } d t$$

equivalentemente se tiene,

con

$$\frac { d Z _ { t } } { Z _ { t } } = \mu _ { Z } d t + \sigma _ { 1 Z } d W _ { t } + \sigma _ { 2 Z } d U _ { t }$$


<!-- p:7 -->


sujeto a

$$\mu _ { Z } & = \left [ \mu \alpha _ { 1 t } + \mu _ { C _ { t } ^ { A } } \alpha _ { 2 t } + ( 1 - \alpha _ { 1 t } - \alpha _ { 2 t } ) r - \frac { c _ { t } } { Z _ { t } } \right ] , \\ \sigma _ { 1 Z } & = [ \sigma \alpha _ { 1 t } + \sigma _ { 1 C _ { t } ^ { A } } \alpha _ { 2 t } ] \quad y \quad \sigma _ { 2 Z } = [ \sigma _ { 2 C _ { t } ^ { A } } \alpha _ { 2 t } ]$$

### 3.2 Planteamiento del problema

En este apartado se establece formalmente el problema de maximización de utilidad del consumidor-inversionista:

$$\max i m i z a r \, E \left [ \int _ { 0 } ^ { T } F \left ( t , c _ { t } \right ) d t \right | F _ { 0 } \right ]$$

$$d Z _ { t } = \mu _ { Z } Z _ { t } d t + \sigma _ { 1 Z } Z _ { t } d W _ { t } + \sigma _ { 2 Z } Z _ { t } d U _ { t }$$

$$Z _ { 0 } & = z _ { 0 } , \\ c _ { t } & \geq 0 , \ \forall t \geq 0$$

## 4. Proceso de solución del problema: ecuación diferencial parcial de Hamilton-Jacobi-Bellman y condiciones de primer orden

### 4.1 Ecuación diferencial parcial de Hamilton-Jacobi-Bellman

Para dar solución al problema planteado se define la función valor como:

$$J \left ( Z _ { t } , \mu _ { A _ { t } } , V _ { t } , t \right ) = \max _ { \alpha _ { 1 t } , \alpha _ { 2 t } \in R , 0 \leq c _ { t } | _ { [ t , T ] } } E \left [ \int _ { t } ^ { T } F \left ( c _ { s } , s \right ) d s \right | F _ { t } \right ]$$

Se considera un incremento diferencial en el tiempo dt ∈ R tal que t &lt; t + dt &lt; T , de donde se tiene la siguiente relación recursiva temporal:

$$= \max _ { \alpha _ { 1 t } , \alpha _ { 2 t } \in R , 0 \leq c _ { t } | _ { [ t , T ] } } E \left [ \int _ { t } ^ { t + d t } F \left ( c _ { s } , s \right ) d s + \int _ { t + d t } ^ { T } F \left ( c _ { s } , s \right ) d s \right | F _ { t } \right ]$$

al aplicar el teorema del valor medio del cálculo integral al primer sumando y recursividad al segundo:

=

$$\max _ { \alpha _ { 1 t } , \alpha _ { 2 t } \in R , 0 \leq c _ { t } | _ { [ t , t + d t ] } } E \left [ F \left ( c _ { t } , t \right ) d t + o \left ( d t \right ) + J ( Z _ { t } + d Z _ { t } , \mu _ { A _ { t } } + d \mu _ { A _ { t } } , V _ { t } + d V _ { t } , \ t + d t ) | \ F _ { t } \right ]$$

si se utiliza expansión en serie de Taylor en el segundo sumando, se obtiene:

$$\stackrel { = } { \Lambda } _ { ( t _ { 1 } , \alpha _ { 2 t } \in R , 0 \leq c _ { t } | _ { ( t , t + a t ] } } } E \left [ F \left ( c _ { t } , t \right ) d t + o \left ( d t \right ) + \stackrel { = } { J } \left ( Z _ { t } , \mu _ { A _ { t } } , V _ { t } , \ t \right ) + d J \left ( Z _ { t } , \mu _ { A _ { t } } , V _ { t } , \ t \right ) + o ( d t ) | \, F _ { t } \right ]$$

se simplificar la expresión anterior, dado que la suma de dos funciones o ( dt ) es otra función o ( dt ) , de donde se tiene que,

$$0 = \max _ { \alpha _ { 1 t } , \alpha _ { 2 t } \in R , 0 \leq c _ { t } | _ { t , t + d t } } E \left [ F \left ( c _ { t } , t \right ) d t + o \left ( d t \right ) + d J \left ( Z _ { t } , \mu _ { A _ { e } } , V _ { t } , \, t \right ) | \, F _ { t } \right ]$$

En la expresión anterior se aplica el lema de Itô a dJ ( Z t , μ A t , V t , t ) para obtener la diferencial estocástica de J; asimismo se toma el valor esperado y toda vez que dW t ∼ N (0 , dt ) y dU t ∼ N (0 , dt ) , resulta

$$0 = & \sum _ { \alpha _ { t } , \alpha _ { t } \in R , 0 \leq c _ { t } | _ { t , t + d t } } \left [ F \left ( c _ { t } , t \right ) d t + o \left ( d t \right ) + \left [ J _ { t } + J _ { Z _ { t } } Z _ { t } \mu _ { Z } + J _ { \mu _ { A _ { t } } } Y _ { t } + J _ { V _ { t } } \gamma V _ { t } \right ] \\ & \frac { 1 } { 2 } \left \{ J _ { Z _ { t } } Z _ { t } \left ( \sigma _ { 1 } ^ { 2 } + \sigma _ { 2 Z } ^ { 2 } \right ) + J _ { V _ { t } } \delta ^ { 2 } V _ { t } ^ { 2 } + J _ { Z _ { t } V _ { t } } Z _ { t } V _ { t } \sigma _ { 2 Z } \delta \right \} \right ] d t + o \left ( d t \right ) \right ]$$


<!-- p:8 -->


ahora, la ecuación obtenida se divide entre dt y se calcula el límite de esta cuando dt → 0 , de donde se obtiene la ecuación diferencial parcial de Hamilton-Jacobi-Bellman (EDPHJB),

$$0 = \max _ { \alpha _ { 1 } , \alpha _ { 2 } , \alpha _ { t } , \infty < c _ { t } } \left [ F ( c _ { t } , t ) + J _ { t } + J _ { Z _ { t } } Z _ { t } \mu _ { Z } + J _ { \mu _ { A _ { t } } } Y _ { t } + J _ { V _ { t } } \gamma V _ { t } \right ] + \\ \frac { 1 } { 2 } \left [ J _ { Z _ { t } Z _ { t } } Z _ { t } ^ { 2 } ( \sigma _ { 1 Z } ^ { 2 } + \sigma _ { 2 Z } ^ { 2 } ) + J _ { V _ { t } V _ { t } } \delta ^ { 2 } V _ { t } ^ { 2 } + J _ { Z _ { t } V _ { t } } Z _ { t } V _ { t } \sigma _ { 2 Z } \delta \right ] \\ A _ { \ } e s t a c u j c i n d e b e n d e i m p o n n e r s e c d i c i o n e s d e f r o n t e r a . \text { para. october. soluc-ci} \hat { n }$$

A esta ecuación deben de imponerse condiciones de frontera para obtener solución única de la EDP-HJB:

$$0 = \max _ { \substack { \alpha _ { 1 } , \alpha _ { 2 } , 0 \leq c _ { t } \\ + \frac { 1 } { 2 } \left [ J _ { Z } z _ { t } Z _ { t } ^ { 2 } ( \sigma _ { 1 } ^ { 2 } z _ { 2 } ) + J _ { V _ { t } V _ { t } } \delta ^ { 2 } V _ { t } ^ { 2 } + J _ { Z _ { t } V _ { t } Z _ { t } V _ { t } \sigma _ { 2 } Z \delta } \right ] } } \\ J ( Z _ { t } V _ { t } , \mu _ { A _ { t } } , T ) = 0 \\ J ( 0 , V _ { t } , \mu _ { A _ { t } } , t ) = 0$$

### 4.2 Condiciones de primer orden

Al realizar las sustituciones correspondientes en la ecuación diferencial parcial de HamiltonJacobi-Bellman y suponer máximo interior se tiene,

$$J _ { Z _ { t } } Z _ { t } \left ( \mu _ { C _ { t } ^ { A } } - r \right ) + \frac { 1 } { 2 } \left \{ J _ { Z _ { t } Z _ { t } } Z _ { t } ^ { 2 } \left [ 2 \sigma _ { 1 C _ { t } ^ { A } } ^ { 2 } \alpha _ { 2 t } + 2 \sigma \sigma _ { 1 C _ { t } ^ { A } } \alpha _ { 1 t } + 2 \sigma _ { 2 C _ { t } ^ { A } } \alpha _ { 2 t } \right ] + J _ { Z _ { t } V _ { t } } Z _ { t } V _ { t } \delta \sigma _ { 2 C _ { t } ^ { A } } \right \} = 0$$

$$J _ { Z _ { t } } Z _ { t } \left ( \mu - r \right ) + J _ { Z _ { t } , Z _ { t } } Z _ { t } ^ { 2 } \left [ \sigma ^ { 2 } \alpha _ { 1 t } + \sigma \sigma _ { 1 C _ { t } ^ { A } } \alpha _ { 2 t } \right ] = 0$$

$$e ^ { - \eta t } \frac { 1 } { c _ { t } } - J _ { Z _ { t } } = 0$$

## 5. Función de utilidad y proporciones óptimas de inversión

### 5.1 Función de utilidad

Ahora se supone que la función de utilidad es F ( c t , t ) = k ( c t ) e - ηt , donde k ( c t ) pertenece a la familia de funciones de utilidad denominadas Hyperbolic Absolute Risk Aversion (HARA), η es un parámetro que representa la ansiedad por consumo del agente. Para el problema se elige la siguiente función de consumo:

$$F ( c _ { t } , t ) = \frac { c _ { t } ^ { \beta } } { \beta } e ^ { - \eta t } \quad 0 < \beta < 1$$

La razón económica para usar esta función es que se tiene una utilidad marginal infinita en c = 0 , lo que forzara a que el consumo optimo se mantenga positivo a través del horizonte de planeación.

### 5.2 Proporciones óptimas de inversión: solución de la EDP de HJB

Se busca una solución que satisfaga la ecuación diferencial parcial de Hamilton-JacobiBellman y se propone una función de producto de variables separables:

$$J \left ( Z _ { t } , \ \mu _ { A _ { t } } , \ V _ { t } , t \right ) = e ^ { - \eta t } G ( \ \mu _ { A _ { t } } , \ V _ { t } , t ) \frac { Z _ { t } ^ { \beta } } { \beta }$$

donde η representa la ansiedad por consumir del agente.

Ahora dado J ( Z t , μ A t , V t , t ) se tiene:


<!-- p:9 -->


$$J _ { t } = - \eta e ^ { - \eta t } G \left ( \mu _ { A _ { t } } , \, V _ { t } , t \right ) \frac { Z _ { \ell } ^ { \beta } } { \beta } + e ^ { - \eta t } G _ { t } \frac { Z _ { \ell } ^ { \beta } } { \beta } \\ J _ { Z _ { t } Z _ { t } } = e ^ { - \eta t } G \left ( \, \mu _ { A _ { t } } , \, V _ { t } , t \right ) Z _ { t } ^ { ( \beta - 1 ) } \\ J _ { \mu _ { t } A _ { t } } = e ^ { - \eta t } \frac { Z _ { \ell } ^ { \beta } } { \beta } G \mu _ { A _ { t } } \\ J _ { V _ { t } } = e ^ { - \eta t } \frac { Z _ { \ell } ^ { \beta } } { \beta } G _ { V _ { t } } \\ J _ { V _ { t } V _ { t } } = e ^ { - \eta t } \frac { Z _ { \ell } ^ { \beta } } { \beta } G _ { V _ { t } V _ { t } } \\ J _ { Z _ { t } V _ { t } } = e ^ { - \eta t } Z _ { t } ^ { ( \beta - 1 ) } G _ { V _ { t } } \\ \intertext { i t u i r l o s val o r e s de ( 1 9 ) e n ( 14 ) , ( 15 ) y ( 1 6 ), se o b t i e n e n l a s prop o r o c i n e s }$$

Al sustituir los valores de (19) en (14), (15) y (16), se obtienen las proporciones óptimas:

$$\alpha _ { 1 t } = \frac { \left ( \mu _ { C _ { t } ^ { A } } - r \right ) + \frac { 1 } { 2 } G _ { V _ { t } } V _ { t } \delta \frac { \sigma _ { 2 C _ { t } ^ { A } } } { G ( \mu _ { A _ { t } } , V _ { t } , t ) } + \frac { 1 } { 2 } \left ( \beta - 1 \right ) \left [ 2 \sigma _ { 2 C _ { t } ^ { A } } \alpha _ { 2 t } + 2 \sigma _ { 2 C _ { t } ^ { A } } \alpha _ { 2 t } \right ] } { - \left ( \beta - 1 \right ) \sigma _ { 1 C _ { t } ^ { A } } } \quad ( 2 0 )$$

$$\alpha _ { 2 t } = \frac { \frac { \mu - r } { \sigma } + ( \beta - 1 ) \, \sigma \alpha _ { 1 t } } { - ( \beta - 1 ) \, \sigma _ { 1 } c _ { t } ^ { A } }$$

$$c _ { t } = Z _ { t } G \left ( \, \mu _ { A _ { t } } , \, V _ { t } , t \right ) ^ { \frac { 1 } { \beta } }$$

De esta manera se obtiene la función que modela el consumo dada por la ecuación (22).

## 6. Ecuación Diferencial Parcial para valuar una opción asiática de compra

Al suponer la solución de esquina con α 1 t = 1 y α 2 t = 0 y sustituir estos valores en los premios al riesgo de la acción y la opción, se obtiene la fórmula de valuación para una opción asiática de tipo europeo análoga a la EDP de Black-Scholes-Merton, a la que se debe de imponer la condición de frontera, que corresponde al valor intrínseco de la opción:

$$C _ { t } ^ { A } + C _ { t \ \mu _ { A } } ^ { A } Y _ { t } + \frac { 1 } { 2 } \left [ C _ { t } ^ { A } Y _ { t } V _ { t } Y _ { t } ^ { 2 } + C _ { t } ^ { A } V _ { t } \, V _ { t } ^ { \delta } V _ { t } ^ { 2 } \right ] + C _ { t } ^ { A } Y _ { t } r Y _ { t } - r C _ { t } ^ { A } + \\ \left [ \gamma V _ { t } - \frac { 1 } { 2 } G V _ { t } \frac { \delta ^ { 2 } V _ { t } ^ { 2 } } { G } \right ] \left [ C _ { t } ^ { A } V _ { t } \right ] = 0 \\ C _ { t } ^ { A } \left ( Y _ { t } , V _ { t } , \mu _ { A _ { t } } , t \right ) = \hat { m } \alpha \left ( \frac { \mu _ { A _ { t } } } { T } - Y _ { T } , 0 \right )$$

## 7. Calibración del modelo con volatilidad estocástica realizada y Simulación Montecarlo

En esta sección se describe un sistema de ecuaciones diferenciales estocásticas que conducen la dinámica de los rendimientos y la volatilidad del activo subyacente, además de una manera de calibrar sus parámetros con datos históricos y de mercado. Se supone que el precio del subyacente y su volatilidad son conducidos movimientos geométricos brownianos con o sin correlación, con la característica de que la ecuación que conduce la volatilidad es con un proceso de tipo CIR, posteriormente se simulan trayectorias del subyacente con la función de pago de la opción y se descuenta con la tasa libre de riesgo el valor final del promedio de las trayectorias. De esta manera se determina el precio de una opción asiática de tipo europea. La simulación de Monte Carlo es muy útil, en especial cuando no se tiene una fórmula cerrada para la valuación.


<!-- p:10 -->


Una manera de considerar la naturaleza estocástica en los rendimientos de los activos financieros es modelarla por medio de procesos de reversión a la media, como por ejemplo con modelos de volatilidad estocástica de Hull y White (1987) y Heston (1993), entre otros. La calibración de los parámetros de estos modelos puede hacerse por series de tiempo, modelos con funciones de pérdida, diversos modelos de la familia GARCH, y con volatilidad realizada, entre otros.

A continuación, se describe la metodología para determinar el precio de una opción asiática con subyacente promedio sin pago de dividendos mediante simulación Monte Carlo.

Suponga que el precio del subyacente es conducido por un movimiento geométrico browniano con volatilidad estocástica σ t conducida por un proceso de reversión a la media y ambos procesos están correlacionados como sigue:

$$\frac { \frac { d S _ { t } } { S _ { t } } = r d t + \sigma _ { t } d W _ { S , t } , } { d \sigma _ { t } = \kappa \left ( \theta - \sigma _ { t } \right ) d t + \sigma _ { \sigma } \sigma _ { t } ^ { \lambda } d W _ { \sigma , t } }$$

donde

W σ,t es un proceso de Wiener correlacionado con W S,t , es decir, Cov( dW σ,t , dW S,t ) = ρdt . Si λ = 0 , entonces la dinámica de la volatilidad es conducida por un modelo de tipo Vasicek y se considera λ = 0 , 5 para un proceso de tipo CIR.

Los parámetros θ, κ y σ σ , se interpretan como la tasa de largo plazo, la velocidad de reversión a la tasa de largo plazo y la volatilidad de la varianza de la tasa de interés (denominada también como la volatilidad de la volatilidad), respectivamente.

Para ejecutar la simulación de ambos procesos se generan trayectorias con una estructura de relación dada por:

$$d \widetilde { W } = \begin{pmatrix} d W _ { S , t } \\ d W _ { \sigma , t } \end{pmatrix} \sim N ( 0 , \Sigma )$$

$$\Sigma = \begin{pmatrix} \Delta t & \rho _ { \sigma , S } \Delta t \\ \rho _ { \sigma , S } \Delta t & \Delta t \end{pmatrix}$$

con:

Para hacer lo anterior, se calcula dado que Σ = LL simular dZ ∼ N (0 , I 2 ) para obtener d  ̃ W = LdZ , se elige un número para la partición del plazo al vencimiento de la opción, por ejemplo N = 100 y mediante el método de remuestreo cuadrático (Barraquand, 1995) generar dZ , que involucra a d  ̃ W por construcción. Sean μ Z y Σ Z , la media teórica y la matriz de covarianza de dZ respectivamente:

$$\mu _ { Z } = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \quad y \quad \Sigma _ { Z } = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$$

Con las ecuaciones anteriores se generan las trayectorias del sistema de ecuaciones diferenciales estocásticas planteado en (24).

El precio de una opción de compra con subyacente promedio está dado por la función de pago:

$$C ( S _ { T } ) = \max \left ( \frac { 1 } { T } \int _ { 0 } ^ { T } S _ { \tau } d \tau - K , 0 \right )$$

y el precio de una opción de venta con subyacente promedio está dado por:

$$P ( S _ { T } ) = \max \left ( K - \frac { 1 } { T } \int _ { 0 } ^ { T } S _ { \tau } d \tau , 0 \right )$$

Si el subyacente es conducido por el sistema dado en (24), entonces el algoritmo para determinar los precios de las opciones de compra y de venta es:


<!-- p:11 -->


1. Generar dW S,t y dW σ,t como:

$$d W _ { S , t } ^ { ( k ) } = Z _ { S , t } ^ { ( k ) } \sqrt { \Delta t } , \\ d W _ { \sigma , t } ^ { ( k ) } = \rho Z _ { \sigma , t } ^ { ( k ) } \sqrt { \Delta t } + \sqrt { 1 - \rho ^ { 2 } } Z _ { \sigma , t } ^ { ( k ) } \sqrt { \Delta t }$$

2. Discretizar el sistema de ecuaciones diferenciales estocásticas como:

$$\sigma _ { i + 1 } ^ { ( k ) } = \sigma _ { i } ^ { ( k ) } + \kappa \left ( \theta - \sigma _ { i } ^ { ( k ) } \right ) \Delta t + \sigma _ { \sigma } \sigma _ { i } ^ { ( k ) } d W _ { \sigma , t } ^ { ( k ) } \\ S _ { i + 1 } ^ { ( k ) } = S _ { i } ^ { ( k ) } \left ( 1 + \sigma ( t _ { i } ) \Delta t + \sigma _ { i } ^ { ( k ) } d W _ { S , t } ^ { ( k ) } \right ) \\ i = 1 , \dots , N - 1$$

donde hace referencia a la k-ésima simulación.

3. Definir la media aritmética de las trayectorias generadas:

$$\bar { S } ^ { ( k ) } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \bar { S } _ { i } ^ { ( k ) } ,$$

4. Calcular el precio de la opción como:

$$C = e ^ { - r T } \frac { 1 } { M } \sum _ { k = 1 } ^ { M } \max \left ( \bar { S } ^ { ( k ) } - K , 0 \right ) \, y \, \ P = e ^ { - r T } \frac { 1 } { M } \sum _ { k = 1 } ^ { M } \max \left ( K - \bar { S } ^ { ( k ) } , 0 \right )$$

donde denota el número de trayectorias simuladas y el número de precios generados.

### 7.1 Análisis y discusión de resultados

En esta sección se calculan por medio de simulación Monte Carlo precios de opciones asiáticas con subyacente promedio, el subyacente es el precio de la acción de WALMEXV y se comparan con los precios de opciones publicadas en el boletín de MexDer del día 16/05/2018. Se supone que los parámetros de volatilidad estocástica se calculan mediante una adaptación del modelo de CIR al método de volatilidad realizada. La tasa de interés se obtiene de la página de Banxico para los cuatro plazos de las opciones del boletín.

La muestra de la volatilidad realizada para calibrar los modelos comprende del 30 de diciembre de 2016 al 16 de mayo de 2018. Los parámetros estimados con el modelo de CIR mediante máxima verosimilitud se observan en el cuadro siguiente:

Cuadro 1. Cuadro resumen de estimación de parámetros de volatilidad realizada con el modelo CIR por el método de máxima verosimilitud.

| Parámetros       |      CIR |
|------------------|----------|
| κ                | 2.280414 |
| θ                | 0.013979 |
| σ                | 0.002504 |
| No. Obs. n       |      344 |
| Likelihood Ratio | 9.433697 |

Fuente: Elaboración propia.

De los resultados del cuadro anterior, se puede verificar que se cumple la condición de Feller, es decir, las trayectorias del proceso que conduce la volatilidad de la volatilidad son siempre positivas. Los resultados de la simulación se muestran en la gráfica 1, en la cual se muestran la serie original de la volatilidad realizada y cien trayectorias simuladas con los parámetros dados por el modelo CIR. Se observa la tendencia de la volatilidad hacia la baja, explicado por la misma dinámica del precio de la acción de WALMEXV.


<!-- p:12 -->


## dσt = κ (θ − σt) dt + σσ √σtdWσ,t

Gráfica 1. Trayectorias simuladas.

Fuente: Elaboración propia.

<!-- p:13 -->


Gráfica 2. Comparación entre precios de opciones de MexDer, opciones europeas y asiáticas con parámetros calibrados con el modelo de CIR. Fuente: Elaboración propia.

<!-- p:14 -->


410

La Gráfica 2 muestra los precios de opciones de compra y de venta europeas, y precios de opciones con subyacente promedio ambas con volatilidad estocástica con parámetros calibrados con volatilidad realizada conducida por el modelo de CIR, en ambos casos los plazos son desde T=30, 128, 219 y 303 días y los precios de ejercicio varían desde $43 hasta $57 con incrementos de $1, tales precios se comparan con los publicados por MexDer el día 16/05/2018. El precio de WALMEXV=$49.39 y número de trayectorias que se simularon para determinar los precios de las opciones fue de 10,000. Se tienen quince precios de ejercicio de los cuales siete están dentro del dinero para opciones de compra y ocho están dentro del dinero para opciones de venta. Se observa que para opciones al plazo de T=30 días en los primeros tres precios de ejercicio, los precios de opciones de compra con subyacente promedio resultaron mayores que los precios publicados por MexDer. Para los plazos de T=128 días y T=219 días solo para el primer precio de ejercicio los precios de opciones de compra son menores en comparación con los precios de las publicadas por MexDer, mientras que para el plazo de T=303 días solamente los dos primeros precios de ejercicio. En cuanto a las opciones de venta el análisis del cuadro A.1 y la gráfica 2 resulta que los precios de opciones de venta con subyacente promedio son menores para los cuatro plazos considerados.

## 8. Conclusiones

En esta investigación se planteó y resolvió un problema de Control Óptimo Estocástico en Optimización Dinámica que modela la toma de decisiones de un consumidor racional quien dispone de una riqueza inicial y enfrenta la decisión de cómo distribuir su riqueza entre consumo y un portafolio de activos en horizonte de planeación finito, de tal forma que maximice su utilidad total esperada por el consumo e inversión. Entre los supuestos del modelo están que el agente puede invertir en una acción con volatilidad estocástica y una opción asiática de venta con precio de ejercicio media aritmética y de tipo europea, cuyas distribuciones respectivas de precios y volatilidad son modeladas por movimientos geométricos Brownianos. Una particularidad de la programación dinámica como herramienta de solución al modelo, es que este se resuelve analíticamente de manera determinista al resolver la EDP de HJB, pero con soluciones estocásticas. Por otra parte en el proceso de solución del modelo, a través de un sistema de ecuaciones diferenciales resultante se deduce una ecuación diferencial parcial de segundo orden equivalente a la de Black-Scholes-Merton con la que se valúa una opción asiática de venta de tipo europeo, con precio de ejercicio variable igual a la media aritmética mediate microfundamentos. Se hace importante observar que la fórmula alternativa de valuación deducida en este trabajo no estaba disponible en la literatura, mediante fundamentos de racionalidad económica. Para verificar las ventajas del modelo propuesto se desarrolla una metodología mediante simulación Montecarlo con los siguientes supuestos: la volatilidad del subyacente es estocástica, los parámetros se pueden obtener a partir de la volatilidad del subyacente, el precio del subyacente y la volatilidad σ t son conducidos por un movimiento geométrico browniano. El subyacente es el precio de la acción de WALMEXV y se comparan con los precios de opciones publicadas en el boletín del mercado mexicano de derivados (MEXDER) del día dieciséis de mayo de dos mil dieciocho. Se supone que los parámetros de volatilidad estocástica se calculan mediante una adaptación del modelo de CIR al método de volatilidad realizada. La tasa de interés se obtiene de la página de Banxico para los cuatro plazos de las opciones del boletín. A partir de la volatilidad anualizada se determinaron los parámetros necesarios para la simulación del precio de la opción. Un resultado relevante es que, al comparar los precios de opciones europeas, tanto simulados como con los publicados por el Mercado Mexicano de Derivados con sus contrapartes asiáticas, los precios de opciones asiáticas son muy cercanos en el caso de opciones de compra y de venta dentro del dinero, en el dinero y fuera del dinero para el corto plazo, pero conforme el plazo al vencimiento de la opción se incrementa, la diferencia entre las europeas y las asiáticas aumenta ya que la prima es menor. Lo anterior se debe a que por el supuesto de volatilidad estocástica, la volatilidad del promedio aritmético tiene variaciones menos significativas, lo que genera diferencia en los precios de opciones europeas versus opciones asiáticas y esta diferencia se acentúa más en el largo plazo. Esto muestra que las opciones asiáticas presentan ventaja respecto a las opciones europeas. Para futuras líneas de investigación se plantea extender la valoración de opciones de tipo asiático con promedio geométrico, tasa de interés y/o volatilidad estocástica y de tipo americana, y en un contexto microeconómico y/o macroeconómico.


<!-- p:15 -->

### Apéndice

Cuadro A1. Precios de opciones europeas de compra y de venta sobre WALMEXV, obtenidos con parámetros calibrados para la volatilidad con adaptación del modelo de CIR.

| Días por vencer   | K           | WALMEXV CallEur      | WALMEXV PutEur   | Average Price Call WALMEXV   | Average Price Put WALMEXV   | WALMEXV Call MexDer   | WALMEXV Put MexDer   |
|-------------------|-------------|----------------------|------------------|------------------------------|-----------------------------|-----------------------|----------------------|
| T=30              | 43.00       | 6.6795               | 0.0084           | 6.6711                       | 0.0000                      | 6.55                  | 0.04                 |
|                   | 44.00       | 5.7025               | 0.0270           | 5.6755                       | 0.0000                      | 5.58                  | 0.05                 |
|                   | 45.00       | 4.7451               | 0.0627           | 4.6824                       | 0.0000                      | 4.62                  | 0.09                 |
|                   | 46.00       | 3.8335               | 0.1455           | 3.6881                       | 0.0000                      | 3.71                  | 0.16                 |
|                   | 47.00       | 3.0005               | 0.3027           | 2.6979                       | 0.0000                      | 2.87                  | 0.28                 |
|                   | 48.00       | 2.2495               | 0.5455           | 1.7040                       | 0.0000                      | 2.13                  | 0.51                 |
|                   | 49.00       | 1.5975               | 0.8889           | 0.7086                       | 0.0000                      | 1.50                  | 0.88                 |
|                   | 50.00       | 1.0942               | 1.3778           | 0.0000                       | 0.2837                      | 1.00                  | 1.41                 |
|                   | 51.00       | 0.6905               | 1.9700           | 0.0000                       | 1.2795                      | 0.62                  | 2.10                 |
|                   | 52.00       | 0.4320               | 2.7033           | 0.0000                       | 2.2713                      | 0.36                  | 2.92                 |
|                   | 53.00       | 0.2583               | 3.5218           | 0.0000                       | 3.2635                      | 0.20                  | 3.82                 |
|                   | 54.00       | 0.1372               | 4.3938           | 0.0000                       | 4.2567                      | 0.10                  | 4.77                 |
|                   | 55.00       | 0.0727               | 5.3230           | 0.0000                       | 5.2503                      | 0.04                  | 5.75                 |
|                   | 56.00       | 0.0316               | 6.2785           | 0.0000                       | 6.2469                      | 0.02                  | 6.75                 |
|                   | 57.00       | 0.0126               | 7.2531           | 0.0000                       | 7.2405                      | 0.01                  | 7.74                 |
|                   | 43.00       | 7.7754               | 0.1894           | 7.5860                       | 0.0000                      | 7.54                  | 0.37                 |
|                   | 44.00       | 6.8738               | 0.2745           | 6.5993                       | 0.0000                      | 6.66                  | 0.49                 |
|                   | 45.00       | 6.0490               | 0.4102           | 5.6388                       | 0.0000                      | 5.83                  | 0.66                 |
|                   | 46.00       | 5.2784               | 0.6110           | 4.6674                       | 0.0000                      | 5.06                  | 0.87                 |
|                   | 47.00       | 4.5288               | 0.8363           | 3.6925                       | 0.0000                      | 4.35                  | 1.14                 |
|                   | 48.00       | 3.8609               | 1.1378           | 2.7232                       | 0.0000                      | 3.71                  | 1.47                 |
|                   | 49.00       | 3.2295               | 1.4843           | 1.7452                       | 0.0000                      | 3.13                  | 1.87                 |
| T=128             | 50.00       | 2.7113               | 1.9292           | 0.7821                       | 0.0000                      | 2.60                  | 2.34                 |
|                   | 51.00       | 2.1980               | 2.3924           | 0.0000                       | 0.1944                      | 2.14                  | 2.89                 |
|                   | 52.00       | 1.8082               | 2.9705           | 0.0000                       | 1.1622                      | 1.73                  | 3.51                 |
|                   | 53.00       | 1.4488               | 3.5853           | 0.0000                       | 2.1365                      | 1.38                  | 4.22                 |
|                   | 54.00       | 1.1066               | 4.2259           | 0.0000                       | 3.1194                      | 1.08                  | 5.00                 |
|                   | 55.00       |                      |                  |                              |                             |                       | 5.85                 |
|                   | 56.00       | 0.8612               | 4.9531           | 0.0000                       | 4.0919                      | 0.82                  | 6.77                 |
|                   | 57.00       | 0.6678 0.5220        | 5.7269 6.5537    | 0.0000 0.0000                | 5.0591 6.0317               | 0.61 0.44             | 7.74                 |
| T=219             | 43.00       | 8.7163               | 0.2790           | 8.4372                       | 0.0000                      | 8.41                  | 0.72                 |
| T=219             | 44.00       | 7.8539               | 0.3805           | 7.4734                       | 0.0000                      | 7.56                  | 0.91                 |
| T=219             | 45.00       | 7.0615               | 0.5362           | 6.5252                       | 0.0000                      | 6.76                  | 1.13                 |
| T=219             | 46.00       | 6.2975               | 0.7293           | 5.5682                       | 0.0000 0.0000               | 6.02 5.33             | 1.40                 |
| T=219             | 47.00 48.00 | 5.6160 4.9236        | 0.9829 1.2546    | 4.6331 3.6691                | 0.0000                      | 4.70                  | 1.71 2.06            |
| T=219             | 49.00       | 4.2585               | 1.5509           | 2.7076                       | 0.0000                      | 4.12                  | 2.47                 |
| T=219             | 50.00       | 3.6920               | 1.9329           | 1.7591                       | 0.0000                      | 3.59                  | 2.92                 |
| T=219             | 51.00       | 3.2505               | 2.4245           | 0.8260                       | 0.0000                      | 3.11                  | 3.43                 |
| T=219             | 52.00       | 2.7192               | 2.8654           | 0.0000                       | 0.1461                      | 2.67                  | 4.00                 |
| T=219             | 53.00       | 2.3132               | 3.4016           | 0.0000                       | 1.0884                      | 2.27                  | 4.63                 |
| T=219             | 54.00       | 1.9343               | 3.9833           | 0.0000                       | 2.0490                      | 1.92                  | 5.32                 |
| T=219             | 55.00       | 1.6394               | 4.6302           | 0.0000                       | 2.9908                      | 1.60                  | 6.07                 |
| T=219             | 56.00       | 1.4280               | 5.3496           | 0.0000                       | 3.9216                      | 1.32                  | 6.89                 |
|                   | 57.00       | 1.1344               | 6.0310           | 0.0000                       | 4.8966                      | 1.07                  | 7.78                 |
|                   | 43.00       | 9.5529               | 0.3415           | 9.2115                       | 0.0000                      | 9.09                  | 1.01                 |
|                   | 44.00       | 8.7188               | 0.4483           | 8.2705                       | 0.0000                      | 8.21                  | 1.22                 |
|                   | 45.00       | 7.9275               | 0.5974           | 7.3301                       | 0.0000                      | 7.39                  | 1.47                 |
|                   | 46.00       | 7.1563               | 0.7685           | 6.3878                       | 0.0000                      | 6.65                  | 1.76                 |
|                   | 47.00       | 6.4727               | 1.0086           | 5.4642                       | 0.0000                      | 5.97                  | 2.09                 |
|                   | 48.00       | 5.7095               | 1.2094           | 4.5001                       | 0.0000                      | 5.36                  | 2.45                 |
| T=303             | 49.00       | 5.1154               | 1.5330           | 3.5824                       | 0.0000                      | 4.81                  | 2.86                 |
| T=303             | 50.00       | 4.5535               | 1.9042           | 2.6493                       | 0.0000                      | 4.31                  | 3.32                 |
| T=303             | 51.00       | 4.0360               | 2.3063           | 1.7296                       | 0.0000                      | 3.85                  | 3.83                 |
| T=303             | 52.00       | 3.5232               | 2.7333           | 0.7899                       | 0.0000                      | 3.43                  | 4.38                 |
| T=303             | 53.00       | 3.0799               | 3.2252           | 0.0000                       | 0.1454                      | 3.03                  | 4.99                 |
| T=303             | 54.00       | 2.6983               | 3.7734           | 0.0000                       | 1.0751                      | 2.66                  | 5.64                 |
| T=303             | 55.00       |                      | 4.2830           | 0.0000                       | 2.0336                      | 2.32                  | 6.36                 |
| T=303             | 56.00 57.00 | 2.2494 1.9166 1.6792 | 4.8858 5.5651    | 0.0000 0.0000                | 2.9692 3.8859               | 1.99 1.69             | 7.12 7.94            |

Fuente: elaboración propia.
