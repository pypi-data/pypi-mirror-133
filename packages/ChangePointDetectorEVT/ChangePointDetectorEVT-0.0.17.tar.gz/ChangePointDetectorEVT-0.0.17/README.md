ChangePointDetector

This module returns change points in a date time series, using Kalman filters and EVT as described in https://www.robots.ox.ac.uk/~sjrob/Pubs/LeeRoberts_EVT.pdf

1. from ChangePointDetector import ChangePointDetector
2. Prepare your time series as data plus Panda dates
3. Create  the necessary Kalman representation by creating a "session" object by calling the ChangePoint class, e.g.:
	Session=ChangePointDetector.ChangePointDetectorSession(data,dates). 
	- 'SeasonalityPeriods' is an optional input, e.g if your data is sequential months, 12 = calendar month seasonality
	- 'ForecastPeriods' is another optional input, indicating how many periods to forecast.  Default = 3
4. Determine the changepoints by running the ChangePointDetectorFunction on your "session", e.g. Results=Session.ChangePointDetectorFunction()
   This will return a "Results" object that contains the following:
	- ChangePoints. This is a list of 0s and 1s the length of the data, where 1s represent changepoints
	- Prediction. This is the Kalman smoothed actuals, plus a 3 period forecast. Note no forecast will be made if there is a changepoint in the last 3 			dates
	- PredictionVariance.  Variance of the smoothed actuals and forecast
	- ExtendedDates. These are the original dates plus 3 exta for the forecast (if a forecast has been made)
	- Trend. This is the linear change factor
	- TrendVariance. Variance of the trend