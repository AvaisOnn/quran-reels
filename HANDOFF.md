# HANDOFF — Quran Reels Instagram automation

**Project folder:** `/Users/apple/quran-reels` (new MacBook, user `apple`)
**Goal:** Faceless Islamic IG page that auto-posts Quran reels 4×/day. Reciter:
**Sheikh Yasser Al-Dosari**. **No music** (halal). Audience first, monetize later
(donations / halal sponsors / digital product).

**Phase 1 (done 2026-10-23):** the whole Quran, page by page (pages 1–604).
**Phase 2 (live since 2026-10-26):** curated **viral verses**, Arabic + English.

---

## 🟢 LIVE — READ THIS FIRST (last updated 2026-10-26)

**The pipeline is built, deployed, and auto-posting. Nothing is required to keep it
running.** Resume only if Avais asks for a change or something broke.

- **Repo (public):** github.com/AvaisOnn/quran-reels
- **Instagram:** @thepathtonoor2026 · **FB Page:** "The Path of Noor" (ID 1190981554088688)
- **Mode:** each run posts the next entry from `viral_verses.json` (177 entries).
  First viral post went live 2026-10-26 (94:5-6, IG media id `18090272759268422`).
  Bookmark `progress.json` → `next_viral` = **1** (i.e. 39:53 is next).
  The list loops back to the start after the last entry (~44 days at 4×/day).
- **Schedule:** 4×/day every 6h at **12 AM / 6 AM / 12 PM / 6 PM Pakistan time** =
  `19:00 / 01:00 / 07:00 / 13:00 UTC` (cron in `.github/workflows/post.yml`).
  Manual run: `gh workflow run post.yml -R AvaisOnn/quran-reels` (posts publicly!).
- **Action secrets (in GitHub, encrypted — NOT in repo):** `IG_USER_ID`
  (`17841431955731562`, not sensitive), `IG_ACCESS_TOKEN`, `FB_PAGE_ID`.

### What a reel looks like (viral mode)
- One reel per entry; one clip per ayah, all on one background (galaxy/nature,
  slow Ken Burns zoom, dark scrim).
- **Arabic** (white, tashkeel) on top, **English — Sahih International** (gold, Lora
  Italic) underneath, `surah:ayah` at the bottom. Text auto-shrinks for long verses
  (Ayat al-Kursi fits).
- Caption: the English translation in quotes, surah name + ref, "save & share" line,
  hashtags (`build_viral_caption` in `quran_reel.py`).
- Basmala is stripped from ayah 1 of a surah (except Al-Fatihah) because the per-ayah
  audio doesn't recite it.

### Editing the verse list
`viral_verses.json` is a plain JSON list of `"surah:ayah"` or `"surah:from-to"`
(e.g. `"94:5-6"`). Posted in file order. Rules used when curating:
- **Whole verses only**, and only where the full verse carries the viral message.
  Dropped for that reason: 65:2 (divorce — kept 65:3), 2:216 (fighting), 2:222
  (menstruation), 12:18, 12:64 — their popular line is only half the verse.
- Keep passages short (1–5 ayahs). Validate new refs with `qr.fetch_verses(ref)`.
- If you insert/remove entries **before** the bookmark index, adjust `next_viral`
  in `progress.json` so nothing is skipped or repeated.

### Token status
- `IG_ACCESS_TOKEN` was set 2026-05-22 and HANDOFF expected expiry ~2026-07-21, but
  **it was still posting fine on 2026-10-26**. Real expiry unknown. If IG posts start
  failing with HTTP 400/190, regenerate it (SETUP.md Part B).
- Set secrets with `gh secret set IG_ACCESS_TOKEN` **in a real Terminal app** — NOT the
  Claude Code `!` prompt (non-interactive → silently stores an EMPTY value).
- 2026-05-24: Avais chose to keep the 60-day user token instead of a permanent Page
  token. Revisit if refreshes become a chore.
- No reminder is armed. (The old `/schedule` reminders were created under *Sana's*
  Claude account, fired to her, and were disabled on 2026-07-07.)

### Facebook cross-posting — still BLOCKED on one scope
Every run's FB step returns **HTTP 403** (`pages_manage_posts` missing). The step is
`continue-on-error`, so it never blocks IG or the bookmark. To enable: regenerate the
token in Graph API Explorer WITH `pages_manage_posts`, exchange to long-lived, then
`gh secret set IG_ACCESS_TOKEN` (real Terminal). `fb_debug.yml` is a no-post scope checker.

