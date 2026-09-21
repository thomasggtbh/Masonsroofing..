# Design Package: thomasdoyle.com (working name)

Tier 1, single continuous 6-second shot. Written before generation. Consumed by the build.
Every line of copy below ships verbatim.

## 1. The brand premise

**Three seconds.** A feed gives you about three seconds before the thumb moves on. A website
gives you about the same before the tab closes. Ads and websites are therefore the same job:
win the first three seconds or lose the person entirely. Thomas Doyle makes the thing that
wins them. So the site does not claim this. The site performs it: the visitor is stopped in
their first three seconds, and then realises that being stopped was the demonstration.
Every section serves that one idea. Attention is the product.

## 2. The palette as CSS tokens

Sampled from the footage world: a deep blue-ink void, cold white-blue light tearing past,
arrival at a still luminous plane. The accent is deliberately warm, the one human thing in a
cold machine world, because the single call to action is calling a person.

```css
:root{
  --canvas:#070d16;         /* deep blue-ink void, tinted from the footage, never pure black */
  --panel:#0e1726;          /* cards and raised surfaces */
  --panel-2:#131f33;        /* the second raised step */
  --accent:#ff6a45;         /* the CTA and rare emphasis: flame against cold light */
  --accent-hover:#ff8563;
  --accent-muted:rgba(255,106,69,.14);  /* whisper level: borders, glows, particles */
  --glow:#7fb4ff;           /* the cold light of the footage */
  --glow-dim:rgba(127,180,255,.16);
  --text-primary:#eef3fb;
  --text-secondary:#93a4bd;
  --line:rgba(147,164,189,.16);
}
```

Measured contrast on --canvas: text-primary 16.9:1, text-secondary 7.68:1, accent 6.86:1,
glow 9.16:1. Ink #0a1220 on the accent button: 6.61:1.

## 3. The type trio

- **Display: Bricolage Grotesque** (600, 800). Real character, slightly irregular, current.
  Not Inter, not Roboto.
- **Body: Figtree** (400, 500, 600). Quiet, warm, highly legible at small sizes.
- **Mono: IBM Plex Mono** (400, 500). Small labels, HUD chips, section numbers.

## 4. The band map

Hero height 560vh, so the scroll range is 460vh. Ranges are starting points, validated by the
flick test. At 0.02 of progress the eased ramps are about 9vh, leaving roughly 96vh of fully
settled plateau per beat.

| Band | Range | Footage moment | Copy (verbatim) | Entrance |
|---|---|---|---|---|
| 1 | 0.00 to 0.22 | Falling into the streaming light, speed at maximum | "Everything scrolls past." | Drift-down, plus the one-time load ramp so the hero opens settled |
| 2 | 0.26 to 0.48 | Still falling, streaks tearing past on both sides | "Faster than you can read this." | Streak-blur to sharp (invented): a horizontally offset static-blur ghost resolves into the sharp copy |
| 3 | 0.52 to 0.72 | Breaking through the last sheet, the lens flare | "Then something stops you." | Word-punch with overshoot, echoing the impact |
| 4 | 0.78 to 1.00 | Stillness. The glowing plane at rest, ripples settling | Headline "That's the whole job." / Subline "I'm Thomas Doyle. I make websites and ad creative people stop for." / CTA "Call or text 630-940-9062" | Word-by-word rise into a staged settle: headline words, then subline, then the CTA row |

Read as one thought: everything scrolls past, faster than you can read this, then something
stops you, that's the whole job. The visitor lives the sentence while reading it.

## 5. The static-hero copy block

For phones and reduced motion, composed over the ending frame.

- Chip: `WEBSITES + AD CREATIVE`
- Headline: **"Everything scrolls past. I make the thing that stops."**
- Subline: "I'm Thomas Doyle. Websites and ad creative built to win the first three seconds."
- Primary CTA: "Call or text 630-940-9062"
- Secondary: "See what I make"

## 6. The below-fold outline

Every section funnels to the one call to action: call or text 630-940-9062.

### A. What I make
- Eyebrow: `What I make`
- H2: **"Two things. Both are the same job."**
- Card 1, Websites: "One page or a whole site, built by hand, with no template underneath.
  Fast on a phone, easy to change, and shaped around the single thing you want people to do."
- Card 2, Ad creative: "Scroll-stopping video and statics for Meta and TikTok. Built to look
  native to the feed instead of looking like an ad somebody paid for."
- Each card carries its own generated still, in the hero's world. Equal treatment, no asymmetry.

### B. The three seconds (holds the interactive moment)
- Eyebrow: `The whole idea`
- H2: **"You get three seconds. That's it."**
- Body: "A feed gives you about three seconds before the thumb moves. A website gives you
  about the same before the tab closes. Most work loses that fight before it has said
  anything at all. Everything I build is designed to win it first and earn the rest after."
