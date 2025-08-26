# Day 14: Custom Colors

**Date:** ___________

## Today's Mission 🚀
Explore advanced color usage, such as gradients or alternating colors!

### New Command:
- `PENCOLOR [R G B]` - Set the pen color using RGB values (0-255).

---

## Let's Start!

### Step 1: Basic Colors
- [ ] Open FMSLogo and type `CS` to clear the screen.
- [ ] Try these commands:
  ```
  PENCOLOR [255 0 0]  ; Red
  FD 100
  PENCOLOR [0 255 0]  ; Green
  FD 100
  PENCOLOR [0 0 255]  ; Blue
  FD 100
  ```
- [ ] Observe the different colors used for each line.

### Step 2: Gradient Effect
- [ ] Type `CS` to start fresh.
- [ ] Try this code:
  ```
  REPEAT 255 [ PENCOLOR [REPCOUNT 0 255-REPCOUNT] FD 2 ]
  ```
- [ ] Notice the gradient effect from red to blue!

---

## Challenge Time! ⭐

### Easy:
- Create a gradient from green to yellow.

### Hard:
- Combine gradients with shapes (e.g., a gradient square or circle).

---

Happy coding! 🌈
