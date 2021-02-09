
#gnuplot -e "plot $1  replot $2 with lines; replot $3 with lines;"
gnuplot << EOF
  set terminal png
  set output '$4.png'
  set xrange [0:100000]
  set yrange [0:1.0]
  plot "$1" with line ,"$2" with line ,"$3" with line
EOF