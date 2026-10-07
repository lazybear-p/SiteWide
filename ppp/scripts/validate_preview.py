"""Exercise review journeys, capture screenshots and export the printable PDF.

Run a temporary local server from the ppp folder on port 8765 first.
This is a design-prototype smoke check, not production commerce validation.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import json
import os
import shutil

ROOT=Path(__file__).resolve().parents[1]
REVIEW=ROOT/'review'
BASE=os.environ.get('PPP_REVIEW_BASE','http://127.0.0.1:8765')
results=[]
errors=[]
def record(label):
    results.append(label)
    print('PASS:',label,flush=True)

with sync_playwright() as p:
    executable=os.environ.get('PPP_CHROMIUM_PATH') or shutil.which('chromium')
    browser=p.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,reduced_motion='reduce')
    page=context.new_page()
    page.on('pageerror',lambda error:errors.append(str(error)))
    requests=[]
    page.on('request',lambda request:requests.append(request.url))
    page.goto(BASE+'/preview.html',wait_until='networkidle')
    expect(page.locator('.product-card')).to_have_count(4)
    assert page.locator('img').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)')
    assert not any(url.startswith(('http://','https://')) and not url.startswith(BASE+'/') for url in requests)
    record('Self-contained preview renders with all illustrations and no external network requests')
    page.screenshot(path=str(REVIEW/'home-desktop.png'),full_page=True)
    page.screenshot(path=str(REVIEW/'hero-desktop.png'),full_page=False)

    page.get_by_role('button',name='Small Gold',exact=True).click()
    expect(page.locator('.product-card')).to_have_count(2)
    assert all('gold' in text.lower() for text in page.locator('.card-type').all_text_contents())
    page.get_by_role('button',name='Gold-plated silver',exact=True).click()
    expect(page.locator('.product-card')).to_have_count(2)
    page.get_by_role('button',name='Festive',exact=True).click()
    expect(page.locator('.product-card')).to_have_count(2)
    page.get_by_role('button',name='The whole edit',exact=True).click()
    record('Collection filters show the correct sample materials and festive selection')

    page.get_by_role('button',name='Search jewellery',exact=True).click()
    page.locator('#search-input').fill('18K')
    expect(page.locator('.search-result')).to_have_count(1)
    expect(page.locator('.search-result')).to_contain_text('Pebble Pendant')
    page.locator('#search-input').fill('not-a-product')
    expect(page.locator('#search-results')).to_contain_text('No sample pieces match')
    page.keyboard.press('Escape')
    expect(page.locator('#search-dialog')).not_to_be_visible()
    record('Search supports material matches, no-result feedback and Escape dismissal')

    page.locator('.product-card a[href="#product/ellipse"]').click()
    expect(page.locator('#view-product')).to_be_visible()
    expect(page.locator('#product-title')).to_have_text('Ellipse Hoops')
    page.screenshot(path=str(REVIEW/'product-desktop.png'),full_page=True)
    page.locator('#quantity').select_option('2')
    page.locator('#product-action').click()
    expect(page.locator('#bag-dialog')).to_be_visible()
    expect(page.locator('#bag-count')).to_have_text('2')
    expect(page.locator('#bag-summary')).to_contain_text('9,600')
    page.get_by_role('button',name='Remove Ellipse Hoops from preview bag').click()
    expect(page.locator('#bag-count')).to_have_text('0')
    expect(page.locator('#bag-items')).to_contain_text('empty')
    page.keyboard.press('Escape')
    record('Ready-stock example adds the chosen quantity; bag subtotal and removal are correct')

    page.goto(BASE+'/preview.html#product/pebble',wait_until='networkidle')
    expect(page.locator('#product-action')).to_contain_text('Request piece details')
    expect(page.locator('#quantity')).to_be_disabled()
    page.locator('#product-action').click()
    expect(page.locator('#info-dialog')).to_contain_text('No message has been sent')
    expect(page.locator('#bag-count')).to_have_text('0')
    page.keyboard.press('Escape')
    record('Supplier-confirmation example opens enquiry information and cannot enter the bag')

    page.goto(BASE+'/preview.html#appointments',wait_until='networkidle')
    page.get_by_role('button',name='Request a conversation').click()
    page.locator('#appointment-form button[type="submit"]').click()
    expect(page.locator('#appointment-result')).not_to_be_visible()
    page.locator('[name="name"]').fill('Preview Example')
    page.locator('[name="phone"]').fill('123')
    page.locator('[name="city"]').select_option(label='Erode')
    page.locator('#appointment-form input[type="checkbox"]').check()
    page.locator('#appointment-form button[type="submit"]').click()
    expect(page.locator('#appointment-result')).not_to_be_visible()
    page.locator('[name="phone"]').fill('9876543210')
    page.locator('#appointment-form button[type="submit"]').click()
    expect(page.locator('#appointment-result')).to_be_visible()
    expect(page.locator('#appointment-result')).to_contain_text('No enquiry was sent')
    expect(page.locator('[name="phone"]')).to_have_value('')
    page.keyboard.press('Escape')
    record('Appointment form rejects missing/invalid details and shows a local demonstration without retaining entries')

    page.get_by_role('button',name='Request a conversation').click()
    page.locator('[name="name"]').fill('Discard on cancel')
    page.keyboard.press('Escape')
    expect(page.locator('[name="name"]')).to_have_value('')
    record('Cancelling an appointment demonstration clears entered details')

    for width in (320,390,768,1440):
        page.set_viewport_size({'width':width,'height':900})
        for route in ('#home','#product/ellipse'):
            page.goto(BASE+'/preview.html'+route,wait_until='networkidle')
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'), f'Overflow at {width} {route}'
            if width==390:
                name='home-mobile.png' if route=='#home' else 'product-mobile.png'
                page.screenshot(path=str(REVIEW/name),full_page=True)
    record('Homepage and product page fit 320, 390, 768 and 1440 px viewports without horizontal overflow')

    page.set_viewport_size({'width':390,'height':844})
    page.goto(BASE+'/preview.html#home',wait_until='networkidle')
    page.get_by_role('button',name='Open menu',exact=True).click()
    expect(page.locator('#menu-dialog')).to_be_visible()
    page.locator('#menu-dialog a[data-shop="gold"]').click()
    expect(page.locator('#menu-dialog')).not_to_be_visible()
    expect(page.locator('.product-card')).to_have_count(2)
    page.get_by_role('button',name='Search jewellery').click()
    page.keyboard.press('Tab')
    assert page.evaluate('document.activeElement.closest("dialog")?.id')=='search-dialog'
    page.keyboard.press('Escape')
    expect(page.locator('#search-dialog')).not_to_be_visible()
    record('Mobile navigation, keyboard modal focus and Escape dismissal work')

    page.goto(BASE+'/prototype/index.html',wait_until='networkidle')
    expect(page.locator('.product-card')).to_have_count(4)
    assert page.locator('img').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)')
    record('Editable multi-file source also renders all sample products and assets')

    # Verify the single-file export without granting browser access to local files.
    offline=browser.new_context(offline=True,viewport={'width':1280,'height':900})
    offline_page=offline.new_page()
    offline_errors=[]
    offline_page.on('pageerror',lambda error:offline_errors.append(str(error)))
    offline_page.set_content((ROOT/'preview.html').read_text(),wait_until='load')
    expect(offline_page.locator('.product-card')).to_have_count(4)
    assert offline_page.locator('img').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)')
    offline_page.get_by_role('button',name='Small Gold',exact=True).click()
    expect(offline_page.locator('.product-card')).to_have_count(2)
    assert not offline_errors
    offline.close()
    record('Self-contained HTML renders and filters with browser network access disabled')

    page.set_viewport_size({'width':1200,'height':1000})
    page.goto(BASE+'/review/founder-pack.html',wait_until='networkidle')
    expect(page.locator('#budget')).to_contain_text('166,750')
    page.pdf(path=str(REVIEW/'founder-pack.pdf'),format='A4',print_background=True,prefer_css_page_size=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font-size:8px;width:100%;padding:0 15mm;color:#777;text-align:right">PPP · Founder review &nbsp; <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    record('Printable founder PDF exported from the current plan, research, decisions and budget')
    assert not errors,errors
    record('No JavaScript page errors during the tested journeys')
    browser.close()

(REVIEW/'validation.json').write_text(json.dumps({'date':'2026-10-07','passed':results,'javascript_errors':errors},indent=2))
(REVIEW/'validation.md').write_text('# Prototype validation\n\nRun: 7 October 2026, Chromium via Playwright in the cloud environment.\n\n'+''.join('- PASS: '+result+'\n' for result in results)+'\n## Scope and limits\n\nThese are design-prototype checks, not production commerce or legal-compliance checks. No real payment, refund, shipment, inventory integration, WhatsApp message, appointment delivery or translation was tested.\n\nThe managed cloud browser blocks direct `file://` navigation. The downloadable standalone HTML was therefore checked over a temporary local HTTP server and independently rendered with all network access disabled. Its scripts, styles and illustrations are embedded; no external resources are required. Direct opening in the user’s desktop browser remains to be checked there.\n\nOnly synthetic example form values were used. The prototype sends no form data and uses no persistent storage.\n')
print(f'Completed {len(results)} meaningful prototype checks.',flush=True)
