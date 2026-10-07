"""Create original vector concept illustrations; no external product imagery."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'prototype' / 'assets'
DEST.mkdir(parents=True, exist_ok=True)

DEFS = '''<defs>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2=".8"><stop stop-color="#6c481f"/><stop offset=".18" stop-color="#d4af68"/><stop offset=".36" stop-color="#fff0ba"/><stop offset=".5" stop-color="#b38b45"/><stop offset=".73" stop-color="#f0d791"/><stop offset=".9" stop-color="#a17531"/><stop offset="1" stop-color="#60431f"/></linearGradient>
<linearGradient id="goldLight" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#9d7436"/><stop offset=".4" stop-color="#f3d893"/><stop offset=".65" stop-color="#c6a05b"/><stop offset="1" stop-color="#865920"/></linearGradient>
<radialGradient id="paper"><stop stop-color="#eee5d5"/><stop offset="1" stop-color="#cfc0aa"/></radialGradient>
<linearGradient id="stone" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#e3d8c2"/><stop offset=".65" stop-color="#bcad93"/><stop offset="1" stop-color="#a9987d"/></linearGradient>
<linearGradient id="shadowPlane" x1="0" y1="0" x2="1" y2=".4"><stop stop-color="#65543e" stop-opacity=".17"/><stop offset="1" stop-color="#65543e" stop-opacity="0"/></linearGradient>
<filter id="shadow" x="-60%" y="-60%" width="240%" height="250%"><feDropShadow dx="12" dy="21" stdDeviation="10" flood-color="#695036" flood-opacity=".28"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="13"/></filter>
</defs>'''

def svg(name, content, w=600, h=750, background='#e7dfd2'):
    (DEST / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{DEFS}<rect width="{w}" height="{h}" fill="{background}"/>{content}</svg>', encoding='utf-8')

hoops='''<g filter="url(#shadow)">
<g transform="translate(231 363) rotate(-27)"><ellipse rx="84" ry="116" fill="none" stroke="url(#gold)" stroke-width="29"/><ellipse cx="-4" cy="-3" rx="76" ry="111" fill="none" stroke="#f9e6b0" stroke-width="2.3" opacity=".6"/><path d="M-16-111 12-114" stroke="#87642e" stroke-width="4"/><path d="M-14-114 15-117" stroke="#ecd091" stroke-width="2"/></g>
<g transform="translate(366 405) rotate(25)"><ellipse rx="73" ry="104" fill="none" stroke="url(#gold)" stroke-width="27"/><ellipse cx="-4" cy="-3" rx="66" ry="99" fill="none" stroke="#fce6a9" stroke-width="2" opacity=".6"/><path d="M-12-102 12-104" stroke="#816032" stroke-width="4"/></g></g>'''
svg('hoops.svg','<path d="M0 565 600 365V750H0Z" fill="#d4c7b2"/><ellipse cx="313" cy="516" rx="140" ry="27" fill="#7e684b" opacity=".09" filter="url(#soft)"/>'+hoops)

pebble='''<path d="M137-30C111 172 137 223 204 285L291 364C320 388 352 329 380 297C453 216 460 89 439-30" fill="none" stroke="#957445" stroke-width="4"/><path d="M137-30C111 172 137 223 204 285L291 364C320 388 352 329 380 297C453 216 460 89 439-30" fill="none" stroke="#ebd394" stroke-width="2" stroke-dasharray="2 5"/>
<g filter="url(#shadow)"><ellipse cx="298" cy="357" rx="14" ry="22" fill="none" stroke="url(#gold)" stroke-width="7"/><path d="M270 379C307 347 343 377 345 418C349 459 323 488 294 480C257 471 246 414 270 379Z" fill="url(#gold)"/><path d="M275 392C273 418 288 450 303 463" fill="none" stroke="#ffecc0" stroke-width="3" opacity=".65"/></g>'''
svg('studs.svg','<path d="M0 560C220 451 390 518 600 396V750H0Z" fill="#dacbb8"/>'+pebble,background='#e4dacc')

ring='''<ellipse cx="321" cy="463" rx="121" ry="20" fill="#81684b" opacity=".17" filter="url(#soft)"/><g transform="translate(300 375) rotate(-24)" filter="url(#shadow)"><ellipse rx="115" ry="78" fill="none" stroke="url(#gold)" stroke-width="36"/><path d="M-92-18C-52-84 34-93 95-22" fill="none" stroke="#f9e5ac" stroke-width="5" opacity=".75"/><path d="M-107 13C-89 79 56 91 108 17" fill="none" stroke="#987039" stroke-width="3" opacity=".55"/></g>'''
svg('ring.svg','<path d="M0 0 600 166V750H0Z" fill="#eee7db"/><path d="M0 590 600 513V750H0Z" fill="#ddd0bd"/>'+ring,background='#dfd3c1')

petal='''<path d="M140-25C115 164 164 267 300 334C436 267 485 164 460-25" fill="none" stroke="#886736" stroke-width="4"/><path d="M140-25C115 164 164 267 300 334C436 267 485 164 460-25" fill="none" stroke="#f0d491" stroke-width="2" stroke-dasharray="3 5"/>
<g filter="url(#shadow)"><ellipse cx="300" cy="335" rx="12" ry="18" fill="none" stroke="url(#gold)" stroke-width="7"/><path d="M300 350C255 357 225 400 239 440C253 483 300 506 300 506C300 506 347 483 361 440C375 400 345 357 300 350Z" fill="url(#gold)"/><path d="M300 355V496M300 356C264 394 270 450 295 489M300 356C335 396 330 450 305 489M286 356C243 390 247 445 285 478M314 356C357 390 353 445 315 478" fill="none" stroke="#85622e" stroke-width="2" opacity=".5"/><path d="M293 363C276 402 284 458 299 486" stroke="#ffedba" stroke-width="3" fill="none" opacity=".7"/></g>'''
svg('pendant.svg','<path d="M0 619C170 486 445 483 600 404V750H0Z" fill="#cdbca5"/>'+petal,background='#ddd0bd')

hero='''<rect width="800" height="860" fill="url(#paper)"/>
<path d="M0 0H165L800 514V725L0 119Z" fill="#f8f0e0" opacity=".25"/>
<path d="M0 510 800 351V860H0Z" fill="#c9baa2" opacity=".55"/>
<ellipse cx="443" cy="689" rx="229" ry="48" fill="#6c5536" opacity=".19" filter="url(#soft)"/>
<path d="M185 418 568 364 647 485 269 568Z" fill="#ece1cc"/>
<path d="M269 568 647 485V634L269 728Z" fill="url(#stone)"/>
<path d="M185 418 269 568V728L185 572Z" fill="#b3a38b"/>
<g opacity=".2" stroke="#81705a" stroke-width="1"><path d="M291 591 627 512M291 650 627 571M292 686 627 607M291 610 627 531"/><path d="M214 487 214 606M235 528 235 652"/></g>
<g transform="translate(7 -57) scale(1.25)">'''+hoops+'''</g>
<path d="M20 800C290 675 572 730 830 614" fill="none" stroke="#f0e5d0" stroke-width="2" opacity=".7"/>
<g transform="translate(664 108)" stroke="#886e45" opacity=".55"><path d="M0-24V24M-24 0H24M-12-12 12 12M12-12-12 12" fill="none" stroke-width="1"/></g>'''
svg('hero.svg',hero,w=800,h=860)

story='''<path d="M0 0H760V720H0Z" fill="#e0d6c5"/><path d="M0 0C230 130 267 230 126 720H0Z" fill="#f3eddf"/><path d="M95 0C343 279 304 553 178 720H356C442 472 395 224 244 0Z" fill="#d4c5b1"/><path d="M480 0C351 232 469 515 760 623V720C468 700 374 501 372 319C370 179 410 78 480 0Z" fill="#eee5d6"/><path d="M490 0C387 314 512 462 760 537" fill="none" stroke="#c3b29a" stroke-width="9" opacity=".24"/>
<g transform="translate(82 -6) scale(1.02)">'''+petal+'''</g>'''
svg('gold-story.svg',story,w=760,h=720)
print(f'Created 6 original concept illustrations in {DEST}')
