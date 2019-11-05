# Malody to osu!mania Converter

Converts Malody Key mode charts to osu!mania\
Roughly coded in python by request\
Supports all keys (4K~9K)\
**This project is discontinued and will be merged to [VSRG-Converter](https://github.com/jakads/VSRG-Converter)**

## How to Use

1. **Drag Key Mode .mc files or .mcz/.zip package files into the program.** This will convert all the files you dragged into .osu files in an instant. .osu files will be created right next to .mc files.
2. You can move the files manually if wanted, but **to compress all .osu files into a mapset(.osz), hit any key.**
3. .osz files will be created right next to the .exe. **Run the files** to add the charts to osu!.

## Disclaimer

* This program is tested in **Windows** only. Execution in the other OS's not guaranteed.
* **Expect bugs.** Please report if you ever experience one!
* All the **.mc files** you have dragged in will be compressed into a **single mapset.**
* All the **.mcz/.zip files** you have dragged in will be compressed into **seperate mapsets.** A mapset per file.
* In case of negative SVs, absolute value of the SV value is used for conversion.
* Bare in mind that osu!mania can only interpret SV values between 0.01x and 10x, and any values outside the range are adjusted to 0.01x or 10x by client.\
This might cause some unexpected and possibly disappointing consequences, such as some SV gimmicks in Malody not being converted properly to osu!mania.

## Changelog

### **vFinal** (v1.4)

* **Final Version, discontinued**
* Support custom hitsounds
* Support SVs
  * In case of negative SVs, absolute value of the SV value is converted.
* Source code improvements
* Removed auto-update feature, faster loading
* Miscellaneous visual fixes
* Bug fixes
  * [#10](https://github.com/jakads/Malody-to-Osumania/issues/10) - The whole tree of converted files are compressed in .osz
  * [#11](https://github.com/jakads/Malody-to-Osumania/issues/11) - Doesn't accept .zip files
  * [#12](https://github.com/jakads/Malody-to-Osumania/issues/12) - "Target File" is not specified in the crash reports

### v1.3.2

* Exports a crash traceback log file upon crash
* Faster download speed by using 8KB chunks instead of 4KB
* Bug fixes
  * [#8](https://github.com/jakads/Malody-to-Osumania/issues/8) - sys.argv Not Delivered Properly Midst of an Update
  * Temporary batch file fails to pass arguments to the updated .exe file
  * v1.3.2.1 : Fails to create a new batch file if the arguments contain UTF-8 characters

### v1.3.1

* Added window title
* Typo, whoops
* Bug fixes
  * Updating fails if the original .exe has a whitespace in its name

### v1.3

* [#4](https://github.com/jakads/Malody-to-Osumania/issues/4) - __**Supports multiple BPMs**__
* Supports time signature changes
* Exports offsets of timing points as floats instead of integers for better accuracy
  * Offset of notes are still exported as integers since osu cannot read it properly
* **Displays error message instead of just crashing**
  * Please report if this ever happens!
* Added .exe details
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

* **Downloads new .exe automatically and then replaces the current one after detecting available update**
* Bug fixes
  * Can't detect files with uppercase extensions (e.g. '.MC', '.MCZ', '.ZIP')

### v1.1

* **Automatically ignores unsupported files**
* **Supports .mcz/.zip files**
* Waits until user's keyboard input using msvcrt.getch() instead of waiting 7 seconds using time.sleep(7)
* Auto-Update feature ~~(temporary, might make it optional or create a seperate Update.exe program)~~\
Made it optional
* Supports multiple BG/Audio files

### v1.0

* **Initial Release**
