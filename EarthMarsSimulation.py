# Source for data: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html

import matplotlib.pyplot as plt
from matplotlib import animation

# Variable definitions ------------------------------------------------------------------------------------------------
G               = 6.6743e-11                        # Gravitational constant [m^3*kg^(-1)*s^(-2)]
massSun         = 1.9891e30                         # Mass of the sun [kg]
massEarth       = 5.97219e24                        # Moss of the Earth [kg]
massMars        = 6.4169e23                         # Mass of Mars [kg]
secondsPerDay   = 24.0*60*60                        # Number of seconds in a day [s]
# Distances [m]
earthPerihelion = 1.47095e11                        # Earth's perihelion (shortest distance to the sun)
earthAphelion   = 1.521e11                          # Earth's aphelion (furthest distance to the sun)
marsPerihelion  = 2.0665e11                         # Mars' perihelion
marsAphelion    = 2.49261e11                        # Mars' aphelion
# Velocities [m*s^(-1)]
earthInitialVelocity   = 29290                      # Earth's velocity at aphelion (furthest from the sun)
marsInitialVelocity    = 21970                      # Mars' velocity at aphelion

# F = (G*M*m)/(r^2) [kg*m*s^(-1)]
# Finding the numerator for each body (G*M*m) [m^3*kg*s^(-2)]
gravConstEarth  = G*massEarth*massSun
gravConstMars   = G*massMars*massSun
# ---------------------------------------------------------------------------------------------------------------------

# Initial Conditions --------------------------------------------------------------------------------------------------
# For Earth
earthPosition  = [earthAphelion, 0, 0]                   # Earth's initial position vector at aphelion
earthVelocity  = [0, earthInitialVelocity, 0]            # Earth's initial velocity vector
# For Mars
marsPosition   = [marsAphelion, 0, 0]                    # Mars' initial position vector at aphelion
marsVelocity   = [0, marsInitialVelocity, 0]             # Mars' initial velocity vector
# For Sun
sunPosition    = [0, 0, 0]                               # Sun's initial position vector is the origin
sunVelocity    = [0, 0, 0]                               # Sun's initially at rest
# Time
t              = 0.0
dt             = secondsPerDay                           # Frame rate is every second
# Opening a list for each dimension containing the history of each body's position
xEarthHist, yEarthHist, zEarthHist = [],[],[]
xSunHist, ySunHist, zSunHist       = [],[],[]
xMarsHist, yMarsHist, zMarsHist    = [],[],[]
# ---------------------------------------------------------------------------------------------------------------------

# Simulation Data -----------------------------------------------------------------------------------------------------
while t<5*365.2422*secondsPerDay: #Simulating 5 years
    modulusEarth, modulusMars = 0, 0
    # Forces on Earth - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    distanceEarth = []
    for i,j in zip(earthPosition,sunPosition):
        differenceEarth = i-j
        distanceEarth.append(differenceEarth)
        modulusEarth += differenceEarth**2
    modulusEarth **= 1.5
    earthForce = [item * (-gravConstEarth/modulusEarth) for item in distanceEarth]
    
    # Update Earth's Velocity, F = m*a thus a = F/m, v = a*dt = (F/m)*dt, then update Earth's position, p = v*dt
    for i in range(3): 
        earthVelocity[i] += (dt/massEarth)*earthForce[i]
        earthPosition[i] += dt*earthVelocity[i]
    
    # Keep a history of Earth's position in each coordinate
    xEarthHist.append(earthPosition[0])
    yEarthHist.append(earthPosition[1])
    zEarthHist.append(earthPosition[2])

    # Forces on Mars - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    distanceMars = []
    for i,j in zip(marsPosition,sunPosition):
        differenceMars = i-j
        distanceMars.append(differenceMars)
        modulusMars += differenceMars**2
    modulusMars **= 1.5
    marsForce = [item * (-gravConstMars/modulusMars) for item in distanceMars]
    
    # Update Mars' Velocity then update Mars' Position
    for i in range(3): 
        marsVelocity[i] += (dt/massMars)*marsForce[i]
        marsPosition[i] += dt*marsVelocity[i]
    
    # Keep a history of Mars' position in each coordinate
    xMarsHist.append(marsPosition[0])
    yMarsHist.append(marsPosition[1])
    zMarsHist.append(marsPosition[2])
    
    # Forces on the Sun - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    enum = 0
    for i,j in zip(earthForce, marsForce):
        sunDeltaVelocity = (-dt/massSun)*(i+j)
        sunVelocity[enum] += sunDeltaVelocity
        sunPosition[enum] += dt*sunVelocity[enum]
        enum += 1
    
    # Keep a history of the sun's position in each coordinate
    xSunHist.append(sunPosition[0])
    ySunHist.append(sunPosition[1])
    zSunHist.append(sunPosition[2])

    # Update time
    t += dt
# ---------------------------------------------------------------------------------------------------------------------

# Simulation Plotting -------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10,10))
ax.set_aspect('equal')
ax.grid()

earthPath,     = ax.plot([],[],'-b',lw=1)
earthMarker,    = ax.plot([earthAphelion], [0], marker="o", markersize=12, markeredgecolor="blue", markerfacecolor="blue")
earthLabel      = ax.text(earthAphelion,0,'Earth')

marsPath,     = ax.plot([],[],'-r',lw=1)
marsMarker,    = ax.plot([marsAphelion], [0], marker="o", markersize=(0.151*12), markeredgecolor="red", markerfacecolor="red")
marsLabel      = ax.text(marsAphelion,0,'Mars')

sunPath,     = ax.plot([],[],'-g',lw=1)
sunMarker,    = ax.plot([0], [0], marker="o", markersize=20, markeredgecolor="yellow", markerfacecolor="yellow")
sunLabel      = ax.text(0,0,'Sun')

earthXPath,earthYPath = [],[]               # Earth's path in two dimensions
sunXPath,sunYPath = [],[]                   # Sun's path in two dimensions
marsXPath,marsYPath = [],[]                 # Mars' path in two dimensions

def update(i):
    earthXPath.append(xEarthHist[i])
    earthYPath.append(yEarthHist[i])
    
    marsXPath.append(xMarsHist[i])
    marsYPath.append(yMarsHist[i])

    sunXPath.append(xSunHist[i])
    sunYPath.append(ySunHist[i])
    
    earthPath.set_data(earthXPath,earthYPath)
    earthMarker.set_data(xEarthHist[i],yEarthHist[i])
    earthLabel.set_position((xEarthHist[i],yEarthHist[i]))
    
    marsPath.set_data(marsXPath,marsYPath)
    marsMarker.set_data(xMarsHist[i],yMarsHist[i])
    marsLabel.set_position((xMarsHist[i],yMarsHist[i]))
    
    sunPath.set_data(sunXPath,sunYPath)
    sunMarker.set_data(xSunHist[i],ySunHist[i])
    sunLabel.set_position((xSunHist[i],ySunHist[i]))
    
    ax.axis('equal')
    ax.set_xlim(-3*earthAphelion,3*earthAphelion)
    ax.set_ylim(-3*earthAphelion,3*earthAphelion)

    return earthPath,earthMarker,earthLabel,marsPath,marsMarker,marsLabel,sunPath,sunMarker,sunLabel

anim = animation.FuncAnimation(fig,func=update,frames=len(xEarthHist),interval=1,blit=True)
plt.show()
# ---------------------------------------------------------------------------------------------------------------------