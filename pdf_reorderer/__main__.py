"""Entrada unica do pacote `pdf_reorderer`.

Suporta:
- modo único: `reordenador input.pdf output.pdf`
- modo batch: `--in-dir <dir> --out-dir <dir>` processa todos os PDFs em
  <dir> e grava em <out-dir> com o mesmo nome de arquivo.
"""

from __future__ import annotations

import argparse
import os
import sys
from glob import glob

sys.dont_write_bytecode = True

import functools

from .modes.booklet import gerar_ordem as gerar_ordem_booklet
from .modes.diagonal_local import gerar_ordem as gerar_ordem_diagonal_local
from .modes.duas_pilhas import gerar_ordem as gerar_ordem_duas_pilhas
from .modes.livreto_costura import gerar_ordem as gerar_ordem_livreto_costura
from .modes.shared import reordenar_pdf


def resolver_entrada(caminho_entrada: str) -> str:
	"""Resolve o PDF de entrada, buscando automaticamente em `in/` quando necessário."""
	if os.path.isfile(caminho_entrada):
		return caminho_entrada

	if os.path.dirname(caminho_entrada):
		return caminho_entrada

	candidato = os.path.join("in", caminho_entrada)
	if os.path.isfile(candidato):
		return candidato

	return caminho_entrada


def resolver_saida(caminho_saida: str) -> str:
	"""Resolve o PDF de saida para a pasta `out/`, mantendo apenas o nome do arquivo."""
	return os.path.join("out", os.path.basename(caminho_saida))


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Reordena PDF para duas-pilhas, diagonal-local, booklet ou livreto-costura"
	)

	# compatibilidade single-file (posicionais opcionais)
	parser.add_argument("entrada", nargs="?", help="Caminho do PDF de entrada")
	parser.add_argument("saida", nargs="?", help="Caminho do PDF de saida")

	# batch via diretorios
	parser.add_argument("--in-dir", dest="in_dir", help="Diretorio com arquivos de entrada (PDF)")
	parser.add_argument("--out-dir", dest="out_dir", default="out", help="Diretorio de saida (padrao: out)")

	parser.add_argument(
		"--modo",
		choices=("duas-pilhas", "diagonal-local", "booklet", "livreto-costura"),
		default="duas-pilhas",
		help="Modo de reordenacao (padrao: duas-pilhas)",
	)

	parser.add_argument(
		"--block-size",
		type=int,
		default=16,
		help="Páginas por assinatura para livreto-costura (múltiplo de 4). Padrão: 16.",
	)

	args = parser.parse_args()

	# Construir modos AQUI com block_size disponível
	modos = {
		"duas-pilhas": gerar_ordem_duas_pilhas,
		"diagonal-local": gerar_ordem_diagonal_local,
		"booklet": gerar_ordem_booklet,
		"livreto-costura": functools.partial(gerar_ordem_livreto_costura, block_size=args.block_size),
	}

	# Batch mode: processa todos os PDFs no diretorio de entrada
	if args.in_dir:
		in_dir = os.path.abspath(args.in_dir)
		out_dir = os.path.abspath(args.out_dir)

		if not os.path.isdir(in_dir):
			print(f"Erro: diretorio de entrada nao encontrado: {in_dir}", file=sys.stderr)
			return 1

		os.makedirs(out_dir, exist_ok=True)

		pdfs = sorted(glob(os.path.join(in_dir, "*.pdf")))
		if not pdfs:
			print(f"Nenhum PDF encontrado em: {in_dir}", file=sys.stderr)
			return 1

		erro = False
		for caminho in pdfs:
			nome = os.path.basename(caminho)
			saida = os.path.join(out_dir, nome)
			try:
				print(f"Processando: {nome} -> {saida} ({args.modo})")
				reordenar_pdf(caminho, saida, modos[args.modo])
			except Exception as exc:
				print(f"Falha em {nome}: {exc}", file=sys.stderr)
				erro = True

		return 1 if erro else 0

	# Single-file fallback (compatibilidade)
	if args.entrada and args.saida:
		try:
			entrada = resolver_entrada(args.entrada)
			saida = resolver_saida(args.saida)
			os.makedirs(os.path.dirname(saida), exist_ok=True)
			reordenar_pdf(entrada, saida, modos[args.modo])
		except Exception as exc:
			print(f"Erro ao reordenar PDF: {exc}", file=sys.stderr)
			return 1

		print(f"PDF reordenado com sucesso ({args.modo}): {saida}")
		return 0

	parser.print_help()
	return 2


if __name__ == "__main__":
	raise SystemExit(main())
