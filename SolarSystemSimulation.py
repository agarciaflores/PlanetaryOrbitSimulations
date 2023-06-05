# Source for data: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html

import matplotlib.pyplot as plt
from matplotlib import animation

# Variable definitions ------------------------------------------------------------------------------------------------
G               = 6.6743e-11                        # Gravitational constant [m^3*kg^(-1)*s^(-2)]
secondsPerDay   = 24.0*60*60                        # Number of seconds in a day [s]
mass = {
    'sun':      1.9891e30,                          # Mass of the sun [kg]
    'mercury':  3.3010e23,                          # Mass of Mercury [kg]
    'venus':    4.8673e24,                          # Mass of Venus [kg]
    'earth':    5.97219e24,                         # Moss of the Earth [kg]
    'mars':     6.4169e23,                          # Mass of Mars [kg]
    'jupiter':  1.89813e27,                         # Mass of Jupiter [kg]
    'saturn':   5.6832e26,                          # Mass of Saturn [kg]
    'uranus':   8.6881e25,                          # Mass of Uranus [kg]
    'neptune':  1.02409e26,                         # Mass of Neptune [kg]
    'pluto':    1.303e22                            # Mass of Pluto [kg]
}
aphelion = {
    'mercury':  6.9818e10,                          # Mercury's furthest distance from the sun [m]
    'venus':    1.08941e11,                         # Venus' furthest distance from the sun [m]
    'earth':    1.521e11,                           # Earth's furthest distance from the sun [m]
    'mars':     2.49261e11,                         # Mars' furthest distance from the sun [m]
    'jupiter':  8.16363e11,                         # Jupiter's furthest distance from the sun [m]
    'saturn':   1.50653e12,                         # Saturn's furthest distance from the sun [m]
    'uranus':   3.00139e12,                         # Uranus' furthest distance from the sun [m]
    'neptune':  4.55886e12,                         # Neptune's furthest distance from the sun [m]
    'pluto':    7.304326e12                         # Pluto's furthest distance from the sun [m]
}
initialVelocity = {
    'mercury':  3.866e4,                            # Mercury's velocity at aphelion [m*s^(-1)]
    'venus':    3.478e4,                            # Venus' velocity at aphelion [m*s^(-1)]
    'earth':    2.929e4,                            # Earth's velocity at aphelion [m*s^(-1)]
    'mars':     2.197e4,                            # Mars' velocity at aphelion [m*s^(-1)]
    'jupiter':  1.244e4,                            # Jupiter's velocity at aphelion [m*s^(-1)]
    'saturn':   9.14e3,                             # Saturn's velocity at aphelion [m*s^(-1)]
    'uranus':   6.49e3,                             # Uranus' velocity at aphelion [m*s^(-1)]
    'neptune':  5.37e3,                             # Neptune's velocity at aphelion [m*s^(-1)]
    'pluto':    3.71e3                              # PLuto's velocity at aphelion [m*s^(-1)]
}
# ---------------------------------------------------------------------------------------------------------------------

# Force definitions ---------------------------------------------------------------------------------------------------
# First opening a dictionry for the gravitational force between each body and opening an additional dictionary for
# position history of each body
grav = {}
history = {}

# F = (G*M*m)/(r^2) [kg*m*s^(-1)]
# Finding the numerator for each body (G*M*m) [m^3*kg*s^(-2)]
for planet, value in mass.items():
    grav[planet+'Sun'] = G*value*mass['sun']
    #The position history is in three dimensions:
    history[planet] = [[],[],[]]
grav.pop('sunSun')

# Initializing a dictionary for the denominator (r^2) [m^2]
modulus = {}

# Initializing a dictionary for force on each body, with only the sun being definied initially
force = {
    'sun': [0,0,0]
}
# ---------------------------------------------------------------------------------------------------------------------

# Initial Conditions --------------------------------------------------------------------------------------------------
# Setting the initial position for each body
# [Note: Here the initial position for each planet is along the x-axis]
position = {
    'sun': [0, 0, 0]
}
for planet, value in aphelion.items():
    position[planet] = [value, 0, 0]

# Setting the initial vcelocity for each body
velocity = {
    'sun': [0, 0, 0]
}
for planet, value in initialVelocity.items():
    velocity[planet] = [0, value, 0]

# Time
t   = 0.0
dt  = secondsPerDay                                 # Frame rate is every second
# ---------------------------------------------------------------------------------------------------------------------

