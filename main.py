import math
import matplotlib.pyplot as plt

from pmsm_class import PMSM
from current_conversion_axis import abc_to_dq, dq_to_abc

if __name__ == "__main__":
    # 1. Define Motor and Mechanical parameters
    Ld_param = 0.005       # 5 mH
    Lq_param = 0.005       # 5 mH
    flux_link_param = 0.1  # V.s
    Rs_param = 1.0         # Ohms
    pole_pairs = 2
    J = 0.0005             # Rotor inertia (kg.m^2)
    B = 0.001              # Viscous friction (N.m.s)
    T_L = 0.5              # Constant load torque (N.m)
    
    # Initialize the PMSM model
    motor = PMSM(Ld_param, Lq_param, flux_link_param, Rs_param, pole_pairs, J, B)
    
    # Simulation parameters
    dt = 25e-6   # sample time
    t_end = 0.2  # simulate for 200 ms
    
    # Data logging arrays
    time_list = []
    Ia_list = []
    Ib_list = []
    Ic_list = []
    Torque_list = []
    speed_list = []
    
    t = 0.0
    
    # To start, motor is at 0 degrees, so theta_e = 0
    theta_e_current = 0.0 
    
    while t < t_end:
        # Generate synthetic 3-phase voltages leading electrical angle by 90 degrees
        V_mag = 100.0
        Va = V_mag * math.cos(theta_e_current + math.pi / 2.0)
        Vb = V_mag * math.cos(theta_e_current + math.pi / 2.0 - 2.0 * math.pi / 3.0)
        Vc = V_mag * math.cos(theta_e_current + math.pi / 2.0 - 4.0 * math.pi / 3.0)
        
        # 2. Convert from ABC to DQ frame
        Vd, Vq = abc_to_dq(Va, Vb, Vc, theta_e_current)
        
        # 3. Call the PMSM class in the DQ frame
        Id, Iq, Torque, omega_m, theta_e_current = motor.update(Vd, Vq, T_L, dt)
        
        # 4. Convert output currents from DQ to ABC frame
        Ia, Ib, Ic = dq_to_abc(Id, Iq, theta_e_current)
        
        # Log data for plotting
        time_list.append(t)
        Ia_list.append(Ia)
        Ib_list.append(Ib)
        Ic_list.append(Ic)
        Torque_list.append(Torque)
        speed_list.append(omega_m)
            
        t += dt
        
    # 5. Plot the results
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    # Plot phase currents
    axs[0].plot(time_list, Ia_list, label='Ia')
    axs[0].plot(time_list, Ib_list, label='Ib')
    axs[0].plot(time_list, Ic_list, label='Ic')
    axs[0].set_ylabel('Current [A]')
    axs[0].set_title('PMSM Phase Currents')
    axs[0].legend(loc='upper right')
    axs[0].grid(True)
    
    # Plot Torque
    axs[1].plot(time_list, Torque_list, 'g', label='Torque')
    axs[1].set_ylabel('Torque [Nm]')
    axs[1].set_title('Electromagnetic Torque')
    axs[1].legend(loc='upper right')
    axs[1].grid(True)
    
    # Plot Speed
    axs[2].plot(time_list, speed_list, 'r', label='Speed (omega_m)')
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Mechanical Speed\n[rad/s]')
    axs[2].set_title('Motor Speed Transient')
    axs[2].legend(loc='lower right')
    axs[2].grid(True)
    
    plt.tight_layout()
    plt.show()