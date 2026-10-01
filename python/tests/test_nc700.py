"""Tests for Noise Cancelling Headphones 700 device configuration."""

from pybmap.catalog import lookup_device
from pybmap.devices import nc700, DEVICES, detect_device_type


class TestNc700Config:
    def test_has_device_info(self):
        assert nc700.DEVICE_INFO["product_id"] == 0x4024
        assert nc700.DEVICE_INFO["codename"] == "goodyear"

    def test_channel_and_init(self):
        assert nc700.RFCOMM_CHANNEL == 8
        assert nc700.INIT_PACKET == (0, 1)

    def test_cnc_is_direct_and_silent(self):
        cnc = nc700.FEATURES["cnc"]
        assert cnc["addr"] == (1, 5)
        assert cnc["builder"] is not None
        assert cnc["silent_setget"] is True

    def test_no_audio_modes(self):
        for feat in ["audio_settings", "current_mode", "mode_config", "anr"]:
            assert feat not in nc700.FEATURES
        assert nc700.PRESET_MODES == {}
        assert nc700.EDITABLE_SLOTS == []

    def test_registered(self):
        assert DEVICES["nc700"] is nc700
        assert detect_device_type(0x4024) == "nc700"
        assert lookup_device(0x4024).config == "nc700"
