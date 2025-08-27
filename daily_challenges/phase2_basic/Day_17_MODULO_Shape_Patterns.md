# Day 17: MODULO for Shape Patterns

**Date:** ___________

## Today's Mission 🚀
Learn how to use the `MODULO` operator to create patterns with different shapes!

### Step 1: Create a Shape Pattern
- Open FMSLogo and type `CS` to clear the screen.
- Try this code:
  ```
  REPEAT 36 [
    MAKE "shape MODULO REPCOUNT 3
    IF (:shape = 0) [REPEAT 3 [FD 50 RT 120]] ; Triangle
    IF (:shape = 1) [REPEAT 4 [FD 50 RT 90]] ; Square
    IF (:shape = 2) [REPEAT 5 [FD 50 RT 72]] ; Pentagon
    RT 10
  ]
  ```
- Observe how the shapes cycle between a triangle, square, and pentagon!

---

Happy coding! 🎨
