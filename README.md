# buscarPosteosFacebook
Script Python que permite acceder automáticamente a la busqueda avanzada de Facebook, extraer un conjunto de posteos, y volcar la información recolectada en un archivo de texto.
Esta herramienta está conformada por un script en lenguaje Python. El mismo navega y recupera automáticamente el código HTML de cada posteo para luego procesarlo mediante la biblioteca Beautiful Soup y exportar los siguientes datos: post_id, username, post_type, post_published, post_published_unix, post_published_sql, post_hora_argentina, like_count_fb, comments_count_fb, reactions_count_fb, shares_count_fb, engagement_fb, rea_NONE, rea_LIKE, rea_LOVE, rea_WOW, rea_HAHA, rea_SAD, rea_ANGRY, rea_THANKFUL, post_message, has_emoji, menciones, hashtags, tiene_hashtags y tiene_menciones.


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
El archivo config.json, permite configurar la herramienta para recuperar los post.
Las opciones que se pueden configurar son:
- base_path: indica la ruta/directorio donde se guardaran los archivos de salida. Por defecto es la carpeta “data” dentro de la herramienta.
- output_filename: nombre del archivo de salida del listado de posteos recuperado. Por defecto, se llama “posts_output.csv
- output_post_filename: nombre del archivo de salida de cada posteo en HTML. Por defecto, se llama “ln_post_.html
- gecko_binary: Ruta al archivo exe del navegador Firefox.
- gecko_driver_exe: Ruta al archivo del archivo exe del driver de selenium. Viene incluido en el paquete de la herramienta y no debería cambiarse.
- user y password: Usuario y Contraseña de Facebook para el login.
- max_scroll: Cantidad máxima de scroll por página de búsqueda.
- page_name: Nombre de la página de Facebook para buscar posts. 
- search_year y search_month: Año y mes a buscar. Como Facebook limita la actividad automática lo mejor es buscar un mes y después esperar un rato (20 minutos) y retomar con otro mes.


## Windows
Para ejecutar en windows hay que instalar el driver de selenium primero. Se puede usar la siguiente Guia: https://medium.com/ananoterminal/install-selenium-on-windows-f4b6bc6747e4
Una vez instalado el driver, en el archivo de configuracion hay
que ajustar los parametros gecko_binary y gecko_driver_exe con las rutas de los exes de Firefox y del driver respectivamente.
