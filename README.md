# EPS400
To use the module, import it, and now you are able to use its functions. Give the functions the input that they need.

fit_timeseries(tlist,ylist) - accepts two lists: t (decimal year) and y (displacement timeseries) as 1-D numpy arrays, and returns the least-squares velocity and uncertainty for that timeseries. 

fit_velocities(filename) - accepts a filename, reads in the data, and uses fit_timeseries() to estimate the E, N and U components of velocity for that site.

get_coordinates(filename) - accepts a filename and returns the average latitude, longitude, and elevation for that site over the time period.

fit_all_velocities(folder,pattern) - accepts a folder name and a 'glob' pattern and returns a pandas data frame with the site name, coordinates, velocities and uncertainties.
