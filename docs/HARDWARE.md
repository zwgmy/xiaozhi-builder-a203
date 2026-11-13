# A203 hardware notes

## Board

Ai-Thinker NodeMCU-Series ESP-S3-12K-KIT, A203 version.

- ESP32-S3
- 8 MB flash (confirmed by user)
- 8 MB PSRAM (board specification / prior board identification)

## Audio wiring

| Device | Pin | ESP32-S3 |
|---|---|---:|
| LMD2718B261 PDM microphone | CLK | GPIO2 |
| LMD2718B261 PDM microphone | DATA | GPIO7 |
| LMD2718B261 PDM microphone | L/R select | GND (LEFT) |
| MAX98357A | BCLK | GPIO12 |
| MAX98357A | LRC | GPIO13 |
| MAX98357A | DIN | GPIO14 |

The microphone and speaker have been tested independently using ESPHome. The MAX98357A successfully plays audio. The PDM microphone produces audio-level changes when configured with `i2s_lrclk_pin: GPIO2` and `i2s_din_pin: GPIO7`.

Important: ESPHome's PDM implementation uses the I2S WS/LRCLK pin configuration as the PDM clock output. Setting `i2s_bclk_pin` alone did not move the clock from GPIO0; setting `i2s_lrclk_pin` to GPIO2 fixed the test.

## Porting cautions

1. XiaoZhi firmware must use the PDM RX driver, not a standard-I2S microphone input.
2. The XiaoZhi source contains `NoAudioCodecSimplexPdm`; board code should use it with the verified mic clock/data and speaker BCLK/WS/DOUT pins.
3. GPIO0 was used during initial ESPHome diagnosis but is not the final microphone clock pin. GPIO2 is the verified final pin.
4. Validate cold boot and download mode before treating the pin map as production-ready.
5. Confirm the final 8 MB partition layout and generated flash arguments before flashing.
