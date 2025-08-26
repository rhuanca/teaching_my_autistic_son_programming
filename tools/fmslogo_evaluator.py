#!/usr/bin/env python3
"""
FMSLogo Code Evaluator
A tool to automatically evaluate FMSLogo code submissions from daily challenges.
"""

import turtle
import math
import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

class TurtleSimulator:
    """Simulates turtle movements without graphics for evaluation"""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.heading = 90.0  # FMSLogo starts facing up
        self.pen_down = True
        self.pen_color = "black"
    
    def position(self):
        return (self.x, self.y)
    
    def heading_angle(self):
        return self.heading
    
    def isdown(self):
        return self.pen_down
    
    def pencolor(self):
        return self.pen_color
    
    def forward(self, distance):
        rad = math.radians(self.heading)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)
    
    def backward(self, distance):
        self.forward(-distance)
    
    def right(self, angle):
        self.heading = (self.heading - angle) % 360
    
    def left(self, angle):
        self.heading = (self.heading + angle) % 360
    
    def penup(self):
        self.pen_down = False
    
    def pendown(self):
        self.pen_down = True
    
    def home(self):
        self.x = 0.0
        self.y = 0.0
        self.heading = 90.0
    
    def setheading(self, angle):
        self.heading = angle % 360
    
    def color(self, color):
        self.pen_color = color
    
    def clear(self):
        pass  # Just a placeholder

