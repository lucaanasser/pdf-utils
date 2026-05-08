"""Funcoes compartilhadas pelos modos de reordenacao."""

from __future__ import annotations

import importlib
import os
from collections.abc import Callable


def carregar_pdf_lib() -> tuple[type, type]:
	"""Carrega PdfReader e PdfWriter de pypdf ou PyPDF2."""
	for nome_modulo in ("pypdf", "PyPDF2"):
		try:
			pacote = importlib.import_module(nome_modulo)
			return pacote.PdfReader, pacote.PdfWriter
		except ImportError:
			continue

	raise SystemExit("Erro: instale a biblioteca 'pypdf' com: pip install pypdf")


def completar_para_multiplo_de_4(total_paginas: int) -> list[int | None]:
	"""Retorna uma lista zero-based com padding ate multiplo de 4."""
	return completar_para_multiplo(total_paginas, 4)


def completar_para_multiplo(total_paginas: int, tamanho_bloco: int) -> list[int | None]:
	"""Retorna uma lista zero-based com padding ate o multiplo informado."""
	resto = total_paginas % tamanho_bloco
	padding = 0 if resto == 0 else tamanho_bloco - resto
	return list(range(total_paginas)) + [None] * padding


def reordenar_pdf(
	caminho_entrada: str,
	caminho_saida: str,
	gerar_ordem: Callable[[int], list[int | None]],
) -> None:
	"""Reordena um PDF usando o modo informado."""
	PdfReader, PdfWriter = carregar_pdf_lib()

	if not os.path.isfile(caminho_entrada):
		raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {caminho_entrada}")

	leitor = PdfReader(caminho_entrada)
	escritor = PdfWriter()

	total = len(leitor.pages)
	if total == 0:
		raise ValueError("O PDF de entrada nao possui paginas")

	ordem = gerar_ordem(total)
	base = leitor.pages[0]
	largura = float(base.mediabox.width)
	altura = float(base.mediabox.height)

	for indice in ordem:
		if indice is None:
			escritor.add_blank_page(width=largura, height=altura)
		else:
			escritor.add_page(leitor.pages[indice])

	with open(caminho_saida, "wb") as arquivo_saida:
		escritor.write(arquivo_saida)
