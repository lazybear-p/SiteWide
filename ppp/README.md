# PPP — jewellery website planning and design kit

Prepared 7 October 2026. This folder is the project working copy in SiteWide.

## Start here

Open **START-HERE.html** in a browser. It links to the interactive design preview, printable website plan and research. The preview works offline: no installation, account or web server is required.

Download the package from [SiteWide on GitHub](https://github.com/lazybear-p/SiteWide/raw/refs/heads/main/ppp/deliverables/ppp-website-review.zip). If the repository is private, sign into GitHub first. You can also use **Code → Download ZIP** on the repository homepage. GitHub's HTML source viewer does not run the website: download and open the HTML file locally.

The working identity **THE EDIT** is a placeholder. Jewellery illustrations, product names, specifications, prices and stock statuses are demonstration content, not an actual catalogue. No payment, message, booking or personal data is sent. The bag is held in memory and clears on reload. Appointment form entries are discarded after the local demonstration.

## Contents

- `docs/website-plan.md`: tailored website specification, scope, flows and acceptance criteria.
- `docs/research.md`: dated official-source findings and implications.
- `docs/decisions.md`: confirmed requirements and decisions still needed.
- `docs/budget.csv`: editable planning estimates, not vendor quotations.
- `docs/platform-cost-model.csv`: editable spreadsheet formulas for platform costs.
- `docs/original-brief.txt`: the founder's original attachment.
- `prototype/`: original, offline HTML/CSS/JavaScript design concept and SVG illustrations.
- `review/`: printable plan and desktop/mobile screenshots generated during validation.
- `scripts/`: reproducible export and browser validation helpers.

## Scope and status

This is a reviewable concept, not the production store or a Shopify theme. The founder requested planning and design review before production implementation. No production checkout, inventory integration, WhatsApp connection, translation or appointment backend is connected.

Initial recommendation: a tailored Shopify storefront, subject to all-in payment costs, staff access, merchant approval and fulfilment requirements. Current Shopify and gateway pricing are documented in the research, including the additional third-party-provider fee.

The selected cloud workspace replaces the earlier request for direct Desktop access. Download and extract the provided ZIP on your computer; the archive contains a top-level `ppp` folder. Extracting it onto your Desktop produces `Desktop/ppp`.

## Development and review

Edit files in the existing checkout. Each cloud task is already isolated; do not create a Git worktree unless requested. Preserve existing user changes. Future production work requires a separate scope/design decision and real supplier assets.

Optional local serving: `python3 -m http.server 8000 --directory /workspace/SiteWide/ppp` in the cloud, or `python3 -m http.server 8000` from a local `ppp` folder. Direct file opening is enough for the design review.

The included browser validation script uses Python Playwright and Chromium. It is a development check, not needed to open the kit. See `review/validation.md` for the actual run and limitations.
