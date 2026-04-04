import os
import re
import librosa
import librosa.display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from datetime import datetime

# ---------------- CONFIG ----------------
INPUT_AUDIO = r'D:\Trinity Western University\Spring 2026\BIO 400\Research\Cape Breton Acoustics'
INPUT_EXCEL = r'D:\Trinity Western University\Spring 2026\BIO 400\Research\Recordings.xlsx'
BASE_OUTPUT = r'D:\Trinity Western University\Spring 2026\BIO 400\Research\FINAL_RESULTS_V2'

BIN_LENGTH = 300
SR = 22050

# Create Distinct Folders for every part of the analysis
STRICT_DIR = os.path.join(BASE_OUTPUT, "STRICT_CLICKS")
INCLUSIVE_DIR = os.path.join(BASE_OUTPUT, "INCLUSIVE_CLICKS")
WHISTLE_DIR = os.path.join(BASE_OUTPUT, "WHISTLE_TRENDS")
SPECTRO_DIR = os.path.join(BASE_OUTPUT, "SPECTROGRAMS")
for d in [STRICT_DIR, INCLUSIVE_DIR, WHISTLE_DIR, SPECTRO_DIR]: os.makedirs(d, exist_ok=True)

# ---------------- HELPERS ----------------
def get_pb_id(fn):
    match = re.search(r'PB\d{5}', fn, re.IGNORECASE)
    return match.group(0).upper() if match else None

def get_date(fn):
    fn = fn.lower()
    m = re.search(r'(july|august)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})', fn)
    if m:
        month = 7 if 'jul' in m.group(1) else 8
        return datetime(int(m.group(3)), month, int(m.group(2))).date()
    m2 = re.search(r'(jul|aug)(\d{2})-(\d{2})', fn)
    if m2:
        month = 7 if m2.group(1) == 'jul' else 8
        return datetime(int("20"+m2.group(3)), month, int(m2.group(2))).date()
    return None

def analyze_segment(seg, sr):
    # 1. CLICK DETECTION (RMS Peaks)
    rms = librosa.feature.rms(y=seg)[0]
    clicks = np.sum(rms > np.mean(rms) * 3)

    # 2. WHISTLE DETECTION (Spectral Density)
    # Looking for tonal energy in the 2-10kHz band
    S = np.abs(librosa.stft(seg))
    freqs = librosa.fft_frequencies(sr=sr)
    whistle_zone = S[(freqs >= 2000) & (freqs <= 10000), :]
    whistle_score = np.mean(whistle_zone) * 100 # Intensity of tonal sounds

    return clicks, whistle_score

# ---------------- 1. DATA PREP ----------------
df_excel = pd.read_excel(INPUT_EXCEL)
df_excel.columns = df_excel.columns.str.strip()
df_excel['date_obj'] = pd.to_datetime(df_excel['YEAR'].astype(str) + '-' +
                                      df_excel['DATE'].astype(str).str.split('.').str[1] + '-' +
                                      df_excel['DATE'].astype(str).str.split('.').str[2], errors='coerce').dt.date

bh_map = {'F': 'Foraging', 'S': 'Socializing', 'R': 'Resting', 'T': 'Traveling'}
df_excel['behavior'] = df_excel['GROUPB'].map(bh_map)
df_excel['group_size'] = pd.to_numeric(df_excel['GROUPSIZE'], errors='coerce')

# ---------------- 2. AUDIO PROCESSING ----------------
raw_results = []
for f in os.listdir(INPUT_AUDIO):
    if not f.endswith(".wav"): continue
    print(f"Processing: {f}")
    path = os.path.join(INPUT_AUDIO, f)
    y, _ = librosa.load(path, sr=SR)

    # Save Spectrogram Visual for report
    plt.figure(figsize=(10, 4))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y[:SR*10])), ref=np.max)
    librosa.display.specshow(D, sr=SR, x_axis='time', y_axis='hz')
    plt.title(f'Spectrogram: {f}')
    plt.savefig(os.path.join(SPECTRO_DIR, f"{f}.png"))
    plt.close()

    pb_id = get_pb_id(f)
    f_date = get_date(f)
    dur = librosa.get_duration(y=y, sr=SR)

    for i, start in enumerate(range(0, int(dur), BIN_LENGTH)):
        if start + BIN_LENGTH > dur: continue
        seg = y[int(start*SR):int((start+BIN_LENGTH)*SR)]
        clicks, whistle_val = analyze_segment(seg, SR)
        raw_results.append({'file': f, 'pb_id': pb_id, 'date': f_date, 'bin': i+1, 'clicks': clicks, 'whistle_val': whistle_val})

df_audio = pd.DataFrame(raw_results)

# ---------------- 3. TRIPLE ANALYSIS ENGINE ----------------
def run_full_stats(df_audio_in, mode_name, output_path, target_var):
    final_rows = []
    for _, row in df_audio_in.iterrows():
        match = None
        if row['pb_id']:
            match = df_excel[df_excel['ENCOUNTER'] == row['pb_id']]
        elif mode_name == "INCLUSIVE" and row['date']:
            match = df_excel[df_excel['date_obj'] == row['date']]

        if match is not None and not match.empty:
            final_rows.append({**row, 'group_size': match['group_size'].mean(), 'behavior': match['behavior'].iloc[0]})

    df = pd.DataFrame(final_rows)
    df['norm_val'] = df[target_var] / df['group_size']

    # Run Two-Way ANOVA [cite: 9, 11]
    model = ols('norm_val ~ C(behavior) * group_size', data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)
    anova.to_excel(os.path.join(output_path, f"{target_var}_ANOVA.xlsx"))

    # Save Scatter Plot
    plt.figure(figsize=(8, 6))
    for b in df['behavior'].unique():
        subset = df[df['behavior'] == b]
        plt.scatter(subset['group_size'], subset['norm_val'], label=b)
    plt.xlabel("Group Size"); plt.ylabel(f"{target_var} per Whale"); plt.title(f"{mode_name}: {target_var}")
    plt.legend(); plt.savefig(os.path.join(output_path, f"{target_var}_Plot.png"))
    plt.close()
    df.to_excel(os.path.join(output_path, f"{target_var}_Raw_Data.xlsx"))

print("\n🧪 Running Strict Click Analysis...")
run_full_stats(df_audio, "STRICT", STRICT_DIR, 'clicks')

print("🧪 Running Inclusive Click Analysis...")
run_full_stats(df_audio, "INCLUSIVE", INCLUSIVE_DIR, 'clicks')

print("🧪 Running Whistle Intensity Analysis...")
run_full_stats(df_audio, "INCLUSIVE", WHISTLE_DIR, 'whistle_val')

print(f"\n🎯 COMPLETE! Check results in: {BASE_OUTPUT}")