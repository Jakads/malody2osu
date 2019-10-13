import os, json, sys, time, zipfile

basedir = os.getcwd()

print("Malody to osu!mania Converter v1.0")
print("October 14th, 2019")
print("by Jakads\n\n")

if len(sys.argv)<=1:
    print("Drag .mc files into this program to convert them to .osu or .osz!")
    time.sleep(7)
    exit()
arg = [x for x in sys.argv if os.path.splitext(x)[1] == ".mc"]

try:
    os.chdir(os.path.split(arg[0])[0])
except:
    print("FILEERROR: This program only accepts .mc files.")
    time.sleep(7)
    exit()

Key = True
MultiBPM = False
name = []
keyname = []
bpmname = []

for i in arg:
    name.append(os.path.split(i)[1])

title = ""
artist = ""
bglist = set()
soundlist = set()

#Converting to osu
print("Converting . . .\n")
for i in name:
    with open(f'{i}',encoding='utf-8') as mc:
        mcFile = json.loads(mc.read())

    if not mcFile['meta']['mode'] == 0:
        Key = False
        print(f"KEYERROR: {i} is not a Key difficulty.")

    else:
        keyname.append(i)
        meta = mcFile['meta']
        line = mcFile['time']
        note = mcFile['note']

        keys = meta["mode_ext"]["column"]
        bpm = int(line[0]["bpm"])

        #이거 예외 확인 좀 더 효율적으로 하는 법 아시는 분 Jakads#0133 디코
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

        if not meta["song"]["title"]=="": title = meta["song"]["title"]
        if not meta["song"]["artist"]=="": artist = meta["song"]["artist"]
        background = meta["background"]
        if not background=="": bglist.add(background)
        sound = note[-1]["sound"]
        if not sound=="": soundlist.add(sound)
        creator = meta["creator"]
        version = meta["version"]

        lineset = set()
        for x in line:
            lineset.add(x["bpm"])
        if len(lineset)>1:
            bpmname.append(i)
            MultiBPM = True
            print(f"BPMERROR: {i} contains one or more BPM changes.")

    if not Key or MultiBPM:
        continue

    def ms(beats): #[beats, n, divide]
        return int(1000*(60/bpm)*(beats[0]+beats[1]/beats[2]))+offset

    def col(column):
        return int(512*(2*column+1)/(2*keys))

    with open(f'{basedir}\\{i}.osu',mode='at',encoding='utf-8') as osu:
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
                     'Source: Malody',
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
            if ms(n["beat"])+offset >= 0:
                if len(n) == 2:  #Regular Note
                    osu.write(f'{col(n["column"])},192,{ms(n["beat"])},1,0\n')
                else:           #Long Note
                    osu.write(f'{col(n["column"])},192,{ms(n["beat"])},128,0,{ms(n["endbeat"])}\n')

    print(f'Converted: {i}')

if not Key or MultiBPM:
    if not Key:
        print("\nThis program does not support any modes other than Key. Please drag the Key mode difficulties only.\nThe following files are in Key mode:")
        if len(keyname)==0: print("None of the files you've dragged are in Key mode.")
        else:
            for i in keyname:
                print(i)

    if MultiBPM:
        print("\nThis program does not support difficulties with multiple BPMs yet. Sorry for the inconvenience.\nThe following files contain one or more BPM changes:")
        for i in bpmname:
            print(i)

    for i in name:
        try:
            os.remove(f'{basedir}\\{i}.osu')
        except:
            pass
    time.sleep(7)
    exit()

print('\nAll .mc files have been converted to .osu!\nEither close the program now and move the files manually,\nor press Enter to compress all into .osz.')
input()

#Compress to .osz
print('\nCompressing . . .\n')

osz = zipfile.ZipFile(f'{basedir}\\{artist} - {title}.osz','w')

for i in name:
    osz.write(f'{basedir}\\{i}.osu')
    os.remove(f'{basedir}\\{i}.osu')
    print(f'Compressed: {i}.osu')
if not len(bglist)==0:
    for i in bglist:
        osz.write(f'{i}')
        print(f'Compressed: {i}')
if not len(soundlist)==0:
    for i in soundlist:
        osz.write(f'{sound}')
        print(f'Compressed: {sound}\n')
osz.close()

print(f'{artist} - {title}.osz has been created!\nRun the file to add the maps to osu! automatically.')
time.sleep(7)
