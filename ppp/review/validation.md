# Prototype validation

Run: 7 October 2026, Chromium via Playwright in the cloud environment.

- PASS: Self-contained preview renders with all illustrations and no external network requests
- PASS: Collection filters show the correct sample materials and festive selection
- PASS: Search supports material matches, no-result feedback and Escape dismissal
- PASS: Ready-stock example adds the chosen quantity; bag subtotal and removal are correct
- PASS: Supplier-confirmation example opens enquiry information and cannot enter the bag
- PASS: Appointment form rejects missing/invalid details and shows a local demonstration without retaining entries
- PASS: Cancelling an appointment demonstration clears entered details
- PASS: Homepage and product page fit 320, 390, 768 and 1440 px viewports without horizontal overflow
- PASS: Mobile navigation, keyboard modal focus and Escape dismissal work
- PASS: Editable multi-file source also renders all sample products and assets
- PASS: Self-contained HTML renders and filters with browser network access disabled
- PASS: Printable founder PDF exported from the current plan, research, decisions and budget
- PASS: No JavaScript page errors during the tested journeys

## Scope and limits

These are design-prototype checks, not production commerce or legal-compliance checks. No real payment, refund, shipment, inventory integration, WhatsApp message, appointment delivery or translation was tested.

The managed cloud browser blocks direct `file://` navigation. The downloadable standalone HTML was therefore checked over a temporary local HTTP server and independently rendered with all network access disabled. Its scripts, styles and illustrations are embedded; no external resources are required. Direct opening in the user’s desktop browser remains to be checked there.

Only synthetic example form values were used. The prototype sends no form data and uses no persistent storage.
