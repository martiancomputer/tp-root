# Security and testing scope

This proof of concept demonstrates an **authenticated, LAN-side** command injection path on the **tested TP-Link Archer AX10 V3** firmware. Reproducing the issue requires a valid router administrator password. It is not established as unauthenticated or remotely exploitable through a WAN interface.

## Operational safety

Use only hardware that you own or are expressly authorized to test. A root-level shell or command on a router can disrupt traffic, weaken device security, or expose private data. Do not run this on someone else's equipment or production networks without authorization and an impact plan.

Until fixed firmware is verified, restrict router management access to trusted administrators on the LAN, separate untrusted/guest networks from the management plane, use a strong unique administrator password, and apply verified vendor security updates when available.

## Vulnerability reports

Do not publish live device identifiers, private IP maps, real administrator credentials, session cookies/tokens, customer traffic, or unredacted screencasts in GitHub issues. Coordinate sensitive reports through a private channel with the repository maintainer and relevant vendor security team.
