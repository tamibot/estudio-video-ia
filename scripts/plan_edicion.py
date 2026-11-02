#!/usr/bin/env python3
"""Arma el documento de planificación de una edición (plan.html) a partir de plan.json.

  python3 scripts/plan_edicion.py proyectos/<v>/plan.json      → proyectos/<v>/plan.html (ábrelo con `open`)

La persona lee el guion de cada tramo («beat»), mira ese pedazo del clip, elige uno de los diseños
recomendados o escribe el suyo, y aprieta «Copiar plan»: pega el plan en el chat y el estudio lo
construye. Lo elegido se guarda en el navegador, así que puede cerrar y seguir.

plan.json (rutas relativas a plan.json):
{
  "titulo": "Cuatro patrones de carrera",
  "clip": "material/limpio.mp4",
  "fuente": "podcast, minuto 12",
  "estilo": "minimal premium",
  "beats": [
    {"desde": 0.0, "hasta": 3.2, "guion": "Hay cuatro patrones de carrera",
     "visto_en": "En las referencias, la idea que ordena el video abre en A-roll (V04, V08).",
     "opciones": [
       {"titulo": "A-roll con subtítulo", "tipo": "A-roll + subtítulos",
        "descripcion": "«cuatro» grande al centro, el resto chico arriba", "ref": "../../perfil/biblioteca/V04-A01/diseno.jpg"},
       {"titulo": "Gráfico de cuatro caminos", "tipo": "Gráfico", "descripcion": "…"}
     ]}
  ]
}
"""
import html
import json
import sys
from pathlib import Path


def validar(p):
    beats = p.get('beats') or []
    if not beats:
        raise SystemExit('plan.json sin beats')
    fin = 0.0
    for i, b in enumerate(beats, 1):
        if not (b.get('hasta', 0) > b.get('desde', -1) >= 0):
            raise SystemExit(f'beat {i}: «desde» y «hasta» no cuadran')
        if b['desde'] < fin - 0.05:
            raise SystemExit(f'beat {i} empieza antes de que termine el anterior')
        if not 1 <= len(b.get('opciones') or []) <= 4:
            raise SystemExit(f'beat {i}: entre 1 y 4 opciones de diseño')
        fin = b['hasta']


