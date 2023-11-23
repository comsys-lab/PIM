#! /bin/bash

# This script is used to run the simulation for the PIM project.

#topology
VIT196='/home/sj/PIM/_Topology/VIT/ViT_base_196.csv'
VIT49='/home/sj/PIM/_Topology/VIT/ViT_base_196.csv'

BERT_Large_128='/home/sj/PIM/_Topology/BERT_Large/BERT_large_128.csv'
BERT_Large_256='/home/sj/PIM/_Topology/BERT_Large/BERT_large_256.csv'
BERT_Large_512='/home/sj/PIM/_Topology/BERT_Large/BERT_large_512.csv'

GPT3_256='/home/sj/PIM/_Topology/GPT-3/GPT3_175B_256.csv'
GPT3_512='/home/sj/PIM/_Topology/GPT-3/GPT3_175B_512.csv'
GPT3_1024='/home/sj/PIM/_Topology/GPT-3/GPT3_175B_1024.csv'
GPT3_2048='/home/sj/PIM/_Topology/GPT-3/GPT3_175B_2048.csv'

#configuration
mobile8=''
mobile16=''
mobile24=''
mobile32=''
mobile40=''
mobile48=''

desktop8=''
desktop16=''
desktop24=''
desktop32=''
desktop40=''
desktop48=''

server8=''
server16=''
server24=''
server32=''
server40=''
server48=''

supercomputer8=''
supercomputer16=''
supercomputer24=''
supercomputer32=''
supercomputer40=''
supercomputer48=''

#energy parameters



#storage path
storage_path=''

#VIT
python3.11 ./PIM/simulation.py -t $VIT196 -c $mobile8 -s $storage_path -e $energy_path


#BERT
python3.11 ./PIM/simulation.py -t $VIT196 -c $mobile8 -s $storage_path -e $energy_path

#GPT3
python3.11 ./PIM/simulation.py -t $VIT196 -c $mobile8 -s $storage_path -e $energy_path

python3.11 ./PIM/simulation.py -t $VIT196 -c $mobile8 -s $storage_path -e $energy_path