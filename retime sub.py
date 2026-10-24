#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 09:47:17 2026

@author: praveeshvalissery
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# --- CONFIGURATION ---
directory = '/Users/praveeshvalissery/Desktop/Better.Call.Saul.S04.1080p.NF.WEBRip.DDP5.1.x264-MIXED[rartv]'
filename_base = 'mal copy'

# Full paths
input_path = os.path.join(directory, f"{filename_base}.srt")
output_path = os.path.join(directory, f"{filename_base}.srt")

# Where the subtitle cue is CURRENTLY located in the .srt file:
SPLIT_TIMESTAMP_STR = "00:01:26,560"

# Where you ACTUALLY hear the dialogue in your media player:
TARGET_TIMESTAMP_STR = "00:01:30,569"


# --- HELPER FUNCTIONS ---
def parse_srt_time(ts_str):
    """Converts 'HH:MM:SS,mmm' or 'HH:MM:SS.mmm' into total milliseconds."""
    clean_ts = ts_str.split('-->')[0].strip().replace('.', ',')
    hours, minutes, rest = clean_ts.split(':')
    seconds, millis = rest.split(',')
    return (
        int(hours) * 3600000 +
        int(minutes) * 60000 +
        int(seconds) * 1000 +
        int(millis)
    )

def format_srt_time(total_ms):
    """Converts total milliseconds back into 'HH:MM:SS,mmm'."""
    total_ms = max(0, total_ms)
    
    hours = total_ms // 3600000
    remainder = total_ms % 3600000
    minutes = remainder // 60000
    remainder = remainder % 60000
    seconds = remainder // 1000
    millis = remainder % 1000
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

def shift_timestamp_line(match, split_threshold_ms, offset_ms):
    """Shifts both timestamps in a '00:00:00,000 --> 00:00:00,000' line if past threshold."""
    start_str, end_str = match.group(1), match.group(2)
    start_ms = parse_srt_time(start_str)
    end_ms = parse_srt_time(end_str)

    if start_ms >= split_threshold_ms:
        start_ms += offset_ms
        end_ms += offset_ms

    return f"{format_srt_time(start_ms)} --> {format_srt_time(end_ms)}"


# --- MAIN EXECUTION ---
def main():
    if not os.path.exists(input_path):
        print(f"[Error] File not found: {input_path}")
        return

    split_threshold_ms = parse_srt_time(SPLIT_TIMESTAMP_STR)
    target_ms = parse_srt_time(TARGET_TIMESTAMP_STR)

    # Automatically derive the delay offset
    delay_ms = target_ms - split_threshold_ms

    ts_pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})'
    )

    with open(input_path, 'r', encoding='utf-8-sig', errors='replace') as infile:
        content = infile.read()

    modified_content = ts_pattern.sub(
        lambda m: shift_timestamp_line(m, split_threshold_ms, delay_ms),
        content
    )

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(modified_content)

    print(f"[Success] Processed cues from {SPLIT_TIMESTAMP_STR} onwards.")
    print(f"[Sync] Current: {SPLIT_TIMESTAMP_STR}  -->  Target: {TARGET_TIMESTAMP_STR}")
    print(f"[Shift] Computed offset: {delay_ms:+d} ms")
    print(f"[Saved] Output written to:\n{output_path}")

if __name__ == '__main__':
    main()