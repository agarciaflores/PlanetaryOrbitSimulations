# Source for formulae: https://en.wikipedia.org/wiki/Semi-major_and_semi-minor_axes
# Source for data: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html

from math import sqrt
import math
import numpy as np
import matplotlib.pyplot as plt

# Variable definitions ------------------------------------------------------------------------------------------------
semiMajor = {
    'mercury':  5.7909e10,                          # Mercury's semi-major axis length [m]
    'venus':    1.0821e11,                          # Venus' semi-major axis length [m]
    'earth':    1.49598e11,                         # Earth's semi-major axis length [m]
    'mars':     2.27956e11,                         # Mars' semi-major axis length [m]
    'jupiter':  7.78479e11,                         # Jupiter's semi-major axis length [m]
    'saturn':   1.43204e12,                         # Saturn's semi-major axis length [m]
    'uranus':   2.86704e12,                         # Uranus' semi-major axis length [m]
    'neptune':  4.51495e12,                         # Neptune's semi-major axis length [m]
    'pluto':    5.869656e12                         # Pluto's semi-major axis length [m]
}
aphelion = {
    'mercury':  6.9818e10,                          # Mercury's furthest distance from the sun [m]
    'venus':    1.08941e11,                         # Venuss' furthest distance from the sun [m]
    'earth':    1.521e11,                           # Earth's furthest distance from the sun [m]
    'mars':     2.49261e11,                         # Mars' furthest distance from the sun [m]
    'jupiter':  8.16363e11,                         # Jupiter's furthest distance from the sun [m]
    'saturn':   1.50653e12,                         # Saturn's furthest distance from the sun [m]
    'uranus':   3.00139e12,                         # Uranus' furthest distance from the sun [m]
    'neptune':  4.55886e12,                         # Neptune's furthest distance from the sun [m]
    'pluto':    7.304326e12                         # Pluto's furthest distance from the sun [m]
}
perihelion = {
    'mercury':  4.6e10,                             # Mercury's closest diatance to the sun [m]
    'venus':    1.0748e11,                          # Venus' closest diatance to the sun [m]
    'earth':    1.47095e11,                         # Earth's closest diatance to the sun [m]
    'mars':     2.0665e11,                          # Mars' closest diatance to the sun [m]
    'jupiter':  7.40595e11,                         # Jupiter's closest diatance to the sun [m]
    'saturn':   1.35755e12,                         # Saturn's closest diatance to the sun [m]
    'uranus':   2.7327e12,                          # Uranus' closest diatance to the sun [m]
    'neptune':  4.47105e12,                         # Neptune's closest diatance to the sun [m]
    'pluto':    4.434987e12                         # PLuto's closest diatance to the sun [m]
}
eccentricity = {
    'mercury':  0.2056,                             # Mercury's eccentricity
    'venus':    0.0068,                             # Venus' eccentricity
    'earth':    0.0167,                             # Earth's eccentricity
    'mars':     0.0935,                             # Mars' eccentricity
    'jupiter':  0.0487,                             # Jupiter's eccentricity
    'saturn':   0.052,                              # Saturn's eccentricity
    'uranus':   0.0469,                             # Uranus' eccentricity
    'neptune':  0.0097,                             # Neptune's eccentricity
    'pluto':    0.2444                              # PLuto's eccentricity
}
# ---------------------------------------------------------------------------------------------------------------------

# Formulae ------------------------------------------------------------------------------------------------------------
# The following formula is used to compute the radius at any angle theta given the length of the semi-major and
# semi-minor axis:
# radius = (semiMajor*semiMinor)/sqrt((semiMajor*sin(theta))**2+(semiMinor*cos(theta))**2)                          (0)

# There are two ways to find the length of the semi-minor axis, one way is to find the geometric mean of the aphelion
# and perihelion:
# semiMinor = sqrt(aphelion*perihelion)                                                                             (1)
# and the other is to find it using the length of the semi-major axis and the eccentricity of the ellipse:
# semiMinor = semiMajor*sqrt(1-eccentricity**2)                                                                     (2)

# We start the program in polar coordinates, so to convert to cartesian coordinates we use the following formulae:
# x = radius*cos(theta)                                                                                             (3)
# y = radius*sin(theta)                                                                                             (4)
# ---------------------------------------------------------------------------------------------------------------------

# Calculations --------------------------------------------------------------------------------------------------------
# Here we use the two methods described above (formula 1 and formula 2) and then find their average in order to get the
# length of the semi-minor axis for each planet:
semiMinor, formula1, formula2 = {}, {}, {}
for planet in semiMajor:
    formula1[planet] = sqrt(aphelion[planet]*perihelion[planet])
    formula2[planet] = semiMajor[planet]*sqrt(1-eccentricity[planet]**2)
    semiMinor[planet] = (formula1[planet]+formula2[planet])/2

# Initializing two dictionaries, one for the radii of ellipse, and the other for the cartesian coordinates
radius, cartesian = {}, {}

# Creating a list containing the name of all planets for the legend
planetList = list(semiMajor.keys())
planetList = [word.title() for word in planetList]

# Creating an array for the angle theta
theta = np.arange(0, (2 * np.pi), 0.01)

for planet in semiMajor:
    # Giving each planet two coordinates
    cartesian[planet] = [[], []]

    # Opening a list for each planet
    radius[planet] = []

    # Here we use formula 0 to find the radius of each ellipse at every angle
    for angle in theta:
        radius[planet].append((semiMajor[planet]*semiMinor[planet])/math.sqrt((semiMajor[planet]*np.sin(angle))**2 + \
                                                                              (semiMinor[planet]*np.cos(angle))**2))
# ---------------------------------------------------------------------------------------------------------------------

# Plotting in cartesian coordinates -----------------------------------------------------------------------------------
for planet in semiMajor:
    # Iterative variable
    enum = 0

    # Converting from polar to cartesian coordinates
    for angle in theta:
        # Using formula 3 to find the x-coordinate corresponding to the given radius and theta values
        cartesian[planet][0].append(radius[planet][enum]*np.cos(angle))

        # Using formula 4 to find the y-coordinate corresponding to the given radius and theta values
        cartesian[planet][1].append(radius[planet][enum]*np.sin(angle))
        enum += 1
    plt.subplot(1, 2, 1)
    plt.plot(cartesian[planet][0], cartesian[planet][1])

plt.title("Planetary Orbit in Cartesian Coordinates")
# ---------------------------------------------------------------------------------------------------------------------

# Plotting in polar coordinates ---------------------------------------------------------------------------------------
for planet in semiMajor:
    plt.subplot(1, 2, 2, projection='polar')
    plt.polar(theta, radius[planet])

plt.title("Planetary Orbit in Polar Coordinates")
plt.legend(planetList, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, title='Planets')
plt.show()
# ---------------------------------------------------------------------------------------------------------------------