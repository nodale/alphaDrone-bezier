#!/bin/bash

# Run gnuplot commands directly
gnuplot -persist <<-EOF
    set multiplot layout 3,1
    set grid
    
    plot "q.txt" using 7:1 with lines title "qx estimate", \
         "q.txt" using 7:4 with lines title "qx vicon"
         
    plot "q.txt" using 7:2 with lines title "qy estimate", \
         "q.txt" using 7:5 with lines title "qy vicon"
         
    plot "q.txt" using 7:3 with lines title "qz estimate", \
         "q.txt" using 7:6 with lines title "qz vicon"
    
    unset multiplot
EOF

