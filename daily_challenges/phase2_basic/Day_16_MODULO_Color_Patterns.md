# Day 16: MODULO for Color Patterns

**Date:** ___________

## Today's Mission 🚀
Learn how to use the `MODULO` operator to create colorful patterns!

### Step 1: Create a Colorful Spiral
- Open FMSLogo and type `CS` to clear the screen.
- Try this code:
  ```
  REPEAT 36 [
    MAKE "color MODULO REPCOUNT 7
    IF (:color = 0) [SETPC [255 0 0]] ; RED
    IF (:color = 1) [SETPC [0 0 255]] ; BLUE
    IF (:color = 2) [SETPC [0 255 0]] ; GREEN
    IF (:color = 3) [SETPC [255 255 0]] ; YELLOW
    IF (:color = 4) [SETPC [255 165 0]] ; ORANGE
    IF (:color = 5) [SETPC [128 0 128]] ; PURPLE
    IF (:color = 6) [SETPC [255 192 203]] ; PINK
    FD 10 + REPCOUNT
    RT 10
  ]
  ```
- Observe how the colors cycle through a rainbow pattern!

---

Happy coding! 🎨
