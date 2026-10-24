#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 21:57:53 2026

@author: praveeshvalissery
"""

import os
import re
from datetime import timedelta

# --- CONFIGURATION ---
directory = '/Users/praveeshvalissery/Desktop/Better Call Saul S03E03/'
filename_base =  'Better Call Saul S03E03 Sunk Costs 1080p WEB-DL 6CH x265 HEVC-PSA'

# Full paths
input_path = os.path.join(directory, f"{filename_base}.srt")
output_path = os.path.join(directory, f"{filename_base}.srt")

# The cue where the shift begins (either the exact string or just the start timestamp)
SPLIT_TIMESTAMP_STR = "00:02:48,281"

# Delay in milliseconds:
# Positive (+) if subtitle appears TOO EARLY (leading the audio, so push it forward)
# Negative (-) if subtitle appears TOO LATE (lagging behind audio, so pull it backward)
DELAY_MS = -28162 


# --- HELPER FUNCTIONS ---
def parse_srt_time(ts_str):
    """Converts 'HH:MM:SS,mmm' into total milliseconds."""
    hours, minutes, rest = ts_str.strip().split(':')
    seconds, millis = rest.split(',')
    return (
        int(hours) * 3600000 +
        int(minutes) * 60000 +
        int(seconds) * 1000 +
        int(millis)
    )

def format_srt_time(total_ms):
    """Converts total milliseconds back into 'HH:MM:SS,mmm'."""
    # Guard against negative timestamps
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

    # Shift only if this cue starts at or after our split point
    if start_ms >= split_threshold_ms:
        start_ms += offset_ms
        end_ms += offset_ms

    return f"{format_srt_time(start_ms)} --> {format_srt_time(end_ms)}"


# --- MAIN EXECUTION ---
def main():
    if not os.path.exists(input_path):
        print(f"[Error] File not found: {input_path}")
        return

    # Extract start time if full line '00:08:32,504 --> ...' was pasted
    clean_split_ts = SPLIT_TIMESTAMP_STR.split('-->')[0].strip()
    split_threshold_ms = parse_srt_time(clean_split_ts)

    # Regex targeting SRT timestamp arrows
    ts_pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})'
    )

    # Use utf-8-sig to automatically handle common Windows/subscene BOM quirks
    with open(input_path, 'r', encoding='utf-8-sig', errors='replace') as infile:
        content = infile.read()

    # Apply shift
    modified_content = ts_pattern.sub(
        lambda m: shift_timestamp_line(m, split_threshold_ms, DELAY_MS),
        content
    )

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(modified_content)

    print(f"[Success] Processed cues from {clean_split_ts} onwards.")
    print(f"[Shift] Applied {DELAY_MS:+d} ms offset.")
    print(f"[Saved] Output written to:\n{output_path}")

if __name__ == '__main__':
    main()