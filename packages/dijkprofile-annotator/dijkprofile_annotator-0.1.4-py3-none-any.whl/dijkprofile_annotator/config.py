import os

CHARPOINT_CONVERSION_DICT = {
    "": "leeg",
    "101_Q19_2": "buitenkruin",
    "101_Q19_3": "binnenkruin",
    "101_Q19_5": "binnenteen",
    "105_T09_11": "insteek_sloot",
    "811_T13_8": "leeg",
    "351_T03_10": "leeg",
    "_T01_KKW": "leeg",
    "108_Q06_250": "leeg",
    "303_Q05_1": "leeg",
    "353__11": "leeg",
    "_T00_17": "leeg",
    "109_Q08_13": "leeg",
    "_Q07_KDM": "leeg",
    "_Q07_KDW": "leeg",
    '0': "leeg",
    None: "leeg",
    'nan': "leeg"
}

CLASS_DICT_REGIONAL = {
    "leeg": 0,
    "startpunt": 1,
    "buitenkruin": 2,
    "binnenkruin": 3,
    "binnenteen": 4,
    "insteek_sloot": 5
}

WEIGHT_DICT_REGIONAL = [0.1, 1.0, 1.1, 1.0, 0.1]

CLASS_DICT_FULL = {
        'leeg': 0,
        'Maaiveld binnenwaarts': 1,
        'Insteek sloot polderzijde': 2,
        'Slootbodem polderzijde': 3,
        'Slootbodem dijkzijde': 4,
        'Insteek sloot dijkzijde': 5,
        'Teen dijk binnenwaarts': 6,
        'Kruin binnenberm': 7,
        'Insteek binnenberm': 8,
        'Kruin binnentalud': 9,
        'Verkeersbelasting kant binnenwaarts': 9,  # 10
        'Verkeersbelasting kant buitenwaarts': 10,
        'Kruin buitentalud': 10,  # 12
        'Insteek buitenberm': 11,
        'Kruin buitenberm': 12,
        'Teen dijk buitenwaarts': 13,
        'Insteek geul': 14,
        'Teen geul': 15,
        'Maaiveld buitenwaarts': 16,
    }

# TODO: write this out explicitely
WEIGHT_DICT_FULL = [1.0] * 17

CLASS_DICT_SIMPLE = {
    'leeg': 0,
    'Maaiveld buitenwaarts': 1,
    'Teen dijk buitenwaarts': 2,
    'Kruin buitentalud': 3,
    'Kruin binnentalud': 4,
    'Teen dijk binnenwaarts': 5,
}

WEIGHT_DICT_SIMPLE = [0.1, 0.5, 0.7, 1.0, 1.0, 0.5]

CLASS_DICT_SIMPLE_SLOOT = {
    'leeg': 0,
    'Maaiveld buitenwaarts': 1,
    'Teen dijk buitenwaarts': 2,
    'Kruin buitentalud': 3,  
    'Kruin binnentalud': 4,
    'Teen dijk binnenwaarts': 5,
    'Insteek sloot dijkzijde': 6,
    'Insteek sloot polderzijde': 7,
    'Slootbodem polderzijde': 8,
    'Slootbodem dijkzijde': 9,
}

WEIGHT_DICT_SIMPLE_SLOOT = [0.1, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.1]

CLASS_DICT_SIMPLE_BERM = {
    'leeg': 0,
    'Maaiveld buitenwaarts': 1,
    'Teen dijk buitenwaarts': 2,
    'Kruin buitentalud': 3,  
    'Kruin binnentalud': 4,
    'Teen dijk binnenwaarts': 5,
    'Insteek sloot dijkzijde': 6,
    'Insteek sloot polderzijde': 7,
    'Slootbodem polderzijde': 8,
    'Slootbodem dijkzijde': 9,
    'Kruin binnenberm': 10,
    'Insteek binnenberm': 11,
}
WEIGHT_DICT_SIMPLE_BERM = [0.1, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.1]

HEADER = ["LOCATIONID",
          "X_Maaiveld binnenwaarts",
          "Y_Maaiveld binnenwaarts",
          "Z_Maaiveld binnenwaarts",
          "X_Insteek sloot polderzijde",
          "Y_Insteek sloot polderzijde",
          "Z_Insteek sloot polderzijde",
          "X_Slootbodem polderzijde",
          "Y_Slootbodem polderzijde",
          "Z_Slootbodem polderzijde",
          "X_Slootbodem dijkzijde",
          "Y_Slootbodem dijkzijde",
          "Z_Slootbodem dijkzijde",
          "X_Insteek sloot dijkzijde",
          "Y_Insteek sloot dijkzijde",
          "Z_Insteek sloot dijkzijde",
          "X_Teen dijk binnenwaarts",
          "Y_Teen dijk binnenwaarts",
          "Z_Teen dijk binnenwaarts",
          "X_Kruin binnenberm",
          "Y_Kruin binnenberm",
          "Z_Kruin binnenberm",
          "X_Insteek binnenberm",
          "Y_Insteek binnenberm",
          "Z_Insteek binnenberm",
          "X_Kruin binnentalud",
          "Y_Kruin binnentalud",
          "Z_Kruin binnentalud",
          "X_Verkeersbelasting kant binnenwaarts",
          "Y_Verkeersbelasting kant binnenwaarts",
          "Z_Verkeersbelasting kant binnenwaarts",
          "X_Verkeersbelasting kant buitenwaarts",
          "Y_Verkeersbelasting kant buitenwaarts",
          "Z_Verkeersbelasting kant buitenwaarts",
          "X_Kruin buitentalud",
          "Y_Kruin buitentalud",
          "Z_Kruin buitentalud",
          "X_Insteek buitenberm",
          "Y_Insteek buitenberm",
          "Z_Insteek buitenberm",
          "X_Kruin buitenberm",
          "Y_Kruin buitenberm",
          "Z_Kruin buitenberm",
          "X_Teen dijk buitenwaarts",
          "Y_Teen dijk buitenwaarts",
          "Z_Teen dijk buitenwaarts",
          "X_Insteek geul",
          "Y_Insteek geul",
          "Z_Insteek geul",
          "X_Teen geul",
          "Y_Teen geul",
          "Z_Teen geul",
          "X_Maaiveld buitenwaarts",
          "Y_Maaiveld buitenwaarts",
          "Z_Maaiveld buitenwaarts"]

SCALER_PATH = os.path.join("data", "trained_models", "scaler.pik")
MODEL_PATH = os.path.join('data', 'trained_models', 'dijknet_simple_95.pt')

INVERSE_CLASS_DICT_FULL = {v: k for k, v in CLASS_DICT_FULL.items()}
INVERSE_CLASS_DICT_SIMPLE = {v: k for k, v in CLASS_DICT_SIMPLE.items()}
INVERSE_CLASS_DICT_SIMPLE_BERM = {v: k for k, v in CLASS_DICT_SIMPLE_BERM.items()}
INVERSE_CLASS_DICT_SIMPLE_SLOOT = {v: k for k, v in CLASS_DICT_SIMPLE_SLOOT.items()}
INVERSE_CLASS_DICT_REGIONAL = {v: k for k, v in CLASS_DICT_REGIONAL.items()}

# manual mappings to get the correct names for plotting later
if 11 in INVERSE_CLASS_DICT_FULL:
    INVERSE_CLASS_DICT_FULL[10] = 'Kruin buitentalud'
