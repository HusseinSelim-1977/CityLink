"""Development fixture dataset for CityLink.

This module provides structured fixture data for verifying frontend visualizations
and interactions prior to integration with real NYC Open Data pipelines in src/data.
NOTE: This data is for technical verification and UI development only;
the website clearly notes when data is loaded from dev fixtures.
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd

# Canonical reference vocabularies
BOROUGHS = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
HOUSING_CATEGORIES = [
    "New Residential Construction",
    "Affordable Housing Preserved",
    "Zoning Alterations",
    "Demolitions & Replacements"
]
TRANSIT_CATEGORIES = [
    "Subway Expansion & Upgrades",
    "Bus Rapid Transit (SBS)",
    "Bike Lane & Micro-Mobility",
    "Ferry Landing & Water Transit"
]

# Representative neighborhood coordinates
NEIGHBORHOODS = {
    "Manhattan": [
        ("Lower Manhattan", 40.7128, -74.0060),
        ("Midtown East", 40.7549, -73.9723),
        ("Chelsea", 40.7465, -74.0014),
        ("Harlem", 40.8116, -73.9465),
        ("Upper West Side", 40.7870, -73.9754)
    ],
    "Brooklyn": [
        ("Downtown Brooklyn", 40.6932, -73.9856),
        ("Williamsburg", 40.7081, -73.9571),
        ("Bushwick", 40.6944, -73.9213),
        ("Bedford-Stuyvesant", 40.6872, -73.9418),
        ("Sunset Park", 40.6455, -74.0124)
    ],
    "Queens": [
        ("Long Island City", 40.7447, -73.9485),
        ("Astoria", 40.7644, -73.9235),
        ("Flushing", 40.7675, -73.8331),
        ("Forest Hills", 40.7181, -73.8448),
        ("Sunnyside", 40.7433, -73.9196)
    ],
    "Bronx": [
        ("Mott Haven", 40.8090, -73.9229),
        ("South Bronx", 40.8167, -73.9189),
        ("Fordham", 40.8614, -73.8906),
        ("Riverdale", 40.8908, -73.9126)
    ],
    "Staten Island": [
        ("St. George", 40.6438, -74.0736),
        ("Stapleton", 40.6268, -74.0754),
        ("Great Kills", 40.5518, -74.1513)
    ]
}


def generate_dev_dataframe() -> pd.DataFrame:
    """Generate a deterministic, realistic fixture dataset for CityLink frontend."""
    # Seed for determinism across app launches
    np.random.seed(42)
    records: List[Dict[str, Any]] = []

    for borough in BOROUGHS:
        hoods = NEIGHBORHOODS[borough]
        for neighborhood, lat_base, lon_base in hoods:
            for year in YEARS:
                for h_cat in HOUSING_CATEGORIES:
                    for t_cat in TRANSIT_CATEGORIES:
                        # Base scaling factors per borough
                        b_mult = {
                            "Manhattan": 1.8,
                            "Brooklyn": 1.5,
                            "Queens": 1.2,
                            "Bronx": 0.9,
                            "Staten Island": 0.5
                        }[borough]

                        year_mult = 1.0 + (year - 2018) * 0.06

                        # Housing metrics
                        units = int(np.random.gamma(shape=5, scale=40 * b_mult * year_mult))
                        rent_sqft = round(float(np.random.normal(loc=55 * b_mult, scale=6)), 2)
                        
                        # Transit metrics
                        transit_ridership = round(float(np.random.normal(loc=12.5 * b_mult * year_mult, scale=2.0)), 2)
                        transit_ridership = max(1.0, transit_ridership)
                        
                        commute_min = round(float(np.random.normal(loc=38.0 / (b_mult ** 0.3), scale=4.0)), 1)
                        station_density = round(float(np.random.uniform(1.2, 5.8) * b_mult), 2)
                        
                        # Composite accessibility score (0 to 100)
                        access_score = round(min(100.0, max(20.0, float(station_density * 12.0 + (60.0 - commute_min) * 0.8))), 1)

                        # Tiny jitter around neighborhood center
                        lat = lat_base + np.random.uniform(-0.005, 0.005)
                        lon = lon_base + np.random.uniform(-0.005, 0.005)

                        records.append({
                            "borough": borough,
                            "neighborhood": neighborhood,
                            "year": year,
                            "housing_category": h_cat,
                            "transit_category": t_cat,
                            "residential_units": max(5, units),
                            "median_rent_sqft": max(20.0, rent_sqft),
                            "transit_ridership_m": transit_ridership,
                            "avg_commute_time_min": max(15.0, commute_min),
                            "subway_station_density": station_density,
                            "transit_accessibility_score": access_score,
                            "latitude": lat,
                            "longitude": lon,
                            "is_fixture": True
                        })

    return pd.DataFrame(records)


# Cached singleton instance for fast dev retrieval
_CACHED_DEV_DF: pd.DataFrame = generate_dev_dataframe()


def get_cached_dev_dataframe() -> pd.DataFrame:
    """Return a copy of the pre-generated development fixture dataset."""
    return _CACHED_DEV_DF.copy()
