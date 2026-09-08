# Reformulación metodológica para una versión publicable

## 1. Diagnóstico del experimento actual

El proyecto tiene una base útil —inferencia Bayesiana de parámetros GBM, implementación explícita de Metropolis–Hastings y valuación Monte Carlo de una opción path-dependent—, pero la versión actual mezcla dos objetos probabilísticos distintos.

### 1.1 Medida física \(\mathbb P\) vs. medida neutral al riesgo \(\mathbb Q\)

Los retornos históricos permiten inferir parámetros del proceso bajo \(\mathbb P\):

\[
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t^{\mathbb P}.
\]

En Black–Scholes, el precio sin arbitraje de un derivado negociable se obtiene bajo \(\mathbb Q\):

\[
dS_t=(r-q)S_t\,dt+\sigma S_t\,dW_t^{\mathbb Q}.
\]

Por tanto, propagar directamente la posterior histórica de \(\mu\) dentro de

\[
e^{-rT}\mathbb E[(\bar S-K)^+]
\]

y llamar al resultado "precio Black–Scholes" no es correcto. Bajo el modelo completo de Black–Scholes, \(\mu\) desaparece del precio de no arbitraje.

La incertidumbre Bayesiana relevante para el pricing básico es la que permanece en parámetros que también afectan la dinámica bajo \(\mathbb Q\), en particular \(\sigma\).

### 1.2 El contraste L2 de Media Bayesiana vs. MAP es circular

En el notebook se define, para muestras posteriores de precio \(C_1,\ldots,C_M\),

\[
L_2(a)=\frac1M\sum_{i=1}^M(C_i-a)^2.
\]

El minimizador exacto es

\[
a^*=\bar C=\frac1M\sum_i C_i.
\]

Por identidad algebraica,

\[
\sum_i(C_i-a)^2
=
\sum_i(C_i-\bar C)^2+M(a-\bar C)^2.
\]

Así, comparar el posterior mean contra un MAP plug-in usando esa misma muestra posterior como "verdad" garantiza que la media tendrá menor o igual pérdida L2. Una prueba de Wilcoxon posterior no convierte esta propiedad en evidencia empírica de mejor pricing.

La evaluación correcta debe hacerse contra:

1. un precio verdadero conocido en un estudio de simulación;
2. un benchmark numérico de alta precisión; o
3. precios de mercado fuera de muestra.

### 1.3 El "MAP" empleado necesita redefinirse

La moda marginal de \(\mu\) obtenida por KDE y la moda marginal de \(\sigma\) obtenida por separado no constituyen, en general, el MAP conjunto

\[
(\hat\mu_{MAP},\hat\sigma_{MAP})
=\arg\max_{\mu,\sigma}p(\mu,\sigma\mid\mathcal D).
\]

Además, la moda no es invariante ante transformaciones no lineales, por lo que "MAP en parámetros" y "moda del precio inducido" son objetos distintos. El ancho de banda del KDE introduce otra decisión metodológica.

### 1.4 Diagnóstico MCMC insuficiente para un artículo

Una sola cadena con autocorrelación de lag 1 cercana a uno en \(\mu\) no es una base adecuada para afirmar convergencia. La versión publicable debe usar, como mínimo:

- múltiples cadenas sobredispersas;
- \(\widehat R\) rank-normalized;
- bulk ESS y tail ESS;
- MCSE de cantidades reportadas;
- trazas y autocorrelaciones;
- muestreo de \(\log\sigma\) o una reparametrización que respete positividad.

Metropolis–Hastings puede mantenerse por razones pedagógicas/metodológicas, pero debe compararse contra un sampler de referencia o una solución numérica de la posterior en este problema bidimensional.

### 1.5 Priors y parametrización

El prior actual \(\sigma\sim\mathrm{InvGamma}(2,0.1)\) está definido directamente sobre la desviación estándar. Es válido como distribución, pero no es el prior conjugado habitual sobre \(\sigma^2\) y no debe llamarse automáticamente "débil". Con esa parametrización tiene media 0.1 y varianza infinita; su interpretación económica debe justificarse mediante prior predictive checks.

## 2. Pregunta de investigación propuesta

> **¿Cuándo la incertidumbre Bayesiana sobre la volatilidad, estimada a partir de retornos históricos, genera diferencias económicamente relevantes entre full Bayesian pricing y plug-in pricing para opciones asiáticas aritméticas bajo una medida neutral al riesgo?**

Esta pregunta conserva el núcleo del proyecto —Bayes, MCMC, GBM, opciones asiáticas y Monte Carlo— pero elimina la confusión entre pronóstico físico y valuación sin arbitraje.

## 3. Objetos matemáticos

### 3.1 Inferencia

\[
p(\mu,\sigma\mid\mathcal D)
\propto
p(\mathcal D\mid\mu,\sigma)p(\mu,\sigma).
\]

Para pricing Black–Scholes basta la marginal

\[
p(\sigma\mid\mathcal D)
=\int p(\mu,\sigma\mid\mathcal D)\,d\mu.
\]

### 3.2 Precio condicional sin arbitraje

Para una call asiática aritmética discretamente monitoreada,

\[
C_Q(\sigma)
=e^{-rT}\mathbb E^{\mathbb Q}_\sigma
\left[\left(\frac1m\sum_{j=1}^mS_{t_j}-K\right)^+\right],
\]

con

\[
dS_t=(r-q)S_tdt+\sigma S_tdW_t^{\mathbb Q}.
\]

### 3.3 Distribución posterior de precios de modelo

\[
p(C\mid\mathcal D)
=\int \delta_{C_Q(\sigma)}\,p(\sigma\mid\mathcal D)\,d\sigma.
\]

