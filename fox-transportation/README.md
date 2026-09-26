# Fox Transportation website

Static site: plain HTML, CSS and JavaScript, no build step. Open `index.html` or serve the folder
(`python3 -m http.server`) and deploy the folder as-is.

## Pages

| Page | Purpose |
| --- | --- |
| `index.html` | Home. Scroll-driven route map hero, stats, local vs. beyond-the-ring services, equipment configurator, terminal, reasons, carrier band, quote CTA |
| `services.html` | Local truckload/LTL, truckload (single or team), rail, hazmat |
| `equipment.html` | Interactive configurator plus 53', 48', rear doors, straight truck, drivers |
| `about.html` | The two companies, authority numbers, timeline |
| `carriers.html` | Carrier setup requirements |
| `quote.html` | **Primary conversion:** quote request form |
| `contact.html` | Phone lines, email, terminal, map |

The primary goal on every page is **Request a quote**: the nav button, the hero, and the dark CTA band before each footer all lead to `quote.html`. Calling dispatch is the secondary action.

**Where quote requests go:** the site has no server. Submitting the form checks it, then opens the visitor's email app with the request pre-addressed to dispatch@foxtrans.net, and the page says so. To receive submissions directly instead, point the form at a form service (Formspree or similar) in `assets/js/site.js`.

## Adding real photos

Every photo slot shows a to-scale line drawing until a real photo exists. To use a photo:

1. Save it in `assets/photos/` under one of these names: `terminal.jpg`, `yard.jpg`,
   `trailer-53.jpg`, `trailer-48.jpg`, `straight-truck.jpg`. Keep it about 2000px wide and under 400KB.
2. Add the filename to the `PHOTOS` list near the "Photo slots" comment in `assets/js/site.js`.

## Facts used (from public listings for foxtrans.net)

- Fox Brothers Transfer, Inc.: trucking since 1991, terminal near I-355 & North Ave, Lombard. Truckload and
  limited LTL within 45 miles of Chicago. 48'/53' trailers, swing or roll doors, straight trucks with lift gates,
  all drivers hazmat certified. USDOT 515265. 630-932-9040.
- Fox Transportation Services, Inc.: formed late 2006. Truckload with single or team drivers, rail to major metros,
  5,000+ contracted carriers (authority, track record, financially strong). USDOT 2238384, MC 592002. 630-261-0800.
- 10 E Progress Road, Lombard, IL 60148 · dispatch@foxtrans.net
- Carrier requirements: MC#, $100,000 cargo insurance, $1,000,000 liability insurance, W-9.

Confirm the phone numbers, the authority numbers and the "1991" date with the owner before launch.

## Accessibility and performance

- Aims for WCAG 2.2 AA: skip link, landmarks, one H1 per page, labeled form fields with inline errors,
  keyboard-operable controls with a visible focus ring, 44px+ touch targets, and computed text contrast.
- `prefers-reduced-motion` is honored at load and if it is switched on mid-visit: the hero becomes static and
  every animation jumps to its end state.
- Phones, short screens and touch devices get a static composed hero instead of the pinned scroll.
- Fonts (Overpass, SIL Open Font License) are self-hosted as Latin-only woff2, with the two main weights preloaded.
- No images are required to render the page; all artwork is inline SVG. There are no third-party requests.
