import pandas as pd
import numpy as np
from pickle import dump

class Watershed:

    def __init__(self, **kwargs):
        """"""
        self.id = (int)(kwargs["id"]) # 编号
        self.name = kwargs["子流域名"] # 名称
        self.region = kwargs["流域名"] # 所属的大型流域
        self.resolution = (int)(kwargs["resolution"]) # 数据分辨率

        self.height = kwargs["h_mean"]
        self.height_std = kwargs["h_std"]
        self.height_min = kwargs["h_min"]
        self.height_max = kwargs["h_max"]
        self.area = kwargs["area"]
        self.length = kwargs["length"]
        self.density = self.area / self.length

        self.slope = kwargs["slope_mean"]
        self.SCA = kwargs["SCA_mean"]
        self.TWI = kwargs["TWI_mean"]

        self.clay = np.mean([kwargs["Clay_1"], kwargs["Clay_2"], kwargs["Clay_3"], kwargs["Clay_4"], kwargs["Clay_5"], kwargs["Clay_6"]])
        self.sand = np.mean([kwargs["Sand_1"], kwargs["Sand_2"], kwargs["Sand_3"], kwargs["Sand_4"], kwargs["Sand_5"], kwargs["Sand_6"]])
        self.silt = np.mean([kwargs["Silt_1"], kwargs["Silt_2"], kwargs["Silt_3"], kwargs["Silt_4"], kwargs["Silt_5"], kwargs["Silt_6"]])

        self.ndvi_trend = kwargs["ndvi_trend"]
        self.ndvi_1 = kwargs["ndvi_season1"]
        self.ndvi_2 = kwargs["ndvi_season2"]
        self.ndvi_3 = kwargs["ndvi_season3"]
        self.ndvi_4 = kwargs["ndvi_season4"]
        self.cropland = kwargs["Cropland"]
        self.urban = kwargs["Urban_and_built_up"]

        self.runoff = kwargs["径流系数"] # 径流系数
        self.baseflow = kwargs["基流系数"] # 基流系数
        self.recession_early = kwargs["退水系数early"] # 退水系数early
        self.recession_custom = kwargs["退水系数custom"] # 退水系数custom
        self.recession_late = kwargs["退水系数late"] # 退水系数late


    def __str__(self):
        """"""
        return "[Watershed %d] %s in %s, resolution=%d" % (self.id, self.name, self.region, self.resolution)


    def feature_S(self, full=True):
        """下垫面特征"""
        if full:
            return np.array([
                self.height,
                self.density,
                self.slope,
                self.TWI,
                self.clay,
                self.sand,
                self.silt,
                self.ndvi_trend,
                self.ndvi_1,
                self.ndvi_2,
                self.ndvi_3,
                self.ndvi_4,
                self.cropland,
                self.urban,
            ]) # (14)
        else:
            return np.array([
                self.height,
                self.density,
                self.slope,
                self.TWI,
            ]) # (4)


    def feature_H(self):
        """水文特征"""
        return np.array([
            self.runoff,
            self.baseflow,
            self.recession_early,
            self.recession_custom,
            self.recession_late
        ]) # (5)


if __name__ == "__main__":

    xls = pd.ExcelFile("./data/Watersheds.xlsx")
    for sheet in xls.sheet_names:
        df = pd.read_excel(io=xls, sheet_name=sheet)
        for _, row in df.iterrows():
                ws = Watershed(**row)
                with open("./cache/%d_r=%d" % (ws.id, ws.resolution), "wb") as f:
                    dump(ws, f)
