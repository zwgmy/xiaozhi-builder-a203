# A203 hardware notes

## Board

Ai-Thinker NodeMCU-Series ESP-S3-12K-KIT, A203 version.

- MCU: ESP32-S3
- Flash: 8 MB (confirmed by user)
- PSRAM: 8 MB (board specification / prior board identification)

## Verified audio wiring

| Device | Signal | ESP32-S3 GPIO |
|---|---|---:|
| LMD2718B261 PDM microphone | CLK | GPIO2 |
| LMD2718B261 PDM microphone | DATA | GPIO7 |
| LMD2718B261 PDM microphone | L/R select | GND (LEFT) |
| MAX98357A | BCLK | GPIO12 |
| MAX98357A | LRC / WS | GPIO13 |
| MAX98357A | DIN | GPIO14 |

The microphone and speaker have been tested using ESPHome 2026.10.2. The MAX98357A successfully plays audio, and the PDM microphone produces audio-level changes.

Important ESPHome finding: in this PDM configuration, the microphone clock is assigned through `i2s_lrclk_pin`, not `i2s_bclk_pin`. With `i2s_lrclk_pin: GPIO2` and `i2s_din_pin: GPIO7`, the microphone works. Changing only `i2s_bclk_pin` did not move the PDM clock.

## PSRAM

- Capacity: 8 MB (confirmed by ESPHome runtime detection).
- Working ESPHome configuration: `mode: quad`, `speed: 80MHz`.
- Runtime log confirmed `Available: YES` and `Size: 8192 KB`.
- Use ESP-IDF `CONFIG_SPIRAM_MODE_QUAD=y` and `CONFIG_SPIRAM_SPEED_80M=y` for XiaoZhi. Octal mode failed to initialize on this board.

## Button

- BOOT button: GPIO0
- Active level: low (button shorts GPIO0 to GND when pressed; confirm board schematic / continuity before final production use).

GPIO0 is reserved for BOOT and must not be assigned to the microphone clock.

## Firmware porting notes

1. Use the XiaoZhi `NoAudioCodecSimplexPdm` codec for PDM RX plus standard I2S TX.
2. Constructor pin order from the current upstream header:
   `(input_rate, output_rate, speaker_bclk, speaker_ws, speaker_dout, mic_sck, mic_din)`.
3. For A203, the intended call is:
   `NoAudioCodecSimplexPdm(16000, 24000, GPIO_NUM_12, GPIO_NUM_13, GPIO_NUM_14, GPIO_NUM_2, GPIO_NUM_7)`.
4. GPIO0 is reserved for the physical BOOT button.
5. Validate cold boot, BOOT/download mode, audio capture, playback and simultaneous full-duplex application behavior before calling the port production-ready.
6. Confirm the selected 8 MB partition table and generated flash arguments before flashing.
