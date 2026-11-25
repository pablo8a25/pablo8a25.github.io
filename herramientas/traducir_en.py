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
    ('<html lang="es">', '<html lang="en">', 1),
    ('<title>Pablo Ortiz Ochoa · IA aplicada y diseño web</title>', '<title>Pablo Ortiz Ochoa · Applied AI &amp; web design</title>', 1),
    ('content="Portafolio de Pablo Ortiz Ochoa: páginas web, automatizaciones y aplicaciones hechas con inteligencia artificial para que los negocios trabajen más rápido."',
     'content="Portfolio of Pablo Ortiz Ochoa: websites, automations and apps built with artificial intelligence to help businesses work faster."', 1),
    ('<meta property="og:title" content="Pablo Ortiz Ochoa · IA aplicada y diseño web">', '<meta property="og:title" content="Pablo Ortiz Ochoa · Applied AI &amp; web design">', 1),
    ('content="Páginas web, automatizaciones y aplicaciones hechas con inteligencia artificial."', 'content="Websites, automations and apps built with artificial intelligence."', 1),
    ('content="img/pablo.jpg"', 'content="https://pablo8a25.github.io/img/pablo.jpg"', 1),
    ('src="img/', 'src="../img/', 5),

    # Encabezado
    ('data-ir>Proyectos</a>', 'data-ir>Projects</a>', 1),
    ('data-ir>Sobre mí</a>', 'data-ir>About me</a>', 1),
    ('aria-label="Pablo Ortiz, inicio"', 'aria-label="Pablo Ortiz, home"', 1),
    ('<b>Lunes a viernes</b>', '<b>Monday to Friday</b>', 1),
    ('<nav class="idiomas" aria-label="Idioma"><span aria-current="page">ES</span><a href="en/" hreflang="en" lang="en" aria-label="Read in English">EN</a></nav>',
     '<nav class="idiomas" aria-label="Language"><a href="../" hreflang="es" lang="es" aria-label="Ver en español">ES</a><span aria-current="page">EN</span></nav>', 1),
    ('data-ir>Hablemos <i', 'data-ir>Let’s talk <i', 1),

    # Portada
    ('aria-label="Sospechosamente bien hecho"', 'aria-label="Suspiciously well made"', 1),
    ('aria-hidden="true">Sospechosamente</span>', 'aria-hidden="true">Suspiciously</span>', 1),
    ('aria-hidden="true">bien hecho</span>', 'aria-hidden="true">well made</span>', 1),
    ('>Diseño web e IA</span>', '>Web design &amp; AI</span>', 1),
    ('>Hecho en Medellín</span>', '>Made in Medellín</span>', 1),
    ('>Cero humo</span>', '>Zero fluff</span>', 1),
    ('</i>Disponible para trabajo remoto</div>', '</i>Available for remote work</div>', 1),
    ('HAGÁMOSLO SENCILLO • CON IA Y BUEN GUSTO • ' * 3 + 'HAGÁMOSLO SENCILLO • CON IA Y BUEN GUSTO •',
     'KEEP IT SIMPLE • WITH AI AND GOOD TASTE • ' * 3 + 'KEEP IT SIMPLE • WITH AI AND GOOD TASTE •', 1),

    # Sobre mí
    ('<span class="rotulo">Un poco sobre mí</span>', '<span class="rotulo">A little about me</span>', 1),
    ('Creo que las buenas ideas necesitan enfoque. Por eso uso la inteligencia artificial para pasar rápido de la idea a algo que funciona, y dedico mi tiempo a lo que importa: que tu negocio se vea bien y trabaje mejor.',
     'I believe good ideas need focus. That’s why I use artificial intelligence to get from an idea to something that works, fast, and I spend my time on what matters: making your business look good and work better.', 1),
    ("const resaltar = ['enfoque.', 'inteligencia', 'artificial', 'funciona,', 'importa:'];",
     "const resaltar = ['focus.', 'artificial', 'intelligence', 'works,', 'matters:'];", 1),
    ('data-en="0.28">Estudiante de Ingeniería Biotecnológica</span>', 'data-en="0.28">Biotechnology Engineering student</span>', 1),
    ('>Obsesionado con los detalles</span>', '>Obsessed with details</span>', 1),
    ('>Aprendo rápido</span>', '>Fast learner</span>', 1),

    # Proyectos
    ('<span class="rotulo">Proyectos</span>', '<span class="rotulo">Projects · in Spanish</span>', 1),
    ('<h2 class="titulo-grande">Trabajos<br>escogidos</h2>', '<h2 class="titulo-grande">Selected<br>work</h2>', 1),
    ('alt="Captura de RutaU: mapa de Medellín con la ruta del bus y la tarjeta de tiempos"', 'alt="RutaU screenshot: map of Medellín with the bus route and the arrival-time card"', 1),
    ('sello">App web</span>', 'sello">Web app</span>', 1),
    ('<small>Buses de la EIA en el mapa</small>', '<small>EIA university buses on the map</small>', 1),
    ('alt="Captura del panel de Café Montaña en Google Sheets con ventas, ganancia e inventario"', 'alt="Café Montaña dashboard in Google Sheets with sales, profit and inventory"', 1),
    ('sello">Automatización</span>', 'sello">Automation</span>', 1),
    ('<small>Google Sheets y Apps Script</small>', '<small>Google Sheets &amp; Apps Script</small>', 1),
    ('alt="Captura del rediseño de Doña Rosa: título rojo y foto de comida típica"', 'alt="Doña Rosa redesign screenshot: red headline and a photo of Colombian food"', 1),
    ('sello">Rediseño web</span>', 'sello">Web redesign</span>', 1),
    ('<small>Concepto no oficial · Restaurante</small>', '<small>Unofficial concept · Restaurant</small>', 1),
    ('alt="Captura del simulador del litotriptor: elipse con los rayos que salen del electrodo y se concentran en el cálculo renal"',
     'alt="Lithotripter simulator screenshot: ellipse with rays leaving the electrode and converging on the kidney stone"', 1),
    ('sello">Simulador · Python</span>', 'sello">Simulator · Python</span>', 1),
    ('<b>Litotriptor HM3</b><small>Geometría aplicada a la medicina</small>', '<b>Lithotripter HM3</b><small>Geometry applied to medicine</small>', 1),
    ('<h3 class="titulo-grande">Podría seguir,<br>pero todo el código<br>está en GitHub.</h3>', '<h3 class="titulo-grande">I could go on,<br>but all the code<br>is on GitHub.</h3>', 1),
    ('r1">Hay más</span>', 'r1">There’s more</span>', 1),
    ('r2">Todo abierto</span>', 'r2">All open source</span>', 1),
    ('r3">Échale un ojo</span>', 'r3">Take a look</span>', 1),
    ('>Ver mi GitHub <i', '>See my GitHub <i', 1),

    # Servicios
    ('style="color:var(--suave)">Servicios</span>', 'style="color:var(--suave)">Services</span>', 1),
    ('<h2 class="titulo-grande">Esto es<br>lo mío</h2>', '<h2 class="titulo-grande">This is<br>what I do</h2>', 1),
    ('<h3 class="titulo-grande">Diseño web</h3>', '<h3 class="titulo-grande">Web design</h3>', 1),
    ('<p>Páginas claras, rápidas y pensadas primero para el celular.</p>', '<p>Clear, fast websites designed for phones first.</p>', 1),
    ('<h3 class="titulo-grande">Automatización</h3>', '<h3 class="titulo-grande">Automation</h3>', 1),
    ('<p>Lo que hoy se hace a mano todos los días, que lo haga el computador.</p>', '<p>The tasks you do by hand every day, done by the computer instead.</p>', 1),
    ('<h3 class="titulo-grande">IA en empresas</h3>', '<h3 class="titulo-grande">AI for business</h3>', 1),
    ('<p>Asistentes y flujos de trabajo con inteligencia artificial.</p>', '<p>Assistants and workflows powered by artificial intelligence.</p>', 1),
    ('<h3 class="titulo-grande">Datos y paneles</h3>', '<h3 class="titulo-grande">Data &amp; dashboards</h3>', 1),
    ('<p>Excel y Google Sheets que se actualizan solos.</p>', '<p>Excel and Google Sheets files that update themselves.</p>', 1),
    ('<p>Respuestas rápidas a las preguntas de siempre de tus clientes.</p>', '<p>Quick answers to the questions your customers always ask.</p>', 1),
    ('<h3 class="titulo-grande">Contenido y traducción</h3>', '<h3 class="titulo-grande">Content &amp; translation</h3>', 1),
    ('<p>Textos para redes y blogs, y traducción español–inglés (nivel B2).</p>', '<p>Copy for social media and blogs, plus Spanish–English translation (B2 level).</p>', 1),

    # Cifras
    ('style="color:var(--suave)">En números</span>', 'style="color:var(--suave)">By the numbers</span>', 1),
    ('<h2 class="titulo-grande">Los números<br>hablan</h2>', '<h2 class="titulo-grande">The numbers<br>speak</h2>', 1),
    ('<span>Rediseño · Doña Rosa</span><b>17 → 1</b><p>Títulos principales en la página: lo que Google necesita para entenderla bien.</p>',
     '<span>Redesign · Doña Rosa</span><b>17 → 1</b><p>Main headings on the page: what Google needs to understand it properly.</p>', 1),
    ('<span>Automatización · Café Montaña</span><b>1.073</b><p>Ventas de ejemplo que la hoja suma, cruza con el inventario y resume sola.</p>',
     '<span>Automation · Café Montaña</span><b>1,073</b><p>Sample sales that the sheet adds up, checks against inventory and summarizes on its own.</p>', 1),
    ('<span>App web · RutaU</span><b>7</b><p>Rutas de buses trazadas sobre las calles reales del Valle de Aburrá y Rionegro.</p>',
     '<span>Web app · RutaU</span><b>7</b><p>Bus routes traced along the real streets of the Aburrá Valley and Rionegro.</p>', 1),
    ('<span>Simulador · Litotriptor HM3</span><b>2a</b><p>Todos los rayos recorren la misma distancia, 27,6 cm, y llegan juntos al cálculo renal.</p>',
     '<span>Simulator · Lithotripter HM3</span><b>2a</b><p>Every ray travels the same distance, 27.6 cm, so they all reach the kidney stone at once.</p>', 1),
    ('<span>Idiomas</span><b>B2</b><p>Inglés certificado por Cambridge, para trabajar con clientes de afuera.</p>',
     '<span>Languages</span><b>B2</b><p>Cambridge-certified English, ready to work with clients abroad.</p>', 1),
    ('<button id="siguiente">Siguiente →</button>', '<button id="siguiente">Next →</button>', 1),

    # Contacto
    ('<h2 class="titulo-grande">Hablemos</h2>', '<h2 class="titulo-grande">Let’s talk</h2>', 1),
    ('c1">Sin compromiso</span>', 'c1">No strings attached</span>', 1),
    ('c2">Respondo rápido</span>', 'c2">Quick replies</span>', 1),
    ('<p class="intro">¿Tienes una idea o una tarea que quieres simplificar? Cuéntame y lo pensamos juntos.</p>',
     '<p class="intro">Got an idea, or a task you’d like to simplify? Tell me about it and we’ll figure it out together.</p>', 1),
    ('>Copiar correo</button>', '>Copy email</button>', 1),
    ('<span>Estudiante de Ingeniería Biotecnológica, EIA · Inglés B2 · Python CS50P (en curso)</span>',
     '<span>Biotechnology Engineering student, EIA · English B2 · Python CS50P (in progress)</span>', 1),
    ('<span>Hecho con HTML, CSS, JavaScript e IA</span>', '<span>Built with HTML, CSS, JavaScript and AI</span>', 1),
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
