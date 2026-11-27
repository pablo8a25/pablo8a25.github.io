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
    ('<nav aria-label="Sitio"><h4>Sitio</h4><a href="#inicio">Inicio</a><a href="#servicios">Áreas</a><a href="#proyectos">Proyectos</a><a href="#perfil">Perfil</a></nav>',
     '<nav aria-label="Site"><h4>Site</h4><a href="#inicio">Home</a><a href="#servicios">Areas</a><a href="#proyectos">Projects</a><a href="#perfil">Profile</a></nav>', 1),
    ('<nav aria-label="Enlaces"><h4>Enlaces</h4><a href="https://github.com/pablo8a25" target="_blank" rel="noopener">GitHub</a><a href="mailto:pablo8abc@gmail.com">Correo</a><a href="en/" hreflang="en" lang="en">English</a></nav>',
     '<nav aria-label="Links"><h4>Links</h4><a href="https://github.com/pablo8a25" target="_blank" rel="noopener">GitHub</a><a href="mailto:pablo8abc@gmail.com">Email</a><a href="../" hreflang="es" lang="es">Español</a></nav>', 1),

    # Cabecera del documento y rutas de archivos
    ('<html lang="es">', '<html lang="en">', 1),
    ('<title>Pablo Ortiz Ochoa · Biotecnología e inteligencia artificial</title>', '<title>Pablo Ortiz Ochoa · Biotechnology and artificial intelligence</title>', 1),
    ('content="Portafolio de Pablo Ortiz Ochoa, estudiante de Ingeniería Biotecnológica en la EIA: une la biotecnología con la inteligencia artificial para la salud, el ambiente y el laboratorio."',
     'content="Portfolio of Pablo Ortiz Ochoa, Biotechnology Engineering student at EIA: bringing biotechnology and artificial intelligence together for health, the environment and the lab."', 1),
    ('<meta property="og:title" content="Pablo Ortiz Ochoa · Biotecnología e inteligencia artificial">', '<meta property="og:title" content="Pablo Ortiz Ochoa · Biotechnology and artificial intelligence">', 1),
    ('content="Biotecnología e inteligencia artificial para la salud, el ambiente y el laboratorio."', 'content="Biotechnology and artificial intelligence for health, the environment and the lab."', 1),
    ('content="img/pablo.jpg"', 'content="https://pablo-ortiz-ochoa.vercel.app/img/pablo.jpg"', 1),
    ('src="img/', 'src="../img/', 7),
    ('href="img/', 'href="../img/', 2),
    ('url(img/logo.svg)', 'url(../img/logo.svg)', 1),

    # Encabezado y menús
    ('aria-label="Pablo Ortiz, inicio"', 'aria-label="Pablo Ortiz, home"', 1),
    ('<nav aria-label="Principal">', '<nav aria-label="Main">', 1),
    ('<a href="#proyectos">Proyectos</a>', '<a href="#proyectos">Projects</a>', 2),
    ('<a href="#servicios">Áreas</a>', '<a href="#servicios">Areas</a>', 1),
    ('<a href="#perfil">Perfil</a>', '<a href="#perfil">Profile</a>', 1),
    ('<span class="idioma"><span aria-current="page">ES</span><a href="en/" hreflang="en" lang="en" aria-label="Read in English">EN</a></span>',
     '<span class="idioma"><a href="../" hreflang="es" lang="es" aria-label="Ver en español">ES</a><span aria-current="page">EN</span></span>', 2),
    ('>Hablemos <span class="flecha"', '>Let’s talk <span class="flecha"', 2),
    ('<nav class="menu" id="menu" aria-label="Secciones">', '<nav class="menu" id="menu" aria-label="Sections">', 1),
    ('<a class="opcional" href="#perfil">Perfil</a>', '<a class="opcional" href="#perfil">Profile</a>', 1),
    ('<a class="opcional" href="#servicios">Áreas</a>', '<a class="opcional" href="#servicios">Areas</a>', 1),
    ('alt="">Hablemos</a>', 'alt="">Let’s talk</a>', 1),

    # Portada
    ('alt="Retrato de Pablo Ortiz Ochoa a contraluz, con el cielo del atardecer detrás"', 'alt="Backlit portrait of Pablo Ortiz Ochoa against a sunset sky"', 1),
    ('aria-label="Biotecnología e inteligencia artificial"', 'aria-label="Biotechnology and artificial intelligence"', 1),
    ('data-letras>Biotecnología</span>', 'data-letras>Biotechnology</span>', 1),
    ('data-letras>e IA</span>', 'data-letras>and AI</span>', 1),
    ('<p class="intro"><b>Hola, soy Pablo.</b> Estudio Ingeniería Biotecnológica y uso la inteligencia artificial para crear herramientas para la salud, el ambiente y el laboratorio.</p>',
     '<p class="intro"><b>Hi, I’m Pablo.</b> I study Biotechnology Engineering and use artificial intelligence to build tools for health, the environment and the lab.</p>', 1),
    ('<div><b>EIA</b><span>Ingeniería Biotecnológica</span></div>', '<div><b>EIA</b><span>Biotechnology Engineering</span></div>', 1),
    ('<div><b>C1</b><span>Inglés fluido</span></div>', '<div><b>C1</b><span>Fluent English</span></div>', 1),
    ('<span>Trabajo remoto</span>', '<span>Remote work</span>', 1),
    ('<span class="vivo">Disponible · Medellín <span id="hora">', '<span class="vivo">Available · Medellín <span id="hora">', 1),

    # Enfoque
    ('<span class="rotulo">[ Enfoque ]</span>', '<span class="rotulo">[ Focus ]</span>', 1),
    ('<li>Ingeniería Biotecnológica · EIA</li>\n          <li>Medellín, Colombia</li>\n          <li>Salud · Ambiente · Laboratorio</li>\n          <li>Prácticas y trabajo remoto</li>',
     '<li>Biotechnology Engineering · EIA</li>\n          <li>Medellín, Colombia</li>\n          <li>Health · Environment · Lab</li>\n          <li>Internships and remote work</li>', 1),
    ('Uno la biotecnología con la inteligencia artificial para analizar datos, simular procesos y crear herramientas que ayuden en la salud, el ambiente y el laboratorio.',
     'I bring biotechnology and artificial intelligence together to analyze data, simulate processes and build tools that help in health, the environment and the lab.', 1),
    ("const resaltar = ['biotecnología', 'inteligencia', 'artificial'];", "const resaltar = ['biotechnology', 'artificial', 'intelligence'];", 1),
    ('>Ver proyectos <span class="flecha"', '>See projects <span class="flecha"', 1),

    # Cinta
    ('<div class="cinta" aria-label="Datos rápidos">', '<div class="cinta" aria-label="Quick facts">', 1),
    ('<li>Biotecnología e IA</li><li>Ingeniería Biotecnológica · EIA</li><li>Python · CS50P de Harvard</li><li>Inglés C1 · fluido</li><li>Medellín, Colombia</li>',
     '<li>Biotechnology and AI</li><li>Biotechnology Engineering · EIA</li><li>Python · Harvard’s CS50P</li><li>Fluent English · C1</li><li>Medellín, Colombia</li>', 2),

    # Áreas
    ('<span class="rotulo">[ Áreas ]</span>', '<span class="rotulo">[ Areas ]</span>', 1),
    ('<span class="t">Salud y medicina</span>', '<span class="t">Health &amp; medicine</span>', 1),
    ('<div class="flujo">Modelar <i></i> Simular</div>', '<div class="flujo">Model <i></i> Simulate</div>', 1),
    ('<p>Simuladores y modelos para entender cómo funcionan los dispositivos y tratamientos médicos.</p>', '<p>Simulators and models to understand how medical devices and treatments work.</p>', 1),
    ('<span class="t">Ambiente</span>', '<span class="t">Environment</span>', 1),
    ('<div class="flujo">Medir <i></i> Proponer</div>', '<div class="flujo">Measure <i></i> Propose</div>', 1),
    ('<p>Análisis de datos ambientales, como el consumo de agua, para encontrar dónde se puede mejorar.</p>', '<p>Analysis of environmental data, such as water use, to find where things can improve.</p>', 1),
    ('<span class="t">Laboratorio y datos</span>', '<span class="t">Lab &amp; data</span>', 1),
    ('<div class="flujo">Registrar <i></i> Analizar</div>', '<div class="flujo">Record <i></i> Analyze</div>', 1),
    ('<p>Automatizar registros, cálculos y reportes de laboratorio con Python, hojas de cálculo e IA.</p>', '<p>Automating lab records, calculations and reports with Python, spreadsheets and AI.</p>', 1),
    ('<span class="t">Herramientas digitales</span>', '<span class="t">Digital tools</span>', 1),
    ('<div class="flujo">Diseñar <i></i> Publicar</div>', '<div class="flujo">Design <i></i> Launch</div>', 1),
    ('<p>Aplicaciones web y herramientas con IA que llevan datos e información técnica a quien la necesita.</p>', '<p>Web apps and AI tools that bring data and technical information to the people who need it.</p>', 1),
    ('>Ejemplo: Litotriptor HM3 ↓', '>Example: Lithotripter HM3 ↓', 1),
    ('>Ejemplo: póster sobre el agua ↓', '>Example: water-use poster ↓', 1),
    ('>Ejemplo: RutaU ↓', '>Example: RutaU ↓', 1),

    # Proyectos
    ('<span class="rotulo">[ Proyectos ]</span>', '<span class="rotulo">[ Projects · in Spanish ]</span>', 1),
    ('data-ver><span>Proyectos<span class="punto">.</span></span></h2>', 'data-ver><span>Projects<span class="punto">.</span></span></h2>', 1),
    ('<dt>Tipo</dt>', '<dt>Type</dt>', 2),
    ('<dt>Tecnología</dt>', '<dt>Stack</dt>', 2),
    ('<dt>Año</dt>', '<dt>Year</dt>', 2),
    ('>Ver proyecto <span class="flecha"', '>View project <span class="flecha"', 2),
    ('>Código</a>', '>Code</a>', 2),
    ('aria-label="Ver RutaU"', 'aria-label="View RutaU"', 1),
    ('alt="Captura de RutaU: mapa de Medellín con la ruta del bus y la tarjeta de tiempos"', 'alt="RutaU screenshot: map of Medellín with the bus route and the arrival-time card"', 1),
    ('<p class="sub">Los buses de la EIA en el mapa</p>', '<p class="sub">EIA university buses on the map</p>', 1),
    ('<p class="resumen">App web para ver las rutas de los buses de la universidad, saber a qué hora pasa el siguiente y abrir el recorrido en Google Maps o Waze.</p>',
     '<p class="resumen">Web app to see the university bus routes, know when the next one comes and open the route in Google Maps or Waze.</p>', 1),
    ('<dd>App web instalable</dd>', '<dd>Installable web app</dd>', 1),
    ('<dd>JavaScript, Leaflet y OpenStreetMap</dd>', '<dd>JavaScript, Leaflet and OpenStreetMap</dd>', 1),
    ('aria-label="Ver el simulador del litotriptor"', 'aria-label="View the lithotripter simulator"', 1),
    ('alt="Captura del simulador del litotriptor: elipse con los rayos que salen del electrodo y se concentran en el cálculo renal"',
     'alt="Lithotripter simulator screenshot: ellipse with rays leaving the electrode and converging on the kidney stone"', 1),
    ('<h3>Litotriptor HM3</h3>', '<h3>Lithotripter HM3</h3>', 1),
    ('<p class="sub">Geometría aplicada a la medicina</p>', '<p class="sub">Geometry applied to medicine</p>', 1),
    ('<p class="resumen">Simulador del reflector elipsoidal que concentra la onda de choque en un cálculo renal. Lo hice para un trabajo en grupo de la EIA; el grupo preparó la presentación.</p>',
     '<p class="resumen">Simulator of the ellipsoidal reflector that focuses the shock wave on a kidney stone. I built it for a group assignment at EIA; the group prepared the presentation.</p>', 1),
    ('<dd>Simulador interactivo</dd>', '<dd>Interactive simulator</dd>', 1),
    ('<dd>Python · React y SVG</dd>', '<dd>Python · React and SVG</dd>', 1),

    ('<b><span data-contar="27.6" data-decimales="1">27,6</span> cm</b><span class="pie-cifra">Distancia que recorre cada rayo hasta el cálculo renal: todos llegan juntos.</span>',
     '<b><span data-contar="27.6" data-decimales="1">27.6</span> cm</b><span class="pie-cifra">Distance each ray travels to the kidney stone: they all arrive at once.</span>', 1),
    ('<b><span data-contar="7">7</span> rutas</b><span class="pie-cifra">Buses de la EIA trazados sobre las calles reales del Valle de Aburrá y Rionegro.</span>',
     '<b><span data-contar="7">7</span> routes</b><span class="pie-cifra">EIA buses traced along the real streets of the Aburrá Valley and Rionegro.</span>', 1),

    # Lema en curva
    ('<section class="lema" aria-label="Medir, probar, construir, publicar">', '<section class="lema" aria-label="Measure, test, build, launch">', 1),
    ('<span>{ Método</span>', '<span>{ Method</span>', 1),
    ('<span>Método }</span>', '<span>Method }</span>', 1),
    ('Medir · Probar · Construir · <tspan class="c">Publicar</tspan> ·', 'Measure · Test · Build · <tspan class="c">Launch</tspan> ·', 4),

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
    ('<li>Inglés fluido <span>C1</span></li>', '<li>Fluent English <span>C1</span></li>', 1),

    # Contacto y pie
    ('<span class="rotulo">[ Contacto ]</span>', '<span class="rotulo">[ Contact ]</span>', 1),
    ('data-ver><span>¿Empezamos<span>?</span></span></h2>', 'data-ver><span>Shall we start<span>?</span></span></h2>', 1),
    ('<p>¿Tienes un proyecto de salud, ambiente o laboratorio donde la inteligencia artificial pueda ayudar? Cuéntame y lo pensamos juntos.</p>',
     '<p>Do you have a health, environmental or lab project where artificial intelligence could help? Tell me about it and we’ll figure it out together.</p>', 1),
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
