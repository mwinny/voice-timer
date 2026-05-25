# Voice Timer

A browser-based timer controlled by voice. Say:

- **"go"** to start (or resume)
- **"stop"** to pause
- **"finish"** to end the run and log it to history

## Local development

The Web Speech API needs `localhost` or HTTPS — opening the file directly will not give the page mic access. From this directory:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000> in **Chrome, Edge, or Safari**. Manual buttons are provided as a fallback for testing without voice.

**Browser support note:** Brave ships without the Google speech API key, so voice commands return `network` errors on Brave. Use Chrome, Edge, or Safari instead.

## Install on iPhone / Android (PWA)

The app is a Progressive Web App, so it installs to your home screen with no App Store. You just need to host it on HTTPS — once.

### 1. Deploy to a free static host

Pick whichever is easiest:

- **GitHub Pages** — push this directory to a repo, then in GitHub: Settings → Pages → Source = `main` branch root. URL: `https://<user>.github.io/<repo>/`.
- **Cloudflare Pages** — <https://dash.cloudflare.com/?to=/:account/pages> → "Direct Upload" → drag this folder. Instant HTTPS URL.
- **Vercel** / **Netlify** — `npx vercel` or drag-drop at netlify.com/drop. Same deal.

### 2. Install on iPhone

1. Open the HTTPS URL in **Safari** (not Chrome — only Safari can install PWAs on iOS).
2. Tap the **Share** button → **Add to Home Screen** → **Add**.
3. Launch the new icon. Grant microphone permission the first time.

### 3. Install on Android

1. Open the URL in **Chrome**.
2. Chrome will offer "Install app" automatically, or use ⋮ menu → **Install app** / **Add to Home Screen**.
3. Launch and grant mic permission.

## Workout caveats (iOS)

- **Screen stays on automatically while running.** The app requests a screen wake lock (`navigator.wakeLock`) when you say (or tap) Go, and releases it on Finish. Requires iOS 16.4+ (any iPhone updated in the last ~3 years).
- **Background ≠ supported.** When you switch apps or the screen turns off, recognition stops. Web Speech can't run in the background on iOS. Only a native Swift app could.
- **iOS uses Apple's on-device recognition.** No internet required for the voice commands themselves on iPhone — just for the initial page load.

## Files

- `index.html` — the entire app (markup, styles, script inline).
- `manifest.json` — PWA metadata (name, icons, theme color).
- `icon-180.png` / `icon-192.png` / `icon-512.png` — generated icons.
- `generate_icons.py` — regenerates the icons if you want to change colors or shape. `python3 generate_icons.py`.
