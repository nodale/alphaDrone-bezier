#!/bin/bash

# Run gnuplot commands directly
gnuplot -persist <<-EOF
    set multiplot layout 3,1
    set grid
    
#    set title "X"
    plot "vel.txt" using 10:1 with lines title "x estimate", \
         "vel.txt" using 10:4 with lines title "x vicon", \
         "vel.txt" using 10:7 with lines title "x setpoint"
           
#    set tvele "Y"
    plot "vel.txt" using 10:2 with lines title "y estimate", \
         "vel.txt" using 10:5 with lines title "y vicon", \
         "vel.txt" using 10:8 with lines title "y setpoint"
           
#    set tvele "Z"
    plot "vel.txt" using 10:3 with lines title "z estimate", \
         "vel.txt" using 10:6 with lines title "z vicon", \
         "vel.txt" using 10:9 with lines title "z setpoint"

    unset multiplot
EOF

