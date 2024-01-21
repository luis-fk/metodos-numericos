# animate_planets.gp

# Set up plotting parameters
set term gif animate delay 1
set output 'planets_animation.gif'
unset xlabel
unset ylabel
unset zlabel
unset border
unset xtics
unset ytics
unset ztics
unset key
set title 'Planets Animation'

# Set up animation settings
num_frames = 250  # Replace with the actual number of frames

# Loop through frames
do for [i=1:num_frames] {
    set view 45, 60, 1, 1
    splot 'output.txt' every 10::1::i*10 using 1:2:3 with lines title 'Planet 1 Trajectory', \
          '' every 10::i*10::i*10 using 1:2:3 with points title 'Planet 1' pt 7, \
          '' every 10::1::i*10 using 4:5:6 with lines title 'Planet 2 Trajectory', \
          '' every 10::i*10::i*10 using 4:5:6 with points title 'Planet 2' pt 7, \
          '' every 10::1::i*10 using 7:8:9 with lines title 'Planet 3 Trajectory', \
          '' every 10::i*10::i*10 using 7:8:9 with points title 'Planet 3' pt 7
}
