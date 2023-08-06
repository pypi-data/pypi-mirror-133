import pandas as pd
import numpy as np
import astropy.io.fits as fits
from datetime import datetime
import julian
from astropy.coordinates import get_sun
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord
from scipy import interpolate
import astropy.coordinates as coord
import matplotlib.pyplot as plt
import pdb


def zodi_L98(ra, dec, time):
    """
        For given RA, DEC and TIME, return the interpolated zodical spectrum in Leinert-1998.

    :param ra: RA in unit of degree, ICRS frame
    :param dec: DEC in unit of degree, ICRS frame
    :param time: the specified string that in ISO format i.e., yyyy-mm-dd.
    :return:
        wave_A: wavelength of the zodical spectrum
        spec_mjy: flux of the zodical spectrum, in unit of MJy/sr
        spec_erg: flux of the zodical spectrum, in unit of erg/s/cm^2/A/sr

    """

    # get solar position
    dt = datetime.fromisoformat(time)
    jd = julian.to_jd(dt, fmt='jd')
    t = Time(jd, format='jd', scale='utc')

    astro_sun = get_sun(t)
    ra_sun, dec_sun = astro_sun.gcrs.ra.deg, astro_sun.gcrs.dec.deg

    radec_sun = SkyCoord(ra=ra_sun*u.degree, dec=dec_sun*u.degree, frame='gcrs')
    lb_sun = radec_sun.transform_to('geocentrictrueecliptic')

    # get offsets between the target and sun.
    radec_obj = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    lb_obj = radec_obj.transform_to('geocentrictrueecliptic')

    beta = abs(lb_obj.lat.degree)
    lamda = abs(lb_obj.lon.degree - lb_sun.lon.degree)

    # interpolated zodical surface brightness at 0.5 um
    zodi = pd.read_csv('refs/zodi_map.dat', sep='\s+', header=None, comment='#')
    beta_angle = np.array([0, 5, 10, 15, 20, 25, 30, 45, 60, 75])
    lamda_angle = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
                          60, 75, 90, 105, 120, 135, 150, 165, 180])
    xx, yy = np.meshgrid(beta_angle, lamda_angle)
    f = interpolate.interp2d(xx, yy, zodi, kind='linear')
    zodi_obj = f(beta, lamda)

    # read the zodical spectrum in the ecliptic
    cat_spec = pd.read_csv('refs/solar_spec.dat', sep='\s+', header=None, comment='#')
    wave = cat_spec[0]       # A
    spec0 = cat_spec[1]      # W m^−2 sr^−1 μm^−1
    zodi_norm = 259e-8       # W m^−2 sr^−1 μm^−1

    spec = spec0 * (zodi_obj / zodi_norm)   # W m^−2 sr^−1 μm^−1

    # convert to the commonly used unit of MJy/sr, erg/s/cm^2/A/sr
    wave_A = wave * 10000
    spec_mjy = spec * 0.1 * wave_A**2 / 3e18 * 1e23 * 1e-6      # MJy/sr
    spec_erg = spec * 0.1                                       # erg/s/cm^2/A/sr
    spec_erg2 = spec_erg / 4.25452e10                           # erg/s/cm^2/A/arcsec^2

    return wave_A, spec_erg2

    # Notes for
    # ---------------------------------------
    # 1 W/m2 sr μm = 0.10 erg/cm2 s sr A
    # 141 10^-8 W/m2 sr μm = 14.1 erg/cm2 s sr A = 14.1 * 5000^2 / 3e18 =  1.175 * 10-10 erg/s/cm^2/Hz/sr
    # = 1.175 * 10^17 * 10^-10 * 10^-8 MJy/sr
    # = 1.175 * 10^-1 Mjy/sr = 0.1175 MJy/sr

    # euclid
    # 2019-01-01 ra=150, dec=30, zodi: 0.23928 MJy/sr

    # 1 Jy = 10^-26 W/m^2/Hz = 10^-23 erg/s/cm^2/Hz
    # 1 MJy = 10^-17 erg/s/cm^2/Hz
    # 1 rad = 206265 arcsec
    # 1 sr = 1 rad^2 = 4.25452e10 arcsec^2
    # ----------------------------------------
