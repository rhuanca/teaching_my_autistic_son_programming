# Day 16: MODULO and Patterns

Today, we will use the MODULO operator to create a pattern of two parallel stepped lines. The horizontal lines will have one color, and the vertical lines will have another color. This will help you understand how the MODULO operator can be used to alternate between values.

## What is the MODULO Operator?
- The MODULO operator (`MODULO` in FMSLogo) gives the remainder when one number is divided by another.
- Example in FMSLogo:
  ```logo
  PRINT MODULO 5 2
  ; Output: 1 (because 5 divided by 2 leaves a remainder of 1)
  ```
- You can use MODULO to alternate between values, such as colors.

## Pattern to Draw

### Example Output
![Parallel Stepped Lines](Day_16/images/parallel_stepped_lines.png)

### Task
Create a pattern of two parallel stepped lines where:
- Horizontal lines have one color.
- Vertical lines have another color.
- Use the MODULO operator to alternate between the two colors.

## Instructions
1. Open FMSLogo.
2. Use the `MAKE` command to create variables for the step size, number of steps, and colors.
3. Use the MODULO operator to alternate between two colors.
4. Write a procedure to draw the pattern.

## Challenge
- Modify the procedure to use more than two colors.
- Experiment with different step sizes and lengths.

---

Happy coding! 🎨
