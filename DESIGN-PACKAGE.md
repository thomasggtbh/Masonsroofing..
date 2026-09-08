# KMI Construction — Design Package

The single creative deliverable. Written before the build; the build consumes it.
Every line of copy below ships verbatim.

## 0. Who this is for (research, Phase 3)

KMI Construction is a **commercial masonry subcontractor** in New Berlin, Wisconsin.
Public listings show: Mason Contractors, Panel Systems (Prefabricated), Restoration
and Preservation (Historical), granite and stone cladding, terra cotta wall panels,
commercial maintenance and repair, masonry design assistance.

**The reader is a general contractor's project manager**, not a homeowner. What
research says decides their bid list:

- **Schedule is the fear.** A masonry sub that slips ripples delay through every
  following trade; the GC eats the liquidated damages.
- **Safety is a gate, not a tiebreaker.** Many GCs will not let a sub bid at all
  with an EMR above 1.0 to 1.2.
- **On restoration the mortar match is the job.** The recurring phrase in reviews
  and forums is that a bad repair "sticks out like a patch job."
- **The complaints that kill a sub are boring.** Not craft. "Getting them to
  respond was difficult." "Said he would come back and never did." "Told me
  August, came September 30."

So the site sells **reliability first, craft second**. Craft is assumed.

## 1. The brand premise

**The joint.** A wall almost never fails at the brick, it fails at the mortar joint.
Water finds the joint, gets behind the face, and Wisconsin's freeze and thaw cycle
does the rest. Restoration is judged at the joint (does the mortar match). A panel
wall is judged at the joint (did it land on the line). And KMI is itself a joint in
the schedule, the seam between the trade before and the trade after. Every section,
the divider lines, the signature element and the interactive moment serve that one
idea.

## 2. Palette (CSS tokens)

Masonry's real material world: fired clay, charcoal mortar, limestone. This sits
close to a look normally avoided as an AI default (near black plus warm accent plus
high contrast serif). It is taken deliberately here because it is the subject's own
material world, and it is kept from reading generic three ways: limestone buff as a
third tone, the running bond mortar line as a signature, and the accent held to rare
doses. Deviation stated out loud, as required.

```css
:root{
  --canvas:#14171a;      /* cold charcoal, never pure black */
  --canvas-2:#1b1f23;
  --panel:#21262b;
  --line:#2e353c;
  --accent:#b8452c;      /* fired clay. CTA fill only */
  --accent-hover:#d4573a;
  --brick-lt:#e8785c;    /* accent as small text, 6.2:1 on canvas */
  --accent-muted:rgba(184,69,44,.18);
  --stone:#c9bda6;       /* limestone buff, kickers, 9.7:1 */
  --text-secondary:#9aa4ad;  /* 7.1:1 */
  --text-primary:#eceae6;    /* 15:1 */
}
```

## 3. Type trio

- **Display:** Fraunces, 700 and 900. A serif with carved weight, not a habitual
  default. Fallback Georgia.
- **Body:** Public Sans, 400 and 600. Quiet, institutional, reads like spec text.
- **Mono:** IBM Plex Mono, 500. Small labels and the spec sheet rows.

No Inter, no Roboto.

## 4. The hero and the band map

