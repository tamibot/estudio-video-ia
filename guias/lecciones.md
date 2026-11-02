# Lecciones aprendidas

Cada regla salió de una ronda de corrección real. Léelas antes de construir y pásalas a los
revisores: si no las conocen, proponen lo mismo que ya se rechazó.

## Movimiento

1. **Nada vibrando todo el tiempo.** Sin latidos con el beat, temblores constantes ni puntos que
   parpadean. Sí golpes puntuales: la entrada de la banda, una palabra clave, el remate.
2. **Cada toma es un mini video con acción propia.** Un zoom lento sobre una foto no es video.
   Gestos según el contenido: un video corta de plano; una imagen se revela de borrosa a nítida;
   una lámina cambia; un carrusel avanza; un prompt se escribe completo; una interfaz recibe clics.
3. **Sin animación de entrada en lo que ya se mueve.** Tomas, íconos y rostros se ven desde el
   primer cuadro de su escena.
4. **Lo que se nombra, se ve.** Si la voz nombra una herramienta o producto, su logo o imagen
   aparece (o crece) en ese momento. Logos sobre una baldosa sólida, nunca vidrio esmerilado.
5. **Titulares línea por línea**, nunca palabras fantasma semitransparentes encima de una foto.
6. **Más dinámico** suele significar: cortinas diagonales entre escenas, rostros o elementos
   grandes que rotan de a uno, listas grandes con los colores de la marca.
7. **Un gráfico nunca mide más que su tarjeta**; nada se sale de su caja.

## Proceso

8. **Mostrar versiones intermedias.** La persona corrige rápido sobre lo que ve; un video
   «terminado» con 10 errores cuesta más que 3 avances.
9. **Revisar cuadro a cuadro antes de entregar**: ninguna toma congelada, nada arranca vacío,
   nada pulsa sin motivo, ningún texto cortado.
10. **Revisores con las reglas y los rechazos de la persona.** Un hallazgo cuenta solo si se ve en
    un cuadro real. Un cuadro en plena transición no es un defecto.
11. **Si la persona cambia algo a mitad de una revisión**, esa revisión quedó obsoleta: aplicar y
    revisar la versión nueva.
12. **Guion aprobado antes de producir audio o imágenes.** Rehacer voz o imágenes cuesta dinero.
13. **Imágenes: primero el plano, después el movimiento.** Una imagen clave por toma, aprobada,
    y recién se anima.

## Gasto y cuotas

14. **Los subagentes no gastan.** Ya pasó que agentes generaron imágenes sin permiso porque veían
    la herramienta. Por eso la puerta exige `permitir` y los agentes dejan pedidos.
15. **Ante un 429 o un 403, parar.** Reintentar empeora el bloqueo. Un yt-dlp viejo también da 403:
    actualizarlo antes de concluir que es un bloqueo.
16. **Una sola descarga por video.** `referencia.py` retoma lo hecho; no bajes dos veces.
17. **Medir con la máquina tranquila.** Con otra tarea pesada corriendo, los tiempos engañan:
    comparar tiempo de CPU, no de reloj.

## Entorno

18. **Fuera de iCloud/Dropbox.** Los archivos «solo en la nube» cuelgan ffmpeg, Chrome y git sin
    dar error. Para detectarlos en Mac: `os.stat(f).st_flags & 0x40000000`.
19. **Imágenes chicas para mirar** (≤ 768 px): cada imagen que se mira queda en el historial de la
    conversación y una PNG completa pesa ~15 veces más. `sips -Z 768 -s format jpeg in.png --out x.jpg`
    (Linux: `ffmpeg -i in.png -vf scale=768:-2 x.jpg`).
20. **Tareas largas por etapas.** Al cerrar una etapa, el estado queda en los archivos del proyecto
    (brief, guion, plan, revision) y se puede seguir en una conversación nueva.

## Herramientas

21. **`hyperframes init` sin `--resolution` sale horizontal** (1920x1080), y el blank de Remotion,
    1280x720. Fijar el formato del plan desde el arranque; cambiarlo después descuadra todo.
22. **Instagram sin sesión dice «rate-limit… anonymously»**: es un pedido de login, no un bloqueo.
    Pasar el archivo a mano o, con OK, la sesión del navegador.
23. **Whisper sin VAD inventa texto** en silencios y en música sin voz («gracias por ver»). Con VAD
    no, y el conteo de palabras por segundo deja de mentir.
24. **Material grabado: primero sacar silencios** (auto-editor), después editar. Montar sobre el
    bruto alarga cada ronda.
25. **Una key mal pegada no es un bloqueo**: un 401 se corrige en `.env`; solo 403/429 son freno.

## Método (tutorial de Joseph, talking head minimal)

26. **Primero entender el estilo como editor, después enseñárselo a Claude.** Sin saber por qué una
    escena funciona, la IA solo produce videos malos más rápido.
27. **Videos = lógica, tablero = diseño.** Las referencias enseñan dónde y cuánto dura cada animación;
    el tablero de Figma por tipo de escena enseña cómo se ve. Hace falta lo uno y lo otro.
28. **El plan lo decide la persona.** La IA recomienda diseños; sola no es lo bastante creativa para
    planificar. El documento de planificación es el paso que más pesa en el resultado.
29. **Anuncia → cara; describe → muéstralo.** Abrir siempre en la cara con subtítulos.
30. **El primer render queda al 60-70 %.** Se espera una ronda de 5-6 correcciones concretas.
31. **La textura se mueve con lo que cubre.** Una textura quieta sobre una escena que se desliza se nota.
32. **En talking head, el sonido va al final**, con la imagen aprobada; la voz ya marca el tiempo.
33. **`npx hyperframes clean` limpia todos los proyectos que recuerda**, no solo la carpeta dada
    (borró capturas de otro proyecto). Limpiar con `kit.sh limpiar`.
