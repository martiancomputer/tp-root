# Vendor disclosure and retest

## Current record

- **Vendor:** TP-Link PSIRT
- **Issue:** command injection in the authenticated DNS-over-HTTPS verification path, resulting in root command execution
- **Access required:** LAN-side management access and the router administrator password
- **Tested hardware:** Archer AX10 V3, product version 3.0.0
- **Most recent confirmed vulnerable firmware in the supplied evidence:** `1.3.3 Build 20260616 rel.46516`
- **Earlier confirmed vulnerable firmware:** `1.3.2 Build 20251125 rel.69127`
- **Vendor-requested retest:** 2 October 2026
- **Patch status:** not established by the evidence provided
- **CVE:** none claimed in this repository

## Timeline

| Date | Event |
| --- | --- |
| Before 2 October 2026 | Research identified authenticated command execution on AX10 V3. |
| 2 October 2026 | Vendor-requested retest compared `1.3.2 Build 20251125` against `1.3.3 Build 20260616`. |
| 2 October 2026 | Reproduction on 1.3.3 confirmed delayed command execution and a root shell on the lab unit. |

The supplied report states that PSIRT requested a retest and cited `1.2.2 Build 20250812`; that image **was not** the image on the tested unit. Do not list 1.2.2 as tested or infer it was fixed.

The report's logged `1.10.2` identifier belongs to the **web UI bundle**, not to `soft_ver`.

## Public disclosure gate

This repository is prepared as a **private release candidate**. Before making it public, confirm coordination with the vendor, release timing, any advisory/CVE reference, existence of a verified fix, and a final secret/PII scan. No claim of vendor endorsement or resolution is made.
