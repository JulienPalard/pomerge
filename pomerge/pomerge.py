#!/usr/bin/env python3

"""Merge translations from one or many po files into one or many others.
"""

import json
import os
import sys
from difflib import SequenceMatcher as SM

import polib
from tqdm import tqdm


def find_best_match(possibilities, to_find):
    best_match = (0, None)
    for possibility in [
        possib for possib in possibilities if possib[:5] == to_find[:5]
    ]:
        match = SM(None, possibility, to_find).ratio()
        if match > best_match[0]:
            best_match = (match, possibility)
    if best_match[0] > .9:
        return best_match[1]


def find_translations(files):
    known_translations = {}
    # Aggregate all known translations
    for po_file in tqdm(files, desc="Searching translations"):
        try:
            po_file = polib.pofile(po_file)
        except OSError as err:
            print("Skipping {}: {}".format(po_file, str(err)), sys.stderr)
            continue
        for entry in po_file:
            if "fuzzy" not in entry.flags and entry.msgstr != "":
                known_translations[entry.msgid] = entry.msgstr
    return known_translations


def read_memory(memory_file):
    with open(memory_file) as memory:
        return json.load(memory)


def write_memory(translations, memory_file):
    with open(memory_file, "w") as memory:
        json.dump(translations, memory)


def write_translations(translations, files, fuzzy=False):
    for po_file in tqdm(files, desc="Updating translations"):
        po_file = polib.pofile(po_file)
        for entry in po_file:
            if entry.msgid in translations:
                entry.msgstr = translations[entry.msgid]
                if "fuzzy" in entry.flags:
                    entry.flags.remove("fuzzy")
            elif fuzzy:
                candidate = find_best_match(list(translations.keys()), entry.msgid)
                if candidate:
                    entry.msgstr = translations[candidate]
                    entry.flags.append("fuzzy")
        po_file.save()


def merge_po_files(from_files, to_files, fuzzy=False):
    """Find known translations from each given files in from_files,
    and update them in files in to_files.
    """
    memory_file = os.path.expanduser("~/.pomerge.json")
    if from_files:
        translations = find_translations(from_files)
    else:
        translations = read_memory(memory_file)
    if to_files:
        write_translations(translations, to_files, fuzzy)
    else:
        write_memory(translations, memory_file)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="""Replicate known translations between sets of po files.
To propagate known translation in a single set of po files,
give it as a source and a destination, like:

    pomerge --from *.po --to *.po

Translations already existing in the destinations po files will be
updated by translations from the source po files.

To find po files recursively, use the globstar option of bash, or your
shell equivalent, like:

    shopt -s globstar
    pomerge --from **/*.po --to **/*.po

Giving only --from or only --to works by using a temporary file, so:

    pomerge --from a/*.po --to b/*.po

is equivalent to:

    pomerge --from a/*.po
    pomerge --to b/*.po
"""
    )
    parser.add_argument(
        "--fuzzy",
        action="store_true",
        help="Also replicate nearly identical strings, "
        "but when doing so, add a fuzzy flag.",
    )
    parser.add_argument(
        "--from-files",
        "-f",
        nargs="+",
        help="File in which known translations are searched",
    )
    parser.add_argument(
        "--to-files",
        "-t",
        nargs="+",
        help="File in which translations will be added or updated",
    )
    args = parser.parse_args()
    if not args.from_files and not args.to_files:
        parser.print_help()
        exit(1)
    merge_po_files(args.from_files, args.to_files, args.fuzzy)


if __name__ == "__main__":
    main()
