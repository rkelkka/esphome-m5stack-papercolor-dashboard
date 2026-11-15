FROM python:3.12-alpine

# Install ImageMagick along with JPEG, WebP, and HEIC format delegates
RUN apk add --no-cache \
    imagemagick \
    imagemagick-jpeg \
    imagemagick-webp \
    imagemagick-heic

WORKDIR /app

# Create the calibrated Spectra 6 palette (actual physical pigment colors on the glass)
RUN magick \
  xc:"#191E21" \
  xc:"#E8E8E8" \
  xc:"#2157BA" \
  xc:"#125F20" \
  xc:"#B21318" \
  xc:"#EFDE44" \
  +append /app/spectra6_calibrated.png

COPY proxy.py /app/proxy.py

EXPOSE 5055
CMD ["python3", "/app/proxy.py"]
