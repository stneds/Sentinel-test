import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# 1. CONFIGURAÇÃO DE CAMINHOS
# ============================================================
# Usamos o 'r' antes da string para o Windows lidar corretamente com as barras \
pasta_extraidos = Path(r"C:\Faculdade\Projeto mauro\downloads\landsat\Extraidos")

# Nomes exatos dos arquivos conforme aparecem na sua pasta
arquivo_red = "LC09_L2SP_219063_20260201_20260202_02_T1_SR_B4.TIF"
arquivo_nir = "LC09_L2SP_219063_20260201_20260202_02_T1_SR_B5.TIF"

caminho_red = pasta_extraidos / arquivo_red
caminho_nir = pasta_extraidos / arquivo_nir

# ============================================================
# 2. LEITURA E CORREÇÃO ATMOSFÉRICA (ESCALONAMENTO)
# ============================================================
print("[INFO] Lendo e corrigindo as bandas do Landsat 9...")

# Abrimos a Banda 4 (Vermelho)
with rasterio.open(caminho_red) as src:
    red = src.read(1).astype('float32')
    profile = src.profile # Guardamos os metadados para salvar o arquivo depois

# Abrimos a Banda 5 (Infravermelho Próximo)
with rasterio.open(caminho_nir) as src:
    nir = src.read(1).astype('float32')

# Fator de escala oficial do Landsat Collection 2 Level-2:
# Isso converte os números inteiros em Reflectância de Superfície (0 a 1)
red_corr = red * 0.0000275 - 0.2
nir_corr = nir * 0.0000275 - 0.2

# Removemos ruídos (valores fora do intervalo 0-1)
red_corr = np.clip(red_corr, 0, 1)
nir_corr = np.clip(nir_corr, 0, 1)

# ============================================================
# 3. CÁLCULO DO NDVI
# ============================================================
print("[INFO] Calculando o índice de vegetação...")

# Fórmula: (NIR - RED) / (NIR + RED)
# Adicionamos 1e-6 (um número bem pequeno) para evitar erro de divisão por zero
ndvi = (nir_corr - red_corr) / (nir_corr + red_corr + 1e-6)

# ============================================================
# 4. EXPORTAÇÃO E VISUALIZAÇÃO
# ============================================================
# Atualizamos o perfil do arquivo para suportar o formato decimal (float32)
profile.update(dtype=rasterio.float32, count=1)

# Salvamos o resultado em um novo arquivo GeoTIFF
with rasterio.open('ndvi_resultado_teresina.tif', 'w', **profile) as dst:
    dst.write(ndvi.astype('float32'), 1)

print("[SUCESSO] Arquivo 'ndvi_resultado_teresina.tif' gerado na pasta do projeto!")

# Criamos o mapa visual
plt.figure(figsize=(10, 7))
plt.imshow(ndvi, cmap='RdYlGn') # Escala do Vermelho (seco/urbano) ao Verde (saudável)
plt.colorbar(label='Índice NDVI')
plt.title('Saúde da Vegetação em Teresina - Landsat 9')
plt.show()