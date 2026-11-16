import os
import random
import csv

# Create datasets directory
os.makedirs("datasets", exist_ok=True)

# Strict 7-column header expected by your dashboard parser
HEADERS = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Temperature", "Humidity"]

# 35 Realistic Real-World Scenarios
SCENARIOS = {
    # Tamil Nadu Specific Clusters
    "01_karur_textile_dying_cluster.csv": {
        "rows": 100, "pm25": (38.0, 72.0), "pm10": (75.0, 145.0), "no2": (22.0, 46.0),
        "so2": (14.0, 36.0), "co": (0.7, 1.6), "temp": (29.0, 37.0), "humidity": (48.0, 68.0)
    },
    "02_chennai_alandur_transit.csv": {
        "rows": 100, "pm25": (42.0, 88.0), "pm10": (85.0, 165.0), "no2": (35.0, 78.0),
        "so2": (8.0, 18.0), "co": (1.1, 2.5), "temp": (28.0, 34.0), "humidity": (65.0, 85.0)
    },
    "03_chennai_manali_petrochemical.csv": {
        "rows": 100, "pm25": (55.0, 115.0), "pm10": (110.0, 210.0), "no2": (40.0, 85.0),
        "so2": (28.0, 68.0), "co": (1.2, 2.8), "temp": (29.0, 35.0), "humidity": (60.0, 80.0)
    },
    "04_coimbatore_sidco_industrial.csv": {
        "rows": 100, "pm25": (32.0, 68.0), "pm10": (65.0, 130.0), "no2": (20.0, 45.0),
        "so2": (10.0, 24.0), "co": (0.6, 1.4), "temp": (24.0, 32.0), "humidity": (50.0, 75.0)
    },
    "05_coimbatore_peelamedu_urban.csv": {
        "rows": 100, "pm25": (24.0, 52.0), "pm10": (48.0, 95.0), "no2": (16.0, 36.0),
        "so2": (6.0, 14.0), "co": (0.4, 1.1), "temp": (25.0, 33.0), "humidity": (55.0, 78.0)
    },
    "06_madurai_collectorate_commercial.csv": {
        "rows": 100, "pm25": (35.0, 75.0), "pm10": (70.0, 140.0), "no2": (24.0, 50.0),
        "so2": (9.0, 20.0), "co": (0.7, 1.5), "temp": (28.0, 38.0), "humidity": (45.0, 68.0)
    },
    "07_salem_steel_corridor.csv": {
        "rows": 100, "pm25": (48.0, 98.0), "pm10": (95.0, 190.0), "no2": (30.0, 65.0),
        "so2": (22.0, 55.0), "co": (1.0, 2.2), "temp": (27.0, 36.0), "humidity": (42.0, 65.0)
    },
    "08_trichy_central_bus_stand.csv": {
        "rows": 100, "pm25": (40.0, 84.0), "pm10": (80.0, 155.0), "no2": (30.0, 62.0),
        "so2": (11.0, 22.0), "co": (0.9, 1.9), "temp": (28.0, 37.0), "humidity": (46.0, 70.0)
    },
    "09_ooty_clean_baseline.csv": {
        "rows": 100, "pm25": (6.0, 22.0), "pm10": (12.0, 38.0), "no2": (4.0, 14.0),
        "so2": (2.0, 6.0), "co": (0.1, 0.45), "temp": (11.0, 20.0), "humidity": (65.0, 92.0)
    },
    "10_kodaikanal_hill_station.csv": {
        "rows": 100, "pm25": (8.0, 24.0), "pm10": (15.0, 42.0), "no2": (5.0, 16.0),
        "so2": (2.0, 7.0), "co": (0.15, 0.5), "temp": (12.0, 21.0), "humidity": (70.0, 95.0)
    },
    "11_tuticorin_thermal_port.csv": {
        "rows": 100, "pm25": (50.0, 105.0), "pm10": (100.0, 215.0), "no2": (32.0, 70.0),
        "so2": (26.0, 64.0), "co": (0.9, 2.1), "temp": (27.0, 35.0), "humidity": (65.0, 88.0)
    },
    "12_tirupur_garment_hubs.csv": {
        "rows": 100, "pm25": (44.0, 86.0), "pm10": (85.0, 160.0), "no2": (26.0, 52.0),
        "so2": (16.0, 38.0), "co": (0.8, 1.8), "temp": (26.0, 35.0), "humidity": (45.0, 68.0)
    },

    # South Indian Metropolitan & Regional Hubs
    "13_bengaluru_btm_layout.csv": {
        "rows": 100, "pm25": (30.0, 68.0), "pm10": (60.0, 125.0), "no2": (25.0, 55.0),
        "so2": (6.0, 16.0), "co": (0.7, 1.6), "temp": (20.0, 30.0), "humidity": (50.0, 78.0)
    },
    "14_bengaluru_peenya_industrial.csv": {
        "rows": 100, "pm25": (58.0, 120.0), "pm10": (115.0, 230.0), "no2": (38.0, 76.0),
        "so2": (16.0, 42.0), "co": (1.1, 2.4), "temp": (21.0, 31.0), "humidity": (48.0, 72.0)
    },
    "15_kochi_eloor_chemical_zone.csv": {
        "rows": 100, "pm25": (28.0, 62.0), "pm10": (55.0, 110.0), "no2": (18.0, 40.0),
        "so2": (14.0, 34.0), "co": (0.6, 1.3), "temp": (26.0, 33.0), "humidity": (70.0, 90.0)
    },
    "16_trivandrum_city_center.csv": {
        "rows": 100, "pm25": (18.0, 42.0), "pm10": (36.0, 80.0), "no2": (14.0, 32.0),
        "so2": (5.0, 12.0), "co": (0.4, 0.9), "temp": (25.0, 32.0), "humidity": (68.0, 88.0)
    },
    "17_hyderabad_sanathnagar.csv": {
        "rows": 100, "pm25": (46.0, 98.0), "pm10": (92.0, 185.0), "no2": (32.0, 68.0),
        "so2": (12.0, 28.0), "co": (0.9, 2.0), "temp": (24.0, 36.0), "humidity": (42.0, 68.0)
    },
    "18_hyderabad_pharma_belt.csv": {
        "rows": 100, "pm25": (62.0, 135.0), "pm10": (120.0, 245.0), "no2": (42.0, 84.0),
        "so2": (24.0, 58.0), "co": (1.2, 2.6), "temp": (25.0, 37.0), "humidity": (40.0, 64.0)
    },
    "19_vizag_industrial_corridor.csv": {
        "rows": 100, "pm25": (42.0, 92.0), "pm10": (85.0, 175.0), "no2": (28.0, 60.0),
        "so2": (18.0, 44.0), "co": (0.8, 1.8), "temp": (26.0, 34.0), "humidity": (65.0, 86.0)
    },

    # Western & Central Hubs
    "20_mumbai_bkc_commercial.csv": {
        "rows": 100, "pm25": (58.0, 125.0), "pm10": (105.0, 210.0), "no2": (44.0, 92.0),
        "so2": (14.0, 32.0), "co": (1.3, 2.7), "temp": (26.0, 34.0), "humidity": (65.0, 88.0)
    },
    "21_mumbai_chembur_refinery.csv": {
        "rows": 100, "pm25": (72.0, 148.0), "pm10": (135.0, 260.0), "no2": (48.0, 98.0),
        "so2": (28.0, 72.0), "co": (1.5, 3.2), "temp": (27.0, 35.0), "humidity": (62.0, 84.0)
    },
    "22_pune_shivajinagar_core.csv": {
        "rows": 100, "pm25": (44.0, 94.0), "pm10": (88.0, 175.0), "no2": (30.0, 65.0),
        "so2": (10.0, 24.0), "co": (0.8, 1.8), "temp": (22.0, 34.0), "humidity": (45.0, 70.0)
    },
    "23_ahmedabad_vatva_industrial.csv": {
        "rows": 100, "pm25": (65.0, 140.0), "pm10": (130.0, 255.0), "no2": (40.0, 82.0),
        "so2": (22.0, 54.0), "co": (1.2, 2.5), "temp": (24.0, 38.0), "humidity": (35.0, 60.0)
    },

    # Northern High Pollution, Inversion & Smog Corridors
    "24_delhi_anand_vihar_severe.csv": {
        "rows": 120, "pm25": (190.0, 380.0), "pm10": (290.0, 520.0), "no2": (70.0, 140.0),
        "so2": (22.0, 52.0), "co": (2.8, 5.8), "temp": (10.0, 18.0), "humidity": (72.0, 94.0)
    },
    "25_delhi_punjabi_bagh_smog.csv": {
        "rows": 120, "pm25": (165.0, 330.0), "pm10": (250.0, 460.0), "no2": (60.0, 120.0),
        "so2": (18.0, 44.0), "co": (2.4, 5.0), "temp": (11.0, 19.0), "humidity": (70.0, 90.0)
    },
    "26_noida_sector_62_traffic.csv": {
        "rows": 100, "pm25": (140.0, 290.0), "pm10": (220.0, 420.0), "no2": (55.0, 110.0),
        "so2": (16.0, 38.0), "co": (2.1, 4.4), "temp": (12.0, 22.0), "humidity": (65.0, 88.0)
    },
    "27_gurugram_industrial_corridor.csv": {
        "rows": 100, "pm25": (150.0, 305.0), "pm10": (230.0, 440.0), "no2": (58.0, 115.0),
        "so2": (18.0, 42.0), "co": (2.2, 4.6), "temp": (12.0, 21.0), "humidity": (64.0, 86.0)
    },
    "28_lucknow_industrial_complex.csv": {
        "rows": 100, "pm25": (115.0, 240.0), "pm10": (185.0, 360.0), "no2": (42.0, 88.0),
        "so2": (15.0, 35.0), "co": (1.8, 3.8), "temp": (14.0, 26.0), "humidity": (60.0, 84.0)
    },
    "29_ludhiana_stubble_biomass.csv": {
        "rows": 100, "pm25": (135.0, 280.0), "pm10": (200.0, 390.0), "no2": (45.0, 92.0),
        "so2": (22.0, 48.0), "co": (2.4, 5.0), "temp": (13.0, 24.0), "humidity": (58.0, 82.0)
    },
    "30_jaipur_arid_dust_belt.csv": {
        "rows": 100, "pm25": (55.0, 115.0), "pm10": (140.0, 290.0), "no2": (32.0, 68.0),
        "so2": (12.0, 28.0), "co": (0.9, 2.0), "temp": (22.0, 36.0), "humidity": (25.0, 48.0)
    },

    # Seasonal Weather Washout & Baselines
    "31_monsoon_heavy_washout.csv": {
        "rows": 100, "pm25": (5.0, 18.0), "pm10": (10.0, 32.0), "no2": (5.0, 14.0),
        "so2": (2.0, 6.0), "co": (0.1, 0.4), "temp": (23.0, 28.0), "humidity": (85.0, 98.0)
    },
    "32_coastal_sea_breeze_dispersion.csv": {
        "rows": 100, "pm25": (15.0, 38.0), "pm10": (30.0, 68.0), "no2": (10.0, 25.0),
        "so2": (4.0, 10.0), "co": (0.3, 0.8), "temp": (27.0, 32.0), "humidity": (75.0, 92.0)
    },
    "33_winter_morning_inversion.csv": {
        "rows": 100, "pm25": (120.0, 250.0), "pm10": (180.0, 360.0), "no2": (50.0, 95.0),
        "so2": (16.0, 36.0), "co": (1.9, 4.0), "temp": (11.0, 17.0), "humidity": (78.0, 94.0)
    },
    "34_rural_agricultural_background.csv": {
        "rows": 100, "pm25": (20.0, 45.0), "pm10": (40.0, 85.0), "no2": (8.0, 20.0),
        "so2": (3.0, 8.0), "co": (0.4, 0.9), "temp": (22.0, 34.0), "humidity": (50.0, 75.0)
    },
    "35_national_mixed_benchmark.csv": {
        "rows": 300, "pm25": (10.0, 220.0), "pm10": (25.0, 340.0), "no2": (8.0, 85.0),
        "so2": (3.0, 45.0), "co": (0.3, 3.5), "temp": (15.0, 38.0), "humidity": (30.0, 90.0)
    }
}