**Tier 1**, one continuous journey, drawn rather than filmed (the media CDN is
blocked by this session's egress policy; the storyboard is unchanged).

**The Descent.** The camera falls down the face of a tall brick and limestone
facade in low raking winter light. Courses stream upward past the lens, limestone
bands pass, scaffold shadows sweep through, dust drifts in the light. Near the end
the fall slows, the camera tilts in and pushes close, focus racking from the wide
facade to a single freshly tooled mortar joint, and everything comes to rest there.

Hero height **700vh** (600vh of scroll range). Plateaus land near 84vh, about 5.6
normal flicks, inside the 80 to 130vh standard. Ranges are starting points,
validated by the flick test.

| Band | Range | Footage moment | Copy (verbatim) | Entrance |
|---|---|---|---|---|
| 1 | 0.00 to 0.17 | High on the facade, courses falling away below | "Every wall fails in the same place." | Drift-down, words fall as the camera falls |
| 2 | 0.19 to 0.37 | Mid descent, courses streaming, scaffold shadow sweeps | "Not the brick. The joint." | Word-punch with overshoot on "joint" |
| 3 | 0.40 to 0.58 | Deeper, the raking light shifts across the wall | "Water gets in. Wisconsin does the rest." | Scatter, characters break apart and reassemble like spalling |
| 4 | 0.61 to 0.79 | Fall slowing, camera begins to tilt in | "We build them so it doesn't. We fix them when it does." | Blur-to-sharp, echoing the focus rack |
| 5 | 0.82 to 1.00 | At rest on the tooled joint | "KMI Construction" + subline + CTA row | Word-by-word rise into a staged settle |

Band 5 subline: "Commercial masonry, historic restoration and panel wall systems.
Family owned in New Berlin, Wisconsin since 1992."
Band 5 CTA row: "Call (262) 548-0632" and "Request a bid".

## 5. Static hero copy block

For phones, portrait tablets, coarse pointer, landscape phones and reduced motion.

- Kicker: "New Berlin, Wisconsin · Family owned since 1992"
- Headline: "Every wall fails at the joint."
- Subline: "Commercial masonry, historic restoration and panel wall systems, built
  so water never finds a way in."
- CTA: "Call (262) 548-0632" and "Request a bid"

## 6. Below-fold outline

Every section funnels to one anchor, `#bid`. No two adjacent sections share a
layout skeleton.

1. **The premise** (asymmetric two column: big serif statement left, drawn wall
   section diagram right, labelled FACE / JOINT / BACKUP / WATER PATH).
   - Kicker "The one thing". H2 "A wall almost never fails at the brick."
   - "It fails at the joint. Water finds the mortar first, gets behind the face,
     and waits for a Wisconsin winter to freeze and expand. Do that a few hundred
     times and the brick face lets go. Every job we take, new or two hundred years
     old, is really about closing the path water uses to get in."
2. **Services** (three cards offset like running bond, each with its own drawn
   SVG, equal treatment).
   - Kicker "What we self perform". H2 "Three lines of work. One standard."
   - **Masonry** — "New commercial brick, block and stone, from small repairs to
     full corporate builds. Our own crews, our own layout, coursing that lines up
     floor to floor."
   - **Restoration** — "Historic and existing buildings brought back without the
     patch job look. We match the mortar to the original for color, sand and
     strength, then tool the profile to match what was there."
   - **Panel wall systems** — "Prefabricated and panelized wall systems, terra
     cotta, stone facing and cladding, set on the line and sealed. Panels land the
     day the schedule says they land."
3. **The interactive moment** (centered, single column, full width band).
   - Kicker "Try it". H2 "Press and hold to strike a joint."
   - "This is the whole trade in one motion. Rake the old mortar out, pack the new
     mortar in, then tool it concave so it sheds water instead of holding it."
   - On completion: "That is the difference between a wall that lasts eighty years
     and a wall that lasts eight."
   - Reduced motion gets the finished state with no hold required.
4. **The spec sheet** (mono labels, data rows, no cards).
   - Kicker "Before you put us on the list". H2 "The boring things that decide the
     bid."
   - SCHEDULE — "We plan the manpower before we sign, not after. If the wall is on
     the critical path, that is our problem, not yours."
   - SAFETY — "Safety is a gate for most GCs, not a tiebreaker. Ask us for our EMR
     and our OSHA history and you get them the same day."
   - COMMUNICATION — "You get a person on the phone. The most common complaint
     about masons in this trade is not craft, it is a call that never comes back."
   - PRECONSTRUCTION — "Masonry design assistance and layout help before the bid,
     so the detail that does not work gets found on paper."
   - COVERAGE — "Licensed and insured, working commercial projects across
     southeastern Wisconsin from New Berlin."
5. **Selected work** (asymmetric grid, mixed tile sizes, drawn elevations).
   - Kicker "Selected work". H2 "Walls we would drive you past."
   - Six honest category tiles. No invented client or project names.
6. **FAQ** (narrow single column accordion, answering the objections found in
   research: falling behind, mortar matching, winter work, prequalification
   paperwork, preconstruction involvement, project size).
7. **Contact** (split: the phone number set large left, form right).
   - Kicker "Request a bid". H2 "Send us the drawings and the dates."
   - Form fields: name, company, phone, project type, message. Button "Send it
     over". Success state: "Your email app should be open with the message ready.
     If it did not open, call (262) 548-0632 and ask for the estimating desk."
   - **Form handling: mailto.** Static site, no backend. The visitor's own email
     app opens addressed to KMI. The address in the build is a marked placeholder
     until confirmed.
8. **Footer.** Real company, so no fictional-brand disclosure. Imagery is drawn
   rather than photographic and carries no AI disclosure, per the decision in
   Phase 2; real project photography drops into the Selected work tiles later.

## 7. The vector layer plan

- **Signature element: the mortar line.** A drawn horizontal rule that behaves like
  a struck joint. It self-draws on scroll at every section boundary, and the running
  bond offset is the page's repeating motif. Remove it and the page changes, which
  is the test.
- Hero wall: SVG running bond pattern tiles (four courses, sixteen bricks, varied
  fired clay fills) on parallax layers, plus limestone bands, scaffold shadow bars,
  a raking light sweep and whisper level dust.
- Drawn diagrams: the wall section in the premise, three service illustrations, the
  strike-a-joint mechanism, six building elevations in Selected work.
- One fixed background environment layer behind everything, a slow cold light drift
  at 90 seconds.
- All of it honors reduced motion: final states shown, drives stopped.

## 8. The engineering list

dt-normalized lerp in a rAF loop that rests, one delta-gated custom property write
per frame driving the whole scene, band pacing validated by the flick test, the four
layer legibility system, the five static-hero gates kept live with change listeners
in CSS and JS character for character, complete without any external asset, the
whole-site-animated standard, and the quality floor.

## 9. The copy gate

Every viewer-facing line above ships verbatim. The built page must pass the grep
gate (zero em dashes, zero stock words) plus the body copy sweep for AI tells before
anyone sees it. The deliberate staccato devices ("Not the brick. The joint.",
"Water gets in. Wisconsin does the rest.") are brand craft and stay.
