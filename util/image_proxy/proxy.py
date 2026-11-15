from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import subprocess
import urllib.request

KIOSK_URL = os.environ.get("KIOSK_URL", "http://immich-kiosk:3000/image")
CALIBRATED_PALETTE = "/app/spectra6_calibrated.png"

class PaperColorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/papercolor.png"):
            try:
                # 1. Fetch image from Immich Kiosk
                req = urllib.request.urlopen(KIOSK_URL, timeout=15)
                raw_bytes = req.read()

                # 2. Resize, sharpen, dither to measured Spectra 6 pigments, and map to driver primaries
                cmd = [
                    "magick", "-",
                    "-auto-orient",
                    "-rotate", "90<",
                    "-resize", "600x400^",
                    "-gravity", "center",
                    "-extent", "600x400",
                    "-sigmoidal-contrast", "3,45%",  # Lifts dark shadows while boosting midtone punch
                    "-modulate", "105,125,100",       # +5% brightness, +25% saturation
                    "-unsharp", "0x1+0.8+0",          # Restores edge crispness after downscaling
                    "-dither", "FloydSteinberg",
                    "-remap", CALIBRATED_PALETTE,
                    "PNG24:-"
                ]
                # Brighter, more saturated option.
#
#                cmd = [
#                    "magick", "-",
#                    "-auto-orient",
#                    "-rotate", "90<",
#                    "-resize", "600x400^",
#                    "-gravity", "center",
#                    "-extent", "600x400",
#                    "-modulate", "100,95,100",
#                    "-unsharp", "0x1+0.4+0",
#                    "-depth", "8",
#                    "-colorspace", "RGB",
#                    "-dither", "FloydSteinberg",
#                    "-remap", CALIBRATED_PALETTE,
#                    "-colorspace", "sRGB",
#                    "-depth", "8",
#                    "-fill", "#000001", "-opaque", "#191E21",
#                    "-fill", "#FFFFFE", "-opaque", "#E8E8E8",
#                    "-fill", "#0000FE", "-opaque", "#2157BA",
#                    "-fill", "#00FE00", "-opaque", "#125F20",
#                    "-fill", "#FE0000", "-opaque", "#B21318",
#                    "-fill", "#FFFE00", "-opaque", "#EFDE44",
#                    "-level", "1%,99%",
#                    "PNG24:-"
#                ]
#
                proc = subprocess.run(cmd, input=raw_bytes, capture_output=True, check=True)

                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(proc.stdout)))
                self.end_headers()
                self.wfile.write(proc.stdout)
                print("Served calibrated image from Immich Kiosk", flush=True)
            except Exception as e:
                print(f"Error: {e}", flush=True)
                self.send_response(502)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print(f"Serving calibrated PaperColor proxy on port 5055 -> {KIOSK_URL}", flush=True)
    HTTPServer(("0.0.0.0", 5055), PaperColorHandler).serve_forever()
