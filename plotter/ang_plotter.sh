#!/bin/bash

# Run gnuplot commands directly
gnuplot -persist <<-EOF
    set multiplot layout 3,1
    set grid
    
    plot "ang.txt" using 7:1 with lines title "roll estimate", \
         "ang.txt" using 7:4 with lines title "roll vicon"
         
    plot "ang.txt" using 7:2 with lines title "pitch estimate", \
         "ang.txt" using 7:5 with lines title "pitch vicon"
         
    plot "ang.txt" using 7:3 with lines title "yaw estimate", \
         "ang.txt" using 7:6 with lines title "yaw vicon"
    
    unset multiplot
EOF

