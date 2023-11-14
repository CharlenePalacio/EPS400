import numpy as np
import pandas as pd
from scipy import stats
import scipy.optimize
import os
import glob
''' GNSS.py '''

def my_fit_timeseries(tlist, ylist):

    m,mcov = scipy.optimize.curve_fit(myLine, tlist, ylist, p0 = [0, 0])
    
    return m[1],np.sqrt(mcov[1,1])


def myLine(t, a, b) :
    return a + b*t 


def fit_timeseries(tlist, ylist):

    slope, intercept, r_value, p_value, std_err = stats.linregress(tlist, ylist)

    # Calculate velocity and velocity uncertainty
    velocity = slope
    velocity_uncertainty = std_err

    return velocity, velocity_uncertainty

def fit_velocities(filename):

    # Load data from the file (assuming the file has three columns: time, E-displacement, N-displacement)
    data = pd.read_csv(filename,delim_whitespace=True)
    
    # Split data into time and displacement arrays
    tlist = np.array(data['yyyy.yyyy'])  # Column 1: time (decimal years)
    e_displacement = np.array(data['__east(m)'])  # Column 2: East displacement
    n_displacement = np.array(data['_north(m)'])  # Column 3: North displacement
    u_displacement = np.array(data['____up(m)'])  


    # You may need to load the Up-displacement data and calculate U velocity similarly
    # Calculate E and N velocities using fit_timeseries
    e_velocity, e_velocity_uncertainty = fit_timeseries(tlist, e_displacement)
    n_velocity, n_velocity_uncertainty = fit_timeseries(tlist, n_displacement)
    u_velocity, u_velocity_uncertainty = fit_timeseries(tlist, u_displacement)

    # You may need to calculate U velocity and its uncertainty in a similar manner

    return e_velocity, e_velocity_uncertainty, n_velocity, n_velocity_uncertainty, u_velocity, u_velocity_uncertainty

def get_coordinates(filename):
    data = pd.read_csv(filename,delim_whitespace=True)

        # Read the binary data from the file
    # with open(filename, 'rb') as file:
    #     data = file.read()

    # Use numpy.frombuffer to interpret the binary data as a NumPy array
    # You may need to specify the data type and byte order based on the format of your TENVI-3 file
    # For example, if the data is stored as 32-bit floats (single precision) in little-endian byte order:
    # data_array = np.frombuffer(data, dtype=np.float32, count=-1, offset=0, order='little')
    
    #data_array = np.frombuffer(data, dtype=np.float32, count=-1, offset=0)
    #data = pd.read_csv(filename,delim_whitespace=True)
    
    

    # Load data from the file (assuming it has columns for latitude, longitude, and elevation)
  #  data = np.loadtxt(filename)

    # Calculate the average latitude, longitude, and elevation
    latitude = np.mean(data['_latitude(deg)'])
    longitude = np.mean(data['_longitude(deg)'])
    elevation = np.mean(data['__height(m)'])

    return latitude, longitude, elevation

def fit_all_velocities(folder, pattern):

    # Initialize lists to store results
    site_names = []
    latitudes = []
    longitudes = []
    elevations = []
    e_velocities = []
    e_velocity_uncertainties = []
    n_velocities = []
    n_velocity_uncertainties = []
    u_velocities = []
    u_velocity_uncertainties = []

    # Find files matching the pattern in the specified folder
    file_list = glob.glob(os.path.join(folder, pattern))
    
    print('file list: ')
    print(file_list)

    # Loop through each data file
    for file_name in file_list:
        # Extract site name from the file name (you may need to adjust this based on your file naming convention)
        site_name = os.path.splitext(os.path.basename(file_name))[0]

        # Get coordinates for the site
        latitude, longitude, elevation = get_coordinates(file_name)

        # Get velocities and uncertainties for the site
        e_velocity, e_velocity_uncertainty, n_velocity, n_velocity_uncertainty, u_velocity, u_velocity_uncertainty = fit_velocities(file_name)

        # Append results to lists
        site_names.append(site_name)
        latitudes.append(latitude)
        longitudes.append(longitude)
        elevations.append(elevation)
        e_velocities.append(e_velocity)
        e_velocity_uncertainties.append(e_velocity_uncertainty)
        n_velocities.append(n_velocity)
        n_velocity_uncertainties.append(n_velocity_uncertainty)
        u_velocities.append(u_velocity)
        u_velocity_uncertainties.append(u_velocity_uncertainty)

    # Create a DataFrame from the results
    result_df = pd.DataFrame({
        'Site': site_names,
        'Latitude': latitudes,
        'Longitude': longitudes,
        'E Velocity': e_velocities,
        'E Velocity Uncertainty': e_velocity_uncertainties,
        'N Velocity': n_velocities,
        'N Velocity Uncertainty': n_velocity_uncertainties,
        'U Velocity': u_velocities,
        'U Velocity Uncertainty': u_velocity_uncertainties
    })

    return result_df

def fit_tide_gauge(filename) :

    file = pd.read_csv(filename, header=None, sep = ';')
    # get the t list and the y list
    tlist = file[0]
    ylist = file[1]
    
    return fit_timeseries(tlist,ylist);

def fit_all_velocities2(folder, pattern, type):
    site_names = []
    latitudes = []
    longitudes = []
    elevations = []
    velocities = []
    velocity_uncertainties = []
    e_velocities = []
    e_velocity_uncertainties = []
    n_velocities = []
    n_velocity_uncertainties = []
    u_velocities = []
    u_velocity_uncertainties = []

    file_list = glob.glob(os.path.join(folder, pattern))
    
    print('file list:')
    print(file_list)

    for file_name in file_list:
        site_name = os.path.splitext(os.path.basename(file_name))[0]
        
        if type == "GNSS":
            e_velocity, e_velocity_uncertainty, n_velocity, n_velocity_uncertainty, u_velocity, u_velocity_uncertainty = fit_velocities(file_name)
            latitude, longitude, elevation = get_coordinates(file_name)
            site_names.append(site_name)
            latitudes.append(latitude)
            longitudes.append(longitude)
            elevations.append(elevation)
            e_velocities.append(e_velocity)
            e_velocity_uncertainties.append(e_velocity_uncertainty)
            n_velocities.append(n_velocity)
            n_velocity_uncertainties.append(n_velocity_uncertainty)
            u_velocities.append(u_velocity)
            u_velocity_uncertainties.append(u_velocity_uncertainty)

        elif type == "tide":
            print("tide:", file_name)
            velocity, velocity_uncertainty = fit_tide_gauge(file_name)
            site_names.append(site_name)
            velocities.append(velocity)
            velocity_uncertainties.append(velocity_uncertainty)
    
    if type == "GNSS":
        
        result_df = pd.DataFrame({
            'Site': site_names,
            'Latitude': latitudes,
            'Longitude': longitudes,
            'E Velocity': e_velocities,
            'E Velocity Uncertainty': e_velocity_uncertainties,
            'N Velocity': n_velocities,
            'N Velocity Uncertainty': n_velocity_uncertainties,
            'U Velocity': u_velocities,
            'U Velocity Uncertainty': u_velocity_uncertainties
        })
    elif type == "tide":
        result_df = pd.DataFrame({
            'Site': site_names,
            'Velocity': velocities,
            'Velocity Uncertainty': velocity_uncertainties,
        })
    
    return result_df