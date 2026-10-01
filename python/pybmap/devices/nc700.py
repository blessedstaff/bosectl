"""Bose Noise Cancelling Headphones 700 device configuration.

Codename "goodyear", product ID 0x4024. Verified on firmware
1.8.2-11524+e0f7590 over macOS IOBluetooth.
BMAP over RFCOMM channel 8; GET [0.1] init answers and is sent on connect.

Key differences from the newer headphones:
  - No AudioModes block 31 (FblockNotSupp on every function). There are no
    mode presets or profiles; noise control is the direct CNC level [1.5].
  - CNC [1.5] SETGET [level, 1] is applied (the headset announces it) but
    the firmware never replies, so the write is confirmed with a GET.
    A 1-byte payload is rejected with ERROR Length (01).
  - The headset announces the level on the Bose app's scale, which runs the
    opposite way: wire 0 is announced "10" (max ANC), wire 5 as "5".
  - No ANR [1.6], no auto-pause [1.24], no auto-answer [1.27], no
    routing [4.12].

Capabilities confirmed on hardware:
  - Battery [2.2], firmware [0.5], serial [0.7], product name [1.2]: GET
  - Voice prompts [1.3], sidetone [1.11], multipoint [1.10], EQ [1.7],
    product name [1.2]: GET + SETGET (replies with STATUS)
  - EQ [1.7]: 3-band, range -10 to +10
  - Buttons [1.9]: GET (Shortcut button 0x80)
  - Source [5.1], power [7.4]: GET
  - Pairing [4.8]: answers RESULT

Unexplored: [1.15] reads 00 00 05 0a, which looks like the button's
CNC cycle levels (0/5/10).
"""

from . import parsers

RFCOMM_CHANNEL = 8

INIT_PACKET = (0, 1)

DEVICE_INFO = {
    "name": "Bose Noise Cancelling Headphones 700",
    "codename": "goodyear",
    "product_id": 0x4024,
}

FEATURES = {
    "battery": {
        "addr": (2, 2),
        "parser": parsers.parse_battery,
    },
    "firmware": {
        "addr": (0, 5),
        "parser": parsers.parse_firmware,
    },
    "product_name": {
        "addr": (1, 2),
        "parser": parsers.parse_product_name,
        "builder": lambda name: name.encode("utf-8"),
    },
    "voice_prompts": {
        "addr": (1, 3),
        "parser": parsers.parse_voice_prompts,
        "builder": parsers.build_voice_prompts,
    },
    "cnc": {
        "addr": (1, 5),
        "parser": parsers.parse_cnc,
        "builder": parsers.build_cnc,
        # SETGET is applied but never answered; confirm with a GET.
        "silent_setget": True,
    },
    "eq": {
        "addr": (1, 7),
        "parser": parsers.parse_eq,
        "builder": parsers.build_eq_band,
    },
    "buttons": {
        "addr": (1, 9),
        "parser": parsers.parse_buttons,
        "builder": parsers.build_buttons,
    },
    "multipoint": {
        "addr": (1, 10),
        "parser": parsers.parse_multipoint,
        "builder": parsers.build_toggle,
    },
    "sidetone": {
        "addr": (1, 11),
        "parser": parsers.parse_sidetone,
        "builder": parsers.build_sidetone,
    },
    "pairing": {
        "addr": (4, 8),
    },
    "source": {
        "addr": (5, 1),
        "parser": parsers.parse_source,
    },
    "power": {
        "addr": (7, 4),
    },
}

# No AudioModes block — noise control is `cnc <0-10>` only.
PRESET_MODES = {}

MODE_BY_IDX = {}

EDITABLE_SLOTS = []
