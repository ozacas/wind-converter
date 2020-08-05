import pytest
from converter import vh, wind_direction, ms_to_knots, convert
import pandas as pd

def test_vh():
   # test base case
   assert pytest.approx(vh(0.0, 0.0), 0.0)
   assert pytest.approx(vh(-0.0, 0.0), 0.0)
   # and unit vectors...
   assert pytest.approx(vh(1.0, 0.0), 1.0)
   assert pytest.approx(vh(0.0, 1.0), 1.0)
   # negative u/v values handled
   assert pytest.approx(vh(-1.0, 0.0), 1.0)
   assert pytest.approx(vh(0.0, -1.0), 1.0)

def test_wind_direction():
   # u, v, expected_vect_dir_deg, expected_met_dir_deg
   test_cases = ( (0.0, 0.0, 0.0, 0.0),
                  (1.0, 0.0, 90.0, 270.0),
                  (1.0, 1.0, 45.0, 225.0),
                  (-1.0, -1.0, 225.0, 45.0),
                  (0.0, 1.0, 0.0, 180.0),
                  (0.0, -1.0, 180.0, 0.0),
   )
   for u, v, expected_vect, expected_met in test_cases:
       result_vect, result_met = wind_direction(u, v)
       #print(result_vect, " ", result_met)
       assert pytest.approx(result_vect, expected_vect)
       assert pytest.approx(result_met, expected_met)

def test_speed_to_knots():
   assert pytest.approx(ms_to_knots(0.0), 0.0)
   assert pytest.approx(ms_to_knots(1.0), 1.93)

def test_convert():
   input_df = pd.DataFrame.from_records([ { 'datetime': '2020-08-04 00.00.00', 'u-comp': -2.0, 'v-comp': 1.0 }])
   output_df = convert(input_df)
   first_row = output_df.iloc[0]
   assert len(output_df) == 1
   assert first_row['date'] == '2020-08-04 00.00.00'
   assert pytest.approx(first_row['WindSpeed'], 4.346568)
   assert pytest.approx(first_row['WindDirection'], 116.565051)
