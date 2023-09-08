import argparse
from sklearn.linear_model import LogisticRegression

import numpy as np
import pandas as pd

I = 'I'  # I: The vertical distance from the chainplates to the headsail halyard exit on the mast
ISP = "ISP"  # Equivalent “I” dimension for the spinnaker sail
J = 'J'  # J: The horizontal distance from the front of the mast to the headstay fitting on the hull
JSP = "JSP"  # Equivalent “J” dimension for the spinnaker sail
P = "P"  # The vertical distance from the upper surface of the boom at the goose neck to the main halyard exit on the mast.
E = "E"  # The maximum horizontal distance from the back of the mast at the boom goose neck to the outhaul for the main clew.

LOA = "LOA"  # Length overall
LWL = "LWL"  # Length of the hull on the waterline with the vessel in racing trim

DISPLACEMENT = "Displacement"  # Displacement is the total weight of the boat.
BALLAST = "Ballast"  # The ballast is specifically the weight of the keel and any weights permanently installed in the
# boat intended to increase stability.
DRAFT = "Draft"
BEAM = "Beam"
RIG_TYPE = "Rig Type"
MAX_HD_SAIL = "Max Hdsail"
DW_RATING = "DW Rating"
RATING = "Rating"
SAIL_NO = "Sail #"
BOAT_TYPE = "Boat Type"
BOAT_NAME = "Boat Name"

# Asymmetric Spinnaker

ASF = "ASF"  # ASF: Asymmetric Spinnaker Foot Length
ASMG = "ASMG"  # ASMG: Asymmetric Spinnaker Mid Girth Length
SLU = "SLU"  # SLU: symmetric Spinnaker Luff Length
SLE = "SLE"  # SLE: Asymmetric Spinnaker Leech Length

# Symmetric Spinnaker
# SL: Spinnaker Luff Length
# SSMG: Symmetric Spinnaker Mid Girth length measured from each half luff length.
# SSF: Symmetric Spinnaker Foot length
# SPL ????

SAD = "SAD"  # Sail Area to Displacement Ratio
DLR = 'DLR'  # Displacement to Length ratio


