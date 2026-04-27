import numpy as np


def calculate_ndvi(nir, red):
    """
    NDVI = (NIR - RED) / (NIR + RED)
    Mede vigor e saúde da vegetação.
    """
    return (nir - red) / (nir + red + 1e-6)


def calculate_ndre(nir, red_edge):
    """
    NDRE = (NIR - RedEdge) / (NIR + RedEdge)
    Útil para detectar estresse em vegetação mais densa.
    """
    return (nir - red_edge) / (nir + red_edge + 1e-6)


def calculate_savi(nir, red, L=0.5):
    """
    SAVI = ((NIR - RED) / (NIR + RED + L)) * (1 + L)
    Reduz influência do solo exposto.
    """
    return ((nir - red) / (nir + red + L + 1e-6)) * (1 + L)


def calculate_evi(nir, red, blue):
    """
    EVI = 2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)
    Melhor para áreas com vegetação densa.
    """
    return 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1 + 1e-6)


def normalize_band(band):
    """
    Normaliza bandas Sentinel-2 ou Landsat para reflectância 0-1.
    """
    band = band.astype("float32")
    return band / 10000.0