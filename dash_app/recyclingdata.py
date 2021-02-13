from pathlib import Path

import pandas as pd


class RecyclingData:
    """Class for retrieving and structuring the data."""

    def __init__(self):
        self.recycling = pd.DataFrame()
        self.area_list = []
        self.recycling_eng = []
        self.compare_to_eng = 0
        self.recycling_area = []
        self.best_rate = 0
        self.best_period = 0
        self.change_area = 0
        self.get_data()

    def get_data(self):
        data_folder = Path('../data')
        csv_file = 'household_recycling.csv'
        self.recycling = pd.read_csv(data_folder / csv_file)
        self.area_list = self.recycling["Area"].unique().tolist()

    def process_data_for_area(self, area):
        # Data for England
        self.recycling_eng = self.recycling.loc[self.recycling['Area'] == 'England']
        by_yr_e = self.recycling_eng.sort_values('Year', ascending=False)
        by_yr_e = by_yr_e.reset_index(drop=True)

        # Data for the selected area
        self.recycling_area = self.recycling.loc[self.recycling['Area'] == area]
        # Calculate the change from the previous year
        by_yr = self.recycling_area.sort_values('Year', ascending=False)
        by_yr = by_yr.reset_index(drop=True)
        self.change_area = by_yr.iloc[0, 3] - by_yr.iloc[1, 3]
        self.compare_to_eng = by_yr.iloc[0, 3] - by_yr_e.iloc[0, 3]
        # Calculate the best year, use most recent if there are more than one years with the same rate
        sort = self.recycling_area.sort_values(['Recycling_Rates', 'Year'], ascending=[False, False])
        sort = sort.reset_index(drop=True)
        self.best_rate = sort.iloc[0, 3]
        self.best_period = sort.iloc[0, 2]
