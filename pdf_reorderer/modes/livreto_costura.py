"""
Modo: livreto-costura
Reordena páginas de um PDF em assinaturas (cadernos) para impressão frente-e-verso
e costura. O tamanho de cada assinatura é configurável e deve ser múltiplo de 4.

Uso típico:
    python3 -m pdf_reorderer entrada.pdf saida.pdf --modo livreto-costura --block-size 16

Lógica de imposição
-------------------
Cada assinatura tem B páginas lógicas, formadas por B/4 folhas físicas dobradas ao meio.
Ao dobrar uma pilha de folhas, a folha mais externa contém as páginas {B, 1} na frente
e {2, B-1} no verso; a folha seguinte contém {B-2, 3} e {4, B-3}; e assim por diante.

Para um bloco de B páginas lógicas (1-indexadas dentro do bloco), a sequência de
impressão — considerando a ordem em que as faces aparecem no PDF de saída — é:

    folha k (k = 0 .. B/4 - 1):
        face frente : página (B - 2k),  página (2k + 1)
        face verso  : página (2k + 2),  página (B - 2k - 1)

Convertendo para 0-based e concatenando todos os blocos gera a lista final de índices.
Páginas faltantes no último bloco são preenchidas com None (branco).
"""

from __future__ import annotations


def _imposicao_bloco(offset: int, b: int, total: int) -> list[int | None]:
    """Retorna a sequência de índices (0-based, None = branco) para um bloco.

    Parameters
    ----------
    offset : int
        Índice 0-based da primeira página lógica deste bloco no documento.
    b : int
        Tamanho do bloco em páginas lógicas (múltiplo de 4).
    total : int
        Total de páginas reais no documento (para detectar páginas inexistentes).
    """
    ordem: list[int | None] = []
    num_folhas = b // 4

    for k in range(num_folhas):
        # Páginas 1-based dentro do bloco
        frente_esq = b - 2 * k          # face frente, lado esquerdo (quando aberto)
        frente_dir = 2 * k + 1          # face frente, lado direito
        verso_esq  = 2 * k + 2          # face verso,  lado esquerdo
        verso_dir  = b - 2 * k - 1      # face verso,  lado direito

        for pag_local in (frente_esq, frente_dir, verso_esq, verso_dir):
            idx = offset + pag_local - 1   # converter para 0-based absoluto
            ordem.append(idx if idx < total else None)

    return ordem


def gerar_ordem(total_paginas: int, block_size: int = 16) -> list[int | None]:
    """Gera a ordem completa de impressão para todos os livretos/assinaturas.

    Parameters
    ----------
    total_paginas : int
        Número de páginas do PDF de entrada.
    block_size : int
        Número de páginas lógicas por assinatura. Deve ser múltiplo de 4.
        Valores típicos: 8, 12, 16, 20, 24, 28, 32, 40, 48.

    Returns
    -------
    list[int | None]
        Índices 0-based na ordem de impressão. None indica página em branco.

    Raises
    ------
    ValueError
        Se block_size não for múltiplo de 4 ou for menor que 4.
    """
    if block_size < 4 or block_size % 4 != 0:
        raise ValueError(
            f"block_size deve ser múltiplo de 4 (recebido: {block_size}). "
            "Valores válidos: 4, 8, 12, 16, 20, 24, 28, 32, ..."
        )

    ordem_total: list[int | None] = []
    offset = 0

    while offset < total_paginas:
        bloco = _imposicao_bloco(offset, block_size, total_paginas)
        ordem_total.extend(bloco)
        offset += block_size

    return ordem_total