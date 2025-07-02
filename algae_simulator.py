# simulator/algae_simulator.py

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os

matplotlib.use("TkAgg")
plt.rcParams['font.family'] = 'Segoe UI Emoji'

# === Load Real Climate Data ===
data_path = os.path.join(os.path.dirname(__file__), "../data/odisha_climate.csv")
climate = pd.read_csv(data_path)

# === Prepare Climate Data ===
climate["Month_Label"] = climate["Month_Name"]
climate["Date"] = pd.to_datetime(climate["Month"], format="%Y-%b")
np.random.seed(42)
climate["Nutrient"] = 1.5 + 2.5 * np.random.rand(len(climate))  # Simulated nutrients

# ✅ FIX: Sort data chronologically to avoid jagged plots
climate = climate.sort_values("Date").reset_index(drop=True)

# === Define Algae Species ===
species_list = ['Ulva lactuca', 'Hypnea musciformis', 'Caulerpa racemosa']

# === Growth Function ===
def algae_growth(temp, sun, nut, species):
    if species == "Ulva lactuca":
        t_opt, n_opt, s_opt = 30, 3.0, 6
        t_tol, n_tol, s_tol = 25, 5.0, 8
    elif species == "Hypnea musciformis":
        t_opt, n_opt, s_opt = 28, 2.8, 7
        t_tol, n_tol, s_tol = 24, 4.0, 8
    else:  # Caulerpa racemosa
        t_opt, n_opt, s_opt = 32, 4.0, 5
        t_tol, n_tol, s_tol = 24, 4.5, 6

    temp_score = max(0.01, 1 - abs(temp - t_opt) / t_tol)
    nut_score  = max(0.01, 1 - abs(nut  - n_opt) / n_tol)
    sun_score  = max(0.01, 1 - abs(sun  - s_opt) / s_tol)

    return 80 * temp_score * nut_score * sun_score

# === Run Simulation ===
for sp in species_list:
    biomass = 0
    growth_vals = []
    print(f"\n🔬 Simulating {sp}...")

    for i in range(len(climate)):
        temp = climate.loc[i, 'TempMax_C']
        sun  = climate.loc[i, 'Sunlight_h']
        nut  = climate.loc[i, 'Nutrient']

        growth = algae_growth(temp, sun, nut, sp)
        biomass = biomass * 0.9 + growth
        growth_vals.append(biomass)

        if i % 12 == 0:
            print(f"📅 {climate.loc[i, 'Month']}: Temp={temp:.1f}°C, Sun={sun:.1f}h, Nut={nut:.1f} → growth={growth:.2f}, biomass={biomass:.2f}")

    climate[sp] = growth_vals

# === Save Simulation Output ===
output_path = os.path.join(os.path.dirname(__file__), "../data/odisha_climate_with_biomass.csv")
climate.to_csv(output_path, index=False)
print(f"\n✅ Biomass simulation saved to: {output_path}")

# === Plotting: Neat Subplots for Each Species ===
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(22, 12), sharex=True)

colors = sns.color_palette("tab10", n_colors=3)
for idx, (ax, sp) in enumerate(zip(axes, species_list)):
    ax.plot(climate["Date"], climate[sp], label=sp, color=colors[idx], linewidth=2.5)
    ax.set_ylabel("Biomass Index", fontsize=12)
    ax.set_title(sp, fontsize=14, loc='left')
    ax.grid(True)
    ax.legend(loc="upper left")

axes[-1].set_xlabel("Time (Monthly)", fontsize=14)
fig.suptitle("Algae Growth Simulation — Chilika (2015–2024)", fontsize=20)
plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for title

# Watermark
fig.text(0.01, 0.96, 'Pixxelraft', fontsize=16, color='gray', alpha=0.5,
         fontname='Segoe UI', weight='bold', ha='left')

# Resize window
try:
    manager = plt.get_current_fig_manager()
    manager.resize(1600, 900)
except Exception:
    pass

# Final Preview
print("\n📊 Final Biomass (last 5 months):")
print(climate[["Date"] + species_list].tail(5))

plt.show()
