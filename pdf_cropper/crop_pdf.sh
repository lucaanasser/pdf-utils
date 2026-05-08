#!/bin/bash

# ==========================================
# Script para instalar dependências e rodar o pdfcrop
# ==========================================

set -e  # Interrompe o script em caso de erro

# ==============================
# Configurações
# ==============================
INPUT="${1:-apostol.pdf}"              # Arquivo de entrada (padrão: apostol.pdf)
OUTPUT="${2:-apostol-cropped.pdf}"     # Arquivo de saída (padrão: apostol-cropped.pdf)
MARGINS="${3:-10}"                     # Margem de segurança em pontos (padrão: 10)

# ==============================
# Funções auxiliares
# ==============================
check_command() {
    command -v "$1" &> /dev/null
}

install_packages() {
    echo "🔧 Instalando dependências necessárias..."
    sudo apt update
    sudo apt install -y \
        ghostscript \
        texlive-extra-utils \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-fonts-recommended
}

# ==============================
# Verificação do sistema
# ==============================
if ! check_command pdfcrop || ! check_command gs || ! check_command pdftex; then
    echo "📦 Dependências não encontradas. Instalando..."
    install_packages
else
    echo "✅ Todas as dependências já estão instaladas."
fi

# ==============================
# Verificar existência do arquivo
# ==============================
if [ ! -f "$INPUT" ]; then
    echo "❌ Erro: Arquivo de entrada '$INPUT' não encontrado."
    echo "Uso: $0 <input.pdf> [output.pdf] [margem_em_pt]"
    exit 1
fi

# ==============================
# Executar o pdfcrop
# ==============================
echo "✂️  Removendo margens do PDF..."
echo "📄 Entrada : $INPUT"
echo "📄 Saída   : $OUTPUT"
echo "📏 Margem  : $MARGINS pt"

# Tenta execução padrão
if pdfcrop --margins "$MARGINS" "$INPUT" "$OUTPUT"; then
    echo "✅ PDF processado com sucesso!"
else
    echo "⚠️  Falha na execução padrão. Tentando novamente com -dNOSAFER..."
    pdfcrop --gscmd "gs -dNOSAFER" --margins "$MARGINS" "$INPUT" "$OUTPUT"
    echo "✅ PDF processado com sucesso usando -dNOSAFER!"
fi

echo "🎉 Processo concluído!"
echo "📁 Arquivo final: $OUTPUT"
