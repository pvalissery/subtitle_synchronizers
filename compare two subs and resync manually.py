#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 12:23:17 2026

@author: praveeshvalissery
"""

import pandas as pd

def excel_to_synced_srt(excel_file, output_srt_file):
    print(f"Reading data from {excel_file}...")
    
    # Load the specific sheet we created earlier
    df = pd.read_excel(excel_file, sheet_name='Dual_Subtitles')
    
    # Filter out any rows that don't have BOTH an English timestamp and Malayalam text
    # This prevents blank subtitles or formatting errors in VLC
    clean_df = df.dropna(subset=['English Time Stamp', 'Malayalam Dialogue'])
    
    print(f"Writing corrected subtitles to {output_srt_file}...")
    
    with open(output_srt_file, 'w', encoding='utf-8') as f:
        new_index = 1
        for _, row in clean_df.iterrows():
            timestamp = str(row['English Time Stamp']).strip()
            dialogue = str(row['Malayalam Dialogue']).strip()
            
            # Write the SRT block
            f.write(f"{new_index}\n")
            f.write(f"{timestamp}\n")
            f.write(f"{dialogue}\n\n")
            
            new_index += 1
            
    print("Done! Synced SRT is ready for VLC.")

# --- Execute ---
input_excel = '/Users/praveeshvalissery/Desktop/Better.Call.Saul.S04.1080p.NF.WEBRip.DDP5.1.x264-MIXED[rartv]/mal.xlsx'
output_srt =  '/Users/praveeshvalissery/Desktop/Better.Call.Saul.S04.1080p.NF.WEBRip.DDP5.1.x264-MIXED[rartv]/maldone.srt'

excel_to_synced_srt(input_excel, output_srt)