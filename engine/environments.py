ENVIRONMENTS = {
    "ship_deck": {
        "name": "Old sailing ship deck",
        "location": "open_ocean",
        "floor": "weathered_wood",
        "lighting": "cloudy_day",
        "atmosphere": "sea_fog",
        "camera": "cinematic_wide",
        "objects": [
            "wooden_mast",
            "ropes",
            "sails",
            "wooden_barrels",
            "ocean_horizon",
        ],
    },

    "captain_cabin": {
        "name": "Captain's cabin",
        "location": "inside_ship",
        "floor": "old_wood",
        "lighting": "dim_window_light",
        "atmosphere": "dust_particles",
        "camera": "cinematic_medium",
        "objects": [
            "wooden_desk",
            "empty_chair",
            "half_eaten_meal",
            "navigation_maps",
            "small_window",
        ],
    },

    "crew_quarters": {
        "name": "Empty crew quarters",
        "location": "inside_ship",
        "floor": "old_wood",
        "lighting": "dim_warm_light",
        "atmosphere": "quiet",
        "camera": "cinematic_wide",
        "objects": [
            "wooden_bunks",
            "unmade_beds",
            "personal_belongings",
            "storage_chests",
        ],
    },

    "ship_hold": {
        "name": "Cargo hold",
        "location": "inside_ship",
        "floor": "old_wood",
        "lighting": "low_lantern_light",
        "atmosphere": "dark_dusty",
        "camera": "cinematic_wide",
        "objects": [
            "large_barrels",
            "wooden_crates",
            "cargo_rope",
        ],
    },

    "open_ocean": {
        "name": "Open ocean",
        "location": "ocean",
        "floor": "water",
        "lighting": "overcast",
        "atmosphere": "thick_fog",
        "camera": "cinematic_extreme_wide",
        "objects": [
            "distant_horizon",
            "rolling_waves",
            "sea_fog",
        ],
    },
}


def get_environment(name):
    return ENVIRONMENTS.get(name, ENVIRONMENTS["open_ocean"])
  
