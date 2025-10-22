# Catalyst Center Port Control Utility

This Python utility communicates with Cisco **Catalyst Center** to perform administrative actions on network switch ports based on a client’s MAC address.

---

## What It Does

- Looks up a client using its MAC address via Catalyst Center APIs
- Identifies the connected **switch and interface port**
- Allows administrative **enabling or disabling of the switch port** (e.g., shut/no shut)

---

## Use Case

Designed for network operations teams or security personnel who need a **quick-response tool** to isolate endpoints (e.g., malware-infected hosts or rogue devices).

> **Note:** While Cisco Adaptive Network Control (ANC) provides a more robust policy-based approach, this script offers an alternative.

---

## Warning: Use With Caution

This tool modifies live **switch interface configuration** (enabling/disabling ports).  
**Double-check the MAC address and confirm the target before applying changes.**

You are responsible for verifying that your usage complies with your organization's change control policies.

---

## Cisco Catalyst Center APIs Used

- `GET /dna/intent/api/v1/client-detail?macAddress=<mac_address>`  
- `GET /dna/intent/api/v1/interface/network-device/<switch_uuid>/interface-name?name=<switch_port>`  
- `PUT /dna/intent/api/v1/interface/<switch_port_uuid>?deploymentMode=Deploy`  
- `GET /api/v1/task/<task_id>`

---

## Getting Started

### Prerequisites

- Python >=3.13 with requests & dotenv packages
- Cisco Catalyst Center instance with API access enabled (script is tested on 2.3.7.10)
- API user credentials with permission to:
  - Query clients and devices
  - Modify interface state

---

### USage 

Download the repository and install [UV](https://github.com/astral-sh/uv) (or use pip/venv if you're familiar with that)

Create an .env file:
```
CC_URL=https://10.10.10.10
CC_USERNAME=username
CC_PASSWORD=password
```

Sync UV (to download the dependencies) and run the script.
```bash
uv sync     # Creates a virtual environment 
uv run main.py
```

---
### Disclaimer

This script is provided "as is" without any warranties of any kind, either express or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. The author does not warrant that the script will be error-free or that it will meet the specific requirements of the user. The user assumes all responsibility for the use of this script and any results obtained from it. In no event shall the author be liable for any damages, including but not limited to direct, indirect, incidental, special, or consequential damages arising out of the use or inability to use this script. Users are advised to test the script thoroughly before relying on it in a production environment.