Los estimadores a comparar pueden incluir

\[
\hat C_{FB}=\mathbb E[C_Q(\sigma)\mid\mathcal D],
\qquad
\hat C_{mean}=C_Q(\mathbb E[\sigma\mid\mathcal D]),
\]

\[
\hat C_{MLE}=C_Q(\hat\sigma_{MLE}),
\qquad
\hat C_{MAP}=C_Q(\hat\sigma_{MAP}).
\]

## 4. Diseño de simulación recomendado

Generar \(R\) datasets independientes bajo parámetros conocidos. Una cuadrícula útil es:

- tamaño histórico \(n\in\{20,60,125,252,504,1260\}\);
- volatilidad verdadera \(\sigma_0\in\{0.10,0.20,0.35,0.50\}\);
- moneyness \(K/S_0\in\{0.8,1.0,1.2\}\);
- madurez \(T\in\{0.25,0.5,1,2\}\);
- número de fechas de monitoreo de la asiática \(m\in\{12,52,252\}\).

Para cada dataset:

1. inferir \(p(\sigma\mid\mathcal D)\);
2. producir los cuatro estimadores de precio;
3. calcular un benchmark \(C_Q(\sigma_0)\) con un Monte Carlo de error despreciable;
4. medir sesgo, RMSE y error absoluto contra ese benchmark;
5. evaluar cobertura de intervalos posteriores de precio;
6. reportar MCSE para separar error de integración Bayesiana y error de pricing Monte Carlo.

El número final de repeticiones debe elegirse por precisión Monte Carlo, no por conveniencia. Para resultados principales, \(R\ge 500\) es un objetivo razonable si la implementación usa reducción de varianza y vectorización.

## 5. Benchmarks numéricos

La opción asiática aritmética no tiene una fórmula Black–Scholes elemental comparable a la call europea. El motor Monte Carlo debe validarse contra:

- opción asiática geométrica discretamente monitoreada, que sí tiene solución cerrada;
- control variate geométrico;
- antithetic variates;
- convergencia en número de trayectorias y fechas de monitoreo;
- cuando sea posible, un segundo método independiente (PDE, transformada o benchmark publicado).

El módulo `src/asian_pricing.py` implementa el primer bloque de esta validación.

## 6. Hipótesis testables

### H1 — Efecto de tamaño muestral

La dispersión posterior de \(\sigma\) y la dispersión inducida de \(C_Q(\sigma)\) deben contraerse al aumentar \(n\).

### H2 — Full Bayes vs. plug-in

La brecha

\[
\Delta_{FB}=\mathbb E[C_Q(\sigma)\mid\mathcal D]
-C_Q(\mathbb E[\sigma\mid\mathcal D])
\]

debe ser mayor en magnitud cuando la posterior de \(\sigma\) sea más dispersa. El signo no debe imponerse de antemano; debe estudiarse a partir de la curvatura de \(C_Q(\sigma)\).

### H3 — Path dependence

La sensibilidad de la incertidumbre paramétrica puede diferir entre una call europea y una call asiática aun bajo los mismos \((S_0,K,r,q,T,\sigma)\). La comparación debe hacerse con vega efectiva y con la curvatura respecto de \(\sigma\), no atribuyendo automáticamente mayor riesgo a la dependencia de trayectoria.

### H4 — Priors

El efecto Bayesiano debe aumentar cuando la información histórica es escasa y disminuir conforme domina la likelihood. Esto se puede evaluar con priors alternativos y prior predictive checks.

## 7. Extensión empírica

Una publicación más fuerte necesita datos reales. Dos rutas son defendibles:

1. **Retornos reales + experimento de valuación:** estimar \(p(\sigma\mid\mathcal D)\) en ventanas históricas reales y estudiar la distribución de precios de modelo para contratos asiáticos hipotéticos. Esto permite hablar de sensibilidad/uncertainty quantification, no de precisión contra mercado.
2. **Datos de opciones observadas:** si se consiguen precios de instrumentos compatibles, evaluar pricing y cobertura fuera de muestra. Para opciones asiáticas OTC la disponibilidad de datos es una restricción real y debe reconocerse.

## 8. Novedad que sí puede defenderse

"Usar Metropolis–Hastings para Black–Scholes" no constituye novedad suficiente. La contribución potencial debe estar en el experimento y en la comparación cuantitativa:

- separación explícita entre inferencia bajo \(\mathbb P\) y pricing bajo \(\mathbb Q\);
- propagación posterior coherente a un payoff path-dependent;
- caracterización del error de plug-in como función de muestra histórica, moneyness, madurez y frecuencia de monitoreo;
- análisis de cobertura y riesgo frecuentista de estimadores Bayesianos de precios;
- reproducibilidad completa y benchmarks numéricos fuertes.

## 9. Criterio de publicación

### No enviar todavía

La versión original contiene una objeción de pricing fundamental y una comparación L2 circular. Un referee de derivados cuantitativos probablemente detendría la evaluación en esos puntos.

### Viable tras la reformulación

Con la corrección \(\mathbb P\to\mathbb Q\), un estudio de simulación bien diseñado, literatura actual, diagnósticos MCMC correctos y benchmarks sólidos, el proyecto puede convertirse en un artículo aplicado/metodológico coherente.

Para una revista de finanzas cuantitativas muy especializada se necesitaría una contribución matemática o computacional más novedosa. Para una revista aplicada de economía/finanzas con alcance en ingeniería financiera, el estándar es más alcanzable si la evidencia empírica y la originalidad están bien articuladas.
