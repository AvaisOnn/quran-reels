# HANDOFF — Quran Reels Instagram automation

**Project folder:** `/Users/apple/quran-reels`
**Goal:** Faceless Islamic IG page that auto-posts the whole Quran as Reels,
in order, 3×/day (~604 Mushaf pages ≈ 200 days). Reciter: **Sheikh Yasser
Al-Dosari**. Arabic only, no English, **no music** (halal). Audience first,
monetize later (donations / halal sponsors / digital product).

---

## 🟢 LIVE as of 2026-05-22

Fully automated and posting. Repo: **github.com/AvaisOnn/quran-reels** (public).
First reel (page 1, Al-Fatihah) posted to **@thepathtonoor2026**. Cron runs 3×/day.
Both Action secrets set: `IG_USER_ID`=17841431955731562, `IG_ACCESS_TOKEN` (long-lived,
expires ~2026-07-21 — re-set before then via `gh secret set IG_ACCESS_TOKEN` in a real
Terminal, NOT the Claude `!` prompt, which sets an empty value).

## STATUS — what's DONE ✅

- **Reel generator** works end-to-end and is verified on macOS:
  Arabic + full tashkeel, Al-Dosari per-ayah audio, calm NASA galaxy/nature
  backgrounds with slow Ken Burns zoom, dark scrim for legibility, one
  background per reel.
- **Batch + bookmark**: `make_next.py` generates the next N pages and advances
  `progress.json`. Currently reset to **page 1** (fresh start).
- **Captions**: auto-generated with surah range + hashtags (`output/page_XXX.txt`).
- **Instagram publisher** (`post_to_instagram.py`) via Graph API — built.
- **GitHub Actions workflow** (`.github/workflows/post.yml`) — cron 3×/day,
  generates → uploads to a public GitHub Release → posts → commits bookmark.
- **Cross-platform fonts**: uses Amiri Quran + HarfBuzz (raqm) on Linux/CI,
  GeezaPro + arabic_reshaper on macOS. (macOS verified; **CI path not yet
  tested live** — verify on first workflow run.)

## STATUS — what's NOT done / TODO ⏳

1. **Accounts (Avas is doing this):**
   - [x] Facebook Page created — **"The Path of Noor"** (Page ID `1190981554088688`).
   - [x] Instagram account created (**@thepathtonoor2026**) + Creator + linked to the Page.
   - [x] Meta Developer app created ("Path Of Noor Poster") + 5 IG/pages scopes.
   - [x] **`IG_USER_ID` = `17841431955731562`** (from me/accounts → instagram_business_account).
   - [ ] Exchange short token → **long-lived `IG_ACCESS_TOKEN`** (~60 days), then it
         goes into GitHub Action secrets (never into chat/repo).
2. **Push to GitHub** (PUBLIC repo so IG can fetch the released video) + add
   `IG_USER_ID` and `IG_ACCESS_TOKEN` as Action secrets. (Steps in `SETUP.md` Part C.)
3. **First live test**: Actions tab → "Post Quran Reel" → Run workflow. This is
   where we confirm the Ubuntu font rendering is correct.
4. **Open tuning items (not blockers):**
   - Long pages → long reels (e.g. Al-Baqarah ~160s). Optionally cap at ~90s by
     splitting long pages into 2 reels.
   - Auto token-refresh so the ~60-day token never has to be re-pasted manually.

---

## RESUME HERE TOMORROW

**If the accounts/token are ready** → do GitHub push + secrets (`SETUP.md` Part C),
then run the workflow once and check the posted reel.

**If still working on the Meta app** → finish `SETUP.md` Part B; the tricky bits:
get `IG_USER_ID` via `me/accounts` → `{page-id}?fields=instagram_business_account`,
then exchange the short token for a long-lived one.

**To preview/generate locally meanwhile:**
```
cd ~/quran-reels
./venv/bin/python make_next.py 3      # next 3 reels -> output/page_XXX.mp4 (+ .txt)
cat progress.json                     # current page (of 604)
open output/page_001.mp4              # preview
```
> Note: `make_next.py` advances `progress.json`. If you only want to *preview*
> without burning the bookmark, reset it after: `echo '{"next_page": 1}' > progress.json`

## KEY FILES
- `quran_reel.py`     — core builder (text render, audio, ffmpeg, captions)
- `make_next.py`      — batch + bookmark
- `post_to_instagram.py` — Graph API publisher
- `.github/workflows/post.yml` — the 3×/day automation
- `SETUP.md`          — full account + token + GitHub checklist
- `progress.json`     — bookmark (next page to post)
- `backgrounds/`      — NASA galaxy + nature images (committed, used by CI)
- `fonts/`            — Amiri Quran (for CI HarfBuzz path)
- `venv/`, `tmp/`, `output/` — gitignored

## DECISIONS LOCKED
- Reciter: Yasser Al-Dosari (`everyayah.com/data/Yasser_Ad-Dussary_128kbps/SSSAAA.mp3`)
- Arabic text: alquran.cloud `quran-uthmani`
- Chunking: one Mushaf page per reel (604 total)
- Runner: GitHub Actions; backgrounds = one per reel (calmer)
- Halal: no music; can't charge for recitation, but view/ad income on da'wah is OK.
