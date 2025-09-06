#!/bin/bash

# Run gnuplot commands directly
gnuplot -persist <<-EOF
    set multiplot layout 3,1
    set grid
    
#    set title "X"
    plot "pos.txt" using 10:1 with lines title "x estimate", \
         "pos.txt" using 10:4 with lines title "x vicon", \
         "pos.txt" using 10:7 with lines title "x setpoint"

#    set title "Y"
    plot "pos.txt" using 10:2 with lines title "y estimate", \
         "pos.txt" using 10:5 with lines title "y vicon", \
         "pos.txt" using 10:8 with lines title "y setpoint"

#    set title "Z"
    plot "pos.txt" using 10:3 with lines title "z estimate", \
         "pos.txt" using 10:6 with lines title "z vicon", \
         "pos.txt" using 10:9 with lines title "z setpoint"

    unset multiplot
EOF

