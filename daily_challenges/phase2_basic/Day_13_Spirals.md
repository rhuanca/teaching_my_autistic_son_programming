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

### Step 4: Introducing Variables
- Variables in FMSLogo allow you to store values and reuse them in your code.
- You can create a variable using the `MAKE` command.
  Example:
  ```
  MAKE "steps 10
  FD :steps
  ```
  - This creates a variable `steps` with a value of `10`.
  - The `FD :steps` command moves the turtle forward by the value stored in `steps`.

- Let's modify the spiral code to use variables:
  ```
  MAKE "angle 10
  MAKE "distance 10
  REPEAT 36 [
    FD :distance
    RT :angle
    MAKE "distance :distance + 2 ; Increment the distance
  ]
  ```
  - This code uses variables `angle` and `distance` to control the spiral.
  - The `distance` variable increases with each step, creating a gradual spiral effect.

### Step 5: Using the MODULO Operator
- The `MODULO` operator helps you find the remainder when dividing two numbers.
- This is useful for creating repeating patterns, such as cycling through colors.

- Example:
  ```
  PRINT MODULO 5 3
  ```
  - This outputs `2` because 5 divided by 3 leaves a remainder of 2.

- Let's use the `MODULO` operator in a spiral:
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
  - The `MODULO` operator cycles through numbers 0 to 6, allowing you to assign a different color for each step.

### Step 6: Using the SETPC Command
- The `SETPC` command in FMSLogo is used to set the pen color using RGB values.
- RGB values are a way to represent colors using three numbers: Red, Green, and Blue.
  - Each number can range from 0 to 255.
  - For example, `[255 0 0]` represents red, `[0 255 0]` represents green, and `[0 0 255]` represents blue.

- Example:
  ```
  SETPC [255 0 0] ; Sets the pen color to red
  FD 50
  SETPC [0 255 0] ; Sets the pen color to green
  FD 50
  ```
  - This code changes the pen color to red, moves forward, then changes it to green and moves forward again.

- You can use `SETPC` to create colorful patterns by combining it with loops and variables.

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
