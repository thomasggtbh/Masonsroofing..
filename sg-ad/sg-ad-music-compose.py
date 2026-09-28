"""Original 15 s instrumental for the S-G General Contracting ad.

Every sound is synthesized here from oscillators, noise and plucked-string
models; nothing is sampled. The arrangement is locked to the video's edit:

  0.0 - 2.9   PRECISION       ticking clock hats, muted plucked arpeggio, sub drone, swell
  2.9 - 6.9   CRAFTSMANSHIP   kick + pulsing bass enter, rim clicks, clean rim clicks
  6.9 - 10.9  TRANSFORMATION  pads open up, brighter arpeggio, clap layer, riser + tom fill
  10.9 - 15.0 CONFIDENCE      impact, warm major-leaning chords, settles and rings out

Tempo 120 BPM, bar lines at 0.9, 2.9, 4.9, 6.9, 8.9, 10.9, 12.9 s.
"""
import numpy as np
from scipy import signal
import pyloudnorm as pyln
import wave

SR = 48000
DUR = 15.0
N = int(SR * DUR)
rng = np.random.default_rng(20260928)

BEAT = 0.5
BAR0 = 0.9                       # first bar line; the video's big moments fall on bars
bar = lambda k: BAR0 + 2.0 * k   # k=1 -> 2.9, k=3 -> 6.9, k=5 -> 10.9, k=6 -> 12.9

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def zeros(): return np.zeros((2, N))
def tvec(d): return np.arange(int(d * SR)) / SR

def place(buf, x, t, gain=1.0, pan=0.0):
    """Add mono or stereo x into buf at time t with equal-power pan."""
    i = int(round(t * SR))
    if i >= N: return
    if x.ndim == 1:
        l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
        x = np.vstack([x * l, x * r])
    n = min(x.shape[1], N - i)
    if i < 0:
        x = x[:, -i:]; n = min(x.shape[1], N); i = 0
    buf[:, i:i + n] += gain * x[:, :n]

def lp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, 'low', fs=SR, output='sos'), x, axis=-1)
def hp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, 'high', fs=SR, output='sos'), x, axis=-1)
def bp(x, lo, hi, order=2):
    return signal.sosfilt(signal.butter(order, [lo, hi], 'band', fs=SR, output='sos'), x, axis=-1)

def adsr(n, a, d, s, r, sus_len=None):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    sus = max(0, n - a - d - r) if sus_len is None else int(sus_len * SR)
    env = np.concatenate([np.linspace(0, 1, max(a, 1)), np.linspace(1, s, max(d, 1)),
                          np.full(sus, s), np.linspace(s, 0, max(r, 1))])
    return np.pad(env, (0, max(0, n - len(env))))[:n]

def saw(f, t, phase=0.0):
    return 2.0 * ((f * t + phase) % 1.0) - 1.0

# ---------------------------------------------------------------- instruments
def kick(level=1.0):
    t = tvec(0.55)
    f = 42 + 95 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 6.5)
    click = hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 400) * 0.25
    return np.tanh(1.6 * (0.7 * body + 1.6 * click)) * level

def hat(open_=False, level=1.0):
    d = 0.22 if open_ else 0.05
    t = tvec(d)
    x = hp(rng.standard_normal(len(t)), 7500, 4)
    ring = np.zeros(len(t))                 # no metallic partials: keeps hats airy, not clinky
    env = np.exp(-t * (14 if open_ else 90))
    y = lp(x + hp(ring, 6000), 12500, 2) * env * level
    a = int(0.0015 * SR)
    y[:a] *= np.linspace(0, 1, a)          # tiny attack ramp, no digital click
    return y * (0.55 if open_ else 0.8)

def rim(level=1.0):
    t = tvec(0.09)
    n = bp(rng.standard_normal(len(t)), 1800, 5200) * np.exp(-t * 110)
    return n * level * 0.8                   # dry click, no pitched ring

def clap(level=1.0):
    t = tvec(0.28)
    n = bp(rng.standard_normal(len(t)), 900, 5000)
    env = np.zeros(len(t))
    for k, off in enumerate((0.0, 0.009, 0.018)):
        i = int(off * SR)
        env[i:] += np.exp(-(t[: len(t) - i]) * (160 if k < 2 else 22)) * (0.6 if k < 2 else 1.0)
    return n * env * level

def tom(midi, level=1.0):
    t = tvec(0.45)
    f = mtof(midi) * (1 + 0.5 * np.exp(-t * 30))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(1.3 * np.sin(ph) * np.exp(-t * 7)) * level

def tick(level=1.0):
    """Precise metallic 'measure' tick used on the service cuts."""
    t = tvec(0.35)
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * dcy)
            for f, dcy in ((2960, 18), (4410, 26), (6230, 40), (8300, 60)))
    x += hp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 300) * 0.6
    return x * 0.3 * level