PLANTILLA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITULO__ · plan de edición</title>
<style>
:root{--azul:#1B42D3;--tinta:#111214;--gris:#6B6E76;--borde:#E3E3E8;--fondo:#16171B;--card:#FFFFFF;--suave:#F5F5F8}
*{box-sizing:border-box}body{margin:0;background:var(--fondo);font:15px/1.45 Inter,system-ui,-apple-system,sans-serif;color:var(--tinta)}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 80px}
.card{background:var(--card);border-radius:18px;padding:24px 26px;margin-bottom:18px}
h1{font-size:34px;letter-spacing:-.02em;margin:0 0 6px}h1 em{color:var(--azul);font-family:"Playfair Display",Georgia,serif;font-weight:600}
.meta{color:var(--gris);font-size:13px}.meta b{color:var(--tinta);font-weight:600}
.barra{display:flex;gap:3px;margin:18px 0 8px;height:30px}.barra a{flex:1;background:#DCE3FA;border-radius:6px;color:#fff;font-size:12px;display:flex;align-items:center;justify-content:center;text-decoration:none}
.barra a.ok{background:var(--azul)}.acciones{display:flex;gap:10px;align-items:center;margin-top:14px}
button{font:inherit;border:0;border-radius:999px;padding:9px 18px;cursor:pointer;background:var(--azul);color:#fff;font-weight:600}
button.sec{background:var(--suave);color:var(--tinta);border:1px solid var(--borde)}
.beat{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:24px}
.cab{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}.cab h2{margin:0;font-size:19px}.cab span{color:var(--gris);font-size:13px}
.eleg{color:var(--azul);font-size:13px;font-weight:600}
textarea{width:100%;min-height:58px;border:1px solid var(--borde);border-radius:10px;padding:10px;font:inherit;resize:vertical}
.ops{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:12px}
.op{border:1.5px solid var(--borde);border-radius:12px;padding:10px;cursor:pointer;background:#fff}.op:hover{border-color:#B9C6F4}
.op.sel{border-color:var(--azul);box-shadow:0 0 0 3px #1B42D322}.op img{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:8px;background:var(--suave);display:block}
.op .l{font-size:12px;color:var(--gris)}.op b{display:block;font-size:14px;margin:6px 0 2px}.op .t{color:var(--azul);font-size:12px}.op p{margin:4px 0 0;font-size:12.5px;color:#3B3D44}
.der{background:var(--suave);border-radius:14px;padding:16px;display:grid;grid-template-columns:150px 1fr;gap:14px;align-content:start}
.der h3{grid-column:1/-1;margin:0;font-size:12px;letter-spacing:.08em;color:var(--gris);text-transform:uppercase}
.guion{grid-column:1/-1;font-size:18px;line-height:1.35;font-weight:500}
video{width:150px;aspect-ratio:9/16;object-fit:cover;border-radius:10px;background:#000}
.visto{font-size:12.5px;color:#3B3D44}.visto i{display:block;color:var(--gris);font-style:normal;font-size:11px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}
.aviso{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:var(--azul);color:#fff;padding:10px 18px;border-radius:999px;display:none}
@media (max-width:820px){.beat{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<div class="card" id="cabecera"></div><div id="beats"></div></div><div class="aviso" id="aviso">Plan copiado: pégalo en el chat</div>
<script type="application/json" id="datos">__DATOS__</script>
<script>
const P = JSON.parse(document.getElementById('datos').textContent);
const clave = 'plan:' + P.titulo + ':' + P.beats.length;
let est = {}; try { est = JSON.parse(localStorage.getItem(clave)) || {}; } catch (e) {}
const guardar = () => { try { localStorage.setItem(clave, JSON.stringify(est)); } catch (e) {} };
const mmss = s => Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const L = 'ABCD';
const dur = P.beats[P.beats.length - 1].hasta;

function cabecera() {
  const hechos = P.beats.filter((b, i) => est[i] && (est[i].op != null || (est[i].nota || '').trim())).length;
  document.getElementById('cabecera').innerHTML =
    `<h1>${esc(P.titulo)} <em>plan de edición</em></h1>
     <div class="meta">Clip: <b>${esc(P.clip)}</b> · Duración <b>${mmss(dur)}</b> · <b>${P.beats.length}</b> beats
     ${P.fuente ? ' · Fuente: <b>' + esc(P.fuente) + '</b>' : ''}${P.estilo ? ' · Estilo: <b>' + esc(P.estilo) + '</b>' : ''}</div>
     <div class="barra">${P.beats.map((b, i) => `<a href="#b${i + 1}" title="${esc(b.guion)}" class="${est[i] && (est[i].op != null || (est[i].nota || '').trim()) ? 'ok' : ''}" style="flex:${Math.max(.6, b.hasta - b.desde)}">${i + 1}</a>`).join('')}</div>
     <div class="meta">${hechos} de ${P.beats.length} beats decididos. Elige un diseño o escribe el tuyo en cada uno.</div>
     <div class="acciones"><button onclick="copiar()">Copiar plan</button><button class="sec" onclick="bajar()">Descargar plan.md</button></div>`;
}

function beats() {
  document.getElementById('beats').innerHTML = P.beats.map((b, i) => {
    const e = est[i] || {};
    const elegido = e.op != null ? `Elegido: ${L[e.op]} · ${esc(b.opciones[e.op].titulo)}` : '';
    return `<div class="card" id="b${i + 1}"><div class="beat"><div>
      <div class="cab"><h2>Beat ${i + 1} <span>${mmss(b.desde)}–${mmss(b.hasta)}</span></h2><span class="eleg" id="e${i}">${elegido}</span></div>
      <textarea placeholder="Escribe tu plan para este beat, o elige un diseño abajo y ajústalo" oninput="nota(${i}, this.value)">${esc(e.nota || '')}</textarea>
      <div class="ops">${b.opciones.map((o, j) => `<div class="op ${e.op === j ? 'sel' : ''}" onclick="elegir(${i}, ${j})">
        ${o.ref ? `<img src="${esc(o.ref)}" alt="">` : ''}<span class="l">${L[j]}</span><b>${esc(o.titulo)}</b>
        <span class="t">${esc(o.tipo || '')}</span><p>${esc(o.descripcion || '')}</p></div>`).join('')}</div></div>
      <div class="der"><h3>Guion</h3><div class="guion">${esc(b.guion)}</div>
        <video src="${esc(P.clip)}#t=${b.desde},${b.hasta}" controls preload="metadata" data-i="${i}"></video>
        <div class="visto"><i>Visto en las referencias</i>${esc(b.visto_en || '—')}</div></div></div></div>`;
  }).join('');
  document.querySelectorAll('video').forEach(v => {  // cada video toca solo su tramo
    const b = P.beats[v.dataset.i];
    v.addEventListener('play', () => { if (v.currentTime < b.desde || v.currentTime >= b.hasta - .05) v.currentTime = b.desde; });
    v.addEventListener('timeupdate', () => { if (v.currentTime >= b.hasta) { v.pause(); v.currentTime = b.desde; } });
  });
}

function elegir(i, j) { est[i] = est[i] || {}; est[i].op = est[i].op === j ? null : j; guardar(); beats(); cabecera(); }
function nota(i, t) { est[i] = est[i] || {}; est[i].nota = t; guardar(); cabecera(); }

function texto() {
  const l = [`# Plan de edición · ${P.titulo}`, '', `Clip: ${P.clip} · ${mmss(dur)} · ${P.beats.length} beats${P.estilo ? ' · estilo ' + P.estilo : ''}`, ''];
  P.beats.forEach((b, i) => {
    const e = est[i] || {}, o = e.op != null ? b.opciones[e.op] : null;
    l.push(`## Beat ${i + 1} · ${mmss(b.desde)}–${mmss(b.hasta)} (${b.desde.toFixed(2)}–${b.hasta.toFixed(2)} s)`);
    l.push(`Guion: «${b.guion}»`);
    l.push(o ? `Diseño: ${L[e.op]} · ${o.titulo} (${o.tipo || ''}) — ${o.descripcion || ''}` : 'Diseño: (sin elegir)');
    if ((e.nota || '').trim()) l.push(`Notas: ${e.nota.trim()}`);
    l.push('');
  });
  return l.join('\n');
}
function avisar(t) { const a = document.getElementById('aviso'); a.textContent = t; a.style.display = 'block'; setTimeout(() => a.style.display = 'none', 2200); }
function copiar() { navigator.clipboard.writeText(texto()).then(() => avisar('Plan copiado: pégalo en el chat'), () => bajar()); }
function bajar() { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([texto()], {type: 'text/markdown'})); a.download = 'plan.md'; a.click(); avisar('plan.md descargado'); }
cabecera(); beats();
</script></body></html>
"""


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    f = Path(sys.argv[1])
    p = json.loads(f.read_text())
    validar(p)
    datos = json.dumps(p, ensure_ascii=False).replace('</', '<\\/')
    salida = f.with_name('plan.html')
    salida.write_text(PLANTILLA.replace('__TITULO__', html.escape(p.get('titulo', 'Video'))).replace('__DATOS__', datos))
    print(f'{salida} · {len(p["beats"])} beats — ábrelo: open {salida}')


if __name__ == '__main__':
    main()
