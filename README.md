# XiaoZhi Builder — Ai-Thinker ESP-S3-12K-KIT A203

This repository is being prepared for a custom XiaoZhi ESP32 firmware build for the Ai-Thinker ESP-S3-12K-KIT (A203).

## Hardware verified

- MCU: ESP32-S3
- Flash: 8 MB
- PSRAM: 8 MB
- Microphone: LMD2718B261 PDM, LEFT channel
- Speaker amplifier: MAX98357A, 4 Ω speaker

### Audio GPIO mapping

| Signal | GPIO |
|---|---:|
| PDM microphone CLK | GPIO2 |
| PDM microphone DATA | GPIO10 |
| MAX98357A BCLK | GPIO12 |
| MAX98357A LRCLK | GPIO13 |
| MAX98357A DIN | GPIO14 |

The PDM clock mapping was verified with ESPHome 2026.10.2: configure the microphone clock using `i2s_lrclk_pin`, not `i2s_bclk_pin`.

## Development status

This repository is in the board-porting stage. The hardware pin map is recorded, but the XiaoZhi board implementation and cloud build workflow are not yet complete. Do not flash any firmware artifact until a successful GitHub Actions build and its flash addresses have been checked.

## Upstream projects

- XiaoZhi ESP32: https://github.com/78/xiaozhi-esp32
- Builder reference: https://github.com/Zipra214/xiaozhi-builder

The builder reference README declares MIT licensing. This repository will keep its own implementation and clearly attribute upstream components.

## Build target

- Chip target: `esp32s3`
- Flash size: `8MB`
- PSRAM: `8MB`
- ESP-IDF: to be pinned to a version compatible with the selected XiaoZhi source revision.
