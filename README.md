# Tinket-M0-CP-media-control
 A Circuit Python USB Media control knob using a Trinket M0 and a rotary encoder.

 I was using an Arduino library I found on github, on an attiny85, but I had stability issues with the USB connection from the '85' to Windows. After looking around the web a bit, it became clear that I was not the only one facing that, and all notes pointed toward a platform with native USB.

 I sort of fell upon the Trinket-M0 just looking around and decided to give it a shot. I have a bit of experience with Python overall, but none with CircuitPython on resource constrained devices.

 I was pleasently surprised how easy it was to start with a working CP Keyboard example, then reading the consumer_device APIs, recast that example with a media controller using a single rotary encoder with a pushbutton to support Volume, Play/Pause, Restart Track (long press) or Skip Track (double click).

 Here is my example code. Use it as you see fit.

 It is all based of the example I found on this page:

 https://learn.adafruit.com/media-dial

 So whatever license is covered by that, should apply to this as well, since it is a derived work.

 NOTE: I did not hook up the LED ring. I am only using the encoder, nothing else.

 Also note: I used the encoders on this link.

 https://www.amazon.com/gp/product/B06XQTHDRR

 They have pullup resistors on the back of the circuit board, and I had quadrature read and button noise issues until I removed those resistors. If you are using a bare, unmounted encoder, you won't have that problem.
