import pandas as pd

def parse_srt_to_df(txt_srt_file, lang_prefix):
    print(f"Parsing {txt_srt_file}...")
    data = []
    
    try:
        with open(txt_srt_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    except UnicodeDecodeError:
        print(f"UTF-8 failed for {txt_srt_file}. Trying fallback encoding...")
        with open(txt_srt_file, 'r', encoding='iso-8859-1') as f:
            lines = [line.strip() for line in f.readlines()]

    current_block = {}
    dialogue_lines = []
    state = 0

    for line in lines:
        if line == "":
            if current_block:
                current_block[f'{lang_prefix} Dialogue'] = " ".join(dialogue_lines)
                data.append(current_block)
                current_block = {}
                dialogue_lines = []
                state = 0
            continue
            
        if state == 0:
            if line.isdigit() or line.replace('\ufeff', '').isdigit():
                current_block['Index Number'] = int(line.replace('\ufeff', ''))
                state = 1
        elif state == 1:
            if '-->' in line:
                current_block[f'{lang_prefix} Time Stamp'] = line
                state = 2
        elif state == 2:
            dialogue_lines.append(line)
            
    if current_block:
        current_block[f'{lang_prefix} Dialogue'] = " ".join(dialogue_lines)
        data.append(current_block)

    return pd.DataFrame(data)

def srt_merged_to_excel(eng_file, mal_file, excel_file):
    df_eng = parse_srt_to_df(eng_file, 'English')
    df_mal = parse_srt_to_df(mal_file, 'Malayalam')
    
    print("Merging subtitles by Index Number...")
    df_merged = pd.merge(df_eng, df_mal, on='Index Number', how='outer')
    df_merged.sort_values('Index Number', inplace=True)
    
    # Rearranged array to force the specific column order you want
    cols = [
        'Index Number', 
        'English Time Stamp', 
        'English Dialogue', 
        'Malayalam Dialogue', 
        'Malayalam Time Stamp'
    ]
    
    cols = [c for c in cols if c in df_merged.columns]
    df_merged = df_merged[cols]
    
    print(f"Exporting {len(df_merged)} rows to {excel_file}...")
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_merged.to_excel(writer, index=False, sheet_name='Dual_Subtitles')
        
        # Swapped widths for D and E to match the new text layout
        worksheet = writer.sheets['Dual_Subtitles']
        worksheet.column_dimensions['A'].width = 15
        worksheet.column_dimensions['B'].width = 35
        worksheet.column_dimensions['C'].width = 50
        worksheet.column_dimensions['D'].width = 50  # Malayalam Dialogue
        worksheet.column_dimensions['E'].width = 35  # Malayalam Time Stamp

    print("Done!")

# --- Execute ---
eng_input = '/Users/praveeshvalissery/Desktop/Better.Call.Saul.S04.1080p.NF.WEBRip.DDP5.1.x264-MIXED[rartv]/eng.srt'
mal_input = '/Users/praveeshvalissery/Desktop/Better.Call.Saul.S04.1080p.NF.WEBRip.DDP5.1.x264-MIXED[rartv]/mal.srt'
output_excel = '/Users/praveeshvalissery/Desktop/Better.Call.Saul.S04.1080p.NF.WEBRip.DDP5.1.x264-MIXED[rartv]/mal.xlsx'

srt_merged_to_excel(eng_input, mal_input, output_excel)