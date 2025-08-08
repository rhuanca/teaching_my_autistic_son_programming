# FMSLogo Quick Reference Card

## Basic Movement Commands
| Command | Shortcut | Description | Example |
|---------|----------|-------------|---------|
| `FORWARD 100` | `FD 100` | Move turtle forward 100 steps | `FD 50` |
| `BACKWARD 50` | `BK 50` | Move turtle backward 50 steps | `BK 25` |
| `RIGHT 90` | `RT 90` | Turn turtle right 90 degrees | `RT 45` |
| `LEFT 90` | `LT 90` | Turn turtle left 90 degrees | `LT 180` |

## Pen Control
| Command | Shortcut | Description |
|---------|----------|-------------|
| `PENUP` | `PU` | Lift pen (move without drawing) |
| `PENDOWN` | `PD` | Put pen down (draw when moving) |
| `PENCOLOR RED` | `PC RED` | Change pen color |
| `SETPENSIZE 3` | | Make pen thicker |

## Position and Direction
| Command | Description | Example |
|---------|-------------|---------|
| `HOME` | Return turtle to center, facing up | `HOME` |
| `SETHEADING 0` | Set turtle direction (0=up, 90=right, 180=down, 270=left) | `SETHEADING 45` |
| `SETXY 100 50` | Move turtle to specific coordinates | `SETXY -50 75` |
| `XCOR` | Show current X position | |
| `YCOR` | Show current Y position | |

## Screen Control
| Command | Shortcut | Description |
|---------|----------|-------------|
| `CLEARSCREEN` | `CS` | Clear screen and return turtle to center |
| `HIDETURTLE` | `HT` | Hide the turtle arrow |
| `SHOWTURTLE` | `ST` | Show the turtle arrow |

## Basic Shapes
| Shape | Command |
|-------|---------|
| **Square** | `REPEAT 4 [FD 100 RT 90]` |
| **Triangle** | `REPEAT 3 [FD 100 RT 120]` |
| **Circle** | `REPEAT 36 [FD 5 RT 10]` |
| **Line** | `FD 100` |

## Colors
**Common Colors:** RED, BLUE, GREEN, YELLOW, BLACK, WHITE, ORANGE, PURPLE, PINK, BROWN, GRAY

## Useful Tips
- Type commands and press ENTER
- Use SPACE between command and number: `FD 100` not `FD100`
- Commands are not case-sensitive: `fd` = `FD` = `Forward`
- To stop a running program: Press Ctrl+G or click HALT
- To see command history: Use UP and DOWN arrow keys

## Angles Quick Reference
- **0°** = Up (North)
- **90°** = Right (East)  
- **180°** = Down (South)
- **270°** = Left (West)

## Common Mistakes to Avoid
- Forgetting spaces: `FD100` ❌ → `FD 100` ✅
- Wrong angle for shapes: Triangle uses 120°, not 60°
- Forgetting to put pen down after PENUP
- Not using REPEAT for repetitive patterns