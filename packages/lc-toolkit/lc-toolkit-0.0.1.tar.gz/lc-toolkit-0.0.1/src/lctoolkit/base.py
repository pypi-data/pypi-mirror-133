from numpy import sin, cos


def get_neff(theta, no, ne):
    """
    See: https://www.fzu.cz/~kuzelp/Optics/Lecture8.pdf

    Returns the effective index for a ray/wave passing through a unixial medium 
    with the optical axis assuming an angle w.r.t. the crystal axis.

    Parameters:
        theta (float-array): angle between optical axis and crystal axis in rad
        no (float): ordinary refractive index
        ne (float): extraordinary refractive index
        
    Returns
        n_eff (float): effective index for extraordinary ray
    """

    return 1/((sin(theta) / ne)**2 + (cos(theta) / no)**2)**.5

def add_one(number):
    return number + 1