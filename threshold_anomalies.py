import numpy as np


def classify_ndvi(ndvi):
    """
    Classificação por limites de NDVI.
    """
    result = np.full(ndvi.shape, 0)

    result[ndvi < 0.2] = 1       # solo exposto, água ou área sem vegetação
    result[(ndvi >= 0.2) & (ndvi < 0.4)] = 2   # vegetação fraca
    result[(ndvi >= 0.4) & (ndvi < 0.6)] = 3   # vegetação moderada
    result[ndvi >= 0.6] = 4      # vegetação saudável

    return result


def classify_ndre(ndre):
    """
    Classificação por limites de NDRE.
    """
    result = np.full(ndre.shape, 0)

    result[ndre < 0.1] = 1
    result[(ndre >= 0.1) & (ndre < 0.3)] = 2
    result[(ndre >= 0.3) & (ndre < 0.5)] = 3
    result[ndre >= 0.5] = 4

    return result


def classify_savi(savi):
    """
    Classificação por limites de SAVI.
    """
    result = np.full(savi.shape, 0)

    result[savi < 0.2] = 1
    result[(savi >= 0.2) & (savi < 0.4)] = 2
    result[(savi >= 0.4) & (savi < 0.6)] = 3
    result[savi >= 0.6] = 4

    return result


def classify_evi(evi):
    """
    Classificação por limites de EVI.
    """
    result = np.full(evi.shape, 0)

    result[evi < 0.2] = 1
    result[(evi >= 0.2) & (evi < 0.4)] = 2
    result[(evi >= 0.4) & (evi < 0.6)] = 3
    result[evi >= 0.6] = 4

    return result


def detect_anomalies(index_array, low_threshold=0.3):
    """
    Identifica áreas anômalas com índice abaixo do limite mínimo.
    Retorna uma máscara:
    1 = anomalia
    0 = normal
    """
    anomaly_mask = np.zeros(index_array.shape)
    anomaly_mask[index_array < low_threshold] = 1

    return anomaly_mask