from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd


class DataProcessor:
    def __init__(self) -> None:
        pass

    def read_files(self, files) -> pd.DataFrame:
        var_df = pd.DataFrame()
        explain_df = pd.DataFrame()
        for file in files:
            if "ScenarioDate" in file:
                explain_df = explain_df.append(
                    self.read_explain_file(file), ignore_index=True
                )
            else:
                var_df = var_df.append(self.read_var_file(file), ignore_index=True)
        return var_df, explain_df

    def read_var_file(self, file) -> pd.DataFrame:
        filepath = Path(file)
        filename = filepath.stem
        filename_array = filename.split("_")
        calculation_date = datetime.strptime(filename_array[2], "%Y%m%d")
        risk_type = filename_array[0]
        df = pd.read_csv(file, parse_dates=["Trading Day"], low_memory=False)
        scenario_date = datetime.strptime(df.columns[-1], "%m/%d/%Y")
        df = df.iloc[:, :-1]
        df = df.drop(
            [
                "T:MeteorId",
                "Met Prod Type",
                "Meteor Underlying",
                "Folder",
                "MVar",
                "CVar",
                "Pv Without Cost",
                "Pv Local",
                "Leg Id",
                "Parent Id",
            ],
            axis=1,
        )
        df.loc[df["Trading Day"] == calculation_date, "IsNewTrade"] = True
        df.loc[df["Trading Day"] != calculation_date, "IsNewTrade"] = False
        df["Calculation Date"] = calculation_date
        df["Scenario"] = scenario_date
        df["Pathfile"] = file
        df["Risk Type"] = risk_type
        return df

    def read_explain_file(self, file) -> pd.DataFrame:
        filepath = Path(file)
        filename = filepath.stem
        filename_array = filename.split("_")
        calculation_date = datetime.strptime(filename_array[2], "%Y%m%d")
        risk_type = filename_array[0]
        df = pd.read_csv(
            file,
            parse_dates=["Underlier Date"],
            dtype={"Volatility Sub Type": str, "Vol Strike": str},
            low_memory=False,
        )
        df["Perturbation Type"] = df["Perturbation Type"].str.replace("Quote", "Fx")
        df["Explain"] = df["Delta Pl"] + df["Vega Pl"] + df["Gamma Pl"]
        df["Sensitivities"] = (
            df["Delta"]
            + df["Vega"]
            + df["Gamma"]
            + df["Today Delta"]
            + df["Today Vega"]
            + df["Today Gamma"]
        )
        df = df.drop(
            [
                "Pl",
                "Delta Pl",
                "Vega Pl",
                "Gamma Pl",
                "Delta",
                "Vega",
                "Gamma",
                "Today Delta",
                "Today Vega",
                "Today Gamma",
            ],
            axis=1,
        )
        scenario_date = datetime.strptime(filename_array[4], "%Y%m%d")
        df = df.rename(
            columns={
                "Commodity:Family": "Commodity Family",
                "Commodity:Commodity Unit Family": "Commodity Unit Family",
                "Commodity:Commodity Long Name": "Commodity Long Name",
                "Commodity:Commodity Type": "Commodity Type",
                "Commodity:Lots Size": "Commodity Lots Size",
                "Commodity:Commodity Reference": "Commodity Reference",
                "Commodity:Risk Unit": "Risk Unit",
                "B:Division Id": "Division Id",
                "B:Desk Id": "Desk Id",
                "B:GOP Name": "GOP Name",
            }
        )
        df["Shock Tenor"] = (
            df["Underlier Date"] - calculation_date
        ).dt.days - self._get_tenor_shift(calculation_date)
        df["Calculation Date"] = calculation_date
        df["Scenario"] = scenario_date
        df["Pathfile"] = file
        df["Risk Type"] = risk_type
        return df

    def _get_tenor_shift(self, date) -> int:
        weekday = date.strftime("%w")
        yesterday = 1
        if weekday == "5":
            yesterday = 3
        return yesterday
