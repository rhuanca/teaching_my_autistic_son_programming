# Day 13: Spirals

**Date:** ___________

## Today's Mission 🚀
Learn how to create spirals by incrementally increasing distances or angles!

### New Concept:
- Incremental changes: Gradually increase the distance or angle in each step to create a spiral effect.

---

## Let's Start!

### Step 1: Simple Spiral
- [ ] Open FMSLogo and type `CS` to clear the screen.
- [ ] Try this code:
  ```
  REPEAT 36 [ FD 10 RT 10 ]
  ```
- [ ] Observe the circular pattern created.

### Step 2: Gradual Spiral
- [ ] Type `CS` to start fresh.
- [ ] Try this code:
  ```
  REPEAT 36 [ FD 10 + REPCOUNT RT 10 ]
  ```
- [ ] Notice how the spiral grows larger with each step!

### Step 3: Learn About the MODULO Operator
- The `MODULO` operator helps find the remainder when dividing two numbers.
- Example:
  - `5 MODULO 2` gives `1` because 5 divided by 2 leaves a remainder of 1.
  - `6 MODULO 3` gives `0` because 6 is evenly divisible by 3.
- Try these commands in FMSLogo:
  ```
  PRINT 5 MODULO 2
  PRINT 6 MODULO 3
  PRINT 10 MODULO 4
  ```
- Notice how the `MODULO` operator cycles through numbers, which is useful for patterns!

---

## Challenge Time! ⭐

### Easy:
- Create a spiral with smaller steps by reducing the angle (e.g., `RT 5`).

### Hard:
- Create a colorful spiral by using the `SETPC` command inside the `REPEAT` loop.
  Example:
  ```
  REPEAT 36 [
        MAKE "remainder MODULO REPCOUNT 7
        MAKE "color :remainder
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

---

Happy coding! 🎨
