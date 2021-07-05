
# <div align="center">
  <h1>Proyecto 2 - Base de datos II </h1>
</div>

Integrantes
- Jean Miraval
- Fabrizio Vásquez
- Mateo Noel

# Tabla de contenido

- [Introducción](#Introducción)
    - [Objetivo del proyecto](#Objetivo-del-proyecto)
- [Generador de data](#Generador-de-data)
- [Construcción del índice invertido](#Construcción-del-indice-invertido)
- [Manejo de memoria secundaria](#Aspectos-importantes-de-la-implementación-de-dichas-técnicas)
- [Ejecución óptima de consultas](#Resultados-Experimentales)
- [Video de uso de la aplicación](#Video-de-uso-de-la-aplicación)

# Introducción
Proyecto válido por el curso Base de Datos II del ciclo 2021-1
## Objetivos del proyecto
- Profundizar los conceptos de recuperación de documentos de texto.
- Implementar un índice invertido en memoria secundaria para ejecutar recuperación de texto.
- Comprender el procesamiento interno en backend de las búsquedas por similitud en documentos de texto-
- Crear un sistema amigable de búsqueda simple en base a una colección de información.

# Generador de data
La data a utilizar fue una colección de tweets recientes, recolectados en tiempo real. Para esto se utilizó un script de twitter tracking, en el cual se accede al API de Twitter para con ciertos parámetros filtrar qué tweets, usuarios o tópicos importantes te interesa seguir.
Como resultado de los scripts se obtiene data completa a detalle de todos los tweets recolectados en formato JSON, pero para aliviar la información, espacio y costo innecesario, se parseó este repositorio de tweets a través de un cleaner, donde solo se mantuvo la información más relevante.
Al final de esta proceso, se obtuvo un documento JSON con información de los tweets. Para aplicar el programa que hemos desarrollado es necesario incluir en el proyecto el archivo JSON con los mismos formatos.

# Construcción del índice invertido
Para construir el índice invertido, como primer paso tuvimos que identificar los stop-words, que son palabras que por lo general son de poca relevancia en relación al tópico del texto. Estos stopwords se obtuvieron desde la plataforma web https://countwordsfree.com/stopwords/spanish, de donde se extrajeron como archivo de texto.


Luego de esto, se procesó toda la información de los tweets a travésde 3 procesos:

 - Separamos el texto de los tweets en palabras -> split()
 - Removemos los Stop-Words del texto -> FIltramos comparando con la data de stop_words obtenida.
 - Aplicamos un Stem a las palabras restantes -> stem() -> Proceso en el cual las palabras se reducen a su raíz o parte significativa, en un esfuerzo por reducir el número de palabras que almcenaremos en nuestro índice.