def read_fleet_roster(args):
    print(f'Reading {args.roster}')
    df = pd.read_excel(args.roster,
                       sheet_name='Table 1',
                       comment='Boat Name',
                       header=None,
                       )

    # printing our spreadsheet using print() method
    row_idx = 0
    boats = []
    while True:
        if pd.isna(df.iloc[row_idx, 0]):
            row_idx += 1
            continue
        # Determine how many rows boat occupies
        row_count = 1
        for i in range(1, 4):
            if row_idx + i >= len(df) - 1:
                row_count = 0
                break

            if not pd.isna(df.iloc[row_idx + i, 1]):
                break
            row_count += 1

        boat = {}

        is_valid_boat = True
        if row_count == 0:
            break
        elif row_count == 4:
            boat_name = df.iloc[row_idx, 0]
            t = boat_name.split('\n')
            if len(t) > 1:
                boat_name = t[0]
                boat_make = t[1]
            else:
                boat_make = df.iloc[row_idx + 2, 0]
        else:  # Boat occupies one row
            is_valid_boat = False
            row_idx += row_count
            continue

        boat[BOAT_NAME] = boat_name
        boat[BOAT_TYPE] = boat_make
        boat[SAIL_NO] = df.iloc[row_idx, 1]
        boat[RATING] = df.iloc[row_idx, 3]
        boat[DW_RATING] = df.iloc[row_idx, 5]

        boat[I] = float(df.iloc[row_idx, 6]) if not isinstance(df.iloc[row_idx, 6], str) else np.NAN
        boat[J] = float(df.iloc[row_idx + 1, 6]) if not isinstance(df.iloc[row_idx + 1, 6], str) else np.NAN
        boat[P] = float(df.iloc[row_idx + 2, 6]) if not isinstance(df.iloc[row_idx + 2, 6], str) else np.NAN
        boat[E] = float(df.iloc[row_idx + 3, 6]) if not isinstance(df.iloc[row_idx + 3, 6], str) else np.NAN

        boat[MAX_HD_SAIL] = float(df.iloc[row_idx, 7]) if not isinstance(df.iloc[row_idx, 7], str) else np.NAN
        boat[RIG_TYPE] = df.iloc[row_idx + 1, 7]
        boat[ISP] = float(df.iloc[row_idx + 2, 7]) if not isinstance(df.iloc[row_idx + 2, 7], str) else np.NAN
        boat[JSP] = float(df.iloc[row_idx + 3, 7])

        boat[LOA] = float(df.iloc[row_idx, 12])
        boat[LWL] = float(df.iloc[row_idx + 1, 12])
        boat[BEAM] = float(df.iloc[row_idx + 2, 12])
        boat[DRAFT] = float(df.iloc[row_idx + 3, 12])

        phrf_disp = float(df.iloc[row_idx, 13])
        if np.isnan(phrf_disp):
            phrf_disp = float(df.iloc[row_idx + 1, 13])
            phrf_ballast = float(df.iloc[row_idx + 2, 13])
            if np.isnan(phrf_ballast):
                phrf_ballast = float(df.iloc[row_idx + 3, 13])
        else:
            phrf_ballast = float(df.iloc[row_idx + 1, 13])
            if np.isnan(phrf_ballast):
                phrf_ballast = float(df.iloc[row_idx + 2, 13])

        boat[DISPLACEMENT] = phrf_disp
        if np.isnan(phrf_disp):
            print(f'Warning: {boat_name} has no displacement')
        boat[BALLAST] = phrf_ballast



        as_yes_no_slu = df.iloc[row_idx + 2, 9]
        has_asym = False
        if isinstance(as_yes_no_slu, str) and as_yes_no_slu.lower().startswith('yes'):
            t = as_yes_no_slu.split()
            if len(t) > 1:
                phrf_slu = float(t[1])
            else:
                phrf_slu = np.NAN
            phrf_sle = float(df.iloc[row_idx + 2, 8])
            phrf_asmg = float(df.iloc[row_idx + 2, 10])
            phrf_asf = float(df.iloc[row_idx + 2, 11])
        else:
            phrf_slu = np.NAN
            phrf_sle = np.NAN
            phrf_asmg = np.NAN
            phrf_asf = np.NAN

        boat[SLE] = phrf_sle
        boat[SLU] = phrf_slu
        boat[ASMG] = phrf_asmg
        boat[ASF] = phrf_asf

        has_asym = not (np.isnan(phrf_slu) or np.isnan(phrf_sle) or np.isnan(phrf_asmg) or np.isnan(phrf_asf))
        if is_valid_boat:
            # Compute Displacement to Length ratio
            boat[DLR] = (boat[DISPLACEMENT] / 2240) / ((boat[LWL] / 100) ** 3)
            # Compute Sail Area to Displacement Ratio
            sa_head = (boat[I] * boat[J]) / 2
            sa_main = (boat[P] * boat[E]) / 2
            sa_upwind = sa_head + sa_main
            boat[SAD] = sa_upwind / (boat[DISPLACEMENT] / 64) ** 0.667

            boats.append(boat)

        row_idx += row_count

    return boats


def store_csv(boats, csv_file_name):
    print(f"Writing {len(boats)} boats to {csv_file_name}")

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(boats)

    # Replace NaN values with an empty string
    df = df.fillna('')

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_name, index=False)


def do_regression(boats):
    # Training model
    df = pd.DataFrame(boats)

    # Drop rows with NaN values since we can't do regression with them
    df = df.dropna(axis=0)

    rating = df['Rating']
    features_list = [LWL, LOA]

    model_features = df[features_list]
    clf = LogisticRegression(random_state=0, solver='liblinear').fit(model_features, rating)

    # Now load our boat data
    df = pd.read_csv('data/sun_dragon.csv')
    target_features = df[features_list]

    predicted_rating = clf.predict(target_features)

    print(f'Predicted rating for {df[BOAT_TYPE][0]} PHRF={predicted_rating[0]}')
    print('Parameters used in regression:')
    for feature in features_list:
        print(f'\t{feature}: {df[feature][0]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("roster", help="PDF file containing fleet roster")

    args_ = parser.parse_args()
    boat_list = read_fleet_roster(args_)
    csv_name = args_.roster + ".csv"
    store_csv(boat_list, csv_name)

    do_regression(boat_list)