def pluck(midi, dur=0.9, bright=0.5, level=1.0):
    """Karplus-Strong plucked string, damped: a wooden, crafted sound."""
    f = mtof(midi)
    L = max(2, int(round(SR / f)))
    n = int(dur * SR)
    exc = np.zeros(n)
    burst = rng.uniform(-1, 1, L)
    burst = lp(burst, 1200 + 6000 * bright, 1)
    exc[:L] = burst
    g = 0.994
    a = np.zeros(L + 2); a[0] = 1.0; a[L] = -g * 0.5; a[L + 1] = -g * 0.5
    y = signal.lfilter([1.0], a, exc)
    y = lp(y, 900 + 5500 * bright)
    return y * adsr(n, 0.001, 0.05, 1.0, 0.08) * level

def pad(midis, dur, bright, level=1.0, attack=0.6, release=0.9):
    """Detuned saw pad, rendered dark and bright for filter-sweep crossfades."""
    t = tvec(dur + release)
    L = np.zeros(len(t)); R = np.zeros(len(t))
    for m in midis:
        f = mtof(m)
        for k, det in enumerate((-0.09, -0.035, 0.0, 0.04, 0.1)):
            ff = f * 2 ** (det / 12)
            v = saw(ff, t, phase=rng.random())
            w = (k - 2) / 2.0
            L += v * (0.5 - 0.35 * w); R += v * (0.5 + 0.35 * w)
    x = np.vstack([L, R]) / (len(midis) * 3.2)
    dark = lp(x, 650, 2); brt = lp(x, 3600, 2)
    if np.isscalar(bright):
        b = np.full(len(t), bright)
    else:
        b = np.interp(t, np.linspace(0, dur, len(bright)), bright)
    y = dark * (1 - b) + brt * b
    env = adsr(len(t), attack, 0.4, 0.85, release, sus_len=max(0, dur - attack - 0.4))
    return y * env * level

def bass_note(midi, dur, level=1.0, cutoff=380):
    t = tvec(dur)
    f = mtof(midi)
    x = 0.7 * saw(f, t) + 0.6 * np.sin(2 * np.pi * f * t) + 0.5 * np.sin(np.pi * f * t)
    x = lp(x, cutoff, 2)
    return np.tanh(1.4 * x) * adsr(len(t), 0.004, 0.12, 0.55, 0.06) * level

def sub_drone(midi, dur, level=1.0):
    t = tvec(dur)
    x = np.sin(2 * np.pi * mtof(midi) * t) + 0.25 * np.sin(2 * np.pi * mtof(midi + 12) * t)
    return x * adsr(len(t), 1.6, 0.1, 1.0, 0.5) * level

def riser(dur, level=1.0):
    t = tvec(dur)
    x = rng.standard_normal(len(t))
    out = np.zeros(len(t)); blk = 512
    for i in range(0, len(t), blk):         # sweeping band-pass, block-wise
        fc = 400 * (22) ** (i / len(t))
        out[i:i + blk] = bp(x[i:i + blk], fc * 0.7, min(fc * 1.4, 20000), 1)
    env = (t / dur) ** 2.2
    tone = np.sin(2 * np.pi * np.cumsum(180 + 520 * (t / dur) ** 2) / SR) * 0.15
    y = (out * 0.8 + tone) * env
    return np.vstack([y, np.roll(y, 240)]) * level

def impact(level=1.0):
    t = tvec(2.6)
    f = 36 + 40 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.9)
    air = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 5) * 0.35
    return np.tanh(1.3 * (boom + air)) * level

def reverse_swell(midis, dur, level=1.0):
    p = pad(midis, dur, 0.55, 1.0, attack=0.01, release=0.01)[:, : int(dur * SR)]
    env = (tvec(dur) / dur) ** 2.5
    return p[:, ::-1] * 0 + p * env * level   # swelling (not literally reversed audio)

# ---------------------------------------------------------------- harmony
Dm9  = [50, 57, 64, 65, 69]   # D3 A3 E4 F4 A4
Bb9  = [46, 53, 60, 62, 65]   # Bb2 F3 C4 D4 F4
F9   = [53, 57, 60, 67, 69]   # F3 A3 C4 G4 A4
Csus = [48, 55, 62, 64, 67]   # C3 G3 D4 E4 G4
BbM9 = [46, 53, 57, 60, 62]   # Bb2 F3 A3 C4 D4
Fadd = [41, 53, 57, 60, 67, 72]  # F2 F3 A3 C4 G4 C5 (final)

drums, bass, pads, plucks, fx = zeros(), zeros(), zeros(), zeros(), zeros()

