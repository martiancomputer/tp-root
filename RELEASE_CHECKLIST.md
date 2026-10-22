# Checklist before making the new repository public

- [x] Create release as a **fresh root commit**, not a fork/mirror that retains the PII video in Git history.
- [x] Remove `demo_mail.mp4` and the public GitHub user-attachment demo URL.
- [x] Exclude old advisory from an unreviewed binary copy; use the uploaded redacted retest instead.
- [x] Exclude `tools/rexfil.py` (hardcoded private host address and home directory).
- [x] Replace the machine-specific default address in `tools/tplink_session.py` with an explicitly configured environment variable.
- [x] Correct `1.10.2` as a UI bundle version, not actual firmware.
- [x] Label AX1500 V3 **unverified**, not confirmed rootable.
- [x] Scrub author metadata from the retest PDF.
- [ ] Confirm the vendor disclosure window and response before making public.
- [ ] Confirm whether a vendor-fixed build exists; add affected/fixed version boundaries if independently verified.
- [ ] Choose and add an explicit project license (if public redistribution is intended).
- [ ] Inspect release commits, GitHub issues, and any uploaded assets for additional PII and secrets.
- [ ] Test CLI/help and lab-only reproduction in a controlled environment.
