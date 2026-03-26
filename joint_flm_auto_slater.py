import csv, re
# import flame
import unicodedata
from pprint import pprint

src_csv_file = r'/Users/jointadmin/Documents/joint_pipe_rnd/auto_slate/auto_slater/sample_csv_001.csv'

def find_isci(row):
    ISCI_PATTERN = re.compile(r"^[A-Z]{4}\d{7}[A-Z]$", re.IGNORECASE)
    for cell in row:
        if ISCI_PATTERN.search(cell):
            return cell
    return None

#def regex_translation():
    # ^           Start of string
    # [A-Z]{4}    Exactly 4 letters (A-Z) — case insensitive due to re.IGNORECASE
    # \d{7}       Exactly 7 digits (0-9)
    # [A-Z]       Exactly 1 letter (A-Z) — case insensitive
    # $           End of string


#### Filename scoring variables

MARKERS_PRIMARY = ("_WEB_", "_BROADCAST_", "_CAPS_", "_NA_", "_Generic_", "_HD_", "_SD_", "_UHD_")
MARKERS_ASPECT = ("16x9", "9x16", "1x1")
DURATION_SUFFIX_RE = re.compile(r"_(\d{2,3})\b")     # e.g., _06, _15, _30, _120
RES_RE = re.compile(r"\b\d{3,5}[xX]\d{3,5}\b")  # e.g., 1920x1080

def score_deliverable_name(s: str):
    norm_s = unicodedata.normalize("NFKC", str(s)).strip()
    score = 0

    if any(m.lower() in norm_s.lower() for m in MARKERS_PRIMARY):
        score += 3
    if any(a in norm_s for a in MARKERS_ASPECT):
        score += 2
    if RES_RE.search(norm_s):
        score += 2
    if DURATION_SUFFIX_RE.search(norm_s):
        score += 2
    if "_" in norm_s:
        score += 1
    # favor longer descriptive strings a bit
    score += min(len(norm_s) // 12, 3)
    return score


def find_deliverable_name(row):
    candidates = []
    for cell in row:
        norm_cell = unicodedata.normalize("NFKC", str(cell)).strip()
        candidates.append(norm_cell)

    best = max(candidates, key=score_deliverable_name)
    return best or None

def format_del_filename(d):
    filename = d['filename'].replace(' ', '_')
    return f"{d['isci']}_{filename}"
    
def parse_delivery_csv(csv_matrix):
    del_list = []

    with open(src_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        count = 0
        for row in csv_reader:
            isci = find_isci(row)
            if isci:
                new_dict = {
                    "isci": isci,
                    "filename": find_deliverable_name(row),
                }
                del_list.append(new_dict)
    formatted_filename = [format_del_filename(d) for d in del_list]
    # pprint(formatted_filename)
    # return formatted_filename     
    pprint(del_list)


parse_delivery_csv(src_csv_file)

#### Flame integration

def parse_filenames_to_flame(selection):
    try:
        formatted_filenames = parse_delivery_csv(src_csv_file)
        print(f"[parse_filenames] Found {len(formatted_filenames)} filenames")

        desktop = flame.project.current_project.current_workspace.desktop
        reel_group = desktop.create_reel_group('delivery_names')
        reel = reel_group.create_reel('sequences')

        for name in formatted_filenames:
            seq = reel.create_sequence()
            seq.name = name
            print(f"[parse_filenames] Created sequence: {name}")

        print("[parse_filenames] Done!")

    except Exception as e:
        print(f"[parse_filenames] ERROR: {e}")
        import traceback
        traceback.print_exc()

def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Delivery",               # submenu name
            "actions": [
                {
                    "name": "Parse Filenames",
                    "execute": parse_filenames_to_flame,
                }
            ]
        }
    ]




"""
Currently this iterates through the csv and creates the delivery filenames
Next work on a version that takes a csv, with a given delivery file name, add adds a slate to it. Assume nothing exists before 01:00:00:00. 

In selected clip -  add slate graphic, add 2 pop, add black frame gap
get selected sequence
get name
if name matches name in formatted_filename
Next, in selected clip - add/modify text node to add slate info 

Add name of deliverable and other elements that can be pulled from sequence info (dur, height)

If all of that is working, then figure out parsing full slate info
"""
