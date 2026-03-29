"""
sentinel2_download_test.py
Script para baixar imagens Sentinel-2 L2A via Copernicus Data Space (CDSE)
"""

from __future__ import annotations
import os
import sys
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

# ============================================================
# CONFIGURAÇÕES (CREDENCIAIS INSERIDAS)
# ============================================================
CDSE_TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
CDSE_ODATA_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
CDSE_DOWNLOAD_URL = "https://download.dataspace.copernicus.eu/odata/v1/Products"

# Suas credenciais oficiais:
CDSE_USERNAME = "antoniosantana4263@gmail.com"
CDSE_PASSWORD = "Bisneto732005."

# Área de interesse (Região de Teresina - WKT POLYGON)
AOI_WKT = (
    "POLYGON(("
    "-42.8200 -5.1500, "
    "-42.7000 -5.1500, "
    "-42.7000 -5.0500, "
    "-42.8200 -5.0500, "
    "-42.8200 -5.1500"
    "))"
)

# Filtros
DATE_START = "2025-12-01T00:00:00.000Z" # Buscando do final de 2025
DATE_END = "2026-03-29T23:59:59.999Z"   # Até a data de hoje
MAX_CLOUD_COVER = 15                   # Máximo 15% de nuvens
PRODUCT_TYPE = "S2MSI2A"               # Nível L2A (Refletância de Superfície)
OUTPUT_DIR = Path("downloads/sentinel2")

# ============================================================
# FUNÇÕES DE EXECUÇÃO
# ============================================================

def log(msg): print(f"[INFO] {msg}")
def fail(msg): print(f"[ERRO] {msg}"); sys.exit(1)

def get_access_token():
    payload = {"client_id": "cdse-public", "grant_type": "password", "username": CDSE_USERNAME, "password": CDSE_PASSWORD}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(CDSE_TOKEN_URL, data=payload, headers=headers)
    if response.status_code != 200:
        fail(f"Falha na autenticação. Verifique e-mail e senha.")
    return response.json().get("access_token")

def search_products(token):
    odata_filter = (
        f"Collection/Name eq 'SENTINEL-2' and "
        f"OData.CSC.Intersects(area=geography'SRID=4326;{AOI_WKT}') and "
        f"ContentDate/Start ge {DATE_START} and ContentDate/Start le {DATE_END} and "
        f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '{PRODUCT_TYPE}') and "
        f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le {MAX_CLOUD_COVER})"
    )
    params = {"$filter": odata_filter, "$orderby": "ContentDate/Start desc", "$top": "5", "$expand": "Attributes"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(CDSE_ODATA_URL, headers=headers, params=params)
    return response.json().get("value", [])

def download_product(token, p_id, p_name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{p_name}.zip"
    url = f"{CDSE_DOWNLOAD_URL}({p_id})/$value"
    headers = {"Authorization": f"Bearer {token}"}
    
    log(f"Baixando: {p_name}...")
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    log(f"Download concluído! Salvo em: {out_path}")

def main():
    log("Iniciando processo...")
    token = get_access_token()
    products = search_products(token)
    
    if not products:
        fail("Nenhuma imagem encontrada com esses filtros.")
    
    best = products[0] # Pega a mais recente
    log(f"Imagem encontrada: {best['Name']}")
    download_product(token, best['Id'], best['Name'])
    log("Processo finalizado com sucesso!")

if __name__ == "__main__":
    main()