# Simulation Data -----------------------------------------------------------------------------------------------------
while t<5*365.422*secondsPerDay: #Simulating 5 years
    # Initializing a dictionary for the distance between the sun and each planet [m]
    distance = {}

    for planet in aphelion:
        # Resetting the modulus and distance to naught
        modulus[planet] = 0                         # [m]
        distance[planet] = []                       # [m]

        for i,j in zip(position[planet],position['sun']):
            difference = i-j                        # [m]
            distance[planet].append(difference)     # [m]
            modulus[planet] += difference**2        # [m^2]

        # Since the distance is in three dimensions, the total distance is (x^2+y^2+z^2)^0.5
        # however, here we do (x^2+y^2+z^2)^1.5
        modulus[planet] **= 1.5                     # [m^3]
        # because we multiply by an additional distance in the numerator here
        force[planet] = [item * (-grav[planet+'Sun']/modulus[planet]) for item in distance[planet]]
        # leaving dimensions of [kg*m*s^(-2)]

        # Updating the position for each planet
        for i in range(3): 
            # v = (s*kg^(-1))*(kg*m*s^(-2)) = m*s^(-1)
            velocity[planet][i] += (dt/mass[planet])*force[planet][i]
            # p = (s)*(m*s^(-1)) = m
            position[planet][i] += dt*velocity[planet][i]
            history[planet][i].append(position[planet][i])
            # The force on the sun is the sum of all forces on the planets from the sun, but negative (seen down below)
            force['sun'][i] += force[planet][i]
            

    # Forces on the Sun - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Updating the position of the sun
    for i in range(3):
        # Here we introduce the negative sign mentioned in line 118
        velocity['sun'][i] += (-dt/mass['sun'])*force['sun'][i]
        position['sun'][i] += dt*velocity['sun'][i]
        history['sun'][i].append(position['sun'][i])

    # Update time
    t += dt
# ---------------------------------------------------------------------------------------------------------------------

print('Data Collection Ready')

# Simulation Plot -----------------------------------------------------------------------------------------------------
fig = plt.figure(figsize=(10,10))
ax = plt.axes()
ax.axis('auto')
ax.grid()

# Establishing the trace, marker, and label for each body
mercuryPath,    = ax.plot([],[],'-g',lw=1)
mercuryMarker,  = ax.plot([aphelion['mercury']], [0], marker="o", markersize=2, markeredgecolor="mediumblue", markerfacecolor="mediumblue")
mercuryLabel    = ax.text(aphelion['mercury'],0,'Mercury')

venusPath,      = ax.plot([],[],'-g',lw=1)
venusMarker,    = ax.plot([aphelion['venus']], [0], marker="o", markersize=4, markeredgecolor="orange", markerfacecolor="orange")
venusLabel      = ax.text(aphelion['venus'],0,'Venus')

earthPath,      = ax.plot([],[],'-g',lw=1)
earthMarker,    = ax.plot([aphelion['earth']], [0], marker="o", markersize=5, markeredgecolor="blue", markerfacecolor="blue")
earthLabel      = ax.text(aphelion['earth'],0,'Earth')

