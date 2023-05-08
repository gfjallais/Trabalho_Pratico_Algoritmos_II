#!/bin/bash

# Define o diretório onde os arquivos .txt estão localizados
dir="/home/gfjallais/Code/TP-ALG2/entrada"

# Cria o arquivo results.txt ou sobrescreve o arquivo existente
echo "" > results.txt
ratios=()
# Itera sobre cada arquivo .txt no diretório
for file in $dir/*.txt; do
  # Define o nome dos arquivos de saída
  input="${file}"
  output1="${file%.*}_saida.z78"
  output2="${file%.*}_saida.txt"
  log="${file%.*}_log.txt"

  # Executa os comandos e salva a saída em um arquivo de log
  python3 TP_ALG2.py -c "${input}" "${output1}" &> "${log}"
  python3 TP_ALG2.py -x "${output1}" "${output2}" &>> "${log}"
  diff "${input}" "${output2}" &>> "${log}"

  # Obtém o tamanho dos arquivos e os grava no arquivo results.txt
  input_size=$(du -h "${input}" | awk '{print $1}')
  output_size=$(du -h "${output1}" | awk '{print $1}')
  ratio=$(bc -l <<< "1 - $output_size/$input_size")
  ratios+=("$ratio")
  echo "${input} tem tamanho ${input_size}. ${output1} tem tamanho ${output_size}. A relação entre os tamanhos é de ${ratio}." >> results.txt

done

mean=$(printf "%s\n" "${ratios[@]}" | awk '{s+=$1} END {print s/NR}')
echo "A média das relações entre os tamanhos é de ${mean}." >> results.txt