master_records = []
total_datasets = 0

print("Regenerating clean 7-column numeric CSV datasets for your dashboard...\n")

for filename, cfg in SCENARIOS.items():
    filepath = os.path.join("datasets", filename)
    
    with open(filepath, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        
        for _ in range(cfg["rows"]):
            pm25 = round(random.uniform(*cfg["pm25"]), 1)
            pm10 = round(random.uniform(*cfg["pm10"]), 1)
            no2  = round(random.uniform(*cfg["no2"]), 1)
            so2  = round(random.uniform(*cfg["so2"]), 1)
            co   = round(random.uniform(*cfg["co"]), 2)
            temp = round(random.uniform(*cfg["temp"]), 1)
            hum  = round(random.uniform(*cfg["humidity"]), 1)
            
            row = [pm25, pm10, no2, so2, co, temp, hum]
            writer.writerow(row)
            master_records.append(row)
            
    total_datasets += 1
    print(f"[{total_datasets:02d}/35] Created: datasets/{filename} ({cfg['rows']} records)")

# Write Master Combined Dataset (Pure 7-numeric columns)
master_path = os.path.join("datasets", "00_master_combined_cpcb_dataset.csv")
with open(master_path, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(HEADERS)
    writer.writerows(master_records)

print(f"\n[MASTER FILE] Created: {master_path} ({len(master_records)} total records)")
print("\nDone! All files now contain the exact 7 numeric columns required by your web cockpit.")