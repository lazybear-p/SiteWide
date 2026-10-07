"""Export a self-contained preview and a printable founder report using stdlib."""
import base64
import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'review'
REVIEW.mkdir(exist_ok=True)

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text

def markdown(text):
    lines = text.splitlines(); output = []; index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1; continue
        heading = re.match(r'^(#{1,4})\s+(.+)', line)
        if heading:
            level = min(6, len(heading[1]) + 1)
            output.append(f'<h{level}>{inline(heading[2])}</h{level}>'); index += 1; continue
        if line.startswith('|'):
            rows=[]
            while index < len(lines) and lines[index].strip().startswith('|'):
                cells=[cell.strip() for cell in lines[index].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+', cell) for cell in cells):rows.append(cells)
                index += 1
            output.append('<div class="table-wrap"><table><thead><tr>'+''.join(f'<th>{inline(cell)}</th>' for cell in rows[0])+'</tr></thead><tbody>')
            output += ['<tr>'+''.join(f'<td>{inline(cell)}</td>' for cell in row)+'</tr>' for row in rows[1:]]
            output.append('</tbody></table></div>'); continue
        if re.match(r'^(- |\d+\. )', line):
            ordered = bool(re.match(r'^\d+\.', line)); tag='ol' if ordered else 'ul'; output.append(f'<{tag}>')
            while index < len(lines) and re.match(r'^(\d+\. |\- )', lines[index].strip()):
                output.append('<li>'+inline(re.sub(r'^(\d+\. |\- )','',lines[index].strip()))+'</li>'); index+=1
            output.append(f'</{tag}>');continue
        paragraph=[line]; index+=1
        while index < len(lines) and lines[index].strip() and not re.match(r'^(#|\||- |\d+\. )',lines[index].strip()):
            paragraph.append(lines[index].strip());index+=1
        output.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return '\n'.join(output)

report_css='''*{box-sizing:border-box}body{margin:0;background:#f6f3ec;color:#292723;font:15px/1.7 Arial,Helvetica,sans-serif}main{max-width:1040px;margin:auto;padding:60px 7%}h1,h2,h3,h4{font-family:Georgia,serif;font-weight:400;line-height:1.15}h1{font-size:66px;letter-spacing:-2px;margin:25px 0}h2{font-size:40px;letter-spacing:-1px;margin:60px 0 25px;border-top:1px solid #d8d1c6;padding-top:35px}h3{font-size:27px;margin:35px 0 15px;color:#482b3b}h4{font-size:21px;margin:22px 0 10px}a{color:#482b3b;text-underline-offset:3px;overflow-wrap:anywhere}p,li{max-width:85ch}li{margin-bottom:7px}code{font-size:12px;overflow-wrap:anywhere}.eyebrow{font-size:11px;letter-spacing:2px;text-transform:uppercase}.lead{font-size:18px;max-width:620px;color:#696258}.cover{border-bottom:1px solid #d8d1c6;padding-bottom:40px}.navigation{display:flex;flex-wrap:wrap;gap:15px;font-size:12px;margin:30px 0}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;margin:20px 0;font-size:12px;line-height:1.5}th{text-align:left;background:#482b3b;color:#fff;padding:12px;vertical-align:top}td{padding:11px 12px;border-bottom:1px solid #d8d1c6;vertical-align:top}tr:nth-child(even) td{background:#eae4d940}.report-footer{margin-top:50px;border-top:1px solid #d8d1c6;padding-top:20px;color:#696258;font-size:11px}@media(max-width:600px){main{padding:35px 6%}h1{font-size:45px}h2{font-size:32px}table{font-size:11px}td,th{padding:9px}}@media print{@page{size:A4;margin:17mm 15mm 19mm}body{background:white;font-size:10pt;line-height:1.55}main{max-width:none;padding:0}.cover{padding-top:20mm;padding-bottom:20mm;break-after:page}h1{font-size:43pt}h2{font-size:26pt;margin:25px 0 16px;padding-top:20px}h3{font-size:18pt;margin-top:22px}h4{font-size:14pt}h2,h3,h4{break-after:avoid}table{font-size:8pt}th,td{padding:8px}tr{break-inside:avoid}thead{display:table-header-group}.table-wrap{overflow:visible}a{color:inherit}p{orphans:3;widows:3}.navigation{display:none}.report-section{break-before:page}.report-section:first-of-type{break-before:auto}}'''

sections=[]
for name, anchor in [('website-plan','plan'),('research','research'),('decisions','decisions')]:
    sections.append(f'<section class="report-section" id="{anchor}">'+markdown((ROOT/'docs'/f'{name}.md').read_text())+'</section>')
budget_rows=list(csv.reader((ROOT/'docs'/'budget.csv').open()))
display_values={6:('145000','320000'),7:('21750','48000'),8:('166750','368000')}
budget_table='<table><thead><tr><th>Workstream</th><th>Low, INR</th><th>High, INR</th><th>Scope / status</th></tr></thead><tbody>'
for row_index,row in enumerate(budget_rows[1:],1):
    low,high=display_values.get(row_index,(row[1],row[2]))
    budget_table+=f'<tr><td>{html.escape(row[0])}</td><td>{int(low):,}</td><td>{int(high):,}</td><td>{html.escape(row[3]+". "+row[4])}</td></tr>'
budget_table+='</tbody></table>'
sections.append('<section class="report-section" id="budget"><h2>Budget worksheet</h2><p>Planning estimates for commissioned work, not vendor quotes. The editable CSV includes formulas. The monthly software reserve is separate from the one-time total.</p>'+budget_table+'<p>Based on the annual-billing platform model at illustrative monthly eligible volume of ₹5,00,000: Basic plus 2% gateway = ₹21,499 before applicable taxes; Grow plus the same gateway = ₹20,599. Difference: ₹900 per month. These are equal-fee-base scenarios, not invoices.</p></section>')
report='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PPP — founder planning pack</title><style>'+report_css+'</style></head><body><main><div class="cover"><p class="eyebrow">PPP / WEBSITE STRATEGY & DESIGN</p><h1>A considered beginning.</h1><p class="lead">A curated jewellery storefront, a personal consultation journey, and the decisions that connect them.</p><p>Founder review · 7 October 2026<br>Prepared for the SiteWide project</p><nav class="navigation"><a href="../START-HERE.html">Start here</a><a href="../preview.html">Open design concept</a><a href="#plan">Website plan</a><a href="#research">Sources</a><a href="#budget">Budget</a><a href="#decisions">Open decisions</a></nav><p>Prototype only. The working identity, illustrations, catalogue and prices are examples. No live orders, enquiries or payments are accepted.</p></div>'+''.join(sections)+'<p class="report-footer">The wider market and business plan is deferred. Current-source facts, founder requirements, recommendations and estimates are distinguished throughout. No production launch or legal compliance certification is claimed.</p></main></body></html>'
(REVIEW/'founder-pack.html').write_text(report,encoding='utf-8')

# All original SVGs, CSS and JavaScript inline into one portable file.
assets={path.name:'data:image/svg+xml;base64,'+base64.b64encode(path.read_bytes()).decode() for path in (ROOT/'prototype'/'assets').glob('*.svg')}
preview=(ROOT/'prototype'/'index.html').read_text()
css=(ROOT/'prototype'/'styles.css').read_text()
js=(ROOT/'prototype'/'app.js').read_text()
js=js.replace('assets/${product.image}','${ASSETS[product.image]}')
preview=preview.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
preview=preview.replace('<script src="app.js" defer></script>','')
preview=re.sub(r'src="assets/([^"]+)"',lambda match:'src="'+assets[match[1]]+'"',preview)
preview=preview.replace('../START-HERE.html','START-HERE.html').replace('../review/founder-pack.html','review/founder-pack.html')
preview=preview.replace('</body>','<script>const ASSETS='+json.dumps(assets)+';\n'+js+'</script></body>')
preview=preview.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; base-uri \'none\'; connect-src \'none\'; form-action \'none\'">')
preview='\n'.join(line.rstrip() for line in preview.splitlines())+'\n'
(ROOT/'preview.html').write_text(preview,encoding='utf-8')
print('Exported review/founder-pack.html and self-contained preview.html')
