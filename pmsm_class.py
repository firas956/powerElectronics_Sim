class PMSM:
    """
    Simulation of a Permanent Magnet Synchronous Motor (PMSM)
    Operates entirely in the DQ reference frame.
    """
    def __init__(self, Ld, Lq, flux_linkage, Rs, pole_pairs, J, B):
        # Electrical parameters
        self.Ld = Ld
        self.Lq = Lq
        self.flux_linkage = flux_linkage
        self.Rs = Rs
        
        # Mechanical parameters
        self.pole_pairs = pole_pairs
        self.J = J
        self.B = B
        
        # State variables for dq currents
        self.Id = 0.0
        self.Iq = 0.0
        
        # Mechanical state variables
        self.omega_m = 0.0  # Mechanical angular velocity (rad/s)
        self.theta_m = 0.0  # Mechanical angle (rad)
        
        # Output variables
        self.Torque = 0.0

    def update(self, Vd, Vq, T_L, dt):
        """
        Evaluate the motor model for the given voltages and load torque.
        Updates internal electrical and mechanical states.
        
        Returns:
            Id, Iq, Torque, omega_m, theta_e
        """
        # Electrical speed and angle
        omega_e = self.omega_m * self.pole_pairs
        theta_e = self.theta_m * self.pole_pairs

        # 1. Compute derivatives based on the PMSM electrical equations in dq-axis
        dId_dt = (Vd + omega_e * self.Lq * self.Iq - self.Rs * self.Id) / self.Ld
        dIq_dt = (Vq - omega_e * self.Ld * self.Id - omega_e * self.flux_linkage - self.Rs * self.Iq) / self.Lq
        
        # 2. Euler integration to update currents
        self.Id += dId_dt * dt
        self.Iq += dIq_dt * dt
        
        # 3. Calculate electromagnetic torque
        self.Torque = 1.5 * self.pole_pairs * (self.flux_linkage * self.Iq + (self.Ld - self.Lq) * self.Iq * self.Id)
        
        # 4. Integrate mechanical equations (Euler method)
        # d(omega_m)/dt = (Torque - Load Torque - Friction) / Inertia
        domega_m_dt = (self.Torque - T_L - self.B * self.omega_m) / self.J
        
        self.omega_m += domega_m_dt * dt
        self.theta_m += self.omega_m * dt
        
        # Update electrical angle to return
        theta_e = self.theta_m * self.pole_pairs
            
        return self.Id, self.Iq, self.Torque, self.omega_m, theta_e
