# Low Cloud: design package (Tier 1)

Not shipped: this file sits outside the site folder (low-cloud/) so it never ends up in a deploy zip.

## 1. Brand premise

Low Cloud is an invented mountain hot-spring bathhouse in a pine valley where a low cloud sits most mornings. The one idea: **below the cloud, it's quiet.** The real complaint people have about hot springs is the crowd and the queue ("crowded but worth it", "waited about an hour for a tub"). Low Cloud caps every two-hour slot at 18 guests, so there is never a line. Every section sells that quiet: the descent, the pools, the hold moment that sinks the noise, the numbers, the booking.

## 2. Palette (sampled toward the footage's grade)

```css
--canvas:#11181c;  /* basalt blue night, never pure black */
--panel:#18232a;
--accent:#93dccf;  /* milky mineral turquoise, CTA and focus only */
--accent-hover:#b5ebe1;
--accent-muted:rgba(147,220,207,.18);
--copper:#d99a68;  /* lantern glow, whisper level only */
--text-secondary:#a9b8b8;
--text-primary:#e9eeec;
```

## 3. Type

- Display: Bricolage Grotesque 500 / 700
- Body: Figtree 400 / 500 / 600
- Labels: DM Mono 400

## 4. Band map (hero 600vh, starting points)

| Band | Range | Footage moment | Copy | Entrance |
|---|---|---|---|---|
| 1 | 0.00 to 0.20 | above the cloud sea, glow underneath | "Up here, the week is still going." | blur to sharp (mist), load ramp |
| 2 | 0.25 to 0.47 | sinking into the cloud | "So sink through it." | drift down |
| 3 | 0.52 to 0.74 | emerging under the cloud ceiling | "Underneath, it's quiet. Eighteen people. Two hours. No line." | scatter (vapour condensing) |
| 4 | 0.80 to 1.00 | the pool at rest, steam rising | "Book a soak below the cloud." / "Mineral pools at 40°C in a pine valley you can't hear the road from." / Book a soak, See the pools | word rise into staged settle |

## 5. Static hero copy

"Book a soak below the cloud." / "Mineral pools at 40°C. Eighteen guests per slot, so there's never a line." / Book a soak

## 6. Below the fold

1. Pools: The Ember 41°C, The Milk 38°C, The Plunge 12°C. One image each.
2. Interactive moment, "Sink in": press and hold, the water rises over the noise words until only "Quiet." is left.
3. How it works: pick a slot, arrive and rinse, soak and plunge. Self-drawing line.
4. Numbers: 18 guests, 2 hours, 40°C, 0 phones in the water.
5. Quotes: three short guest lines about the lack of crowd.
6. Prices: Weekday slot $38, Weekend slot $46, Private pool for two $120.
7. FAQ: crowds, tattoos, swimsuits, what to bring, kids, cancelling.
8. Book form: JS-only success state. Demo site, nothing is sent, and the form says so.
9. Footer: Low Cloud is a fictional brand made for a design demo. All imagery is AI generated.

## 7. Vector layer

Drawn brand mark (cloud line over water line), contour dividers that draw on entry, the steps line that draws on scroll, steam motes over the pool cards. All pinned to final state under reduced motion.

## 8. Engineering

Blob fetch with loading ring and watchdog, dt-normalized lerp, gated seeks, delta-gated DOM writes, band pacing plus flick test, four-layer legibility, five live static-hero gates, complete without video, quality floor.

## 9. Copy gate

Zero em dashes, zero stock words, body sweep for AI tells before anyone sees it.
