# buscarPosteosFacebook
Script Python que utilizar  y permite exportar los posteos a un archivo CSV
Permite acceder automáticamente la busqueda avanzada de Facebook y extraer un conjunto de posteos, y volcar la información recolectada en un archivo de texto. 
Esta herramienta está conformada por un script en lenguaje Python. El mismo navega y recupera automáticamente el código HTML de cada posteo para luego procesarlo mediante la biblioteca Beautiful Soup y exportar los siguientes datos: post_id, username, post_type, post_published, post_published_unix, post_published_sql, post_hora_argentina, like_count_fb, comments_count_fb, reactions_count_fb, shares_count_fb, engagement_fb, rea_NONE, rea_LIKE, rea_LOVE, rea_WOW, rea_HAHA, rea_SAD, rea_ANGRY, rea_THANKFUL, post_message, has_emoji, menciones, hashtags, 	tiene_hashtags y tiene_menciones.


## Dependencias
Para utilizar el script es necesario instalar las siguientes librerias python:
- BeautifulSoup4
- Pandas
- Selenium
- Selenium Driver para Firefox

La instalacion puede hacerse utilizando pip de la siguiente manera:
- \$ su
- \# pip3 install pandas
- \# pip3 install selenium
- \# pip3 install bs4
- \# installgeckodriver.sh


## Configuracion
El archivo config.json, permite configurar los datos de la cuenta de Facebook que se usara para recuperar los post. Tambien se puede configurar los nombres de los archivos de entrada y salida asi como el directorio base de esos archivos.

## Windows
Para ejecutar en windows hay que instalar el driver de selenium primero. Se puede usar la siguiente Guia: https://medium.com/ananoterminal/install-selenium-on-windows-f4b6bc6747e4
Una vez instalado el driver, en el archivo de configuracion hay
que ajustar los parametros gecko_binary y gecko_driver_exe con las rutas de los exes de Firefox y del driver respectivamente.