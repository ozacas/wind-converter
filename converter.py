import pandas as pd
import numpy as np
import argparse
import math
import random

def vh(u, v):
   return math.sqrt(u**2 + v**2)

def wind_direction(u, v):
    theta_vect_deg = 180.0 / math.pi * math.atan2(u, v)
    assert theta_vect_deg >= 0.0 and theta_vect_deg <= 360.0
    theta_met_deg = theta_vect_deg + 180.0
    if theta_met_deg > 360.0:
        theta_met_deg -= 360.0
    return (theta_vect_deg, theta_met_deg)

def convert(input_df):
   assert input_df is not None
   assert len(input_df) > 0

   output_rows = []
   for  _, dt, u, v in input_df.itertuples(): # ignore pandas index when unpacking tuple
       wind_azimuth, wind_dir = wind_direction(u, v)
       d = { 'date': dt,
             'WindSpeed': vh(u, v),
             'WindDirection': wind_dir }
       output_rows.append(d)
   output_df = pd.DataFrame.from_records(data=output_rows)
   assert len(output_df) == len(input_df)
   return output_df

if __name__ == "__main__":
   a = argparse.ArgumentParser(description="Convert input CSV between wind descriptors and formats")
   a.add_argument("--csv", help="Input file (CSV) []", required=True, type=str)
   a.add_argument("--out", help="Output file (CSV) to save to", type=str, default=None)
   a.add_argument("--average", help="Output is to be rolling averages of X measurements [10]", type=int, required=False)
   args = a.parse_args()
   print(args)
   in_dataframe = pd.read_csv(args.csv)
   # eg. 2020-03-27 04.00.00
   in_dataframe['datetime'] = pd.to_datetime(in_dataframe['datetime'], format='%Y-%m-%d %H.%M.%S')

   # basic validation to ensure we dont produce garbage results and types are what is expected
   columns = in_dataframe.dtypes
   is_valid_data = all(['u-comp' in columns,
                        'v-comp' in columns,
                        'datetime' in columns,
                        isinstance(columns['datetime'].type, type(np.datetime64)),
                        isinstance(columns['u-comp'].type, type(np.float64)),
                        isinstance(columns['v-comp'].type, type(np.float64))
                       ])
   assert is_valid_data # abort run iff the data is not known to be supported - stringent but thats better than making garbage

   # print an input data summary to ensure user can abort run if they see something strange
   print("**** DESCRIPTIVE STATISTICS of WIND VELOCITY COMPONENTS")
   print(in_dataframe.describe())
   out_dataframe = convert(in_dataframe)
   is_valid_output = all([ len(out_dataframe) > 0,
                          'date' in out_dataframe,
                          'WindSpeed' in out_dataframe,
                          'WindDirection' in out_dataframe,
                        ])
   assert is_valid_output

   if args.average is not None:
      out_dataframe['WindSpeed'] = out_dataframe['WindSpeed'].rolling(args.average).mean()
      out_dataframe['WindDirection'] = out_dataframe['WindDirection'].rolling(args.average).mean()
      out_dataframe = out_dataframe.iloc[args.average-1::args.average] # every tenth datapoint by default, from the tenth

   print("**** SAVING CSV TO {}".format(args.out))
   if not args.out is None:
      out_dataframe.to_csv(args.out, sep=',', float_format='%.6f', index=False) # dont write row indexes (index=False)
   else:
      print("WARNING: no output file specified (--out). Data not saved.")
   print("Run completed.")
   exit(0)