class FMSLogoEvaluator:
    def __init__(self):
        self.screen = None
        self.turtle = None
        self.simulation_mode = False
        self.reset_graphics()
        
        # Track turtle state during execution
        self.positions = []
        self.angles = []
        self.pen_states = []
        self.colors = []
        self.commands_used = []
        self.repeat_commands_used = []  # Track REPEAT usage separately
        
    def reset_graphics(self, force_simulation=False):
        """Initialize or reset turtle graphics"""
        if self.screen:
            try:
                self.screen.bye()
            except:
                pass
        
        if force_simulation:
            # Force simulation mode (for console or when graphics fail)
            print("Running in simulation mode (no graphics window)")
            self.simulation_mode = True
            self.screen = None
            self.turtle = TurtleSimulator()
        else:
            # Try graphics first, fall back to simulation if it fails
            try:
                # Clear any existing turtle instances
                turtle.TurtleScreen._RUNNING = True
                
                self.screen = turtle.Screen()
                self.screen.setup(600, 600)
                self.screen.bgcolor("white")
                self.screen.title("FMSLogo Code Evaluator - Results")
                
                # Disable animation for faster execution
                self.screen.tracer(0)
                
                self.turtle = turtle.Turtle()
                self.turtle.speed(0)
                self.turtle.shape("triangle")
                
                self.simulation_mode = False
                print("Graphics window initialized successfully")
                
            except Exception as e:
                print(f"Graphics failed ({e}), using simulation mode")
                self.simulation_mode = True
                self.screen = None
                self.turtle = TurtleSimulator()
        
        self.reset_turtle_state()
    
    def reset_turtle_state(self):
        """Reset turtle to starting position and clear tracking"""
        try:
            self.turtle.clear()
            self.turtle.home()
            self.turtle.pendown()
            self.turtle.color("black")
            self.turtle.setheading(90)  # Face up like FMSLogo
        except Exception as e:
            if not self.simulation_mode:
                print(f"Graphics command failed: {e}, switching to simulation mode")
                self.simulation_mode = True
                self.screen = None
                self.turtle = TurtleSimulator()
                self.turtle.clear()
                self.turtle.home()
                self.turtle.pendown()
                self.turtle.color("black")
                self.turtle.setheading(90)
        
        # Reset tracking
        self.positions = [(0, 0)]
        self.angles = [90]  # FMSLogo starts facing up
        self.pen_states = [True]
        self.colors = ["black"]
        self.commands_used = []
        self.repeat_commands_used = []
    
    def track_state(self, command):
        """Track turtle state after each command"""
        try:
            self.positions.append(self.turtle.position())
            # Handle both real turtle and simulator
            if self.simulation_mode:
                self.angles.append(self.turtle.heading_angle())
            else:
                self.angles.append(self.turtle.heading())
            self.pen_states.append(self.turtle.isdown())
            self.colors.append(self.turtle.pencolor())
        except Exception as e:
            if not self.simulation_mode:
                print(f"Tracking failed: {e}, switching to simulation mode")
                self.simulation_mode = True
                self.screen = None
                self.turtle = TurtleSimulator()
        self.commands_used.append(command)
    
    def switch_to_simulation(self):
        """Switch from graphics to simulation mode"""
        if self.screen:
            try:
                self.screen.bye()
            except:
                pass
        self.simulation_mode = True
        self.screen = None
        # Copy current state from graphics turtle to simulator
        old_pos = self.positions[-1] if self.positions else (0, 0)
        old_angle = self.angles[-1] if self.angles else 90
        old_pen = self.pen_states[-1] if self.pen_states else True
        old_color = self.colors[-1] if self.colors else "black"
        
        self.turtle = TurtleSimulator()
        self.turtle.x, self.turtle.y = old_pos
        self.turtle.heading = old_angle
        self.turtle.pen_down = old_pen
        self.turtle.pen_color = old_color
    
    def execute_command(self, func_name, *args):
        """Execute a turtle command with automatic fallback to simulation"""
        try:
            getattr(self.turtle, func_name)(*args)
        except Exception as e:
            if not self.simulation_mode:
                print(f"Graphics command failed, switching to simulation mode")
                self.switch_to_simulation()
                getattr(self.turtle, func_name)(*args)
    
    def parse_line_with_repeat(self, line):
        """Parse a line that might contain REPEAT commands"""
        if 'REPEAT' not in line:
            # No REPEAT, just split by spaces
            return line.split()
        
        # Handle REPEAT command: REPEAT n [commands]
        try:
            # Find REPEAT pattern
            if line.startswith('REPEAT'):
                parts = line.split('[', 1)
                if len(parts) != 2:
                    print(f"Error: REPEAT needs [ ] brackets: {line}")
                    return line.split()
                
                # Extract repeat count
                repeat_part = parts[0].strip()  # "REPEAT n"
                commands_part = parts[1].strip()  # "commands]"
                
                if not commands_part.endswith(']'):
                    print(f"Error: REPEAT needs closing ] bracket: {line}")
                    return line.split()
                
                # Remove closing bracket
                commands_part = commands_part[:-1].strip()
                
                # Get repeat count
                repeat_words = repeat_part.split()
                if len(repeat_words) != 2:
                    print(f"Error: REPEAT format should be 'REPEAT n': {line}")
                    return line.split()
                
                try:
                    repeat_count = int(repeat_words[1])
                except ValueError:
                    print(f"Error: REPEAT count must be a number: {line}")
                    return line.split()
                
                # Track REPEAT usage for evaluation
                self.repeat_commands_used.append(f"REPEAT {repeat_count} [{commands_part}]")
                
                # Expand REPEAT into individual commands
                expanded_commands = []
                command_list = commands_part.split()
                for _ in range(repeat_count):
                    expanded_commands.extend(command_list)
                
                return expanded_commands
            else:
                # REPEAT somewhere else in line - not supported yet
                return line.split()
                
        except Exception as e:
            print(f"Error parsing REPEAT: {e}")
            return line.split()
    
    def parse_and_execute(self, code):
        """Parse FMSLogo code and execute with Python turtle"""
        self.reset_turtle_state()
        
        # Clean and split code into commands, handling REPEAT
        lines = code.strip().split('\n')
        commands = []
        for line in lines:
            line = line.strip().upper()
            if line and not line.startswith('#') and not line.startswith('//'):
                commands.extend(self.parse_line_with_repeat(line))
        
        print(f"Executing commands: {commands}")
        
        i = 0
        while i < len(commands):
            cmd = commands[i]
            
            try:
                if cmd in ['FORWARD', 'FD']:
                    if i + 1 < len(commands):
                        distance = float(commands[i + 1])
                        self.execute_command('forward', distance)
                        self.track_state(f"FD {distance}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['BACKWARD', 'BK', 'BACK']:
                    if i + 1 < len(commands):
                        distance = float(commands[i + 1])
                        self.execute_command('backward', distance)
                        self.track_state(f"BK {distance}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['RIGHT', 'RT']:
                    if i + 1 < len(commands):
                        angle = float(commands[i + 1])
                        self.execute_command('right', angle)
                        self.track_state(f"RT {angle}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['LEFT', 'LT']:
                    if i + 1 < len(commands):
                        angle = float(commands[i + 1])
                        self.execute_command('left', angle)
                        self.track_state(f"LT {angle}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['PENUP', 'PU']:
                    self.execute_command('penup')
                    self.track_state("PU")
                    i += 1
                    
                elif cmd in ['PENDOWN', 'PD']:
                    self.execute_command('pendown')
                    self.track_state("PD")
                    i += 1
                    
                elif cmd in ['HOME']:
                    self.execute_command('home')
                    self.execute_command('setheading', 90)  # Face up like FMSLogo
                    self.track_state("HOME")
                    i += 1
                    
                elif cmd in ['CLEARSCREEN', 'CS']:
                    self.execute_command('clear')
                    self.execute_command('home')
                    self.execute_command('setheading', 90)
                    self.track_state("CS")
                    i += 1
                    
                elif cmd == 'PENCOLOR':
                    if i + 1 < len(commands):
                        color = commands[i + 1].lower()
                        color_map = {
                            'red': 'red', 'blue': 'blue', 'green': 'green',
                            'yellow': 'yellow', 'black': 'black', 'white': 'white',
                            'orange': 'orange', 'purple': 'purple', 'pink': 'pink',
                            'brown': 'brown', 'gray': 'gray', 'grey': 'gray'
                        }
                        if color in color_map:
                            self.turtle.color(color_map[color])
                            self.track_state(f"PENCOLOR {color.upper()}")
                        i += 2
                    else:
                        print(f"Error: PENCOLOR needs a color name")
                        i += 1
                        
                else:
                    print(f"Unknown command: {cmd}")
                    i += 1
                    
            except (ValueError, TypeError) as e:
                print(f"Error with command {cmd}: {e}")
                i += 1
            except Exception as e:
                print(f"Unexpected error with {cmd}: {e}")
                i += 1
    
    def evaluate_day(self, code, day_number):
        """Evaluate code against specific day requirements"""
        try:
            self.parse_and_execute(code)
            
            if day_number == 1:
                return self.evaluate_day1()
            elif day_number == 2:
                return self.evaluate_day2()
            elif day_number == 3:
                return self.evaluate_day3()
            elif day_number == 4:
                return self.evaluate_day4()
            elif day_number == 5:
                return self.evaluate_day5()
            elif day_number == 6:
                return self.evaluate_day6()
            elif day_number == 7:
                return self.evaluate_day7()
            elif day_number == 8:
                return self.evaluate_day8()
            elif day_number == 9:
                return self.evaluate_day9()
            elif day_number == 10:
                return self.evaluate_day10()
            else:
                return {"error": f"Day {day_number} not implemented yet"}
        except Exception as e:
            return {"error": f"Execution error: {str(e)}"}
    
    def evaluate_day1(self):
        """Day 1: Forward and Backward"""
        results = {
            "day": 1,
            "title": "First Steps - Forward and Backward",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Uses movement commands
        has_movement = any(cmd.startswith(('FD', 'BK', 'FORWARD', 'BACKWARD')) 
                          for cmd in self.commands_used)
        if has_movement:
            results["tests"].append({"name": "Uses movement commands", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Great! You used movement commands!")
        else:
            results["tests"].append({"name": "Uses movement commands", "passed": False})
            results["feedback"].append("❌ Try using FORWARD or BACKWARD commands")
        results["total"] += 1
        
        # Test 2: Creates visible lines
        if len(set(self.positions)) > 1:
            results["tests"].append({"name": "Creates visible drawing", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! You drew something visible!")
        else:
            results["tests"].append({"name": "Creates visible drawing", "passed": False})
            results["feedback"].append("❌ Make sure to use numbers with commands: FD 100")
        results["total"] += 1
        
        # Test 3: Bonus - Uses multiple commands
        if len(self.commands_used) >= 2:
            results["tests"].append({"name": "BONUS: Uses multiple commands", "passed": True})
            results["passed"] += 1
            results["feedback"].append("⭐ Excellent! You used multiple commands!")
        results["total"] += 1
        
        return results
    
    def evaluate_day2(self):
        """Day 2: Left and Right turns"""
        results = {
            "day": 2,
            "title": "Turning Around - Left and Right",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Uses turning commands
        has_turns = any(cmd.startswith(('RT', 'LT', 'RIGHT', 'LEFT')) 
                       for cmd in self.commands_used)
        if has_turns:
            results["tests"].append({"name": "Uses turning commands", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Great! You made the turtle turn!")
        else:
            results["tests"].append({"name": "Uses turning commands", "passed": False})
            results["feedback"].append("❌ Try using RIGHT 90 or LEFT 90")
        results["total"] += 1
        
        # Test 2: Changes direction
        angle_changes = len(set([round(a) for a in self.angles])) > 1
        if angle_changes:
            results["tests"].append({"name": "Turtle changes direction", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Awesome! The turtle changed direction!")
        else:
            results["tests"].append({"name": "Turtle changes direction", "passed": False})
            results["feedback"].append("❌ Make sure turtle actually turns")
        results["total"] += 1
        
        # Test 3: Creates connected lines (corner)
        has_movement = any(cmd.startswith(('FD', 'BK')) for cmd in self.commands_used)
        if has_turns and has_movement and len(self.positions) >= 3:
            results["tests"].append({"name": "Creates connected lines with corners", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! You made connected lines with corners!")
        else:
            results["tests"].append({"name": "Creates connected lines with corners", "passed": False})
            results["feedback"].append("❌ Try: FD 50, RT 90, FD 50")
        results["total"] += 1
        
        return results
    
    def evaluate_day3(self):
        """Day 3: All Directions - Lines from center using HOME"""
        results = {
            "day": 3,
            "title": "All Directions - Lines from Center",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Uses HOME command
        has_home = any('HOME' in cmd for cmd in self.commands_used)
        if has_home:
            results["tests"].append({"name": "Uses HOME command", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Great! You used HOME to return to center!")
        else:
            results["tests"].append({"name": "Uses HOME command", "passed": False})
            results["feedback"].append("❌ Try using HOME to return to center between lines")
        results["total"] += 1
        
        # Test 2: Creates radial pattern (multiple directions from center)
        # Count how many times turtle returns close to center (0,0)
        center_returns = 0
        for pos in self.positions:
            distance_from_center = math.sqrt(pos[0]**2 + pos[1]**2)
            if distance_from_center < 20:  # Close to center
                center_returns += 1
        
        if center_returns >= 3:  # At least 3 times at center (start + 2 returns)
            results["tests"].append({"name": "Creates radial pattern from center", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Excellent! You made lines going out from center!")
        else:
            results["tests"].append({"name": "Creates radial pattern from center", "passed": False})
            results["feedback"].append("❌ Try: FD 50, HOME, RT 90, FD 50, HOME")
        results["total"] += 1
        
        # Test 3: Uses different directions (various angles or turns)
        has_turns = any(cmd.startswith(('RT', 'LT', 'RIGHT', 'LEFT')) 
                       for cmd in self.commands_used)
        different_angles = len(set([round(a/45)*45 for a in self.angles])) >= 3  # At least 3 different directions
        
        if has_turns and different_angles:
            results["tests"].append({"name": "Uses different directions", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! You drew lines in different directions!")
        else:
            results["tests"].append({"name": "Uses different directions", "passed": False})
            results["feedback"].append("❌ Try turning to different angles: RT 90, RT 180, LT 90")
        results["total"] += 1
        
        # Test 4: Bonus - Creates star-like pattern (4+ directions)
        if center_returns >= 5 and different_angles:  # More returns = more lines
            results["tests"].append({"name": "BONUS: Creates star pattern", "passed": True})
            results["passed"] += 1
            results["feedback"].append("⭐ Amazing! You created a star-like pattern!")
        results["total"] += 1
        
        return results
    
    def evaluate_day4(self):
        """Day 4: Pen Control - PENUP and PENDOWN"""
        results = {
            "day": 4,
            "title": "Pen Control - Up and Down",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Uses PENUP command
        has_penup = any('PU' in cmd or 'PENUP' in cmd for cmd in self.commands_used)
        if has_penup:
            results["tests"].append({"name": "Uses PENUP command", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Great! You lifted the pen with PENUP!")
        else:
            results["tests"].append({"name": "Uses PENUP command", "passed": False})
            results["feedback"].append("❌ Try using PENUP (or PU) to lift the pen")
        results["total"] += 1
        
        # Test 2: Uses PENDOWN command  
        has_pendown = any('PD' in cmd or 'PENDOWN' in cmd for cmd in self.commands_used)
        if has_pendown:
            results["tests"].append({"name": "Uses PENDOWN command", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! You put the pen down with PENDOWN!")
        else:
            results["tests"].append({"name": "Uses PENDOWN command", "passed": False})
            results["feedback"].append("❌ Try using PENDOWN (or PD) to put the pen down")
        results["total"] += 1
        
        # Test 3: Shows pen state control (changes between up/down)
        pen_changes = 0
        for i in range(1, len(self.pen_states)):
            if self.pen_states[i] != self.pen_states[i-1]:
                pen_changes += 1
                
        if pen_changes >= 2:  # At least 2 pen state changes (up then down, or down then up)
            results["tests"].append({"name": "Controls pen state properly", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Excellent! You controlled when to draw and when not to draw!")
        else:
            results["tests"].append({"name": "Controls pen state properly", "passed": False})
            results["feedback"].append("❌ Try: FD 50, PU, FD 50, PD, FD 50")
        results["total"] += 1
        
        # Test 4: Bonus - Creates separated elements (moves without drawing)
        if has_penup and has_pendown and len(self.positions) >= 4:
            results["tests"].append({"name": "BONUS: Creates separate shapes", "passed": True})
            results["passed"] += 1
            results["feedback"].append("⭐ Amazing! You made separate shapes or dashed lines!")
        results["total"] += 1
        
        return results
    
    def evaluate_day6(self):
        """Day 6: Triangle Time"""
        results = {
            "day": 6,
            "title": "Triangle Time",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Uses 120-degree turns (correct for triangles)
        has_120_turns = any('120' in cmd for cmd in self.commands_used)
        if has_120_turns:
            results["tests"].append({"name": "Uses 120-degree turns", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! You used RT 120 for triangle corners!")
        else:
            results["tests"].append({"name": "Uses 120-degree turns", "passed": False})
            results["feedback"].append("❌ Triangles need RT 120 turns, not RT 90!")
        results["total"] += 1
        
        # Test 2: Shows triangle drawing attempt (at least 2 triangle sides)
        triangle_sides = 0
        i = 0
        while i < len(self.commands_used) - 1:
            cmd = self.commands_used[i]
            next_cmd = self.commands_used[i + 1] if i + 1 < len(self.commands_used) else ""
            
            # Count FD commands followed by RT 120
            if cmd.startswith('FD') and ('RT 120' in next_cmd or 'LT 120' in next_cmd):
                triangle_sides += 1
            i += 1
            
        if triangle_sides >= 2:  # At least 2 sides of triangle with correct turns
            results["tests"].append({"name": "Draws triangle with correct angles", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Great! You drew triangle sides with RT 120!")
        else:
            results["tests"].append({"name": "Draws triangle with correct angles", "passed": False})
            results["feedback"].append("❌ Try: FD 80, RT 120, FD 80, RT 120, FD 80")
        results["total"] += 1
        
        # Test 3: Has enough commands for a triangle (at least 6: FD RT FD RT FD RT)
        movement_commands = len([cmd for cmd in self.commands_used if cmd.startswith(('FD', 'FORWARD'))])
        turn_commands = len([cmd for cmd in self.commands_used if 'RT' in cmd or 'LT' in cmd])
        
        if movement_commands >= 3 and turn_commands >= 3:
            results["tests"].append({"name": "Has enough commands for triangle", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Excellent! You have enough sides and turns!")
        else:
            results["tests"].append({"name": "Has enough commands for triangle", "passed": False})
            results["feedback"].append("❌ A triangle needs 3 forward moves and 3 turns")
        results["total"] += 1
        
        # Test 4: Bonus - Demonstrates triangle vs square understanding
        has_90_turns = any('90' in cmd for cmd in self.commands_used)  
        has_both_shapes = has_120_turns and has_90_turns
        
        if has_both_shapes:
            results["tests"].append({"name": "BONUS: Shows both triangles and squares", "passed": True})
            results["passed"] += 1
            results["feedback"].append("⭐ Amazing! You made both triangles (RT 120) and squares (RT 90)!")
        elif has_120_turns:
            results["tests"].append({"name": "BONUS: Uses triangle angles", "passed": True})
            results["passed"] += 1
            results["feedback"].append("⭐ Great! You understand triangle angles!")
        results["total"] += 1
        
        return results
    
    def evaluate_day7(self):
        """Day 7: Colors and Fun"""
        results = {
            "day": 7,
            "title": "Colors and Fun",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Uses PENCOLOR command
        has_pencolor = any('PENCOLOR' in cmd for cmd in self.commands_used)
        if has_pencolor:
            results["tests"].append({"name": "Uses PENCOLOR command", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Great! You changed pen colors!")
        else:
            results["tests"].append({"name": "Uses PENCOLOR command", "passed": False})
            results["feedback"].append("❌ Try using PENCOLOR RED or PENCOLOR BLUE")
        results["total"] += 1
        
        # Test 2: Uses multiple colors
        unique_colors = set()
        for cmd in self.commands_used:
            if 'PENCOLOR' in cmd:
                # Extract color from command like "PENCOLOR RED"
                parts = cmd.split()
                if len(parts) > 1:
                    unique_colors.add(parts[1])
        
        if len(unique_colors) >= 2:
            results["tests"].append({"name": "Uses multiple colors", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Awesome! You used multiple colors!")
        else:
            results["tests"].append({"name": "Uses multiple colors", "passed": False})
            results["feedback"].append("❌ Try using different colors like RED, BLUE, GREEN")
        results["total"] += 1
        
        # Test 3: Creates colorful drawing (color changes + movement)
        color_changes = len([cmd for cmd in self.commands_used if 'PENCOLOR' in cmd])
        has_movement = any(cmd.startswith(('FD', 'BK')) for cmd in self.commands_used)
        
        if color_changes >= 2 and has_movement:
            results["tests"].append({"name": "Creates colorful drawing", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! You made a colorful drawing!")
        else:
            results["tests"].append({"name": "Creates colorful drawing", "passed": False})
            results["feedback"].append("❌ Try: PENCOLOR RED, FD 50, PENCOLOR BLUE, FD 50")
        results["total"] += 1
        
        # Test 4: Bonus - Uses 3 or more colors  
        if len(unique_colors) >= 3:
            results["tests"].append({"name": "BONUS: Rainbow creation", "passed": True})
            results["passed"] += 1
            results["feedback"].append("⭐ Amazing! You created a colorful rainbow!")
        results["total"] += 1
        
        return results
    
    def evaluate_day8(self):
        """Day 8: First REPEAT - The Power Loop!"""
        results = {
            "day": 8,
            "title": "First REPEAT - The Power Loop!",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Uses REPEAT command
        has_repeat = len(self.repeat_commands_used) > 0
        if has_repeat:
            results["tests"].append({"name": "Uses REPEAT command", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Awesome! You discovered the power of REPEAT!")
        else:
            results["tests"].append({"name": "Uses REPEAT command", "passed": False})
            results["feedback"].append("❌ Try using REPEAT 4 [FD 80 RT 90] for a square")
        results["total"] += 1
        
        # Test 2: Creates recognizable shape (returns close to start)
        start_pos = self.positions[0]
        end_pos = self.positions[-1]
        distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
        
        if distance < 30:  # Close to starting position = closed shape
            results["tests"].append({"name": "Creates closed shape", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! Your shape closes properly!")
        else:
            results["tests"].append({"name": "Creates closed shape", "passed": False})
            results["feedback"].append("❌ Make sure your shape closes: try REPEAT 4 [FD 80 RT 90]")
        results["total"] += 1
        
        # Test 3: Uses efficient coding (fewer typed commands than old way)
        total_commands = len(self.commands_used)
        if has_repeat and total_commands <= 10:  # REPEAT makes code much shorter
            results["tests"].append({"name": "Writes efficient code", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Great! REPEAT made your code much shorter!")
        else:
            results["tests"].append({"name": "Writes efficient code", "passed": False})
            results["feedback"].append("❌ REPEAT should make your code shorter - try REPEAT instead of typing each command")
        results["total"] += 1
        
        # Test 4: Bonus - Shows understanding of loops concept
        if has_repeat and distance < 30:  # Both uses REPEAT AND makes proper shape
            results["tests"].append({"name": "BONUS: Masters loop concept", "passed": True})
            results["passed"] += 1
            results["feedback"].append("⭐ Amazing! You understand how loops work!")
        results["total"] += 1
        
        return results

    def evaluate_day_8(self):
        """Evaluate Day 8: REPEAT Command Patterns"""
        print("\nEvaluating Day 8: REPEAT Command Patterns")

        # Reset turtle state
        self.reset_turtle_state()

        # Example Day 8 pattern: Draw a square using REPEAT
        try:
            self.execute_command("REPEAT 4 [ FD 100 RT 90 ]")
            print("Day 8 evaluation completed successfully.")
        except Exception as e:
            print(f"Error during Day 8 evaluation: {e}")

    def evaluate_day_9(self):
        """Evaluate Day 9: Advanced REPEAT Patterns"""
        print("\nEvaluating Day 9: Advanced REPEAT Patterns")

        # Reset turtle state
        self.reset_turtle_state()

        # Example Day 9 pattern: Draw a star using REPEAT
        try:
            self.execute_command("REPEAT 5 [ FD 100 RT 144 ]")
            print("Day 9 evaluation completed successfully.")
        except Exception as e:
            print(f"Error during Day 9 evaluation: {e}")

# Example usage
if __name__ == "__main__":
    evaluator = FMSLogoEvaluator()
    evaluator.evaluate_day_9()
    
    def close(self):
        """Close the evaluator and clean up resources"""
        if self.screen and not self.simulation_mode:
            try:
                self.screen.bye()
            except Exception as e:
                print(f"Error closing graphics window: {e}")
        print("Evaluator closed successfully.")

class EvaluatorGUI:
    def __init__(self):
        self.evaluator = FMSLogoEvaluator()
        self.setup_gui()
    
    def setup_gui(self):
        """Create the GUI interface"""
        self.root = tk.Tk()
        self.root.title("FMSLogo Code Evaluator")
        self.root.geometry("800x600")
        
        # Day selection
        day_frame = tk.Frame(self.root)
        day_frame.pack(pady=10)
        
        tk.Label(day_frame, text="Day:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.day_var = tk.StringVar(value="1")
        day_menu = tk.OptionMenu(day_frame, self.day_var, "1", "2", "3", "4", "5", "6", "7")
        day_menu.pack(side=tk.LEFT, padx=(5, 0))
        
        # Code input
        tk.Label(self.root, text="Enter FMSLogo Code:", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        tk.Label(self.root, text="Enter FMSLogo Code:", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        self.code_text = scrolledtext.ScrolledText(self.root, height=10, font=("Courier", 10))
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="📊 Evaluate Code", command=self.evaluate_code,
                 bg="lightblue", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🧹 Clear", command=self.clear_code,
                 font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="❌ Exit", command=self.close_app,
                 bg="lightcoral", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        # Results display
        tk.Label(self.root, text="Results:", font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=10)
        self.results_text = scrolledtext.ScrolledText(self.root, height=8, font=("Courier", 10))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Example code
        example_code = """CS
FD 100
RT 90
FD 100"""
        self.code_text.insert("1.0", example_code)
    
    def evaluate_code(self):
        """Evaluate the entered code"""
        code = self.code_text.get("1.0", tk.END).strip()
        day = int(self.day_var.get())
        
        if not code:
            messagebox.showwarning("Warning", "Please enter some code to evaluate!")
            return
        
        try:
            # Reset evaluator for new evaluation (try graphics first in GUI mode)
            self.evaluator.reset_graphics(force_simulation=False)
            results = self.evaluator.evaluate_day(code, day)
            
            # Update graphics window if available
            if self.evaluator.screen and not self.evaluator.simulation_mode:
                self.evaluator.screen.update()
                # Keep window open for viewing
                self.evaluator.screen.tracer(1)
                # Set clear title for closing
                self.evaluator.screen.title("FMSLogo Results - Close with X button or click anywhere")
                # Make window close on click (non-blocking)
                def close_on_click(x, y):
                    try:
                        self.evaluator.close()
                    except:
                        pass
                self.evaluator.screen.onclick(close_on_click)
            
            # Display results
            self.display_results(results)
            
        except Exception as e:
            messagebox.showerror("Error", f"Evaluation failed: {str(e)}")
    
    def display_results(self, results):
        """Display evaluation results"""
        self.results_text.delete("1.0", tk.END)
        
        if "error" in results:
            self.results_text.insert(tk.END, f"❌ Error: {results['error']}\n")
            return
        
        # Header
        self.results_text.insert(tk.END, f"📊 Results for Day {results['day']}: {results['title']}\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Score
        score = results['passed']
        total = results['total']
        percentage = (score / total * 100) if total > 0 else 0
        self.results_text.insert(tk.END, f"Score: {score}/{total} tests passed ({percentage:.0f}%)\n\n")
        
        # Individual test results
        self.results_text.insert(tk.END, "📋 Test Results:\n")
        for test in results['tests']:
            status = "✅ PASS" if test['passed'] else "❌ FAIL"
            self.results_text.insert(tk.END, f"  {status}: {test['name']}\n")
        
        # Feedback
        self.results_text.insert(tk.END, "\n💬 Feedback:\n")
        for feedback in results['feedback']:
            self.results_text.insert(tk.END, f"  {feedback}\n")
        
        # Overall assessment
        self.results_text.insert(tk.END, "\n📈 Overall Assessment:\n")
        if percentage >= 80:
            self.results_text.insert(tk.END, f"  🎉 Excellent work! Ready for the next day!\n")
        elif percentage >= 60:
            self.results_text.insert(tk.END, f"  👍 Good job! Try the challenge extensions!\n")
        else:
            self.results_text.insert(tk.END, f"  📚 Keep practicing! Review the lesson and try again!\n")
    
    def clear_code(self):
        """Clear the code input"""
        self.code_text.delete("1.0", tk.END)
        self.results_text.delete("1.0", tk.END)
    
    def close_app(self):
        """Close the application"""
        self.evaluator.close()
        self.root.destroy()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def show_console_results_gui(code, results, evaluator):
    """Show a GUI popup with visual results for console mode"""
    import tkinter as tk
    from tkinter import scrolledtext
    import turtle
    
    # Create popup window
    popup = tk.Tk()
    popup.title(f"Day {results['day']} Visual Results")
    popup.geometry("1000x700")
    
    # Create main frame with two sections
    main_frame = tk.Frame(popup)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Left side - embedded turtle graphics
    left_frame = tk.Frame(main_frame, relief=tk.SUNKEN, bd=2)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    tk.Label(left_frame, text="🐢 Turtle Drawing:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    
    # Create embedded turtle canvas
    canvas_frame = tk.Frame(left_frame)
    canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    try:
        # Create turtle canvas embedded in the tkinter window
        canvas = tk.Canvas(canvas_frame, width=400, height=400, bg="white")
        canvas.pack()
        
        # Create turtle screen using the canvas
        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("white")
        
        # Create turtle
        t = turtle.RawTurtle(screen)
        t.speed(0)
        t.shape("triangle")
        
        # Execute the code step by step for visual feedback
        lines = code.strip().split('\n')
        commands = []
        for line in lines:
            line = line.strip().upper()
            if line and not line.startswith('#'):
                words = line.split()
                commands.extend(words)
        
        # Execute commands
        i = 0
        while i < len(commands):
            cmd = commands[i]
            try:
                if cmd in ['CLEARSCREEN', 'CS']:
                    t.clear()
                    t.home()
                    t.setheading(90)
                    i += 1
                elif cmd in ['FORWARD', 'FD'] and i + 1 < len(commands):
                    t.forward(float(commands[i + 1]))
                    i += 2
                elif cmd in ['BACKWARD', 'BK'] and i + 1 < len(commands):
                    t.backward(float(commands[i + 1]))
                    i += 2
                elif cmd in ['RIGHT', 'RT'] and i + 1 < len(commands):
                    t.right(float(commands[i + 1]))
                    i += 2
                elif cmd in ['LEFT', 'LT'] and i + 1 < len(commands):
                    t.left(float(commands[i + 1]))
                    i += 2
                elif cmd in ['HOME']:
                    t.home()
                    t.setheading(90)
                    i += 1
                elif cmd in ['PENUP', 'PU']:
                    t.penup()
                    i += 1
                elif cmd in ['PENDOWN', 'PD']:
                    t.pendown()
                    i += 1
                else:
                    i += 1
            except:
                i += 1
        
        screen.update()
        tk.Label(left_frame, text="✅ Drawing complete! Click turtle canvas to close it.", 
                font=("Arial", 10), fg="green").pack(pady=2)
        
        # Add click to close functionality for embedded turtle
        def close_embedded_turtle():
            try:
                canvas.destroy()
            except:
                pass
        screen.onclick(lambda x, y: close_embedded_turtle())
                
    except Exception as e:
        tk.Label(left_frame, text=f"Graphics error: {str(e)}", 
                font=("Arial", 10), fg="red").pack(pady=5)
    
    # Right side - results
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    tk.Label(right_frame, text="📊 Evaluation Results:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    
    results_text = scrolledtext.ScrolledText(right_frame, height=20, font=("Courier", 10))
    results_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
    
    # Display results (same format as GUI)
    results_text.insert(tk.END, f"📊 Results for Day {results['day']}: {results['title']}\n")
    results_text.insert(tk.END, "=" * 50 + "\n\n")
    
    score = results['passed']
    total = results['total']
    percentage = (score / total * 100) if total > 0 else 0
    results_text.insert(tk.END, f"Score: {score}/{total} tests passed ({percentage:.0f}%)\n\n")
    
    results_text.insert(tk.END, "📋 Test Results:\n")
    for test in results['tests']:
        status = "✅ PASS" if test['passed'] else "❌ FAIL"
        results_text.insert(tk.END, f"  {status}: {test['name']}\n")
    
    results_text.insert(tk.END, "\n💬 Feedback:\n")
    for feedback in results['feedback']:
        results_text.insert(tk.END, f"  {feedback}\n")
    
    results_text.insert(tk.END, "\n📈 Overall Assessment:\n")
    if percentage >= 80:
        results_text.insert(tk.END, f"  🎉 Excellent work! Ready for the next day!\n")
    elif percentage >= 60:
        results_text.insert(tk.END, f"  👍 Good job! Try the challenge extensions!\n")
    else:
        results_text.insert(tk.END, f"  📚 Keep practicing! Review the lesson and try again!\n")
    
    # Close button
    close_btn = tk.Button(right_frame, text="✅ Close Results", 
                         command=popup.destroy,
                         bg="lightgreen", font=("Arial", 12))
    close_btn.pack(pady=5)
    
    # Handle window close
    popup.protocol("WM_DELETE_WINDOW", popup.destroy)
    
    # Show the popup
    popup.mainloop()

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        # Console mode
        print("FMSLogo Code Evaluator - Console Mode")
        print("=" * 40)
        
        evaluator = FMSLogoEvaluator()
        # Don't force simulation - let it try graphics for the popup
        
        try:
            # Get day number
            day = int(input("Which day is this for? (1-7): "))
            
            # Get code
            print("Enter your FMSLogo code (press Ctrl+D or Ctrl+Z when done):")
            code_lines = []
            try:
                while True:
                    line = input()
                    code_lines.append(line)
            except EOFError:
                pass
            
            code = '\n'.join(code_lines)
            
            # Evaluate
            results = evaluator.evaluate_day(code, day)
            
            # Display results in console first
            if "error" in results:
                print(f"❌ Error: {results['error']}")
                return
            
            print(f"\n📊 Results for Day {results['day']}: {results['title']}")
            print("=" * 60)
            print(f"Score: {results['passed']}/{results['total']} tests passed")
            
            print("\n📋 Test Results:")
            for test in results['tests']:
                status = "✅ PASS" if test['passed'] else "❌ FAIL"
                print(f"  {status}: {test['name']}")
            
            print("\n💬 Feedback:")
            for feedback in results['feedback']:
                print(f"  {feedback}")
            
            percentage = (results['passed'] / results['total']) * 100
            if percentage >= 80:
                print(f"\n🎉 Excellent work! ({percentage:.0f}%) Ready for next day!")
            elif percentage >= 60:
                print(f"\n👍 Good job! ({percentage:.0f}%) Try the challenges!")
            else:
                print(f"\n📚 Keep practicing! ({percentage:.0f}%) Review and try again!")
            
            # Now show GUI popup with visual results
            print(f"\n🖼️  Opening visual results window...")
            show_console_results_gui(code, results, evaluator)
            
            input("\nPress Enter to close...")
            
        except KeyboardInterrupt:
            print("\nEvaluation cancelled.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            evaluator.close()
    else:
        # GUI mode (default)
        app = EvaluatorGUI()
        app.run()

if __name__ == "__main__":
    main()
