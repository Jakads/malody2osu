# Malody to osu!mania Converter
Converts Malody Key mode charts to osu!mania\
Roughly coded in python by request\
Supports all keys (4K~9K)
# How to Use
1. **Drag Key Mode .mc files or .mcz/.zip package files into the program.** This will convert all the files you dragged into .osu files in an instant.
2. You can move the files manually if wanted, but **to compress all .osu files into a mapset(.osz), hit any key.**
3. .osz files will be created. **Run the files** to add the charts to osu!.
# Disclaimer
* Expect bugs.
* All the .mc files you have dragged will be compressed into a single mapset.
* All the .mcz/.zip files you have dragged will be compressed into seperate mapsets. A mapset per file.
* **Only supports charts with no BPM changes for the time being.** Should really work on that.
* Doesn't support custom hitsounds and SVs yet.
# TODO
* Support folders
* **Support multiple BPMs**
* Support custom hitsounds and SVs
* Various color output using Colorama
* More user-friendly GUI using Tkinter... maybe?
# Changelog
## v1.2
* Downloads new .exe automatically and then replaces the current one after detecting available update
* Bug fixes
    * Can't detect files with uppercase extensions (e.g. '.MC', '.MCZ', '.ZIP')
## v1.1
* Automatically ignores unsupported files
* Supports .mcz/.zip files
* Waits until user's keyboard input using msvcrt.getch() instead of waiting 7 seconds using time.sleep(7)
* Auto-Update feature ~~(temporary, might make it optional or create a seperate Update.exe program)~~\
Made it optional
* Supports multiple BG/Audio files
## v1.0
* Initial Release
