# Freenove 4WD RC Car — Firmware Rewrite

A ground-up rewrite of the firmware and control system for the [Freenove 4WD Smart Car](https://store.freenove.com/products/fnk0043) built on a Raspberry Pi. The original codebase was replaced with a clean, minimal Python implementation — no bloat, no unnecessary abstractions, no external server frameworks.

Controlled in real time from a laptop over WiFi using WASD keys and arrow keys, with a live camera feed streamed back to the controller window.

---

## Architecture

```
Laptop (Client)                        Raspberry Pi (Server)
┌──────────────────────┐               ┌──────────────────────────┐
│  pygame window       │               │  server.py               │
│  WASD → motor cmds   │ ──port 5000─▶ │  motor.py                │
│  arrows → servo cmds │               │  servo.py                │
│                      │               │  camera.py               │
│  camera feed display │ ◀─port 5001── │  pca9685.py (I2C driver) │
└──────────────────────┘               └──────────────────────────┘
```

Two sockets run in parallel — one for commands, one for the camera stream. Both are handled in separate threads on each side.

---

## Controls

| Key | Action |
|-----|--------|
| `W` | Forward |
| `S` | Reverse |
| `A` | Rotate left |
| `D` | Rotate right |
| `W + D` | Forward right curve |
| `W + A` | Forward left curve |
| `S + D` | Reverse right curve |
| `S + A` | Reverse left curve |
| `↑` | Tilt camera up |
| `↓` | Tilt camera down |
| `←` | Pan camera left |
| `→` | Pan camera right |
| `Ctrl+C` | Graceful shutdown |

---

## Hardware

- Raspberry Pi 3 (on car)
- Freenove 4WD Smart Car chassis
- PCA9685 16-channel PWM driver (I2C, address `0x40`)
- 4x DC motors (channels 0–7 on PCA9685)
- 2x SG90 servos — pan (channel 8), tilt (channel 9)
- Raspberry Pi Camera Module (CSI)

---

## Stack

**Server (Pi)**
- Python 3 — `socket`, `threading`
- `picamera2` — camera capture
- `smbus` — I2C communication with PCA9685
- No pip dependencies beyond what ships with Raspberry Pi OS

**Client (Laptop)**
- Python 3 — `socket`, `threading`
- `pygame` — keyboard input and camera display
- `numpy` — frame buffer handling

---

## How It Works

### Motor Control
Each motor uses two PCA9685 channels — one for forward, one for backward. Duty cycles run 0–4095 (12-bit). Setting both channels to 4095 simultaneously triggers an active brake. Turning is achieved by stopping one side of wheels while the other drives at full speed, causing the car to skid-pivot in the direction of the stopped side. This is skid-steer, the same mechanism used in tanks and bulldozers.

### Servo Control
Servos are driven at 50Hz via the PCA9685. Pulse width maps to angle — 500μs to 2500μs covers the full 0–180 degree range. Pan and tilt are incremental — each keypress adjusts the current pulse by a fixed offset, so the camera holds its position when the key is released.

### Camera Streaming
The Pi captures raw RGB888 frames via `picamera2` at 640x480. Each frame is sent over a dedicated TCP socket — prefixed with a 4-byte big-endian size header so the client knows exactly how many bytes to read. The client reassembles the frame, converts it to a numpy array, and blits it directly to the pygame surface.

### Command Protocol
Commands are plain UTF-8 strings sent over TCP. `TCP_NODELAY` is enabled on both sockets to bypass Nagle's algorithm — critical for real-time control where small packets need to be sent immediately without buffering.

```
"move_forward"      → all four wheels forward at duty 2000
"turn_forward_right"→ left wheels full speed, right wheels stopped
"tilt_up"           → tilt servo pulse += 10
"stop"              → all channels set to 4095 (active brake)
"quit"              → stop motors, close sockets, exit
```

---

## Dev Environment

Developed on a Raspberry Pi 5 workstation ([bare-metal](https://gtullio12.github.io/bare-metal/)) running Neovim. The Pi 3 filesystem was mounted over SSH using SSHFS, allowing files to be edited locally and executed directly on the car with no sync step.

```
sshfs pi@<car-ip>:/home/pi ~/mnt/car
```

---

## Running It

**On the Pi:**
```bash
cd ~/car/Server
python3 server.py
```

**On the laptop:**
```bash
cd Client
python3 client.py
```

Start the server first — the client will error on connection if the server isn't listening yet.

---

## What I Learned

**TCP for real-time control is non-trivial.** Nagle's algorithm buffers small packets to improve throughput — great for file transfers, terrible for sending a 12-byte keypress command every 30ms. Disabling it with `TCP_NODELAY` was the difference between laggy and responsive.

**Terminals aren't built for game input.** Python's `curses` library relies on OS key repeat, which has a built-in delay before a held key starts auto-repeating. For motor control this caused a noticeable stutter on first press. Switching to pygame's `key.get_pressed()` — which polls the state of every key simultaneously — fixed it completely.

**Each motor needs two PWM channels.** The motor driver chip uses one channel for forward and one for backward. Setting both to full duty simultaneously creates an active brake rather than a coast-to-stop. Understanding this was key to getting clean directional control.

**Hardware drivers don't need rewriting.** The PCA9685 driver is dictated entirely by the chip's datasheet — register addresses, I2C protocol, bit manipulation. Copying it and understanding it is more valuable than rewriting it for no reason.

**Threading is necessary for simultaneous I/O.** Camera streaming and command handling need to run concurrently. A single-threaded server would block on `recv()` while the camera starves, or block on frame capture while commands queue up. Two threads, two sockets, clean separation.
