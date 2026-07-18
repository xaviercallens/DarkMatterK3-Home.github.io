#!/usr/bin/env python3
import os
import time
import pandas as pd
from astroquery.sdss import SDSS
from datetime import datetime

# Target directory on the massive 1TB secondary drive
DATA_DIR = "/mnt/disks/disk-socrateai-local-1/callensxavier_home_data/bulk_astronomy_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Define a massive scope across the sky (Northern and Equatorial)
ra_ranges = [(ra, ra+10) for ra in range(100, 250, 10)]
dec_ranges = [(dec, dec+10) for dec in range(-10, 60, 10)]

print(f"[{datetime.utcnow().isoformat()}] Starting bulk download to {DATA_DIR}...")
total_galaxies = 0

for ra_min, ra_max in ra_ranges:
    for dec_min, dec_max in dec_ranges:
        print(f"[{datetime.utcnow().isoformat()}] Querying SDSS SpecObj for RA:{ra_min}-{ra_max}, DEC:{dec_min}-{dec_max}")
        query = f"""
        SELECT TOP 100000
            ra, dec, z
        FROM SpecObj
        WHERE class = 'GALAXY'
          AND z > 0.05 AND z < 0.6
          AND zWarning = 0
          AND ra BETWEEN {ra_min} AND {ra_max}
          AND dec BETWEEN {dec_min} AND {dec_max}
        """
        try:
            res = SDSS.query_sql(query, timeout=120)
            if res is not None:
                df = res.to_pandas()
                filename = os.path.join(DATA_DIR, f"sdss_ra{ra_min}_{ra_max}_dec{dec_min}_{dec_max}.csv")
                df.to_csv(filename, index=False)
                count = len(df)
                total_galaxies += count
                print(f"  -> Saved {count} galaxies to {filename}")
            else:
                print("  -> No data found in this sector.")
        except Exception as e:
            print(f"  -> SDSS Query Failed: {e}")
        
        # Polite delay to prevent rate-limiting from SDSS CasJobs API
        time.sleep(2)

print(f"[{datetime.utcnow().isoformat()}] Bulk download complete. Total real galaxies acquired: {total_galaxies}")
