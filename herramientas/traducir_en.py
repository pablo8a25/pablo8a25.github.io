"""Genera en/index.html (inglés) a partir de index.html (español).

Si cambias un texto en index.html, cambia también su traducción aquí y corre:
    python herramientas/traducir_en.py
El script se detiene y avisa si algún texto en español ya no coincide.
"""
import pathlib, sys

raiz = pathlib.Path(__file__).resolve().parent.parent  # carpeta de la página
html = (raiz / "index.html").read_text(encoding="utf-8")

# (texto en español, texto en inglés, veces que debe aparecer)
pares = [
    # Pie (va primero porque repite enlaces del menú)
    ('<nav aria-label="Sitio"><h4>Sitio</h4><a href="#inicio">Inicio</a><a href="#servicios">Servicios</a><a href="#proyectos">Proyectos</a><a href="#perfil">Perfil</a></nav>',
     '<nav aria-label="Site"><h4>Site</h4><a href="#inicio">Home</a><a href="#servicios">Services</a><a href="#proyectos">Projects</a><a href="#perfil">Profile</a></nav>', 1),
    ('<nav aria-label="Enlaces"><h4>Enlaces</h4><a href="https://github.com/pablo8a25" target="_blank" rel="noopener">GitHub</a><a href="mailto:pablo8abc@gmail.com">Correo</a><a href="en/" hreflang="en" lang="en">English</a></nav>',
     '<nav aria-label="Links"><h4>Links</h4><a href="https://github.com/pablo8a25" target="_blank" rel="noopener">GitHub</a><a href="mailto:pablo8abc@gmail.com">Email</a><a href="../" hreflang="es" lang="es">Español</a></nav>', 1),

    # Cabecera del documento y rutas de archivos
    ('<html lang="es">', '<html lang="en">', 1),
    ('<title>Pablo Ortiz Ochoa · IA aplicada y diseño web</title>', '<title>Pablo Ortiz Ochoa · Applied AI &amp; web design</title>', 1),
    ('content="Portafolio de Pablo Ortiz Ochoa: páginas web, automatizaciones y herramientas con inteligencia artificial para que los negocios trabajen mejor."',
     'content="Portfolio of Pablo Ortiz Ochoa: websites, automations and AI-powered tools that help businesses work better."', 1),
    ('<meta property="og:title" content="Pablo Ortiz Ochoa · IA aplicada y diseño web">', '<meta property="og:title" content="Pablo Ortiz Ochoa · Applied AI &amp; web design">', 1),
    ('content="Páginas web, automatizaciones y herramientas con inteligencia artificial."', 'content="Websites, automations and AI-powered tools."', 1),
    ('content="img/pablo.jpg"', 'content="https://pablo8a25.github.io/img/pablo.jpg"', 1),
    ('src="img/', 'src="../img/', 9),
    ('href="img/', 'href="../img/', 2),
    ('url(img/logo.svg)', 'url(../img/logo.svg)', 1),

    # Encabezado y menús
    ('aria-label="Pablo Ortiz, inicio"', 'aria-label="Pablo Ortiz, home"', 1),
    ('<nav aria-label="Principal">', '<nav aria-label="Main">', 1),
    ('<a href="#proyectos">Proyectos</a>', '<a href="#proyectos">Projects</a>', 2),
    ('<a href="#servicios">Servicios</a>', '<a href="#servicios">Services</a>', 1),
    ('<a href="#perfil">Perfil</a>', '<a href="#perfil">Profile</a>', 1),
    ('<span class="idioma"><span aria-current="page">ES</span><a href="en/" hreflang="en" lang="en" aria-label="Read in English">EN</a></span>',
     '<span class="idioma"><a href="../" hreflang="es" lang="es" aria-label="Ver en español">ES</a><span aria-current="page">EN</span></span>', 2),
    ('>Hablemos <span class="flecha"', '>Let’s talk <span class="flecha"', 2),
    ('<nav class="menu" id="menu" aria-label="Secciones">', '<nav class="menu" id="menu" aria-label="Sections">', 1),
    ('<a class="opcional" href="#perfil">Perfil</a>', '<a class="opcional" href="#perfil">Profile</a>', 1),
    ('<a class="opcional" href="#servicios">Servicios</a>', '<a class="opcional" href="#servicios">Services</a>', 1),
    ('alt="">Hablemos</a>', 'alt="">Let’s talk</a>', 1),

    # Portada
    ('alt="Retrato de Pablo Ortiz Ochoa a contraluz, con el cielo del atardecer detrás"', 'alt="Backlit portrait of Pablo Ortiz Ochoa against a sunset sky"', 1),
    ('aria-label="Diseño web y automatización con IA"', 'aria-label="Web design and automation with AI"', 1),
    ('data-letras>Diseño web</span>', 'data-letras>Web design</span>', 1),
    ('data-letras>y automatización</span>', 'data-letras>and automation</span>', 1),
    ('data-letras>con IA</span>', 'data-letras>with AI</span>', 1),
    ('<p class="intro"><b>Hola, soy Pablo.</b> Hago páginas web, automatizaciones y herramientas con inteligencia artificial que le ahorran tiempo a los negocios.</p>',
     '<p class="intro"><b>Hi, I’m Pablo.</b> I build websites, automations and AI-powered tools that save businesses time.</p>', 1),
    ('<span>Proyectos publicados</span>', '<span>Published projects</span>', 1),
    ('<span>Inglés (Cambridge)</span>', '<span>English (Cambridge)</span>', 1),
    ('<span>Trabajo remoto</span>', '<span>Remote work</span>', 1),
    ('<span class="vivo">Disponible · Medellín <span id="hora">', '<span class="vivo">Available · Medellín <span id="hora">', 1),

    # Qué hago
    ('<span class="rotulo">[ Qué hago ]</span>', '<span class="rotulo">[ What I do ]</span>', 1),
    ('<li>Ingeniería Biotecnológica · EIA</li>\n          <li>Medellín, Colombia</li>\n          <li>Trabajo remoto · ES / EN</li>\n          <li>Diseño web + IA</li>',
     '<li>Biotechnology Engineering · EIA</li>\n          <li>Medellín, Colombia</li>\n          <li>Remote work · ES / EN</li>\n          <li>Web design + AI</li>', 1),
    ('Páginas web, automatizaciones y herramientas con inteligencia artificial, hechas para negocios que quieren trabajar mejor, no más.',
     'Websites, automations and tools powered by artificial intelligence, built for businesses that want to work smarter, not harder.', 1),
    ("const resaltar = ['inteligencia', 'artificial,', 'mejor,'];", "const resaltar = ['artificial', 'intelligence,', 'smarter,'];", 1),
    ('>Ver proyectos <span class="flecha"', '>See projects <span class="flecha"', 1),

    # Cinta
    ('<div class="cinta" aria-label="Datos rápidos">', '<div class="cinta" aria-label="Quick facts">', 1),
    ('<li>5 proyectos publicados</li><li>Inglés B2 · Cambridge</li><li>Python · CS50P de Harvard</li><li>Medellín, Colombia</li><li>Trabajo remoto en español e inglés</li>',
     '<li>5 published projects</li><li>English B2 · Cambridge</li><li>Python · Harvard’s CS50P</li><li>Medellín, Colombia</li><li>Remote work in Spanish and English</li>', 2),

    # Servicios
    ('<span class="rotulo">[ Servicios ]</span>', '<span class="rotulo">[ Services ]</span>', 1),
    ('<span class="t">Diseño web</span>', '<span class="t">Web design</span>', 1),
    ('<div class="flujo">Diseñar <i></i> Publicar</div>', '<div class="flujo">Design <i></i> Launch</div>', 1),
    ('<p>Páginas claras y rápidas, pensadas primero para el celular y publicadas en línea.</p>', '<p>Clear, fast websites, designed for phones first and published online.</p>', 1),
    ('<span class="t">Automatización</span>', '<span class="t">Automation</span>', 1),
    ('<div class="flujo">Registrar <i></i> Resumir</div>', '<div class="flujo">Record <i></i> Summarize</div>', 1),
    ('<p>Lo que hoy se hace a mano todos los días, que lo haga el computador: hojas de cálculo, reportes y alertas.</p>',
     '<p>The tasks you do by hand every day, done by the computer instead: spreadsheets, reports and alerts.</p>', 1),
    ('<span class="t">IA aplicada</span>', '<span class="t">Applied AI</span>', 1),
    ('<div class="flujo">Preguntar <i></i> Responder</div>', '<div class="flujo">Ask <i></i> Answer</div>', 1),
    ('<p>Asistentes y chatbots que responden con la información de tu negocio, sin inventar.</p>', '<p>Assistants and chatbots that answer with your business’s own information, without making things up.</p>', 1),
    ('<span class="t">Datos y cálculo</span>', '<span class="t">Data &amp; computing</span>', 1),
    ('<div class="flujo">Medir <i></i> Mostrar</div>', '<div class="flujo">Measure <i></i> Show</div>', 1),
    ('<p>Simuladores, paneles y gráficas con Python y JavaScript para entender los números.</p>', '<p>Simulators, dashboards and charts with Python and JavaScript to make sense of the numbers.</p>', 1),
    ('>Ejemplo: Litotriptor HM3 ↓', '>Example: Lithotripter HM3 ↓', 1),
    ('>Ejemplo: ', '>Example: ', 3),

    # Proyectos
    ('<span class="rotulo">[ Proyectos ]</span>', '<span class="rotulo">[ Projects · in Spanish ]</span>', 1),
    ('data-ver><span>Proyectos<span class="punto">.</span></span></h2>', 'data-ver><span>Projects<span class="punto">.</span></span></h2>', 1),
    ('<dt>Tipo</dt>', '<dt>Type</dt>', 4),
    ('<dt>Tecnología</dt>', '<dt>Stack</dt>', 4),
    ('<dt>Dato</dt>', '<dt>Key fact</dt>', 4),
    ('<dt>Año</dt>', '<dt>Year</dt>', 4),
    ('>Ver proyecto <span class="flecha"', '>View project <span class="flecha"', 3),
    ('>Código</a>', '>Code</a>', 2),
    ('aria-label="Ver RutaU"', 'aria-label="View RutaU"', 1),
    ('alt="Captura de RutaU: mapa de Medellín con la ruta del bus y la tarjeta de tiempos"', 'alt="RutaU screenshot: map of Medellín with the bus route and the arrival-time card"', 1),
    ('<p class="sub">Los buses de la EIA en el mapa</p>', '<p class="sub">EIA university buses on the map</p>', 1),
    ('<p class="resumen">App web para ver las rutas de los buses de la universidad, saber a qué hora pasa el siguiente y abrir el recorrido en Google Maps o Waze.</p>',
     '<p class="resumen">Web app to see the university bus routes, know when the next one comes and open the route in Google Maps or Waze.</p>', 1),
    ('<dd>App web instalable</dd>', '<dd>Installable web app</dd>', 1),
    ('<dd>JavaScript, Leaflet y OpenStreetMap</dd>', '<dd>JavaScript, Leaflet and OpenStreetMap</dd>', 1),
    ('<dd>7 rutas trazadas sobre calles reales</dd>', '<dd>7 routes traced along real streets</dd>', 1),
    ('aria-label="Ver Café Montaña"', 'aria-label="View Café Montaña"', 1),
    ('alt="Captura del panel de Café Montaña en Google Sheets con ventas, ganancia e inventario"', 'alt="Café Montaña dashboard in Google Sheets with sales, profit and inventory"', 1),
    ('<p class="sub">La caja que se cuadra sola</p>', '<p class="sub">The till that balances itself</p>', 1),
    ('<p class="resumen">Automatización en Google Sheets para una cafetería de ejemplo: registra ventas, descuenta el inventario, avisa lo que se acaba y hace el cierre de caja.</p>',
     '<p class="resumen">Google Sheets automation for a sample café: it records sales, updates the inventory, flags what is running low and closes the till.</p>', 1),
    ('<dd>Automatización de procesos</dd>', '<dd>Process automation</dd>', 1),
    ('<dd>Google Sheets y Apps Script</dd>', '<dd>Google Sheets and Apps Script</dd>', 1),
    ('<dd>1.073 ventas de ejemplo resumidas al instante</dd>', '<dd>1,073 sample sales summarized instantly</dd>', 1),
    ('>Ver hoja <span class="flecha"', '>View sheet <span class="flecha"', 1),
    ('aria-label="Ver el rediseño de Doña Rosa"', 'aria-label="View the Doña Rosa redesign"', 1),
    ('alt="Captura del rediseño de Doña Rosa: título rojo y foto de comida típica"', 'alt="Doña Rosa redesign screenshot: red headline and a photo of Colombian food"', 1),
    ('<p class="sub">Rediseño con asistente de IA</p>', '<p class="sub">Redesign with an AI assistant</p>', 1),
    ('<p class="resumen">Concepto no oficial para un restaurante paisa, con un chat que responde sobre la carta, los precios y las sedes en español o inglés.</p>',
     '<p class="resumen">Unofficial concept for a restaurant from Medellín, with a chat that answers questions about the menu, prices and locations in Spanish or English.</p>', 1),
    ('<dd>Rediseño web + chatbot</dd>', '<dd>Web redesign + chatbot</dd>', 1),
    ('<dd>De unos 250 archivos a 15 por visita</dd>', '<dd>From about 250 files to 15 per visit</dd>', 1),
    ('>Antes y después</a>', '>Before and after</a>', 1),
    ('aria-label="Ver el simulador del litotriptor"', 'aria-label="View the lithotripter simulator"', 1),
    ('alt="Captura del simulador del litotriptor: elipse con los rayos que salen del electrodo y se concentran en el cálculo renal"',
     'alt="Lithotripter simulator screenshot: ellipse with rays leaving the electrode and converging on the kidney stone"', 1),
    ('<h3>Litotriptor HM3</h3>', '<h3>Lithotripter HM3</h3>', 1),
    ('<p class="sub">Geometría aplicada a la medicina</p>', '<p class="sub">Geometry applied to medicine</p>', 1),
    ('<p class="resumen">Simulador del reflector elipsoidal que concentra la onda de choque en un cálculo renal. Lo hice para un trabajo en grupo de la EIA; el grupo preparó la presentación.</p>',
     '<p class="resumen">Simulator of the ellipsoidal reflector that focuses the shock wave on a kidney stone. I built it for a group assignment at EIA; the group prepared the presentation.</p>', 1),
    ('<dd>Simulador interactivo</dd>', '<dd>Interactive simulator</dd>', 1),
    ('<dd>Python · React y SVG</dd>', '<dd>Python · React and SVG</dd>', 1),
    ('<dd>PF₁ + PF₂ = 2a: todos los rayos llegan juntos</dd>', '<dd>PF₁ + PF₂ = 2a: every ray arrives at once</dd>', 1),

    # Lema en curva
    ('<section class="lema" aria-label="Medir, probar, construir, publicar">', '<section class="lema" aria-label="Measure, test, build, launch">', 1),
    ('<span>{ Método</span>', '<span>{ Method</span>', 1),
    ('<span>Método }</span>', '<span>Method }</span>', 1),
    ('Medir · Probar · Construir · <tspan class="c">Publicar</tspan> ·', 'Measure · Test · Build · <tspan class="c">Launch</tspan> ·', 3),

    # Perfil
    ('<span class="rotulo">[ Perfil ]</span>', '<span class="rotulo">[ Profile ]</span>', 1),
    ('Estudio <em>Ingeniería Biotecnológica</em> en la EIA, en Medellín. Me gusta entender cómo funcionan las cosas y después construir la herramienta que las hace más fáciles.',
     'I study <em>Biotechnology Engineering</em> at EIA in Medellín. I like understanding how things work and then building the tool that makes them easier.', 1),
    ('<span class="rotulo">Lado A</span>', '<span class="rotulo">Side A</span>', 1),
    ('<h3>Biotecnología</h3>', '<h3>Biotechnology</h3>', 1),
    ('<p>La ciencia me enseñó a medir, a probar y a no conformarme con la primera respuesta. Uso eso para resolver problemas con datos.</p>',
     '<p>Science taught me to measure, to test and not to settle for the first answer. I use that to solve problems with data.</p>', 1),
    ('<li>Ingeniería Biotecnológica, EIA <span>2026 –</span></li>', '<li>Biotechnology Engineering, EIA <span>2026 –</span></li>', 1),
    ('<li>Póster: agua en centros de datos de IA <span>EIA</span></li>', '<li>Poster: water use in AI data centers <span>EIA</span></li>', 1),
    ('<li>Modelo ONU: debate y logística <span>Colegio</span></li>', '<li>Model UN: debate and logistics <span>School</span></li>', 1),
    ('<span class="rotulo">Lado B</span>', '<span class="rotulo">Side B</span>', 1),
    ('<h3>Tecnología</h3>', '<h3>Technology</h3>', 1),
    ('<p>Diseño y programo con ayuda de la inteligencia artificial para pasar rápido de la idea a algo publicado y funcionando.</p>',
     '<p>I design and code with the help of artificial intelligence to go quickly from an idea to something live and working.</p>', 1),
    ('<li>Python, CS50P de Harvard <span>En curso</span></li>', '<li>Python, Harvard’s CS50P <span>In progress</span></li>', 1),
    ('<li>HTML, CSS y JavaScript <span>Web</span></li>', '<li>HTML, CSS and JavaScript <span>Web</span></li>', 1),
    ('<li>Inglés certificado por Cambridge <span>B2</span></li>', '<li>Cambridge-certified English <span>B2</span></li>', 1),

    # Cifras
    ('<span class="rotulo">[ En números ]</span>', '<span class="rotulo">[ By the numbers ]</span>', 1),
    ('<th>Item</th><th>Valor</th><th class="ocultar">Detalle</th>', '<th>Item</th><th>Value</th><th class="ocultar">Detail</th>', 1),
    ('<td class="valor"><span data-contar="7">7</span> rutas</td><td class="ocultar">Buses de la EIA trazados sobre las calles reales del Valle de Aburrá y Rionegro.</td>',
     '<td class="valor"><span data-contar="7">7</span> routes</td><td class="ocultar">EIA buses traced along the real streets of the Aburrá Valley and Rionegro.</td>', 1),
    ('<td class="valor"><span data-contar="1073">1.073</span></td><td class="ocultar">Ventas de ejemplo que la hoja suma, cruza con el inventario y resume sola.</td>',
     '<td class="valor"><span data-contar="1073">1,073</span></td><td class="ocultar">Sample sales that the sheet adds up, checks against inventory and summarizes on its own.</td>', 1),
    ('<td class="ocultar">Títulos principales en la página: lo que Google necesita para entenderla bien.</td>',
     '<td class="ocultar">Main headings on the page: what Google needs to understand it properly.</td>', 1),
    ('<td class="valor"><span data-contar="27.6" data-decimales="1">27,6</span> cm</td><td class="ocultar">Distancia que recorre cada rayo hasta el cálculo renal: todos llegan juntos.</td>',
     '<td class="valor"><span data-contar="27.6" data-decimales="1">27.6</span> cm</td><td class="ocultar">Distance each ray travels to the kidney stone: they all arrive at once.</td>', 1),

    # Contacto y pie
    ('<span class="rotulo">[ Contacto ]</span>', '<span class="rotulo">[ Contact ]</span>', 1),
    ('data-ver><span>¿Empezamos<span>?</span></span></h2>', 'data-ver><span>Shall we start<span>?</span></span></h2>', 1),
    ('<p>¿Tienes una idea o una tarea que quieres simplificar? Cuéntame y lo pensamos juntos.</p>',
     '<p>Got an idea, or a task you’d like to simplify? Tell me about it and we’ll figure it out together.</p>', 1),
    ('>Copiar correo</button>', '>Copy email</button>', 1),
    ('<span>Hecho con HTML, CSS, JavaScript e IA</span>', '<span>Built with HTML, CSS, JavaScript and AI</span>', 1),
    ('<span>Retratos hechos con IA a partir de mis fotos</span>', '<span>Portraits made with AI from my own photos</span>', 1),
    ('role="status">Correo copiado</div>', 'role="status">Email copied</div>', 1),

    # Script
    ("toLocaleTimeString('es-CO',", "toLocaleTimeString('en-US',", 1),
]

errores = []
for es, en, veces in pares:
    n = html.count(es)
    if n != veces:
        errores.append(f"{n}× (esperado {veces}): {es[:70]}")
    html = html.replace(es, en)

if errores:
    print("NO COINCIDEN:\n" + "\n".join(errores)); sys.exit(1)

(raiz / "en").mkdir(exist_ok=True)
(raiz / "en" / "index.html").write_text(html, encoding="utf-8", newline="\n")
print("OK:", len(pares), "reemplazos")
