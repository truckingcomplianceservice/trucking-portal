# Trucking Compliance Services — Operations Portal (COMPLETE)

Cloud file backup (Cloudflare R2) — activates when you add the R2 keys.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push.

## Cloud file backup — SETUP (do these once)
Uploaded files (documents, PODs, receipts, logos) will be stored in Cloudflare
R2 instead of the Railway disk, so they are safe and permanent.

STEP 1 - Cloudflare account: sign up free at cloudflare.com.
STEP 2 - Turn on R2: dash.cloudflare.com -> R2 -> enable (may ask for a card,
         but the free tier is 10 GB, no charge under that).
STEP 3 - Create a bucket: R2 -> Create bucket -> name it e.g. "trucking-files".
STEP 4 - Create an API token: R2 -> Manage R2 API Tokens -> Create -> "Object
         Read & Write" -> for your bucket. Copy the Access Key ID, Secret Access
         Key, and your account's S3 endpoint URL
         (https://<accountid>.r2.cloudflarestorage.com).
STEP 5 - Add these in Railway -> web service -> Variables -> New Variable:
         R2_ACCESS_KEY_ID       = (Access Key ID)
         R2_SECRET_ACCESS_KEY   = (Secret Access Key)
         R2_BUCKET              = trucking-files
         R2_ENDPOINT            = https://<accountid>.r2.cloudflarestorage.com
         (optional) R2_PUBLIC_URL = public bucket URL if you make one public
         Save -> Railway redeploys automatically.

That's it: from then on, every uploaded file goes to R2 automatically. If the
keys are NOT set, the app keeps using local storage (nothing breaks).

NOTE: files uploaded BEFORE R2 was turned on stay on the old disk; new uploads
go to R2. We can migrate the old files afterward if needed.

## Includes everything to date
R2 cloud backup, manual multi-stop load, truck P&L date fix, test suite,
factoring, doc viewer, company docs, company logins, FMCSA lookup, receipts.
