"""Modo de livreto tradicional."""

from __future__ import annotations

from .shared import completar_para_multiplo_de_4


def gerar_ordem(total_paginas: int) -> list[int | None]:
	"""Retorna indices zero-based no formato livreto tradicional."""
	paginas = completar_para_multiplo_de_4(total_paginas)
	left = 0
	right = len(paginas) - 1
	ordem: list[int | None] = []

	while left < right:
		ordem.append(paginas[right])
		ordem.append(paginas[left])
		left += 1
		right -= 1

		if left > right:
			break

		ordem.append(paginas[left])
		ordem.append(paginas[right])
		left += 1
		right -= 1

	return ordem
