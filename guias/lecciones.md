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
    conversación y una PNG completa pesa ~15 veces más. `sips -Z 768 -s format jpeg in.png --out x.jpg`.
20. **Tareas largas por etapas.** Al cerrar una etapa, el estado queda en los archivos del proyecto
    (brief, guion, plan, revision) y se puede seguir en una conversación nueva.
