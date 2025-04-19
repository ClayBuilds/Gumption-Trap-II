# This file includes some functions for parsing and manipulating sensor data 
# for the current/voltage sensors, gps path, control variables, other logged data
import matplotlib.pyplot as plt
import numpy as np

def parseBB(raw_blackbox):
    time = []    #seconds since startup
    state = []   #0 manual, 1 auto
    lat = []     #latitude
    long = []    #longitude
    chead = []   #current heading
    ghead = []   #goal heading
    tpoint = []  #target waypoitn #
    PIDO = []    #pid output
    pport = []   #PWM signal to port motor
    pstar = []   #PWM signal to starboard motor
    prud = []    #PWM signal to rudder
    Imot = []    #current drawn by load
    vbat = []    #voltage measured at battery connection point
    Isol = []    #current coming from solar panel
    vsol = []    #voltage measured from input on solar charge controller

    for bb in raw_blackbox:
        time.append(bb[0])
        state.append(bb[1])
        lat.append(bb[2])
        long.append(bb[3])
        chead.append(bb[4])
        ghead.append(bb[5])
        tpoint.append(bb[6])
        PIDO.append(bb[7])
        pport.append(bb[8])
        pstar.append(bb[9])
        prud.append(bb[10])
        Imot.append(bb[11]/1000) #convert mA to A
        vbat.append(bb[12]/1000) #convert mV to V
        Isol.append(bb[13]/1000)
        vsol.append(bb[14]/1000)

    #time may have some discontinuities from the boat being turned off and back on. make it all continuous here
    lastmaxt = 0
    for i in range(1,len(time)):
        lastt = time[i-1]
        if(time[i] < (lastt - lastmaxt)):
            lastmaxt += lastt
        time[i] += lastmaxt

    #collect the indexes where it's in manual mode
    imanual = []
    for i , s in enumerate(state):
        if s == 0:
            imanual.append(i)

    bbdata = [time, state, lat, long, chead, ghead, tpoint, PIDO, pport, pstar, prud, Imot, vbat, Isol, vsol, imanual]
    return bbdata

#plot all the data
def plotbb(bbdata):
    #Power consumption plots
    fig, axs = plt.subplots(2, 1, figsize = (12, 8))
    axs[0].plot(bbdata[0], bbdata[13], color = 'green', label = 'Panel Supply')
    axs[0].plot(bbdata[0], bbdata[11], color = 'red', label = 'System Draw')
    dI = [Iin - Iout for Iin, Iout in zip(bbdata[13], bbdata[11])]
    axs[0].plot(bbdata[0], dI, color = 'black', label = 'Net to battery')
    axs[0].legend()
    axs[0].set_ylabel('Current (A)')
    axs[0].set_xlabel('Time (s)')

    W = [V*I for V, I in zip(bbdata[12], dI)] #power in watts to battery
    Thours = max(bbdata[0])/3600
    netpower = (sum(W)/len(W))*Thours
    netah = netpower/(sum(bbdata[12])/len(bbdata[12])) #net amphours

    axs[0].set_title(f'Power Consumption vs Time. Net to Battery = {netpower:.2f} Wh or {netah:.2f} Ah')

    axs[1].set_title('Battery Voltage Over Time')
    axs[1].plot(bbdata[0], bbdata[12], color = 'blue')
    axs[1].set_ylabel('Battery Voltage (V)')
    axs[1].set_xlabel('Time (s)')

    #PWM Plots
    fig, axs = plt.subplots(2, 1, figsize = (12, 8))
    axs[0].set_title('Motor PWM (Auto Mode Only)')

    # Convert to NumPy arrays
    bbdata[8] = np.array(bbdata[8], dtype=float)
    bbdata[9] = np.array(bbdata[9], dtype=float)
    bbdata[10] = np.array(bbdata[10], dtype=float)
    bbdata[15] = np.array(bbdata[15])

    i2kill = bbdata[15]

    pwmtime = np.delete(bbdata[0], i2kill, 0)
    pwmP = np.delete(bbdata[8], i2kill, 0)
    pwmS = np.delete(bbdata[9], i2kill, 0)
    pwmR = np.delete(bbdata[10], i2kill, 0)

    axs[0].scatter(pwmtime, pwmP, color = 'blue', label = 'Port')
    axs[0].scatter(pwmtime, pwmS, color = 'orange', label = 'Starboard')
    axs[0].legend()
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Pulse Width (µS)')


    axs[1].set_title('Rudder PWM (Auto Mode Only)')
    axs[1].set_ylabel('Pulse Width (µS)')
    axs[1].scatter(pwmtime, pwmR, color = 'violet')
    axs[1].set_xlabel('Time (s)')

    #PID Plots
    fig, axs = plt.subplots(2, 1, figsize = (12, 8))
    axs[0].set_title('Actual Vs Goal Heading (Auto Mode Only)')

    # Convert to NumPy arrays
    bbdata[8] = np.array(bbdata[4], dtype=float)
    bbdata[9] = np.array(bbdata[5], dtype=float)
    bbdata[10] = np.array(bbdata[7], dtype=float)
 
    Hac = np.delete(bbdata[4], i2kill, 0)
    Hgo = np.delete(bbdata[5], i2kill, 0)
    Po = np.delete(bbdata[7], i2kill, 0)

    axs[0].scatter(pwmtime, Hac, color = 'blue', label = 'Actual')
    axs[0].scatter(pwmtime, Hgo, color = 'orange', label = 'Goal')
    axs[0].legend()
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Compass Heading (Degrees)')


    axs[1].set_title('PID Steering Output')
    axs[1].set_ylabel('%')
    axs[1].scatter(pwmtime, pwmR, color = 'violet')
    axs[1].set_xlabel('Time (s)')

    plt.tight_layout()
    plt.show()