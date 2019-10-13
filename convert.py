import os, json, sys, time, zipfile

arg = [x for x in sys.argv if os.path.splitext(x)[1] == ".mc"]

try:
    os.chdir(os.path.split(arg[0])[0])
except:
    print("Only accepts .mc")
    time.sleep(5)
    exit()

Key = True
name = []

for i in arg:
    name.append(os.path.split(i)[1])

title = artist = background = sound = ""

#Converting to osu
for i in name:
    with open(f'{i}',encoding='utf-8') as mc:
        mcFile = json.loads(mc.read())

    if not (mcFile['meta']['mode'] == 0):
        Key = False
        print(f"{i} is not a Key difficulty")

    if not Key:
        continue

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

    title = meta["song"]["title"]
    artist = meta["song"]["artist"]
    background = meta["background"]
    sound = note[-1]["sound"]
    creator = meta["creator"]
    version = meta["version"]

    if(len(line)>1):
        print("Doesn't support diffs with multiple BPMs")
        time.sleep(5)
        exit()

    def ms(beats): #[beats, n, divide]
        return int(1000*(60/bpm)*(beats[0]+beats[1]/beats[2]))+offset

    def col(column):
        return int(512*(2*column+1)/(2*keys))

    with open(f'{i}.osu',mode='at',encoding='utf-8') as osu:
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
            if(ms(n["beat"])+offset>=0):
                if(len(n)==2):  #Regular Note
                    osu.write(f'{col(n["column"])},192,{ms(n["beat"])},1,0\n')
                else:           #Long Note
                    osu.write(f'{col(n["column"])},192,{ms(n["beat"])},128,0,{ms(n["endbeat"])}\n')

    print(f'{i}.osu converted successfully.')

if not Key:
    for i in name:
        try:
            os.remove(f'{i}.osu')
        except:
            pass
    time.sleep(5)
    exit()

print('\nPress Enter to compress the files into .osz . . .')
input()

#Compress to .osz
print('\nCompressing...')

osz = zipfile.ZipFile(f'{artist} - {title}.osz','w')

for i in name:
    osz.write(f'{i}.osu')
    os.remove(f'{i}.osu')
    print(f'{i}.osu Compressed Successfully.')
if not (background==""):
    osz.write(f'{background}')
    print(f'{background} Compressed Successfully.')
osz.write(f'{sound}')
print(f'{sound} Compressed Successfully.\n')
osz.close()

print(f'{artist} - {title}.osz has been created.\nRun the file to add the maps to osu! automatically.')
time.sleep(5)
