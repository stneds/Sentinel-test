# Sentinel & Landsat Vegetation Analysis

Este projeto realiza o download, processamento e análise de imagens de satélite (Landsat 8/9 e Sentinel-2) para cálculo de índices de vegetação (NDVI, NDRE, SAVI, EVI) e detecção de anomalias em áreas de Teresina-PI.

## Estrutura dos Scripts

- **landsat_download_test.py**: Baixa imagens Landsat 8/9 da USGS M2M API para a área de Teresina-PI, filtrando por datas e cobertura de nuvens. Salva os arquivos em `downloads/landsat`.
- **sentinel2_download_test.py**: Baixa imagens Sentinel-2 L2A do portal Copernicus Data Space, usando credenciais do usuário. Salva os arquivos em `downloads/sentinel2`.
- **processamento_ndvi.py**: Lê bandas espectrais (Vermelho e Infravermelho Próximo) de imagens Landsat, aplica correção atmosférica, calcula o NDVI, salva o resultado em GeoTIFF e exibe o mapa.
- **vegetation_indices.py**: Fornece funções para calcular NDVI, NDRE, SAVI e EVI a partir das bandas espectrais, além de normalização de bandas.
- **threshold_anomalies.py**: Classifica índices de vegetação em categorias (solo, vegetação fraca, moderada, saudável) e detecta anomalias (áreas abaixo de um limiar).

## Requisitos

- Python 3.8+
- Pacotes: `numpy`, `rasterio`, `matplotlib`, `requests`

Instale os requisitos com:

```
pip install numpy rasterio matplotlib requests
```

## Como Executar

1. **Baixar imagens Landsat:**
   - Edite as credenciais em `landsat_download_test.py`.
   - Execute:
     ```
     python landsat_download_test.py
     ```
   - Os arquivos serão salvos em `downloads/landsat`.

2. **Baixar imagens Sentinel-2:**
   - Edite usuário e senha em `sentinel2_download_test.py`.
   - Execute:
     ```
     python sentinel2_download_test.py
     ```
   - Os arquivos serão salvos em `downloads/sentinel2`.

3. **Processar NDVI (Landsat):**
   - Ajuste os nomes dos arquivos das bandas em `processamento_ndvi.py` conforme os arquivos baixados.
   - Execute:
     ```
     python processamento_ndvi.py
     ```
   - O resultado será salvo como `ndvi_resultado_teresina.tif` e exibido em um mapa.

4. **Cálculo de índices e classificação:**
   - Utilize as funções de `vegetation_indices.py` e `threshold_anomalies.py` em seus próprios scripts para calcular e classificar NDVI, NDRE, SAVI e EVI.

## Observações Importantes

- As credenciais de acesso (USGS e Copernicus) devem ser válidas.
- Os downloads podem gerar arquivos grandes (>1GB).
- Os scripts são focados na área de Teresina-PI, mas podem ser adaptados para outras regiões.

## Exemplo de Fluxo

1. Baixe as imagens.
2. Extraia as bandas desejadas (ex: B4, B5 do Landsat).
3. Execute o processamento e visualize os índices.
4. Classifique e detecte anomalias conforme sua aplicação.

---

Projeto acadêmico para análise de vegetação por sensoriamento remoto.
