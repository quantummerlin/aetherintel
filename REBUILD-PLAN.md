# ÆTHER INTEL — Full Rebuild Plan

> **Domain:** aetherintel.au (to be registered)
> **Live site:** ai.quantummerlin.com (current)
> **GitHub:** github.com/quantummerlin/aetherintel
> **Owner:** Quantum Merlin (Wayne)

---

## Executive Summary

The current site is a well-designed single-page AI news/blog with ~140+ articles. The code is clean, the design is solid (dark theme, indigo/neon palette), but it has structural issues that limit growth. This plan addresses everything — from quick wins to the full aetherintel.au migration.

**Priority order:**
1. Fix what's broken (conflicting claims about tracking, no dates, no pagination)
2. Add what's missing (category filter, email capture, search, publish dates)
3. Migrate to aetherintel.au with proper CI/CD
4. Add newsletter functionality

---

## Audit Findings

### What's Good
- Dark theme with consistent neon indigo palette — works well for AI/tech audience
- Strong CSS architecture (3932 lines, well-organized with custom properties)
- Good font choices: Orbitron + Space Grotesk + Sora
- Hero slideshow with touch swipe support
- Article cards with hover effects and badges
- SEO basics covered: OG tags, Twitter cards, canonical URLs, meta descriptions
- Accessibility: aria-live, aria-label, reduced-motion support
- Lazy loading on images, preconnect for fonts, preload for LCP

### What Needs Fixing

#### 1. Conflicting Identity
- **Problem:** Meta description says "no tracking" but Google Analytics + AdSense are hardcoded
- **Fix:** Remove both. The site doesn't need them yet. Add them later if ad revenue becomes a goal.
- **Files:** `index.html` inline `<script>` tags (lines 27-30 of live HTML)

#### 2. No Publish Dates
- **Problem:** Article cards show no date. Readers can't tell if content is fresh or stale.
- **Fix:** Add `article:published_time` meta from article pages → render as a date on each card
- **Format:** "Jun 12" or "3 days ago" — relative dates for recent, absolute for older
- **Files:** Article HTML templates, CSS for date styling, card markup

#### 3. No Pagination or Category Filter
- **Problem:** 140+ articles on one infinite scroll page. No way to filter by topic.
- **Fix:** Add category filter bar above the grid (All | Agents | Safety | Tools | Business | Culture | Work)
- **Fix:** Add pagination or "Load More" — 12 per page, progressive enhancement with JS
- **Files:** index.html, main.js, style.css

#### 4. "LIVE INTELLIGENCE" Bar Is Misleading
- **Problem:** Says "LIVE" but it's just a hero slideshow. Not real-time.
- **Fix:** Rename to "FEATURED" or "TOP STORIES". Remove pulsing dot.
- **Files:** index.html line 134-137

#### 5. No Email Capture / Newsletter CTA
- **Problem:** Building an audience but no way to capture emails.
- **Fix:** Add a simple email signup section between the hero and article grid
- **Fix:** Add footer signup with Mailchimp/ConvertKit embed (or simple form→webhook)
- **Files:** index.html, style.css

#### 6. Article Title Formula Fatigue
- **Problem:** Nearly every title follows "X Happened. Here Is Why" pattern
- **Fix:** Not a code fix — editorial guideline. Vary structures:
  - Direct: "Microsoft Stopped Being a Software Company"
  - Question: "Can Two People With Disrupt Your Business in 90 Days?"
  - List: "The 4 Security Holes in Every AI Agent Workflow"
  - Statement: "AI Is Getting Dumber"

#### 7. No Search
- **Problem:** 140+ articles and no way to search
- **Fix:** Add a client-side search index (JSON) + search bar in topbar
- **Files:** `js/search.js`, `data/search-index.json`, topbar markup, style.css

#### 8. Repo Structure
- **Problem:** GitHub repo has 140 articles but no `index.html` at root — the live site is a separate file
- **Fix:** Rebuild the repo as the single source of truth with a proper index.html
- **Fix:** Set up GitHub Actions to deploy to GitHub Pages (or push to Cloudflare Pages)

---

## Implementation Plan

### Phase 1: Quick Wins (Can Do Today)
**Goal: Fix the most visible issues on the existing site**

