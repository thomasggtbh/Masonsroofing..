# Fox Transportation · Design Package (10K, Tier 1)

Kept outside the deploy folder on purpose. Every line of copy here ships verbatim.

## 1. Brand premise

**Answered.** Fox is the trucking company that picks up: by the second ring, within the hour on a quote, and on the dock when it said it would. Its own trucks cover Chicagoland from Lombard; a vetted carrier network and rail cover everything past that. Every section proves one of those two things, and funnels to one action: **Request a quote**.

## 2. Palette (sampled from the hero footage: winter lot, chrome, amber marker lights)

```css
:root{
  --canvas:#e9ece9;      /* overcast concrete */
  --panel:#f5f6f3;
  --accent:#c2410f;      /* amber marker light pushed to fox orange, CTA only */
  --accent-hover:#a8380c;
  --accent-muted:#f07a3e;
  --text-secondary:#3b4753;
  --text-primary:#111820; /* wet asphalt */
}
```

## 3. Type

Overpass (display 800/900, body 400/600/700), Overpass Mono 500 for labels. Overpass descends from Highway Gothic, the lettering on US interstate signs.

## 4. Band map (hero: 400vh, 300vh of scrub)

| Band | Range (starting point) | Footage moment | Copy | Entrance |
|---|---|---|---|---|
| 1 | 0.00 to 0.30 | Wide on the lot, truck idling right of frame | Kicker "Lombard, Illinois · Since 1991". H1 "Our trucks in Chicagoland. The right carrier beyond it." Lede "Truckload and limited LTL on Fox trucks inside 45 miles of Chicago. Single or team drivers, more than 5,000 contracted carriers and rail for everything farther." | Word rise, load ramp |
| 2 | 0.34 to 0.64 | Camera pushing in, chrome filling frame | Tag "Dispatch". H2 "Someone picks up by the second ring." Body "Every shipment is tracked and traced, and you hear how it is going the way you prefer: phone, text, email or fax." | Approach from depth (echoes the push) |
| 3 | 0.68 to 1.00 | Low hero angle on the grille, at rest | Tag "Quotes". H2 "Send the lane. Hear back within the hour." Body "Email a quote request and dispatch replies within the hour. Or call 630-261-0800." CTA "Request a quote" | Word rise into staged settle |

## 5. Static hero (phones, portrait tablets, coarse portrait, landscape phones, reduced motion)

Ending frame as the image. Band 1 copy with both buttons.

## 6. Below the fold (home)

Mile markers (1991, 45 mi, 5,000+, 2 rings) · Two ways we move freight · The 45-mile ring map (draws itself on view) · Equipment configurator (the one interactive moment) · Lombard terminal with the real fleet photo · Why shippers call Fox · Management team · Carrier band · Quote CTA.

Management team copy (from foxtrans.net/about, reworded, nothing added):

- **Thomas W. Fox**, Transportation management. "Thomas has worked in transportation management since he was about 19, and he learned it from the ground up: driving tractor-trailers, working the docks, hand-loading trailers and putting in more overtime than anyone could count. He still loses sleep over freight, which is exactly the kind of person you want watching yours."
- **Ramon G. Fox**, Fleet and drivers. "Ramon has spent his whole life in trucking. He can back a tractor-trailer faster and straighter than most drivers can pull one forward, and when freight has to move overnight, he is the one up moving it. He runs the Fox tractor-trailer drivers with a firm, fair hand."
- **Richard Nisivaco**, Sales and customer accounts, owner. "Rich brings thirty years of sales experience and works side by side with operations to shape service around what each customer actually needs. He stays on the account after the sale to make sure the standard holds, and as an owner he can make the call on the spot. If Rich promised it, Fox delivers it, even when a single move costs the company money."

Form: mailto to dispatch@foxtrans.net, success state says so honestly.

## 7. Vector layer

Chicagoland map (expressways, 45-mile ring, terminal pin, routes past the ring), to-scale truck elevations, lane-stripe environment layer, dashed road in the CTA.

## 8. Engineering

Blob fetch with loading ring and 20s watchdog, dt-normalized lerp, gated seeks, delta-gated writes, smoothstep band pacing, four-layer legibility (base scrim, band scrim, text shadow, chips), five static gates identical in CSS and JS with live change listeners, complete without video, reduced motion honored live both ways.

## 9. Copy gate

Zero em dashes, zero stock words (leverage, seamless, empower, unlock, robust, actionable, data-driven, solutions), plus the body sweep for AI tells, before anyone sees it.
