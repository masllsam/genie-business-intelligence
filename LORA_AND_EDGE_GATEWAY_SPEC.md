# 📻 Genie LoRa Mesh & Low-Bandwidth Edge Gateway Specification
**Hardware, Protocol & Packet Encoding Architecture for Extreme Reachability**  
*Operating on Meshtastic, LoRaWAN, Cellular SMS, and Satellite Channels*

---

## 1. Architectural Motivation: Intelligence Beyond Broadband

Most AI systems assume continuous high-speed optical broadband and gigabyte-heavy JavaScript browsers. If a disaster strikes, cell towers degrade, or an operator operates in remote terrain (mountains, maritime, off-grid), conventional AI becomes completely unreachable.

**Genie's Edge Gateway** solves this by establishing a bidirectional, ultra-compressed packet pipeline between pocket hardware nodes (e.g., LoRa phones, Meshtastic radios, e-ink terminals) and the cloud-hosted Genie Autonomous Fleet.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EDGE TO CLOUD DATA PIPELINE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [ 📻 Pocket LoRa Node ] (Heltec V3 / T-Beam / 868MHz / 915MHz)             │
│        │                                                                    │
│        │  LoRa RF Packet (~128 Bytes Payload)                               │
│        ▼                                                                    │
│  [ 📡 Genie Base Station / Mesh Relay ] (Solar-powered LoRa Gateway)        │
│        │                                                                    │
│        │  HTTPS / MQTT / Starlink or LTE Uplink                             │
│        ▼                                                                    │
│  [ ⚡ Genie Dispatcher ] (https://antifatypes.com:8443/webhook/edge)        │
│        │                                                                    │
│        ▼                                                                    │
│  [ 🧠 Genie Worker & ReAct Engine ] (:9000 -> OpenRouter / Ollama)          │
│        │                                                                    │
│        │  Autonomous Execution -> Web App Published at /s/site_xxx          │
│        ▼                                                                    │
│  [ 📦 Byte-Conserved Ack Packet ] (32 Bytes: Base91 / CBOR)                │
│        │                                                                    │
│        ▼                                                                    │
│  [ 📻 Pocket LoRa Node Screen ] ("OK site_lbE4 €49 book_active")            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Supported Edge Hardware Platforms

1. **Meshtastic ESP32 / nRF52 Radios**:
   - **Heltec WiFi LoRa 32 V3** ($19 USD): 0.96-inch OLED, SX1262 LoRa transceiver, battery charging circuit.
   - **LilyGO TTGO T-Beam** ($35 USD): GPS, 18650 battery holder, IPEX antenna.
   - **RAK Wireless WisBlock Core** ($28 USD): Solar-powered ultra-low-power base station.
2. **LoRa Feature Phones & E-Ink Terminals**:
   - **T-Deck / Keyboard Terminals**: Standalone pocket QWERTY messenger with LoRa + Bluetooth.
   - **SMS / 2G / 4G Feature Phones**: Accessible via standard SMS gateway (`+43...`) dispatching commands.

---

## 3. Compact Packet Encoding Protocol

To fit within strict LoRa packet constraints (128–240 bytes payload):

### 3.1 Command Opcode Format
```
[1 Byte: Opcode] [2 Bytes: Nonce] [1 Byte: Flags] [N Bytes: Compressed Intent]
```

| Opcode | Command | Example Payload | Expanded Backend Action |
| :---: | :--- | :--- | :--- |
| `0x01` | **Goal Trigger** | `G:site:fpv_drone_vienna:49` | Hires `website_builder`, compiles Tailwind site, deploys to `/s/site_{token}/` |
| `0x02` | **Doc Generator** | `D:prop:cloud_strategy` | Hires `doc_builder`, compiles WebCrypto AES-256 encrypted proposal at `/d/doc_{token}/` |
| `0x03` | **Code Exec** | `C:py:import math; print(math.pi)` | Spawns sandboxed Python worker, executes, returns stdout |
| `0x04` | **Watcher Register** | `W:http://target.com:interval=300` | Registers background watcher in PostgreSQL `live_mode_watchers` |
| `0x05` | **Model Toggle** | `M:ollama/llama3.2:1b` | Switches tenant LLM preference in memory |
| `0x06` | **Status / Ping** | `S` | Returns fleet health, token usage, active agent status |

### 3.2 Response Acknowledgement
Responses sent back across LoRa are compressed using Base91 or CBOR:
- Success Web: `OK:s/site_Xw4:book_act`
- Success Doc: `OK:d/doc_dRs:enc_pin=4821`
- Error/Refusal: `ERR:limit_exceeded`

---

## 4. Disaster Resilience & Zero-Broadband Operating Mode

In a total internet blackout:
1. The on-premise or vehicle-mounted Genie Edge Server runs **100% offline** on local Ollama models (`llama3.2:1b`, `qwen2.5-coder:3b`).
2. Edge nodes communicate entirely over local 868/915 MHz radio frequencies without relying on external internet infrastructure.
3. Once back online, the edge node automatically syncs state, database records, and logs to the primary cloud cluster.

---

*Engineered for extreme reliability, low latency, and uncompromising user sovereignty.*
