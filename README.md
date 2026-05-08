# pdf-utils

## Quickstart

```bash
cd pdf_utils
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Reordenar um PDF (saida sempre em out/)
python3 -m pdf_reorderer in/arquivo.pdf saida.pdf --modo duas-pilhas

# Outros modos disponiveis
python3 -m pdf_reorderer in/arquivo.pdf saida.pdf --modo diagonal-local
python3 -m pdf_reorderer in/arquivo.pdf saida.pdf --modo booklet
python3 -m pdf_reorderer in/arquivo.pdf saida.pdf --modo livreto-costura --block-size 16
```
