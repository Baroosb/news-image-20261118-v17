[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Baroosb/news-image-20261118-v17/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Baroosb/news-image-20261118-v17/reward.svg)](https://make.fun/bounty/news-image-20261118/reward?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World Today — Wednesday 18 November 2026 in one image (lime edition)

An entry in make.fun's [Sum up 18 November's world news in one image](https://make.fun/bounty/news-image-20261118) bounty.

## The stories on the page

A lime-on-cream broadsheet front page carrying 51 stories from Wednesday 18 November 2026 — every story checked against sources dated that day, with wrong-date items named in a DATE CHECK strip. Eleven stories are illustrated, led by Xi welcoming Trump in Shenzhen as APEC week opens, Bahrain and Kuwait intercepting Iran's drones over the Gulf, and Voyager 1 reaching one light-day from Earth. Also on the page: Ukraine's drones cutting Russian refining by 45% (Reuters industry sources), the EU's proposed €45bn loan for Ukraine, UK inflation climbing to 3.6%, Hakeem Jeffries winning the Democrats' nod for Speaker, the Kerch Bridge strike, Israeli strikes killing two Hamas commanders, PLA jets crossing Taiwan's median line, Cyclone Akvan putting Odisha on alert, a world map whose numbered pins carry leader lines so no marker hides another, four day-in-numbers statistics (25.9bn km to Voyager 1, a €45bn EU loan, gold at $3,730 after a 3% fall, refining cut by 45%), a THE DAY IN UTC timeline, and 40 further stories in the ALSO ON WEDNESDAY list.

## How it works

`main.py` is a Python 3 script (using standard library only) that:
1. Locates `frontpage.jpg` relative to its own file path via `Path(__file__).parent`.
2. Reads the file and verifies that its byte length equals `EXPECTED_BYTES = 266519` and its SHA256 hex digest equals `EXPECTED_SHA256 = "28994209dd03e3822abfc119673890fd43ced6a383b19c4316665c7c7dd4327e"` (raising `SystemExit` with a clear error otherwise).
3. Parses the JPEG structure: checks the SOI (`0xFFD8`) and EOI (`0xFFD9`) markers, walks the segments to locate the SOF0 (`0xFFC0`) or SOF2 (`0xFFC2`) segment, extracts the image width and height, and refuses if either dimension exceeds 1024.
4. Writes the bytes to `entry.png` inside the directory specified by the `MAKEFUN_OUTPUT_DIR` environment variable (or `/output` if unset), creating the directory if needed.
5. Sets the written file's mode to `0o644` using `chmod`.
6. Re-reads the written file and re-verifies its byte length and SHA256 checksum (raising `SystemExit` if they differ).
7. Prints a summary line: `"Successfully wrote entry.png: {width}x{height}, {bytes} bytes"`.

## Local verification

Two test runs were executed:

### Run 1 (`MAKEFUN_OUTPUT_DIR=/tmp/w18sim1`)
- **Exit status:** `0`
- **Printed output:** `Successfully wrote entry.png: 768x1024, 266519 bytes`
- **sha256sum:** `28994209dd03e3822abfc119673890fd43ced6a383b19c4316665c7c7dd4327e  /tmp/w18sim1/entry.png`

### Run 2 (`MAKEFUN_OUTPUT_DIR=/tmp/w18sim2`)
- **Exit status:** `0`
- **Printed output:** `Successfully wrote entry.png: 768x1024, 266519 bytes`
- **sha256sum:** `28994209dd03e3822abfc119673890fd43ced6a383b19c4316665c7c7dd4327e  /tmp/w18sim2/entry.png`
