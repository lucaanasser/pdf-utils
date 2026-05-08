"""Modo de duas pilhas sequenciais."""

from __future__ import annotations

from .shared import completar_para_multiplo_de_4


def gerar_ordem(total_paginas: int) -> list[int | None]:
	"""Retorna indices zero-based para gerar duas pilhas apos corte."""
	paginas = completar_para_multiplo_de_4(total_paginas)
	total_final = len(paginas)
	metade = total_final // 2
	primeira_metade = paginas[:metade]
	segunda_metade = paginas[metade:]
	ordem: list[int | None] = []

	for i in range(0, metade, 2):
		a1 = primeira_metade[i]
		a2 = primeira_metade[i + 1]
		b1 = segunda_metade[i]
		b2 = segunda_metade[i + 1]
		ordem.extend([a1, b1, b2, a2])

	return ordem
