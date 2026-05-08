"""Modo diagonal local por blocos de quatro paginas."""

from __future__ import annotations

from .shared import completar_para_multiplo_de_4


def gerar_ordem(total_paginas: int) -> list[int | None]:
	"""Retorna indices zero-based no padrao [a, c, d, b]."""
	paginas = completar_para_multiplo_de_4(total_paginas)
	ordem: list[int | None] = []

	for i in range(0, len(paginas), 4):
		a = paginas[i]
		b = paginas[i + 1]
		c = paginas[i + 2]
		d = paginas[i + 3]
		ordem.extend([a, c, d, b])

	return ordem
