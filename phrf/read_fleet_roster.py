import argparse

import numpy as np
import pandas as pd


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
            if row_idx + i >= len(df)-1:
                row_count = 0
                break

            if not pd.isna(df.iloc[row_idx + i, 1]):
                break
            row_count += 1

        boat = None
        # Each boat data should have 4 rows and 8 columns
        # Excel has some of them merged, so we need to split them back

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
                boat_make = df.iloc[row_idx+2, 0]
        else:  # Boat occupies one row
            is_valid_boat = False
            boat_name = 'Unknown'
            boat_make = 'Unknown'

        sail_no = df.iloc[row_idx, 1]
        rating = df.iloc[row_idx, 3]
        dw_rating = df.iloc[row_idx, 5]

        phrf_i = float(df.iloc[row_idx, 6]) if not isinstance(df.iloc[row_idx, 6], str) else np.NAN
        phrf_j = float(df.iloc[row_idx+1, 6]) if not isinstance(df.iloc[row_idx + 1, 6], str) else np.NAN
        phrf_p = float(df.iloc[row_idx+2, 6]) if not isinstance(df.iloc[row_idx+2, 6], str) else np.NAN
        phrf_e = float(df.iloc[row_idx+3, 6]) if not isinstance(df.iloc[row_idx+3, 6], str) else np.NAN

        max_head_sail = float(df.iloc[row_idx, 7]) if not isinstance(df.iloc[row_idx, 7], str) else np.NAN
        rig_type = df.iloc[row_idx+1, 7]
        phrf_isp = float(df.iloc[row_idx+2, 7]) if not isinstance(df.iloc[row_idx+2, 7], str) else np.NAN
        phrf_jsp = float(df.iloc[row_idx+3, 7])

        phrf_loa = float(df.iloc[row_idx, 12])
        phrf_lwl = float(df.iloc[row_idx+1, 12])
        phrf_beam = float(df.iloc[row_idx+2, 12])
        phrf_draft = float(df.iloc[row_idx+3, 12])

        phrf_disp = float(df.iloc[row_idx, 13])
        if np.isnan(phrf_disp):
            phrf_disp = float(df.iloc[row_idx + 1, 13])
            phrf_ballast = float(df.iloc[row_idx+2, 13])
            if np.isnan(phrf_ballast):
                phrf_ballast = float(df.iloc[row_idx + 3, 13])
        else:
            phrf_ballast = float(df.iloc[row_idx + 1, 13])
            if np.isnan(phrf_ballast):
                phrf_ballast = float(df.iloc[row_idx + 2, 13])

        if np.isnan(phrf_disp):
            print(f'Warning: {boat_name} has no displacement')

        if is_valid_boat:
            print(f'{boat_name},{boat_make},{sail_no},{rating},{dw_rating},{phrf_i},{phrf_j},{phrf_p},{phrf_e},{max_head_sail},{phrf_isp}')

        row_idx += row_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("roster", help="PDF file containing fleet roster")

    read_fleet_roster(parser.parse_args())

