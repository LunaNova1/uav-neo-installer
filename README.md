# uav-neo-installer
Template repository for native UAV Neo installation on local computer

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Updating](#updating)
- [Deploying to the drone (real hardware)](#deploying-to-the-drone-real-hardware)
- [Troubleshooting](#troubleshooting)
  - [Connection diagnostics](#connection-diagnostics)
  - [Setup log files](#setup-log-files)
  - [Simulator won't connect (Windows/WSL2)](#simulator-wont-connect-windowswsl2)
  - [Python 3.9 fails to install](#python-39-fails-to-install)
  - [Virtual environment issues](#virtual-environment-issues)
  - [WSL1 vs WSL2](#wsl1-vs-wsl2)
  - [drone command not found](#drone-command-not-found)

---

## Prerequisites

- **Windows**: Windows 10/11 with [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) installed (Ubuntu 22.04 recommended)
- **Mac**: macOS with a terminal (Homebrew will be installed automatically)
- **Linux**: Ubuntu 22.04 or 24.04 recommended

The setup script will automatically install Python 3.9, a virtual environment, and all required dependencies.

---

## Installation

1. Clone the install repository into your computer (entry point)

```sh
git clone https://github.com/MITUavNeo/uav-neo-installer.git
```

2. Run the installer script

```sh
bash uav-neo-installer/drone-student/scripts/setup.sh
```

3. When prompted, select your operating system and course curriculum.

```sh
Welcome to the UAV Neo Drone command-line installer for Windows, Mac, and Linux.
[1/3] Select your operating system: [windows, mac, linux]
1) windows
2) mac
3) linux
#? 1

[2/3] Select your course curriculum: [oneshot, outreach]
1) oneshot
2) outreach
#? 1

[3/3] Installing all drone libraries and dependencies...
```

4. Enter your sudo password and wait for the installation to finish. The script will automatically:
   - Clone the simulator, library, and lab files
   - Create a Python 3.9 virtual environment
   - Install all pip dependencies from `requirements.txt`
   - Configure your shell environment

5. **Windows only (WSL2):** The setup script will display an orange warning with a PowerShell command to configure your Windows Firewall. Open **PowerShell as Administrator** on Windows and run the command shown. This is required for the simulator to communicate with your Python scripts over the network. You only need to do this once. If the command fails, see [Simulator won't connect](#simulator-wont-connect-windowswsl2) in the troubleshooting section.

6. At the end of setup, a post-installation check will run automatically. All 10 checks should show `[PASS]`. If any show `[FAIL]`, review the log file printed in the installation summary and contact your instructor.

**Successful setup example (Windows):**
```
==========================================================================
[IMPORTANT] Windows Firewall Configuration Required
==========================================================================
WSL2 requires a Windows Firewall rule to allow the UAVNeo Simulator to
communicate with your Python scripts. Without this rule, the simulator
may fail to connect when your computer is connected to the internet.

Please open PowerShell as Administrator on Windows and run:

  New-NetFirewallRule -DisplayName "WSL2 UAVNeo Simulator" -Direction Inbound -InterfaceAlias (Get-NetAdapter -IncludeHidden | Where-Object { $_.Name -like '*WSL*' } | Select-Object -First 1 -ExpandProperty Name) -Action Allow -Protocol UDP -LocalPort 5064-5065

If that command fails, first find your WSL adapter name:
  Get-NetAdapter -IncludeHidden | Where-Object { $_.Name -like '*WSL*' }
Then use the Name from the output in place of the -InterfaceAlias parameter.

You only need to run this command once.
==========================================================================

Running post-setup checks...
==========================================================================
```
```diff
+  [PASS] Simulator folder exists
+  [PASS] Labs folder exists
+  [PASS] Library folder exists
+  [PASS] Virtual environment exists
+  [PASS] Shell config added to ~/.bashrc
+  [PASS] .local_bashrc.sh created
+  [PASS] .config file created
+  [PASS] Drone tool is working
+  [PASS] No command failures detected in log file
+  [PASS] All Python dependencies installed
+
+  All 10 checks passed!
```
```
==========================================================================

======================== INSTALLATION SUMMARY ========================
  Platform:         windows
  Curriculum:       outreach
  Install location: /home/user/uav-neo-installer
  Log file:         /home/user/uav-neo-installer/drone-student/scripts/.logs/setup_2026-03-29_18-41-11.log
  Duration:         0m 48s
======================================================================

##########################################################################
##                                                                      ##
##   Run  source ~/.bashrc  or open a new terminal to finish setup.     ##
##                                                                      ##
##########################################################################

UAV Neo Drone Setup Complete.
```

**If something goes wrong**, you may see output like:
```diff
+  [PASS] Simulator folder exists
+  [PASS] Labs folder exists
+  [PASS] Library folder exists
-  [FAIL] Virtual environment not found
+  [PASS] Shell config added to ~/.bashrc
+  [PASS] .local_bashrc.sh created
+  [PASS] .config file created
+  [PASS] Drone tool is working
+  [PASS] No command failures detected in log file
-  [FAIL] Cannot verify dependencies — virtual environment not found
-
-  2 of 10 checks failed. Review the log: /home/user/.../setup_2026-03-29_18-41-11.log
```

If any checks fail, share the log file (found in `drone-student/scripts/.logs/`) with your instructor for help.

**If Python 3.9 fails to install**, the script will stop early with:
```
[ERROR] Python 3.9 installation failed. Cannot continue setup.
Check that your Ubuntu version is supported by the deadsnakes PPA.
See https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa for supported versions.
```

7. Source your environment. You should see a `(drone-venv)` virtual environment appear in your prompt.

```sh
# Windows / Linux
source ~/.bashrc

# Mac
source ~/.zshrc
```

8. Test the custom `drone` command.

```sh
drone test
```

```sh
drone tool set up successfully!
  DRONE_ABSOLUTE_PATH: /home/user/uav-neo-installer/drone-student
  DRONE_IP: 127.0.0.1
  DRONE_TEAM: student
```

9. Open the simulator.

```sh
drone cd && cd ../../UAVNeo-Simulator

# Open file in file explorer
explorer.exe .    # Windows
open .            # Mac
nautilus .        # Linux

# Find the executable called UAVSim and open it.
UAVSim.exe        # Windows
UAVSim.app        # Mac
UAVSim.x86_64     # Linux
```

10. In the terminal, run `demo.py` to check that the setup was successful.

```sh
drone cd

drone sim demo.py

# Hit the Enter key in the simulator.
# The "A" button (1 key on computer) prints a statement to the terminal (Sim -> Python check)
# The "B" button (2 key on computer) launches the drone, flies it forward and to the right, then lands the drone (Python <-> Sim check)
```

---

## Updating

To update your labs, library, or simulator after initial setup:

```sh
bash uav-neo-installer/drone-student/scripts/update.sh
```

You will be prompted to select which component to update (labs, library, or sim). A post-update check will verify everything is working correctly.

**Note:** Updating labs will replace your existing labs folder. Back up any work before running the update.

### Testing unreleased changes (branch or fork)

`setup.sh` and `update.sh` clone the labs and library from each repo's **default branch**
(`main`). To test changes that are not on `main` yet, set these environment variables before
running either script. They are unset by default, so students always get `main`.

| Variable | Effect |
|----------|--------|
| `NEO_LABS_REF` / `NEO_LIB_REF` | Clone this branch or tag instead of the default branch. |
| `NEO_LABS_URL` / `NEO_LIB_URL` | Clone from a different remote (a fork) or a local `file://` path instead of the canonical repo. |

**A branch on the canonical GitHub repo** (the change must be pushed):

```sh
NEO_LABS_REF=feature/my-labs NEO_LIB_REF=feature/my-lib \
  bash uav-neo-installer/drone-student/scripts/update.sh
```

**A fork on GitHub:**

```sh
NEO_LABS_URL=https://github.com/you/uav-neo-summer-course-labs.git NEO_LABS_REF=my-branch \
  bash uav-neo-installer/drone-student/scripts/update.sh
```

**A local clone, no push needed** (clones committed local state; use a `file://` URL):

```sh
NEO_LABS_URL=file:///home/you/uav-neo-summer-course-labs NEO_LABS_REF=feature/my-labs \
  bash uav-neo-installer/drone-student/scripts/update.sh
```

The labs and library are cloned independently, so set the `LABS` variables, the `LIB`
variables, or both. `update.sh` updates one component per run; the overrides also apply to the
automatic library resync at the end of a labs update. Uncommitted working-tree edits are not
included — only committed state is cloned.

---

## Deploying to the drone (real hardware)

The same lab code runs on the real drone. Deployment copies your `labs/` and `library/` to the
Pi over SSH; the `drone` tool handles it.

1. **Point at the Pi.** Edit `drone-student/scripts/.config` and set `DRONE_IP` to the drone's
   address and `DRONE_TEAM` to your team name, then reload (`source ~/.bashrc` or a new
   terminal). The SSH account defaults to `uav`; set `DRONE_USER` in `.config` if your drone
   uses a different login. The tool connects as `<DRONE_USER>@<DRONE_IP>` and deploys to
   `/home/<DRONE_USER>/jupyter_ws/<DRONE_TEAM>`.
2. **First time:** `drone setup` — creates your team directory on the Pi and does an initial
   `drone sync all`.
3. **After each change:** `drone sync all` (or `drone sync labs` / `drone sync library`) —
   rsyncs your local `labs/` and `library/` to the Pi. Sync `library` too, so the drone runs
   the same library version as your simulator.
4. **Run it:** `drone connect` (SSH into the Pi), then `python3 <path>/main.py`. There is no
   `-s` flag, so `create_drone()` uses the real-drone backend instead of the simulator.

Handled outside this installer, on the Pi or by the flight crew:

- The ROS 2 flight stack must be running on the Pi (`teleop.launch.py`), and the Pi's own
  tooling selects which synced library Python loads.
- A **safety pilot** arms the drone and switches it to **OFFBOARD** to hand control to your
  program; switching out is the abort. Nothing moves until then.
- For position/waypoint flights, lower the PX4 `MPC_*` speed limits in QGroundControl first so
  the drone is safe indoors.

See `labs/flights/README.md` in the labs repo for the flight-day roles and per-flight steps.

---

## Troubleshooting

### Connection diagnostics

Run the built-in diagnostic script to check your networking setup:

```sh
python3 uav-neo-installer/drone-student/scripts/diagnose.py
```

This checks your simulator IP resolution, UDP connectivity on ports 5064/5065, Windows Firewall rule status, and WSL adapter configuration. Share the output with your instructor if you need help.

### Setup log files

Setup and update logs are saved to `drone-student/scripts/.logs/`. Each run creates a timestamped log file (e.g., `setup_2026-03-29_18-41-11.log`). Share this file with your instructor if you encounter issues.

### Simulator won't connect (Windows/WSL2)

If the simulator connects when offline but not when connected to the internet, you need to configure the Windows Firewall. Open **PowerShell as Administrator** and run:

```powershell
New-NetFirewallRule -DisplayName "WSL2 UAVNeo Simulator" -Direction Inbound -InterfaceAlias (Get-NetAdapter -IncludeHidden | Where-Object { $_.Name -like '*WSL*' } | Select-Object -First 1 -ExpandProperty Name) -Action Allow -Protocol UDP -LocalPort 5064-5065
```

If you get an error saying **"The specified interface was not found"**, the WSL adapter on your machine has a different name. Find it by running:

```powershell
Get-NetAdapter -IncludeHidden | Where-Object { $_.Name -like '*WSL*' }
```

Common adapter names include:
- `vEthernet (WSL)` — older Windows builds
- `vEthernet (WSL (Hyper-V firewall))` — newer Windows builds

Use the exact `Name` value from the output and run:

```powershell
New-NetFirewallRule -DisplayName "WSL2 UAVNeo Simulator" -Direction Inbound -InterfaceAlias "YOUR_ADAPTER_NAME_HERE" -Action Allow -Protocol UDP -LocalPort 5064-5065
```

**Alternative: WSL2 mirrored networking mode**

If you cannot get the firewall rule working, you can switch WSL2 to mirrored networking mode. This makes WSL2 share the Windows host's network stack directly, so no firewall rule is needed. **Requires Windows 11 22H2 or later** (will not work on Windows 10).

1. Open (or create) the file `%USERPROFILE%\.wslconfig` in a text editor (e.g., `C:\Users\YourName\.wslconfig`)
2. Add the following:

```ini
[wsl2]
networkingMode=mirrored
```

3. Shut down WSL and reopen your terminal:

```powershell
wsl --shutdown
```

> **Note:** Mirrored mode is a system-wide setting that may affect other WSL2 tools such as Docker. If you experience issues with other applications, remove the setting and use the firewall rule approach instead.

### Python 3.9 fails to install

The setup script uses the [deadsnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) to install Python 3.9. This PPA supports Ubuntu 22.04 (jammy) and 24.04 (noble). If you are on a different version, you may need to install Python 3.9 manually.

### Virtual environment issues

If the virtual environment fails to activate or dependencies are missing, try recreating it:

```sh
cd uav-neo-installer
python3.9 -m venv drone-venv
source drone-venv/bin/activate
pip install --upgrade pip
pip install -r drone-student/scripts/requirements.txt
```

### WSL1 vs WSL2

UAV Neo works with both WSL1 and WSL2, but **WSL2 is recommended**. WSL1 shares the Windows network stack directly (the simulator is reachable at `127.0.0.1`), while WSL2 uses a virtual network that may require firewall configuration. Some diagnostic features (firewall checks, adapter detection) may not work on WSL1.

To check your version, open PowerShell and run:

```powershell
wsl -l -v
```

If you want to upgrade to WSL2, run the following in **PowerShell as Administrator**:

```powershell
# Enable the Virtual Machine Platform feature
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart your computer, then open PowerShell as Administrator again

# Set WSL2 as the default version
wsl --set-default-version 2

# Convert your existing distro (replace "Ubuntu" with your distro name from wsl -l -v)
wsl --set-version Ubuntu 2
```

**Requirements:**
- Windows 10 version 1903+ (build 18362+) or Windows 11
- Virtualization must be enabled in BIOS (VT-x / AMD-V)

The conversion can take a few minutes. No data is lost. After completing, verify with `wsl -l -v` that the VERSION column shows `2`.

### drone command not found

Make sure you have sourced your shell configuration:

```sh
# Windows / Linux
source ~/.bashrc

# Mac
source ~/.zshrc
```

---
