# Affected and rootable devices

This table deliberately distinguishes **verified root execution** from **potential model compatibility**.

| TP-Link router | Hardware / region evidence | Firmware (actual `soft_ver`) | Status | Confidence |
| --- | --- | --- | --- | --- |
| Archer AX10, AX1500-class router | V3 / product version 3.0.0 / laboratory device reports country `US` | `1.3.2 Build 20251125 rel.69127` | Root execution verified before upgrade | Confirmed for tested AX10 V3 |
| Archer AX10, AX1500-class router | V3 / product version 3.0.0 / laboratory device reports country `US` | `1.3.3 Build 20260616 rel.46516` | Root execution verified on retest | Confirmed for tested AX10 V3 |
| Archer AX1500, separate product label | V3 listed in AX10 V3 firmware support-list | Not independently measured | Suspected compatibility; **rootability unverified** | Insufficient evidence for a confirmed vulnerability claim |

Only **AX10 and AX1500** are in scope here. The report's support-list also mentions other names, but they are intentionally **not** included because this investigation has not demonstrated the vulnerability on them.

## Evidence and terminology

The laboratory retest on 2 October 2026 found:

- Before upgrade: AX10 V3, `soft_ver:1.3.2 Build 20251125 rel.69127`, root ash via a laboratory session; the detection request took 5.3 seconds for a five-second delay.
- After upgrade: same AX10 V3, `soft_ver:1.3.3 Build 20260616 rel.46516`; the detection request took 9.0 seconds and the resulting shell reported `uid=0(root) gid=0(root)`.
- The device identified itself as `product_name:Archer AX10`, `product_ver:3.0.0`, `hw_ver:00000003`, country `US`.
- Its firmware support list included `Archer AX1500` V3. That **does not** prove a physically distinct AX1500 SKU or different region is vulnerable.
- The HTML/UI metadata string `AX10v3_1.10.2_...` is not the firmware `soft_ver`. This identifier is not an installed firmware version.

**Not established:** earliest affected version, full affected-version range, whether 1.2.2 is vulnerable, other hardware revisions, other countries/OEM builds, currently fixed firmware, WAN reachability, or unauthenticated exploitation.

Source: laboratory report `docs/AX10_V3_retest_1.3.3_redacted.pdf`, 2 October 2026.