# ---------------------------------------------------------------- A: PRECISION (0 - 2.9)
place(bass, sub_drone(38, 3.2), 0.0, 0.12)                               # low D, fades in
for i in range(10):                                                      # clock tick hats, 8ths from 0.4
    t = 0.4 + i * 0.25
    place(drums, hat(level=0.35 if i % 2 else 0.55), t, pan=0.25 if i % 2 else -0.15)
arpA = [62, 69, 64, 65, 69, 64, 62, 69, 64, 65]                          # D A E F ... (muted, low)
for i, m in enumerate(arpA):
    place(plucks, pluck(m, 0.7, bright=0.35 + 0.03 * i), 0.4 + i * 0.25, 0.32, pan=-0.3 + 0.06 * i)
place(pads, pad(Dm9, 2.5, np.linspace(0.1, 0.35, 8), 0.45, attack=1.4), 0.4, 1.0)
place(fx, riser(1.0, 0.11), 1.9)

# ---------------------------------------------------------------- B: CRAFTSMANSHIP (2.9 - 6.9)
chordsB = [(bar(1), Bb9 if False else Dm9), (bar(2), Bb9)]
for t0, ch in chordsB:
    place(pads, pad(ch, 2.0, 0.28, 0.6, attack=0.08, release=0.6), t0)
rootsB = [(bar(1), 38), (bar(2), 34 + 12)]                               # D2, Bb2
for t0, r in rootsB:
    for k in range(8):                                                   # 8th-note pulse
        place(bass, bass_note(r if k % 4 != 3 else r + 12, 0.22, 0.55 if k % 2 == 0 else 0.4, 320 + 60 * (k % 2)), t0 + k * 0.25)
for b in range(2):
    t0 = bar(1 + b)
    place(drums, kick(0.9), t0); place(drums, kick(0.55), t0 + 1.0)
    place(drums, kick(0.35), t0 + 1.75)
    for q in (0.5, 1.5):
        place(drums, rim(0.55), t0 + q, pan=0.2)
    for s in range(16):
        acc = 0.45 if s % 4 == 2 else (0.3 if s % 2 == 0 else 0.18)
        place(drums, hat(level=acc), t0 + s * 0.125, pan=0.3 if s % 2 else 0.1)
arpB = [62, 69, 72, 69, 64, 69, 65, 69]                                  # D A C A E A F A
for i in range(16):
    t = bar(1) + i * 0.25
    notes = arpB if t < bar(2) else [58, 65, 70, 65, 62, 65, 60, 65]
    place(plucks, pluck(notes[i % 8], 0.6, bright=0.45), t, 0.33, pan=0.35 if i % 2 else -0.35)
place(fx, riser(0.9, 0.08), 6.0)

# ---------------------------------------------------------------- C: TRANSFORMATION (6.9 - 10.9)
place(drums, kick(1.0), bar(3))
place(pads, pad(F9, 2.0, np.linspace(0.35, 0.8, 10), 1.0, attack=0.05, release=0.5), bar(3))
place(pads, pad(Csus, 2.0, np.linspace(0.8, 1.0, 10), 1.15, attack=0.05, release=0.5), bar(4))
for t0, r in ((bar(3), 41), (bar(4), 36)):                               # F2, C2
    for k in range(8):
        place(bass, bass_note(r if k % 4 != 3 else r + 12, 0.22, 0.6 if k % 2 == 0 else 0.45, 420 + 80 * (k % 2)), t0 + k * 0.25)
for b in range(2):
    t0 = bar(3 + b)
    place(drums, kick(0.95), t0); place(drums, kick(0.7), t0 + 1.0); place(drums, kick(0.4), t0 + 1.75)
    for q in (0.5, 1.5):
        place(drums, clap(0.5), t0 + q, pan=-0.1); place(drums, rim(0.35), t0 + q, pan=0.2)
    for s in range(16):
        acc = 0.5 if s % 4 == 2 else (0.34 if s % 2 == 0 else 0.22)
        place(drums, hat(open_=(s == 14), level=acc), t0 + s * 0.125, pan=0.3 if s % 2 else 0.1)
arpC = [(bar(3), [65, 72, 77, 72, 67, 72, 69, 72]), (bar(4), [64, 67, 72, 67, 62, 67, 64, 67])]
for t0, notes in arpC:
    for i in range(8):
        place(plucks, pluck(notes[i] + (12 if i % 4 == 2 else 0), 0.55, bright=0.75), t0 + i * 0.25, 0.42, pan=0.4 if i % 2 else -0.4)
place(fx, riser(2.0, 0.2), 8.9)                                          # build into the reveal
for k, (m, t) in enumerate(((50, 10.4), (45, 10.525), (43, 10.65), (38, 10.775))):
    place(drums, tom(m, 0.3 + 0.06 * k), t, pan=0.3 - 0.2 * k)

