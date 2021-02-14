
#gnuplot -e "plot $1  replot $2 with lines; replot $3 with lines;"
gnuplot << EOF
  set terminal png font "VL PGothic,20"
  set xlabel '試合数(回)' font "Ryumin-Light-EUC-H,14"
  set ylabel '勝率+引き分け率' font "Ryumin-Light-EUC-H,14"
  set output '$4.png'
  set xrange [0:100000]
  set yrange [0:1.0]
  plot "$1" with line ,"$2" with line ,"$3" with line
EOF
