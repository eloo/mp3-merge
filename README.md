# Mp3-Merge

This is a simple script to merge mp3's and copy the metadata as well.  
Its tested for the use in TonUINO using TonUINO Toolbox.

## Requirements

This script uses the following cli tools which needed to be installed in advance:

* mp3wrap - https://wiki.ubuntuusers.de/mp3wrap/
* ffmpeg - https://wiki.ubuntuusers.de/FFmpeg/
* id3cp - https://www.unix.com/man-page/debian/1/ID3CP/

Further the required python libraries are in the `requirements.txt`.  
So you should install them as well.

```shell
pip3 install -r requirements
```
 
## Usage example

```shell
python3 merge.py --source-dir test --target-dir output
```

```shell
Copy to: output/Bibi Blocksberg - Bibi Blocksberg Lied.mp3
Merge to: Bibi Blocksberg - Folge 1 - Hexen gibt es doch - Kapitel  01-05
Merge to: Bibi Blocksberg - Folge 1 - Hexen gibt es doch - Kapitel  06-10
Merge to: Bibi Blocksberg - Folge 1 - Hexen gibt es doch - Kapitel  11-15
Merge to: Bibi Blocksberg - Folge 1 - Hexen gibt es doch - Kapitel  16-20
Merge to: Bibi Blocksberg - Folge 1 - Hexen gibt es doch - Kapitel  21-25
Merge to: Bibi Blocksberg - Folge 1 - Hexen gibt es doch - Kapitel  26-30
Copy to: Bibi Blocksberg - Folge 1 - Hexen gibt es doch - Kapitel  31
```

### Process a whole directory

If you want to process a whole directory in a recursive manner you run the script like this

```shell
# cd into the directory you want to process

find . -type d -print0 | xargs -0 -i python3 <path-to-this-script>/merge.py --source-dir="{}" --target-dir="<absolute-target-dir>/{}"
```

## Links

- https://wiki.ubuntuusers.de/Archiv/Skripte/MP3_Zusammenf%C3%BChren/