# FogMonitor on Cloudflare Pages

FogMonitor is a **Windows desktop application** (Python/Tkinter). Cloudflare Pages cannot compile or execute it as a desktop program. This repository now separates the two jobs:

- `public/` is the static marketing/download site deployed by Cloudflare Pages.
- `.github/workflows/windows-release.yml` builds the Windows `.exe` and portable ZIP on a Windows GitHub Actions runner.

## Cloudflare Pages build settings

In Cloudflare Dashboard → Workers & Pages → Create application → Pages → connect this repository, use:

- **Framework preset:** None
- **Root directory:** repository root (leave blank)
- **Build command:** `exit 0` (or leave the command blank for a plain static site)
- **Build output directory:** `public`
- **Environment variables:** none

The important part is that `public/index.html` exists. Do not set `FogMonitor.py`, `Build-EXE.bat`, or `requirements-build.txt` as the Cloudflare build command; those are for the Windows desktop app, not for Pages.

`wrangler.toml` also declares `pages_build_output_dir = "./public"` for deployments using Wrangler.

## Publish the Windows executable

Run `Build-EXE.bat` on Windows, or push the repository to GitHub and use **Actions → Build Windows release**. The workflow has a manual trigger and a release trigger for tags `v*`. It produces `FogMonitor-by-FogLabs-Windows.zip` containing `FogMonitor.exe`, a short readme and the license.

Cloudflare Pages currently hosts the source ZIP so the website is useful without a release URL. After a GitHub Release exists, you can optionally replace the source-download links in `public/index.html` with the URL of the release asset.

## Official Cloudflare guidance

- https://developers.cloudflare.com/pages/configuration/build-configuration/
- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/
