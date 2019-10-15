import os
import json
import sys
import zipfile
from shutil import rmtree
from msvcrt import getch
import requests
import webbrowser

print("Malody to osu!mania Converter v1.1")
print("October 15th, 2019")
print("by Jakads\n\n")

version = "1.1"

print("(i) Checking for updates . . .")
try:
    response = requests.get('https://raw.githubusercontent.com/jakads/Malody-to-Osumania/master/version.txt')
    print(f"(i) Latest Version = v{response.text}")

    if response.text != version:
        print("\n[!] New update is available! A browser will be opened for you. Please download the latest version.")
        webbrowser.open('https://github.com/jakads/Malody-to-Osumania/releases')
        print("(i) Press any key to turn off the program.")
        getch()
        sys.exit()

    print("\n(i) Your program is as good as new! We're good to go.\n\n")
except:
    print("(i) Latest Version = v???\n[!] Connection to GitHub failed. Will just continue...\n\n")

def recursive_file_gen(mydir):
    for root, dirs, files in os.walk(mydir):
        for file in files:
            yield os.path.join(root, file)
            #https://stackoverflow.com/questions/2865278
            
def convert(i, bgtmp, soundtmp):
    try:
        with open(f'{i}',encoding='utf-8') as mc:
            mcFile = json.loads(mc.read())
        mcFile['meta']['mode']
    except:
        print(f"[!] FileWarning: {os.path.split(i)[1]} is not a valid .mc file. Ignoring...")
        return 1

    if not mcFile['meta']['mode'] == 0:
        print(f"[!] KeyWarning: {os.path.split(i)[1]} is not a Key difficulty. Ignoring...")
        return 1

    else:
        line = mcFile['time']

        lineset = set()
        for x in line:
            lineset.add(x["bpm"])
        if len(lineset)>1:
            bpmname.append(os.path.split(i)[1])
            print(f"[!] BPMWarning: {os.path.split(i)[1]} contains one or more BPM changes. Ignoring...")
            MultiBPM = True
            return 1

    meta = mcFile['meta']
    note = mcFile['note']

    keys = meta["mode_ext"]["column"]
    bpm = int(line[0]["bpm"])

    try:
        offset = -int(note[-1]["offset"])
    except:
        offset = 0

    try:
        preview = meta["preview"]
    except:
        preview = -1

    try:
        titleorg = meta["song"]["titleorg"]
    except:
        titleorg = meta["song"]["title"]

    try:
        artistorg = meta["song"]["artistorg"]
    except:
        artistorg = meta["song"]["artist"]

    global title
    title = meta["song"]["title"]
    global artist
    artist = meta["song"]["artist"]
    background = meta["background"]
    if not background=="": bgtmp.append(f'{os.path.split(i)[0]}\\{background}')
    sound = note[-1]["sound"]
    if not sound=="": soundtmp.append(f'{os.path.split(i)[0]}\\{sound}')
    creator = meta["creator"]
    version = meta["version"]

    with open(f'{os.path.splitext(i)[0]}.osu',mode='at',encoding='utf-8') as osu:
        osuformat = ['osu file format v14',
                     '',
                     '[General]',
                     f'AudioFilename: {sound}',
                     'AudioLeadIn: 0',
                     f'PreviewTime: {preview}',
                     'Countdown: 0',
                     'SampleSet: Soft',
                     'StackLeniency: 0.7',
                     'Mode: 3',
                     'LetterboxInBreaks: 0',
                     'SpecialStyle: 0',
                     'WidescreenStoryboard: 0',
                     '',
                     '[Editor]',
                     'DistanceSpacing: 1.2',
                     'BeatDivisor: 4',
                     'GridSize: 8',
                     'TimelineZoom: 2.4',
                     '',
                     '[Metadata]',
                     f'Title:{title}',
                     f'TitleUnicode:{titleorg}',
                     f'Artist:{artist}',
                     f'ArtistUnicode:{artistorg}',
                     f'Creator:{creator}',
                     f'Version:{version}',
                     'Source:Malody',
                     'Tags:Malody Convert by Jakads',
                     'BeatmapID:0',
                     'BeatmapSetID:-1',
                     '',
                     '[Difficulty]',
                     'HPDrainRate:8',
                     f'CircleSize:{keys}',
                     'OverallDifficulty:8',
                     'ApproachRate:5',
                     'SliderMultiplier:1.4',
                     'SliderTickRate:1',
                     '',
                     '[Events]',
                     '//Background and Video events',
                     f'0,0,\"{background}\",0,0',
                     '',
                     '[TimingPoints]',
                     f'{offset},{60000/bpm},4,1,0,0,1,0',
                     '',
                     '[HitObjects]\n']
        osu.write('\n'.join(osuformat))
        #https://thrillfighter.tistory.com/310

        for n in note[:-1]:
            if ms(n["beat"], bpm, offset)+offset >= 0:
                if len(n) == 2:  #Regular Note
                    osu.write(f'{col(n["column"], keys)},192,{ms(n["beat"], bpm, offset)},1,0\n')
                else:           #Long Note
                    osu.write(f'{col(n["column"], keys)},192,{ms(n["beat"], bpm, offset)},128,0,{ms(n["endbeat"], bpm, offset)}\n')
    return 0

def ms(beats, bpm, offset): #beats = [measure, nth beat, divisor]
    return int(1000*(60/bpm)*(beats[0]+beats[1]/beats[2]))+offset