- **The interactive moment: press and hold.** A ring that fills over three real seconds while
  the visitor holds. Release early and it eases back down, never snapping. Complete it and the
  three supporting points light up in sequence.
  - Prompt label: "Press and hold for three seconds"
  - Completion line: **"Three seconds. Felt long, didn't it? Now imagine asking a stranger for them."**
  - The three points revealed: "The hook does the work" / "One thing to do, made obvious" /
    "Fast enough that nobody waits"
  - Reduced motion gets the completed state immediately, no hold required.

### C. How it works
- Eyebrow: `How it works`
- H2: **"Four steps. No mystery, no disappearing."**
1. **We talk.** "Call or text me. Fifteen minutes, no pitch. I ask what you sell and who you sell it to."
2. **You get a price.** "One number, in writing, before anything starts. It does not move later."
3. **I build it.** "You get a live link on day one and watch it fill in. One person on the job, and you always know who to text."
4. **You own it.** "Files, accounts, all of it, handed over. Want a change next year, text me. Nothing is locked to me."

### D. What it costs
- Eyebrow: `Money`
- H2: **"No surprise invoices."**
- Body: "You get one fixed price in writing before I start. Not an estimate, not an hourly
  rate that quietly grows. If the job changes, you hear what it costs before I touch it. The
  number you agree to is the number you pay."
- Three points: "Fixed price, agreed up front" / "Nothing starts until you have it in writing"
  / "Changes are quoted before they happen"
- NOTE FOR THOMAS: real starting numbers here would make this section hit twice as hard.
  Left out rather than invented.

### E. Answers (FAQ, built from the real objections in the research)
- Eyebrow: `Straight answers`
- H2: **"The things people ask before they call."**
1. "How do I know you will actually finish?" / "Because you can see it the whole time. You get
   the live link on day one and it changes as I build. You watch it happen instead of waiting
   on an email that never comes."
2. "What if it looks great and still brings me nothing?" / "Then it failed. Looking good is the
   entry fee, not the job. Every page I build aims at one action, and I tell you what that
   action is and how you will know it worked before I start."
3. "Why not just use a website builder?" / "Use one if a template fits you. They are genuinely
   fine. You are reading this because you want something people remember, and templates are
   built so thousands of businesses can share a look."
4. "Can I get just the ads, or just the site?" / "Yes. Most people start with one and add the
   other once they have seen it work."
5. "How long does it take?" / "Most one-page sites are days, not months. You get a date along
   with the price, and if I am ever going to miss it you hear it from me first."

### F. The close
- H2: **"Let's talk."**
- Body: "Call or text. I answer. If I am heads down on a build I will come back to you the same day."
- Primary CTA: the number itself, huge. Tap to call on a phone, click to copy on a desktop.
- Microcopy under it: "No form, no funnel, no autoresponder. Just me."

### G. Footer
- Name, the number, one line: "Websites and ad creative. Built to win the first three seconds."
- Not a fictional brand, so no fictional-brand disclosure.

### The form
**No form at all**, by the user's own choice of call or text as the single action. The number
is the button: `tel:` on coarse pointers, click to copy on desktop with a real confirmation
state. Nothing is collected and nothing is sent anywhere, so nothing needs to be disclosed.

## 7. The vector layer plan

**The signature element: the rail.** One continuous drawn line fixed to the left gutter,
running the full viewport height, with a glowing head dot that travels down it as the page
scrolls. Behind the head the line is drawn in accent; ahead of it the line is faint. Section
nodes sit along it and light up in accent as each section arrives. It is the scroll itself,
drawn. Remove it and the page loses its spine, which is the test of a real signature.
Hidden below 1100px and on short screens, where there is no room for it.

- Self-drawing arcs: the hold ring in section B draws itself from the rail's accent.
- Whisper particles: slow drifting light motes on one fixed full-page canvas layer.
- The fixed environment layer: a very slow drifting radial glow in --glow at whisper opacity,
  on a 70 second cycle, so scrolling feels like moving through one place.
- All of it honors reduced motion: final states shown, drives stopped.

## 8. The engineering list

The full standard from `references/scrub-pipeline.md`, no half-measures: the Blob fetch with
the loading ring, the dt-normalized lerp in a rAF loop that rests, gated seeks with the
deadlock escape, delta-gated DOM writes, band pacing validated by the flick test, the
four-layer legibility system audited against worst frames at 3.5:1 or better, the five
static-hero gates kept live with change listeners in CSS and JS matching character for
character, complete-without-video, and the quality floor. Plus the whole-site-animated
standard: nothing snaps, one living element per section at whisper level, one interactive
moment, entrances that echo their content.

## 9. The copy gate

Every viewer-facing line above ships verbatim. The built page must pass the Phase 9 grep gate
with zero em dashes and zero stock words, plus the body-copy sweep for AI tells, before anyone
sees it. The deliberate devices here stay: the four-beat hero sentence, the "Two things. Both
are the same job." punch, and the "No form, no funnel, no autoresponder. Just me." triplet
were all chosen on purpose for this brand.
