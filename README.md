# Malody to osu!mania Converter

Windows-only program that converts Malody Key mode charts to osu!mania\
Roughly coded in python by request\
Supports all keys (4K~9K)

## How to Use

1. **Drag Key Mode .mc files or .mcz/.zip package files into the program.** This will convert all the files you dragged into .osu files in an instant.
2. You can move the files manually if wanted, but **to compress all .osu files into a mapset(.osz), hit any key.**
3. .osz files will be created. **Run the files** to add the charts to osu!.

## Disclaimer

* Expect bugs.
* All the .mc files you have dragged will be compressed into a single mapset.
* All the .mcz/.zip files you have dragged will be compressed into seperate mapsets. A mapset per file.
* **Only supports charts with no BPM changes for the time being.** Should really work on that.
* Doesn't support custom hitsounds and SVs yet.

## TODO

* Support folders
* Support custom hitsounds and SVs
* Various color output using Colorama
* More user-friendly GUI using Tkinter... maybe?

## Changelog

### v1.3

* [#4](https://github.com/jakads/Malody-to-Osumania/issues/4) - __**Supports multiple BPMs**__
* Supports time signature changes
* Exports offsets of timing points as floats instead of integers for better accuracy
  * Offset of notes are still exported as integers since osu cannot read it properly
* Displays error message instead of just crashing
  * Please report if this ever happens!
* New program icon by [@Nakaisu1](https://twitter.com/Nakaisu1)
* Bug fixes
  * [#6](https://github.com/jakads/Malody-to-Osumania/issues/6) - If the target .osu already exists, it adds to it instead of overwriting it
  * [#5](https://github.com/jakads/Malody-to-Osumania/issues/5) - Crashes when the BG and Audio file specified in .mc file is not found
  * Randomly crashes while compressing

### v1.2.1

* This update partially is to check if the auto-download feature implemented in v1.2 works as intended.
* Better wording (Press any key to turn off the program. → Press any key to exit.)
* Opens this page(changelog) after finishing update
* Bug fixes
  * [#3](https://github.com/jakads/Malody-to-Osumania/issues/3) - Unable to deny the update

### v1.2

* Downloads new .exe automatically and then replaces the current one after detecting available update
* Bug fixes
  * Can't detect files with uppercase extensions (e.g. '.MC', '.MCZ', '.ZIP')

### v1.1

* Automatically ignores unsupported files
* Supports .mcz/.zip files
* Waits until user's keyboard input using msvcrt.getch() instead of waiting 7 seconds using time.sleep(7)
* Auto-Update feature ~~(temporary, might make it optional or create a seperate Update.exe program)~~\
Made it optional
* Supports multiple BG/Audio files

### v1.0

* Initial Release