### Workflow hardening
- **2026-10-26:** a run hung 15+ min on `apt-get` (stalled Ubuntu mirror); default job
  timeout is 6h. Added `timeout-minutes: 30` on the job, `8` on the ffmpeg install,
  and apt retries/timeouts. A stuck run now fails fast; the next slot posts normally.
- Bookmark push uses `git pull --rebase` so a concurrent push can't desync it.
- `concurrency: post-reel` — never two posts at once.

### Security / hygiene
- Token & App Secret exist ONLY in GitHub encrypted secrets + Avais's local notes.
- `.gitignore` excludes `.claude/`, `CLAUDE.md`, `*.env`, `venv/`, `tmp/`, `output/`,
  `.DS_Store`.
- 2026-05-23: an `fb_debug.yml` run printed a derived Page token to a public log; run
  deleted, script now redacts. Regenerating `IG_ACCESS_TOKEN` invalidates it for good.

---

## TODO / ideas ⏳
1. **Enable Facebook** — regenerate token with `pages_manage_posts` (Avais, later).
2. **Find out the IG token's real expiry** (Graph API `debug_token`) and set a reminder
   under the correct Claude account.
3. Optional: grow `viral_verses.json` before it loops (~2026-12-09), or shuffle themes.
4. Optional: auto token refresh / permanent Page token.

## Preview locally (does NOT post)
```
cd ~/quran-reels
./venv/bin/python -c "import quran_reel as qr; a=qr.fetch_verses('2:255'); qr.build_reel(a,'/tmp/t.mp4',bg_seed=0); print(qr.build_viral_caption(a))"
open /tmp/t.mp4
```
Don't run `make_viral.py` locally unless you mean to — it advances `progress.json`
(only matters if you commit it). macOS has no raqm, so local Arabic uses GeezaPro +
arabic_reshaper and wraps narrower than CI (Amiri Quran + HarfBuzz).

## KEY FILES
- `make_viral.py`        — **current** driver: next entry from `viral_verses.json`
                           → `output/reel.mp4` + `output/reel.txt`, advances `next_viral`
- `viral_verses.json`    — curated verse list (177 entries)
- `quran_reel.py`        — core builder: `fetch_verses` (Arabic + en.sahih via
                           alquran.cloud, 429 back-off), overlay render, audio, ffmpeg,
                           captions
- `make_next.py`         — Phase 1 page-by-page driver (finished; kept for reference)
- `post_to_instagram.py` — IG Graph API publisher
- `post_to_facebook.py`  — FB Page Reels publisher (blocked on `pages_manage_posts`)
- `fb_debug.py` / `.github/workflows/fb-debug.yml` — no-post token/scope checker
- `.github/workflows/post.yml` — 4×/day automation: generate → GitHub Release →
                                  IG → FB → commit bookmark
- `progress.json`        — `next_viral` (live) + `next_page: 605` (Phase 1, done)
- `backgrounds/`         — NASA galaxy + nature images
- `fonts/`               — Amiri Quran (CI Arabic), Lora Italic (English)
- `SETUP.md`             — account + token + GitHub checklist

## DECISIONS LOCKED
- Reciter: Yasser Al-Dosari (`everyayah.com/data/Yasser_Ad-Dussary_128kbps/SSSAAA.mp3`)
- Text: alquran.cloud `quran-uthmani`; translation `en.sahih` (Sahih International)
- Content: curated popular verses, rendered ourselves on our own backgrounds —
  **no scraping or reposting other creators' reels** (IG "unoriginal content"
  penalty + copyright).
- Runner: GitHub Actions; one background per reel.
- Halal: no music; can't charge for recitation, but view/ad income on da'wah is OK.

## HISTORY
- 2026-05-22 → 05-24: pipeline built, IG live, FB wired (blocked), schedule 4×/day.
- 2026-07-07: misrouted token reminders disabled.
- 2026-10-23: Phase 1 complete — page 604 posted (IG media `17947772331074794`).
- 2026-10-23 → 10-26: every run failed (`no matches found for output/page_605.mp4`) —
  nothing left to post.
- 2026-10-26: switched to viral-verse mode (Arabic + English); first post live; workflow
  timeouts added. Repo re-located on the new MacBook at `/Users/apple/quran-reels`.