# ---------------------------------------------------------------- D: CONFIDENCE (10.9 - 15)
place(fx, impact(0.75), bar(5))
place(drums, kick(1.0), bar(5))
place(drums, hat(open_=True, level=0.35), bar(5))
place(pads, pad(BbM9, 2.0, 0.85, 1.15, attack=0.03, release=0.4), bar(5))
place(pads, pad(Fadd, 1.3, np.linspace(0.85, 0.45, 6), 1.0, attack=0.03, release=0.8), bar(6))
for k in range(8):                                                       # Bb pulse, then settle
    place(bass, bass_note(34 + 12 if k % 4 != 3 else 46 + 12, 0.22, 0.5 if k % 2 == 0 else 0.38, 380), bar(5) + k * 0.25)
place(bass, bass_note(41, 1.9, 0.6, 300), bar(6))                        # F root, held
place(bass, sub_drone(29 + 12, 2.1, 0.1), bar(6))
for s in range(16):
    acc = 0.4 if s % 4 == 2 else (0.26 if s % 2 == 0 else 0.15)
    place(drums, hat(level=acc), bar(5) + s * 0.125, pan=0.3 if s % 2 else 0.1)
place(drums, kick(0.7), bar(5) + 1.0)
for q in (0.5, 1.5):
    place(drums, rim(0.45), bar(5) + q, pan=0.2)
place(drums, kick(0.85), bar(6)); place(fx, impact(0.35), bar(6))
arpD = [70, 74, 77, 74, 72, 74, 69, 74]
for i in range(8):
    place(plucks, pluck(arpD[i], 0.6, bright=0.7), bar(5) + i * 0.25, 0.38, pan=0.35 if i % 2 else -0.35)
for i, m in enumerate((65, 69, 72, 76, 77)):                             # final rising strum, F add9
    place(plucks, pluck(m, 1.8, bright=0.55), bar(6) + i * 0.045, 0.3, pan=-0.3 + 0.15 * i)

# ---------------------------------------------------------------- mix
def sidechain(x, depth=0.35):
    """Gentle pump on beats 1 and 3 of each bar from 2.9 s (glue, not EDM)."""
    g = np.ones(N)
    for k in range(1, 6):
        for q in (0.0, 1.0):
            i = int((bar(k) + q) * SR); n = int(0.28 * SR)
            if i < N:
                seg = 1 - depth * np.exp(-np.arange(min(n, N - i)) / SR * 14)
                g[i:i + len(seg)] = np.minimum(g[i:i + len(seg)], seg)
    return x * g

def reverb(x, secs=2.2, damp=4500, wet=0.25):
    n = int(secs * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((2, n)) * np.exp(-t * 6.9 / secs)
    ir = lp(ir, damp, 1)
    ir[:, : int(0.012 * SR)] = 0                                          # pre-delay
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    y = np.vstack([signal.fftconvolve(x[c], ir[c])[:N] for c in range(2)])
    return x * (1 - wet) + y * wet

pads = sidechain(hp(pads, 120), 0.3)
bass = sidechain(bass, 0.2)
plucks = hp(plucks, 180)
music = (1.0 * drums + 0.95 * bass + 0.8 * pads + 0.9 * plucks + 0.85 * fx)
music = reverb(music, 2.0, 5000, 0.18) + reverb(0.6 * pads + 0.5 * plucks, 3.0, 3500, 0.25) * 0.45

# master: tame lows, soft clip, fade out by 15.0
music = hp(music, 32, 2)
music = music - 0.5 * lp(music, 90, 2) + 0.35 * bp(music, 2200, 7000, 2) + 0.05 * hp(music, 9000, 2)
music = lp(music, 16500, 2)
music = np.tanh(music * 1.2) / 1.2
t = np.arange(N) / SR
music *= np.clip((DUR - t) / 1.4, 0, 1) ** 1.5                            # tail rings out, silent at 15.0
music *= np.clip(t / 0.02, 0, 1)

meter = pyln.Meter(SR)
loud = meter.integrated_loudness(music.T)
music = pyln.normalize.loudness(music.T, loud, -16.0).T                   # a bed under the picture
peak = np.abs(music).max()
if peak > 0.89: music *= 0.89 / peak                                      # about -1 dBFS
print(f"integrated LUFS before norm {loud:.1f}; final peak {20*np.log10(np.abs(music).max()):.1f} dBFS; LUFS {meter.integrated_loudness(music.T):.1f}")

pcm = (np.clip(music, -1, 1).T * 32767).astype('<i2')
with wave.open('sg-ad-music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote sg-ad-music.wav', pcm.shape[0] / SR, 's')
