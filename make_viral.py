#!/usr/bin/env python3
"""
Generate the next reel from the curated list in viral_verses.json, advancing
a persistent bookmark. Loops back to the start when the list is exhausted.

Usage: python make_viral.py
Outputs: output/reel.mp4 + output/reel.txt (caption)
State:   progress.json  -> {"next_viral": i, ...}
"""
import os, json
import quran_reel as qr

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRESS = os.path.join(HERE, "progress.json")
VERSES = os.path.join(HERE, "viral_verses.json")
OUT = os.path.join(HERE, "output")

def main():
    os.makedirs(OUT, exist_ok=True)
    verses = json.load(open(VERSES))
    state = json.load(open(PROGRESS)) if os.path.exists(PROGRESS) else {}
    i = state.get("next_viral", 0) % len(verses)
    ref = verses[i]
    print(f"== Verse {i + 1}/{len(verses)}: {ref} ==", flush=True)
    ayahs = qr.fetch_verses(ref)
    mp4 = os.path.join(OUT, "reel.mp4")
    qr.build_reel(ayahs, mp4, bg_seed=i)
    open(os.path.join(OUT, "reel.txt"), "w").write(qr.build_viral_caption(ayahs))
    state["next_viral"] = i + 1
    json.dump(state, open(PROGRESS, "w"), indent=2)
    print(f"   -> {mp4}\nNext run: entry {(i + 1) % len(verses) + 1}.")

if __name__ == "__main__":
    main()
