"""
landsat_download_test.py
Download de imagens Landsat 8-9 via USGS M2M API
"""

import requests
import json
import sys
from pathlib import Path

# ============================================================
# CONFIGURAÇÕES
# ============================================================
M2M_BASE_URL = "https://m2m.cr.usgs.gov/api/api/json/stable/"

# Seus dados oficiais do print:
USGS_USERNAME = "stneds"
USGS_TOKEN = "Wet6BqjeCKOS6c7vrL7Ji2TtlpGGpD3rrIRBOYW!rE4NUs0lJkG4i68qUJL@yCmW" # Gere seu Application Token em: https://ers.cr.usgs.gov/profile/access

# Coordenadas de Teresina-PI
MIN_LON, MIN_LAT = -42.8200, -5.1500
MAX_LON, MAX_LAT = -42.7000, -5.0500

DATE_START = "2025-01-01"
DATE_END = "2026-03-29"
MAX_CLOUD_COVER = 20
OUTPUT_DIR = Path("downloads/landsat")

# ============================================================
# EXECUÇÃO
# ============================================================

def post_m2m(endpoint, payload, api_key=None):
    # O USGS quer o endpoint grudado no /json/
    url = f"{M2M_BASE_URL}{endpoint}" 
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0" # Engana o servidor para ele não bloquear o script
    }
    
    if api_key: 
        headers["X-Auth-Token"] = api_key
    
    # Converte o dicionário Python para uma string JSON real
    json_data = json.dumps(payload)
    
    response = requests.post(url, data=json_data, headers=headers, timeout=60)
    
    if response.status_code != 200:
        print(f"[DEBUG] URL: {url}")
        print(f"[ERRO] Resposta: {response.text}")
        sys.exit(1)
        
    return response.json()

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("[INFO] Autenticando no USGS...")
    login_data = post_m2m("login-token", {"username": USGS_USERNAME, "token": USGS_TOKEN})
    api_key = login_data.get("data")
    
    if not api_key:
        print("[ERRO] Não foi possível obter a API KEY. Verifique usuário e senha.")
        return

    print("[INFO] Pesquisando cenas Landsat 8-9...")
    search_params = {
        "datasetName": "landsat_ot_c2_l2", # Landsat 8-9 C2 L2
        "sceneFilter": {
            "spatialFilter": {"filterType": "mbr", "lowerLeft": {"latitude": MIN_LAT, "longitude": MIN_LON}, "upperRight": {"latitude": MAX_LAT, "longitude": MAX_LON}},
            "acquisitionFilter": {"start": DATE_START, "end": DATE_END},
            "cloudCoverFilter": {"max": MAX_CLOUD_COVER, "min": 0}
        },
        "maxResults": 1
    }
    
    scenes = post_m2m("scene-search", search_params, api_key)
    results = scenes.get("data", {}).get("results", [])
    
    if not results:
        print("[INFO] Nenhuma cena encontrada para os filtros aplicados.")
        return

    selected = results[0]
    entity_id = selected['entityId']
    print(f"[INFO] Cena selecionada: {selected['displayId']}")

    # Solicitar Download
    print("[INFO] Solicitando link de download...")
    download_opts = post_m2m("download-options", {"datasetName": "landsat_ot_c2_l2", "entityIds": [entity_id]}, api_key)
    
    # Busca o produto "Bundle" (completo) que esteja disponível
    product_id = None
    for opt in download_opts.get("data", []):
        if opt.get("available"):
            product_id = opt['id']
            break
            
    if product_id:
        request_data = post_m2m("download-request", {"downloads": [{"entityId": entity_id, "productId": product_id}]}, api_key)
        download_url = request_data.get("data", {}).get("availableDownloads", [{}])[0].get("url")
        
        if download_url:
            print(f"[INFO] Iniciando download: {download_url}")
            # Aqui você pode usar o mesmo fluxo de stream_download do Sentinel
            print("[AVISO] Arquivos Landsat podem ser muito grandes (>1GB).")
        else:
            print("[INFO] O download foi solicitado, mas o link ainda não está pronto (processamento em fila).")
    
    # Logout
    post_m2m("logout", {}, api_key)
    print("[INFO] Processo finalizado.")

if __name__ == "__main__":
    main()