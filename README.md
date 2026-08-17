# Trucking Compliance Services — Operations Portal (COMPLETE)

Load documents (POD / Rate con / BOL): upload + view right on the load page.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## Truck documents vs Load documents
- TRUCK documents (registration, insurance, inspection) live on the TRUCK page
  (Vehicles -> a truck -> Documents). Popup viewer there.
- LOAD documents (Proof of Delivery, Rate confirmation, Bill of Lading) live on
  the LOAD page (Dispatch -> a load). These are per-trip proof.

## New on the LOAD page (Files section)
- See POD / Rate con / BOL with a "View" that opens in a POPUP over the page
  (close with X or Esc, "Open in new tab" also available).
- Upload them right there: pick the type (POD / Rate con / BOL), choose the file,
  click Upload. No more going into Admin to edit the load.

## Includes everything to date
Load doc upload+viewer, truck doc popup viewer, custom category, CSV load import,
hide load $, pay basis, rental contracts, settlement tools, pay history.
