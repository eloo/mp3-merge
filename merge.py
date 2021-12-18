import os
import glob
import re
import subprocess
from pathlib import Path
import click


# Defaults
default_batch_size = 5

default_file_pattern = "*Kapitel [0-9]*.mp3"
default_copy_pattern = "*Lied.mp3"

default_chapter_pattern = "(.*Kapitel )(\d+)\.mp3"

def create_target_dir(target_dir):
    Path(target_dir).mkdir(parents=True, exist_ok=True)


def copy_files(source_dir, target_dir, copy_pattern):
    files = sorted(glob.glob(source_dir + "/" + copy_pattern))
    for file in files:
        target_file = file.replace(source_dir + "/", target_dir + "/")
        print("Copy to: {}".format(target_file))
        list_files = subprocess.run(["cp", file, target_file])


@click.command()
@click.option("--source-dir", required=True, help="Directory with source files")
@click.option("--target-dir", required=True, help="Directory for the output files")
@click.option(
    "--batch-size", default=default_batch_size, help="Size of batch to be merged"
)
@click.option(
    "--chapter-pattern",
    default=default_chapter_pattern,
    help="Pattern to match the chapter",
    show_default=True
)
@click.option(
    "--merge-file-pattern",
    default=default_file_pattern,
    help="Pattern to files to process for merge",
    show_default=True
)
@click.option(
    "--copy-file-pattern",
    default=default_copy_pattern,
    help="Pattern to files to copy",
    show_default=True
)
def merge(source_dir, target_dir, batch_size, chapter_pattern,merge_file_pattern,copy_file_pattern):
    """Merge files from the source-dir based on the batch-size"""

    create_target_dir(target_dir)
    copy_files(source_dir, target_dir, copy_file_pattern)

    files = sorted(glob.glob(source_dir + "/" + merge_file_pattern))

    chapter_regex = re.compile(".*/" + chapter_pattern)

    for i in range(0, len(files), batch_size):
        batch = files[i : i + batch_size]
        start_chapter = chapter_regex.match(batch[0]).group(2)
        end_chapter = chapter_regex.match(batch[-1]).group(2)
        target_file_name = "{}{}-{}".format(
            chapter_regex.match(batch[0]).group(1), start_chapter, end_chapter
        )
        if len(batch) == 1:
            target_file_name = "{} {}".format(
                chapter_regex.match(batch[0]).group(1), start_chapter
            )
            print("Copy to: {}".format(target_file_name))
            list_files = subprocess.run(
                ["cp", batch[0], target_dir + "/" + target_file_name + ".mp3"]
            )
            continue

        print("Merge to: {}".format(target_file_name))
        list_files = subprocess.run(
            ["mp3wrap", target_dir + "/" + target_file_name + ".mp3", *batch],
            stdout=open(os.devnull, "wb"),
        )
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "0",
                "-i",
                target_dir + "/" + target_file_name + "_MP3WRAP.mp3",
                "-acodec",
                "copy",
                target_dir + "/" + target_file_name + ".mp3",
            ]
        )
        subprocess.run(
            ["id3cp", batch[0], target_dir + "/" + target_file_name + ".mp3"],
            stdout=open(os.devnull, "wb"),
        )
        subprocess.run(["rm", target_dir + "/" + target_file_name + "_MP3WRAP.mp3"])


if __name__ == "__main__":
    merge()