marsPath,       = ax.plot([],[],'-g',lw=1)
marsMarker,     = ax.plot([aphelion['mars']], [0], marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
marsLabel       = ax.text(aphelion['mars'],0,'Mars')

jupiterPath,    = ax.plot([],[],'-g',lw=1)
jupiterMarker,  = ax.plot([aphelion['jupiter']], [0], marker="o", markersize=9, markeredgecolor="burlywood", markerfacecolor="burlywood")
jupiterLabel    = ax.text(aphelion['jupiter'],0,'Jupiter')

saturnPath,     = ax.plot([],[],'-g',lw=1)
saturnMarker,   = ax.plot([aphelion['saturn']], [0], marker="o", markersize=8, markeredgecolor="beige", markerfacecolor="beige")
saturnLabel     = ax.text(aphelion['saturn'],0,'Saturn')

uranusPath,     = ax.plot([],[],'-g',lw=1)
uranusMarker,   = ax.plot([aphelion['uranus']], [0], marker="o", markersize=7, markeredgecolor="turquoise", markerfacecolor="turquoise")
uranusLabel     = ax.text(aphelion['uranus'],0,'Uranus')

neptunePath,    = ax.plot([],[],'-g',lw=1)
neptuneMarker,  = ax.plot([aphelion['neptune']], [0], marker="o", markersize=6, markeredgecolor="lightsteelblue", markerfacecolor="lightsteelblue")
neptuneLabel    = ax.text(aphelion['neptune'],0,'Neptune')

plutoPath,      = ax.plot([],[],'-g',lw=1)
plutoMarker,    = ax.plot([aphelion['pluto']], [0], marker="o", markersize=1, markeredgecolor="brown", markerfacecolor="brown")
plutoLabel      = ax.text(aphelion['pluto'],0,'Pluto')

sunPath,        = ax.plot([],[],'-g',lw=1)
sunMarker,      = ax.plot([0], [0], marker="o", markersize=10, markeredgecolor="yellow", markerfacecolor="yellow")
sunLabel        = ax.text(0,0,'Sun')

# Initializing a list for the position of each body in two dimensions
mercuryXPath, mercuryYPath  = [], []
venusXPath, venusYPath      = [], []
earthXPath,earthYPath       = [], []
marsXPath,marsYPath         = [], []
jupiterXPath, jupiterYPath  = [], []
saturnXPath, saturnYPath    = [], []
uranusXPath, uranusYPath    = [], []
neptuneXPath, neptuneYPath  = [], []
plutoXPath, plutoYPath      = [], []
sunXPath,sunYPath           = [], []

# Defnining a function for the simulation
def update(i):
    # This function pulls values from the history dictionary and adds them to the paths of the corresponding body
    mercuryXPath.append(history['mercury'][0][i])
    mercuryYPath.append(history['mercury'][1][i])

    venusXPath.append(history['venus'][0][i])
    venusYPath.append(history['venus'][1][i])

    earthXPath.append(history['earth'][0][i])
    earthYPath.append(history['earth'][1][i])
    
    marsXPath.append(history['mars'][0][i])
    marsYPath.append(history['mars'][1][i])

    jupiterXPath.append(history['jupiter'][0][i])
    jupiterYPath.append(history['jupiter'][1][i])

    saturnXPath.append(history['saturn'][0][i])
    saturnYPath.append(history['saturn'][1][i])

    uranusXPath.append(history['uranus'][0][i])
    uranusYPath.append(history['uranus'][1][i])

    neptuneXPath.append(history['neptune'][0][i])
    neptuneYPath.append(history['neptune'][1][i])

    plutoXPath.append(history['pluto'][0][i])
    plutoYPath.append(history['pluto'][1][i])

    sunXPath.append(history['sun'][0][i])
    sunYPath.append(history['sun'][1][i])

    mercuryPath.set_data(mercuryXPath,mercuryYPath)
    mercuryMarker.set_data(history['mercury'][0][i],history['mercury'][1][i])
    mercuryLabel.set_position((history['mercury'][0][i],history['mercury'][1][i]))

    venusPath.set_data(venusXPath,venusYPath)
    venusMarker.set_data(history['venus'][0][i],history['venus'][1][i])
    venusLabel.set_position((history['venus'][0][i],history['venus'][1][i]))

    earthPath.set_data(earthXPath,earthYPath)
    earthMarker.set_data(history['earth'][0][i],history['earth'][1][i])
    earthLabel.set_position((history['earth'][0][i],history['earth'][1][i]))
    
    marsPath.set_data(marsXPath,marsYPath)
    marsMarker.set_data(history['mars'][0][i],history['mars'][1][i])
    marsLabel.set_position((history['mars'][0][i],history['mars'][1][i]))

    jupiterPath.set_data(jupiterXPath,jupiterYPath)
    jupiterMarker.set_data(history['jupiter'][0][i],history['jupiter'][1][i])
    jupiterLabel.set_position((history['jupiter'][0][i],history['jupiter'][1][i]))

    saturnPath.set_data(saturnXPath,saturnYPath)
    saturnMarker.set_data(history['saturn'][0][i],history['saturn'][1][i])
    saturnLabel.set_position((history['saturn'][0][i],history['saturn'][1][i]))

    uranusPath.set_data(uranusXPath,uranusYPath)
    uranusMarker.set_data(history['uranus'][0][i],history['uranus'][1][i])
    uranusLabel.set_position((history['uranus'][0][i],history['uranus'][1][i]))

    neptunePath.set_data(neptuneXPath,neptuneYPath)
    neptuneMarker.set_data(history['neptune'][0][i],history['neptune'][1][i])
    neptuneLabel.set_position((history['neptune'][0][i],history['neptune'][1][i]))

    plutoPath.set_data(plutoXPath,plutoYPath)
    plutoMarker.set_data(history['pluto'][0][i],history['pluto'][1][i])
    plutoLabel.set_position((history['pluto'][0][i],history['pluto'][1][i]))
    
    sunPath.set_data(sunXPath,sunYPath)
    sunMarker.set_data(history['sun'][0][i],history['sun'][1][i])
    sunLabel.set_position((history['sun'][0][i],history['sun'][1][i]))
    
    # Defining the axis of the graph
    ax.axis('equal')
    # The x- and y-axis are set to Pluto's furthest distance from the sun
    ax.set_xlim(-aphelion['pluto'],aphelion['pluto'])
    ax.set_ylim(-aphelion['pluto'],aphelion['pluto'])

    return mercuryPath,mercuryMarker,mercuryLabel,venusPath,venusMarker,venusLabel,earthPath,earthMarker,earthLabel,\
        marsPath,marsMarker,marsLabel,jupiterPath,jupiterMarker,jupiterLabel,saturnPath,saturnMarker,saturnLabel,\
            uranusPath,uranusMarker,uranusLabel,neptunePath,neptuneMarker,neptuneLabel,\
                plutoPath,plutoMarker,plutoLabel,sunPath,sunMarker,sunLabel

anim = animation.FuncAnimation(fig,func=update,frames=len(history['pluto'][0]),interval=1,blit=True)
plt.show()
# ---------------------------------------------------------------------------------------------------------------------