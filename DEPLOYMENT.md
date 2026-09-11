# Deployment Guide: Divine Collection by Verma Jewellers

This repository is optimized for zero-configuration, production-grade deployment across all major modern static hosting and CDN platforms.

---

## Supported Hosting Platforms

### 1. Vercel (Recommended)
1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Deploy production ready Divine Collection"
   git push origin main
   ```
2. In the [Vercel Dashboard](https://vercel.com/new), select **Import Project** and select your GitHub repository.
3. Keep default settings:
   - **Framework Preset**: Other
   - **Build Command**: `npm run build`
   - **Output Directory**: `./` (leave blank)
4. Click **Deploy**.
5. *Clean URLs and path rewrites (`/products/:handle` -> `product.html?id=:handle`) are handled automatically by `vercel.json`.*

---

### 2. Netlify
1. Push to your GitHub repository.
2. Log into [Netlify](https://app.netlify.com/) and choose **Add new site** > **Import an existing project**.
3. Settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `.`
4. Click **Deploy site**.
5. *The included `_redirects` and `_headers` files configure clean product routing and 1-year immutable caching for `/images/*` automatically.*

---

### 3. GitHub Pages
1. Push the repository to GitHub:
   ```bash
   git push origin main
   ```
2. Go to your repository on GitHub: **Settings** > **Pages**.
3. Under **Build and deployment**:
   - **Source**: Deploy from a branch
   - **Branch**: `main` / `root`
4. Click **Save**.
5. *Direct navigation to `/products/<handle>/` works seamlessly thanks to the pre-rendered static route directories and our smart `404.html` fallback.*

---

### 4. Cloudflare Pages
1. In the [Cloudflare Dashboard](https://dash.cloudflare.com/), go to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
2. Select your repository.
3. Build Settings:
   - **Build command**: `npm run build`
   - **Build output directory**: `/`
4. Click **Save and Deploy**.

---

### 5. Traditional Server (Apache / Nginx / S3 / Caddy)
Simply serve the root folder of this repository. All paths, scripts, and stylesheets are relative and self-contained.

For local preview:
```bash
npm run dev
# or
python3 -m http.server 8000
```
Then visit `http://localhost:8000/`.

---

## Pre-Deployment Verification

Before deploying, you can run the automated deployment audit:
```bash
npm run build
```
This tests:
- File size compliance across all repository assets.
- 100% case-sensitive path resolution for Linux production servers.
- Product catalog schema, images, and 96 fallback route files.
- Configuration files (`vercel.json`, `_redirects`, `_headers`, `404.html`).
- Navigational links and zero hardcoded localhost references.
