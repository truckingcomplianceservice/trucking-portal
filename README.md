# Trucking Compliance Services — Operations Portal (COMPLETE)

Fix: document popup now shows IMAGES (JPG/PNG/photos) and PDFs correctly.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
The "View" popup showed a broken-document icon for image files (photos of
documents, JPG/PNG). The popup now detects the file type:
- Images (jpg/jpeg/png/gif/webp/heic/tiff...) show as a picture.
- PDFs and everything else show in the frame as before.
- "Open in new tab" still available.
Applied to Company documents, Truck documents, and Load documents viewers.

## Includes everything to date
Smart doc viewer, company docs, company logins, FMCSA lookup, multi-stop import,
fuel + expense receipts, load docs, truck docs, hide load $, pay basis, rentals.