1. Remove Google Analytics and AdSense scripts
2. Change "LIVE INTELLIGENCE" → "FEATURED"
3. Add publish dates to article cards (read from `article:published_time` meta)
4. Add category filter bar (All, Agents, Safety, Tools, Business, Culture, Work)
5. Add a simple email signup form in the hero area

### Phase 2: Structural Improvements (This Week)
**Goal: Make the site usable at scale**

6. Pagination / "Load More" — 12 articles per page
7. Client-side search (builds index from article card data)
8. Footer with email signup, social links, copyright, sitemap link
4. Clean up article card markup — some cards use `<span class="badge">`, others use `<div class="article-card-cat">`. Standardize.
5. Add `rel="noopener"` on any external links

### Phase 3: Newsletter System
**Goal: Build an audience**

6. Set up email service (recommendation: Buttondown, free up to 1000 subs)
7. Add inline signup form (email only, no name required — less friction)
8. Create a weekly digest template
9. Connect form to service via their embed or API webhook

### Phase 4: Domain Migration
**Goal: Move to aetherintel.au**

10. Register aetherintel.au
11. Set up Cloudflare in front (you already have the zone patterns)
12. Update all canonical URLs from `ai.quantummerlin.com` → `aetherintel.au`
13. Set up GitHub Actions workflow for CI/CD
14. Configure DNS: Cloudflare CNAME → GitHub Pages (or direct to Cloudflare Pages)
15. Set up 301 redirects from old domain
16. Update OG tags, Twitter cards, manifest.json

---

## File-by-File: What Changes Where

### `index.html` (root)
- [ ] Remove GA + AdSense inline scripts
- [ ] Rename "LIVE INTELLIGENCE" → "FEATURED"
- [ ] Add category filter bar (after hero, before article grid)
- [ ] Add email signup section (after hero)
- [ ] Add publish dates to article cards
- [ ] Standardize card markup (badge → article-card-cat)
- [ ] Add search input in topbar
- [ ] Add footer with signup + links + social
- [ ] Add pagination / Load More button

### `css/style.css`
- [ ] New: category filter chip styles
- [ ] New: email signup section styles
- [ ] New: search bar styles
- [ ] New: publish date styling on cards
- [ ] New: pagination / Load More button styles
- [ ] New: footer styles (if not already defined)
- [ ] Fix: standardize badge vs card-cat classes

### `js/main.js`
- [ ] New: category filter logic
- [ ] New: pagination / Load More
- [ ] New: client-side search
- [ ] New: email form handling
- [ ] Fix: date formatting (relative dates)

### `data/search-index.json` (new)
- [ ] Auto-generated from article metadata (title, URL, category, date, excerpt)

### `.github/workflows/deploy.yml` (new)
- [ ] GitHub Actions workflow for deploying to GitHub Pages or Cloudflare Pages

### `footer.js`
- [ ] Update canonical URLs
- [ ] Add social links
- [ ] Add newsletter form embed

---

## DNS / Deployment Architecture

```
aetherintel.au (Cloudflare)
  ├── GitHub Pages (origin) — or — Cloudflare Pages
  ├── CDN: Cloudflare edge cache
  ├── DNS: Cloudflare nameservers
  ├── Redirect: ai.quantummerlin.com → aetherintel.au (301)
  └── Email: Cloudflare Email Routing → your inbox
```

---

## Estimated Effort

| Phase | Tasks | Time |
|-------|-------|------|
| 1 - Quick Wins | 5 fixes | 2-3 hours |
| 2 - Structural | 6 improvements | 4-6 hours |
| 3 - Newsletter | 4 items | 2-3 hours |
| 4 - Migration | 6 items | 3-4 hours |
| **Total** | **21 items** | **~12-16 hours** |

---

## Notes

- Do NOT add React/Vanilla JS frameworks. Keep it static HTML + vanilla JS.
- Continue using Cloudflare for DNS + CDN (you already have the setup)
- Keep the design language — it's good. Only add, don't redesign.
- Domain cost: ~AUD $20/year for .au via Cloudflare Registrar or VentraIP
- Newsletter: Buttondown free tier → convertkit free tier → Mailchimp for growth
