import math

def abc_to_dq(A, B, C, theta_e):
    """Clarke and Park transform from ABC to DQ frame."""
    sqrt_2_3 = math.sqrt(2.0 / 3.0)
    pi_2_3 = 2.0 * math.pi / 3.0
    
    D = sqrt_2_3 * (math.cos(theta_e) * A + math.cos(theta_e - pi_2_3) * B + math.cos(theta_e + pi_2_3) * C)
    Q = sqrt_2_3 * (-math.sin(theta_e) * A - math.sin(theta_e - pi_2_3) * B - math.sin(theta_e + pi_2_3) * C)
    return D, Q

def dq_to_abc(D, Q, theta_e):
    """Inverse Park and Clarke transform from DQ to ABC frame."""
    pi_2_3 = 2.0 * math.pi / 3.0
    pi_4_3 = 4.0 * math.pi / 3.0
    
    A = math.cos(theta_e) * D - math.sin(theta_e) * Q
    B = math.cos(theta_e - pi_2_3) * D - math.sin(theta_e - pi_2_3) * Q
    C = math.cos(theta_e - pi_4_3) * D - math.sin(theta_e - pi_4_3) * Q
    return A, B, C
