
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
- [Construcción del índice invertido](#Construcción-del-índice-invertido)
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
   <image src= https://media.discordapp.net/attachments/731643901248536657/861472435098222642/unknown.png>
 - Separamos el texto de los tweets en palabras -> split()
 - Removemos los Stop-Words del texto -> FIltramos comparando con la data de stop_words obtenida.
 - Aplicamos un Stem a las palabras restantes -> stem() -> Proceso en el cual las palabras se reducen a su raíz o parte significativa, en un esfuerzo por reducir el número de palabras que almcenaremos en nuestro índice.

Luego de esto obtenemos una representación de cada oración del contenido en basea estas palabras, denominados tokens. Este proceso también será aplicado luego a las querys
Por ejemplo, una oración que originalmente sería "Keiko y pedro Castillo presidentes", se vería de la siguiente manera una vez tokenizada:
<image src=https://media.discordapp.net/attachments/731643901248536657/861473133859831828/unknown.png>

Repitiendo  el proceso en los textos, podemos obtener fácilmente la lista de tokens que usaremos en la colección de documentos. Mientras obtenemos estos tokens, también iremos construyendo el índice invertido. El índice invertido es una especie de diccionario que utilizaremos para almcenar las id de los tweets que contienen el token. Para esto, cada token irá "registrando" el tweet al que perteneces, de tal manera que al iterar por todo el documento, procesaremos a la par 3 cosas:

 - A qué documento pertenece un determinado token -> Si el token ya estaba en nuestro índice, se hace una especie de append con el valor del id del tweet al que pertenece. Caso contrario, se añadirá una nueva entrada al índice.
 - Se calculará luego la longitud del tweet en una estructura global para luego recuperarla al momento de normalizarlos scores.
 - Se contabilizará la frecuencia en la colección de cada token, simplemente contando en cuantos documentos está presente, osea cuantas veces hemos intentado añadir un id nuevo al índice.

Al finalizar la iteración por la colección tendremos un gran índice de la siguiente estructura:

 - Token -> Frecuencia -> id[0] -> id[1] -> .....

# Manejo de memoria secundaria
Obviamente, este índice obtenido solo puede ser almacenado en RAM si el tamaño de la colección lo permite. Para colecciones mucho más grandes, será necesario almacenar el propio índice en memoria secundaria.

Una muestra de cómo se vé el índice almacenando sus valores en un archivo txt:
<image src=https://media.discordapp.net/attachments/731643901248536657/861474847653625876/unknown.png>

Cuando la data crece a tamaños aún mayores, para temas de optimización a veces será necesario realizar un sorted based index, en el cual el propio índice será almacenado en "bloques", siendo cada bloque una especie de índice por su cuenta. En este caso, los procesos de recuperación primero necesitarán ejecutar un algoritmo para recuperar de manera ordenada el índice adecuado.

#Ejec

