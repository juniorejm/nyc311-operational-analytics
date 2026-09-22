# NYC 311 Operational Analytics

Predicción y priorización de solicitudes de servicio de NYC 311: estimar qué solicitudes superarán un umbral de tiempo de cierre, para ayudar a los equipos de servicio a priorizar.

## Estado

🚧 En desarrollo · Semana 1: análisis estadístico exploratorio de los tiempos de cierre.

## Datos

- Fuente: [NYC 311 Service Requests](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9), NYC Open Data.
- Alcance inicial: categoría "Noise - Residential".
- Los datos no se incluyen en el repositorio. Ver `data/README.md` para descargarlos.

## Estructura

Basada en [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/), con el paquete en `src/` y dependencias gestionadas con `uv`.

## Cómo ejecutarlo

```bash
uv sync
```

## Stack

Python 3.12 · pandas · NumPy · SciPy · statsmodels · scikit-learn · matplotlib · seaborn