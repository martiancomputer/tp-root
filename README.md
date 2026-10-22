# tp-root

**Authenticated root command injection on TP-Link Archer AX10 V3 (AX1500-class router).**

The DNS-over-HTTPS server verification path in the router's management backend passes an unsanitized value to a shell command. With an authenticated management session, this allows commands to execute with root privileges.

**Requirements:** access to the router's management interface from the LAN and the router administrator password. This is not an unauthenticated exploit. WAN-side reachability has not been established.

## Affected / rootable devices

| Device | Hardware revision | Firmware (`soft_ver`) | Root access | Evidence |
| --- | --- | --- | --- | --- |
| TP-Link Archer AX10 (AX1500 class) | V3 / `product_ver:3.0.0` | **1.3.2 Build 20251125 rel.69127** | **Confirmed** | Laboratory test before upgrade |
| TP-Link Archer AX10 (AX1500 class) | V3 / `product_ver:3.0.0` | **1.3.3 Build 20260616 rel.46516** | **Confirmed** | Laboratory retest, 2 October 2026; root UID verified |
| TP-Link Archer AX1500 | V3 (listed in AX10 V3 firmware support list) | Not independently established | **Unverified** | Firmware support-list entry only |

Only the **Archer AX10 V3** has been independently tested. A shared firmware support-list entry is not proof that a separately marketed AX1500 unit is rootable.

See [AFFECTED_DEVICES.md](AFFECTED_DEVICES.md) for evidence boundaries and version details.

## Technical evidence

The [AX10 V3 retest report](docs/AX10_V3_retest_1.3.3_redacted.pdf) records authenticated command execution as root on `1.3.3 Build 20260616 rel.46516`, including `uid=0(root) gid=0(root)`. The previous `1.3.2 Build 20251125 rel.69127` result is recorded for comparison.

The `AX10v3_1.10.2_...` string identifies the **web UI bundle**, not the firmware version. The firmware version is given by `soft_ver`. No fixed firmware version has been independently confirmed by these tests.

## Repository contents

- `exploit/ax1500_doh_rce.py` — authenticated proof of concept and timing-based check.
- `exploit/ax1500_doh_rce_auto.py` — optional automated proof of concept.
- `exploit/requirements.txt` — Python dependency specification.
- `tools/tplink_session.py` — authenticated router management-session helper.
- `docs/AX10_V3_retest_1.3.3_redacted.pdf` — laboratory retest evidence.
- `SECURITY.md` — testing scope and reporting guidance.