def col(column, keys):
    return int(512*(2*column+1)/(2*keys))

def compress(compressname, name, bglist, soundlist):
    osz = zipfile.ZipFile(f'{compressname}.osz','w')

    for i in name:
        osz.write(f'{os.path.splitext(i)[0]}.osu')
        os.remove(f'{os.path.splitext(i)[0]}.osu')
        print(f'[O] Compressed: {os.path.split(i)[1]}.osu')
    if not len(bglist)==0:
        for i in bglist:
            osz.write(f'{i}')
            print(f'[O] Compressed: {os.path.split(i)[1]}')
    if not len(soundlist)==0:
        for i in soundlist:
            osz.write(f'{i}')
            print(f'[O] Compressed: {os.path.split(i)[1]}\n')
    osz.close()
    oszname.append(f'{compressname}.osz')

if len(sys.argv)<=1:
    print("(i) Drag .mc or .mcz/.zip files into this program to convert them to .osu or .osz!")
    print("(i) Press any key to turn off the program.")
    getch()
    sys.exit()

MCDragged = False
MCValid = False
ZIPDragged = False
MultiBPM = False
mcname = []
zipname = []
bpmname = []
foldername = []
oszname = []

mctmp = []
for x in sys.argv[1:]:
    isMCZ = False
    if os.path.isdir(x):
        print(f"[!] FileWarning: {os.path.split(x)[1]} is a directory, not a file. Ignoring...")
    elif not os.path.isfile(x):
        print(f"[!] FileWarning: {os.path.split(x)[1]} does not exist. I recommend dragging the file into the program, not with a command prompt. Ignoring...")
    elif os.path.splitext(x)[1] == ".mc":
        mctmp.append(x)
        MCDragged = True
    elif os.path.splitext(x)[1] == (".mcz" or ".zip"):
        if os.path.splitext(x)[1] == ".mcz":
            isMCZ = True
            os.rename(x, f'{os.path.splitext(x)[0]}.zip')
            x = f'{os.path.splitext(x)[0]}.zip'
        mcz = zipfile.ZipFile(x)
        mcz.extractall(os.path.splitext(x)[0])
        mcz.close()
        if isMCZ:
            os.rename(x, f'{os.path.splitext(x)[0]}.mcz')
        zipname.append(os.path.splitext(x)[0])
        ZIPDragged = True
    else:
        print(f"[!] FileWarning: The file type of {os.path.split(x)[1]} is not supported. Ignoring...")
if MCDragged:
    mcname.append(mctmp)

if not MCDragged and not ZIPDragged:
    print("\n[X] FILEERROR: None of the files you've dragged in are supported. This program only accepts .mc, .mcz, or .zip files.")
    print("(i) Press any key to turn off the program.")
    getch()
    sys.exit()

title = ""
artist = ""
mctitle = ""
mcartist = ""
bglist = []
soundlist = []

print("\n\n(i) Converting . . .\n")

#Converting to .osu (dragged .mc files)
if MCDragged:
    bgtmp = []
    soundtmp = []
    for i in mcname[0]:
        if not convert(i, bgtmp, soundtmp):
            print(f'[O] Converted: {os.path.split(i)[1]}')
            MCValid = True
    mctitle = title
    mcartist = artist
    bglist.append(bgtmp)
    soundlist.append(soundtmp)


#Converting to .osu (dragged .mcz/.zip files)
if ZIPDragged:
    for folder in zipname:
        print(f'\n(i) Converting {os.path.split(folder)[1]} . . .\n')
        c=0
        bgtmp = []
        soundtmp = []
        mctmp = []
        filelist = list(recursive_file_gen(folder))
        for files in filelist:
            if os.path.splitext(files)[1] == ".mc":
                if not convert(files, bgtmp, soundtmp):
                    print(f'[O] Converted: {os.path.split(files)[1]}')
                    c+=1
                    MCValid = True
                    mctmp.append(files)
        if c>0:
            foldername.append(folder)
            bglist.append(bgtmp)
            soundlist.append(soundtmp)
            mcname.append(mctmp)

if MultiBPM:
    print("\n(i) This program does not support difficulties with multiple BPMs yet, thus the following files has not been converted.\n(i) Sorry for the inconvenience, and please try again in the future updates.")
    for i in bpmname:
        print(f'* {i}')

if not MCValid:
    print("\n[X] FILEERROR: None of the files you've dragged are supported.")
    print("(i) Press any key to turn off the program.")
    getch()
    sys.exit()

print('\n\n(i) All the supported .mc files have been converted to .osu!\n(i) Either close the program now and move the files manually,\n(i) or press Enter to compress all into .osz.')
getch()

print('\n(i) Compressing  . . .\n')
#Compress to .osz (dragged .mc files as single mapset)
if MCDragged:
    compress(f'{mcartist} - {mctitle}', mcname[0], set(bglist[0]), set(soundlist[0]))

if ZIPDragged:
    i = 1 if MCDragged else 0
    for folder in zipname:
        print(f'\n(i) Compressing {os.path.split(folder)[1]} . . .\n')
        compress(f'{os.path.split(folder)[1]}', mcname[i], set(bglist[i]), set(soundlist[i]))
        i+=1
        rmtree(folder)

print('\n(i) The following .osz files have been created! Run the files to add the maps to osu! automatically.\n')
for i in oszname:
    print(f'* {i}')
print('\n(i) Press any key to turn off the program.')
getch()
