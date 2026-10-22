# tp-axploit

**Authenticated command injection affecting TP-Link Archer AX10 V3 (AX1500 product family).**

The vulnerable DNS-over-HTTPS verification path in the router's web management backend can execute a supplied shell command with root privileges. This issue was reproduced on a laboratory **Archer AX10 V3** after an administrator authenticated through the router's management interface.

**Prerequisites:** LAN-side access to the router management interface **and the administrator password**. This is **not** evidence of an unauthenticated, internet-facing exploit. No other router models or hardware revisions have been confirmed rootable by this research.

## Affected / rootable devices

| Device | Hardware revision | Firmware (`soft_ver`) | Root execution confirmed? | Evidence |
| --- | --- | --- | --- | --- |
| TP-Link Archer AX10 (AX1500 class) | V3 / `product_ver:3.0.0` | **1.3.2 Build 20251125 rel.69127** | **Yes** — tested | Before-upgrade result in the 2 Oct 2026 retest |
| TP-Link Archer AX10 (AX1500 class) | V3 / `product_ver:3.0.0` | **1.3.3 Build 20260616 rel.46516** | **Yes** — tested | Vendor-requested retest, 2 Oct 2026: 9.0 s detection and `uid=0(root)` |
| TP-Link Archer AX1500 | V3 (appears in AX10 V3 firmware support list) | **Not independently established** | **Unverified** | Firmware support-list entry only; not an independent device test |

**Important:** `AX10v3_1.10.2_...` is the **web UI bundle identifier**, **not** the installed firmware version. Use `soft_ver` when reporting affected versions. Being listed in a firmware support list is not proof that a separately marketed AX1500 unit is exploitable.

See [AFFECTED_DEVICES.md](AFFECTED_DEVICES.md) for the evidence limits and [DISCLOSURE.md](DISCLOSURE.md) for the timeline.

## Evidence

- [Vendor-requested AX10 V3 retest (2 Oct 2026)](docs/AX10_V3_retest_1.3.3_redacted.pdf) — supplied report; identifying host/network fields redacted and PDF metadata cleared.
- The lab report documents post-authentication command execution as root on `1.3.3 Build 20260616 rel.46516`, with the preceding 1.3.2 result recorded for comparison.
- A patched or unaffected version has **not** been confirmed by this report. Do not treat versions absent from the table as safe.

## Project layout

- `exploit/`: existing proof-of-concept scripts, preserved from the original research repository; documentation version labels corrected.
- `tools/tplink_session.py`: auxiliary authenticated-session helper, with machine-specific default address removed.
- `SECURITY.md`: responsible-use guidance and operational limitations.

The privacy-bearing demonstration video and all external demo links have been removed. The one-off output-callback helper containing local machine paths and addresses is excluded from this release candidate.

## Disclosure and responsible use

The issue was reported to TP-Link PSIRT, which requested a retest. The retest was completed on **2 October 2026**. This private release candidate is **not** a statement that a fix has shipped, that the vendor has completed its review, or that public disclosure has been coordinated.

Only operate the code against hardware you own or have explicit authorization to test. Avoid exposing the router management interface to untrusted LAN users. Maintain a strong administrator password and install vendor security updates once a fix is verified.

There is no demonstration video in this release; do not reintroduce source-host identifiers or session tokens to documentation or issues.
