# Trucking Compliance Services — Operations Portal

Now with a full Driver Qualification File (DQF) workflow, team management, and
the whole TMS (operations, hiring, compliance, factoring, tax, brokers, fuel).

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents (including operations/static/logo.png).
3. Commit. Railway redeploys automatically.

## New: Driver Qualification File (DQF) — like a DQF portal

### Per-driver DQF file  (Drivers -> a driver -> "DQF file")
- A checklist of the FMCSA-style required documents (CDL, application, medical,
  MVR, annual review, road test, PSP, drug test, Clearinghouse, safety history),
  each with a **red / yellow / green** status:
  - Green = complete, Yellow = pending review or expiring soon, Red = missing or expired.
- A progress bar and an overall badge: **Qualified / Attention / Action needed**.
- The Drivers list shows each driver's DQF status at a glance.

### Drivers upload their own documents, you approve
- Each driver has a **private upload link** (shown on their DQF page, with a Copy
  button). Send it by text/email.
- The driver opens it on their phone, sees their checklist, and uploads documents
  (medical card, MVR, etc.) — **no login**.
- Uploads arrive as **Pending review**. You **Approve** or **Reject** them from the
  DQF page with one click. Approved items turn green and start expiry tracking.

## Not included (would need extra services)
DOT-style AI license scanning (OCR auto-fill), e-signatures, and built-in MVR/PSP
ordering require third-party AI/e-sign/screening providers + credentials. The
manual upload + approve workflow above covers the core DQF process today.
