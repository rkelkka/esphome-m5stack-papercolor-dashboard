# M5Stack PaperColor Immich Kiosk Proxy

A lightweight Dockerized HTTP proxy that fetches images from **Immich Kiosk** and converts them on the fly into **600×400, 6-color Floyd-Steinberg dithered PNGs** optimized for the **M5Stack PaperColor** (Spectra 6 e-ink display) running ESPHome.

| Original | Optimized through the proxy |
| :---: | :---: |
| ![Original image](sample/sample_original.png) | ![Optimized image](sample/sample_proxied.png) |

## What It Does

1. **Fetches Images:** Pulls a random photo from your Immich Kiosk `/image` endpoint on each request.
2. **Orients & Crops:** Auto-rotates based on EXIF tags, rotates portrait images 90° clockwise to fill the landscape screen, and center-crops to `600×400`.
3. **Calibrated E-Ink Dithering:** Applies subtle sharpening and tone adjustments, dithers the image using Floyd-Steinberg error diffusion against the physical Spectra 6 pigment colors, and maps the pixels to the pure primary RGB values expected by ESPHome's `epaper_spi` driver.
4. **Serves Lossless PNG:** Returns a crisp 24-bit RGB PNG at `http://<host>:5055/papercolor.png`.

## Quick Start

1. Set your `KIOSK_URL` in `docker-compose.yml` (supports any Immich Kiosk query parameters such as `?album=...`, `?person=...`, or `?layout=landscape`).
2. Build and start the container:
   ```bash
   docker compose up -d --build
   ```
3. Verify it works by opening `http://<server-ip>:5055/papercolor.png` in a browser.

## ESPHome Configuration

Configure `online_image` in your M5Stack PaperColor YAML:

```yaml
image:
  - platform: online_image
    id: my_online_image
    url: "http://<server-ip>:5055/papercolor.png"
    format: PNG
    type: RGB565
    transparency: opaque
```
