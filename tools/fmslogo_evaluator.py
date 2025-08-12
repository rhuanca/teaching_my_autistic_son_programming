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

class FMSLogoEvaluator:
    def __init__(self):
        self.screen = None
        self.turtle = None
        self.reset_graphics()
        
        # Track turtle state during execution
        self.positions = []
        self.angles = []
        self.pen_states = []
        self.colors = []
        self.commands_used = []
        
    def reset_graphics(self):
        """Initialize or reset turtle graphics"""
        if self.screen:
            try:
                self.screen.bye()
            except:
                pass
        
        self.screen = turtle.Screen()
        self.screen.setup(600, 600)
        self.screen.bgcolor("white")
        self.screen.title("FMSLogo Code Evaluator")
        
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)  # Fastest drawing
        self.turtle.shape("triangle")
        self.reset_turtle_state()
    
    def reset_turtle_state(self):
        """Reset turtle to starting position and clear tracking"""
        self.turtle.clear()
        self.turtle.home()
        self.turtle.pendown()
        self.turtle.color("black")
        self.turtle.setheading(90)  # Face up like FMSLogo
        
        # Reset tracking
        self.positions = [(0, 0)]
        self.angles = [90]  # FMSLogo starts facing up
        self.pen_states = [True]
        self.colors = ["black"]
        self.commands_used = []
    
    def track_state(self, command):
        """Track turtle state after each command"""
        self.positions.append(self.turtle.position())
        self.angles.append(self.turtle.heading())
        self.pen_states.append(self.turtle.isdown())
        self.colors.append(self.turtle.pencolor())
        self.commands_used.append(command)
    
    def parse_and_execute(self, code):
        """Parse FMSLogo code and execute with Python turtle"""
        self.reset_turtle_state()
        
        # Clean and split code into commands
        lines = code.strip().split('\n')
        commands = []
        for line in lines:
            line = line.strip().upper()
            if line and not line.startswith('#') and not line.startswith('//'):
                # Split by spaces but keep command pairs together
                words = line.split()
                commands.extend(words)
        
        print(f"Executing commands: {commands}")
        
        i = 0
        while i < len(commands):
            cmd = commands[i]
            
            try:
                if cmd in ['FORWARD', 'FD']:
                    if i + 1 < len(commands):
                        distance = float(commands[i + 1])
                        self.turtle.forward(distance)
                        self.track_state(f"FD {distance}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['BACKWARD', 'BK', 'BACK']:
                    if i + 1 < len(commands):
                        distance = float(commands[i + 1])
                        self.turtle.backward(distance)
                        self.track_state(f"BK {distance}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['RIGHT', 'RT']:
                    if i + 1 < len(commands):
                        angle = float(commands[i + 1])
                        self.turtle.right(angle)
                        self.track_state(f"RT {angle}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['LEFT', 'LT']:
                    if i + 1 < len(commands):
                        angle = float(commands[i + 1])
                        self.turtle.left(angle)
                        self.track_state(f"LT {angle}")
                        i += 2
                    else:
                        print(f"Error: {cmd} needs a number")
                        i += 1
                        
                elif cmd in ['PENUP', 'PU']:
                    self.turtle.penup()
                    self.track_state("PU")
                    i += 1
                    
                elif cmd in ['PENDOWN', 'PD']:
                    self.turtle.pendown()
                    self.track_state("PD")
                    i += 1
                    
                elif cmd in ['HOME']:
                    self.turtle.home()
                    self.turtle.setheading(90)  # Face up like FMSLogo
                    self.track_state("HOME")
                    i += 1
                    
                elif cmd in ['CLEARSCREEN', 'CS']:
                    self.turtle.clear()
                    self.turtle.home()
                    self.turtle.setheading(90)
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
    
    def evaluate_day5(self):
        """Day 5: Making a Square"""
        results = {
            "day": 5,
            "title": "Making a Square",
            "tests": [],
            "passed": 0,
            "total": 0,
            "feedback": []
        }
        
        # Test 1: Has enough commands for a square
        if len(self.commands_used) >= 8:  # FD RT FD RT FD RT FD RT minimum
            results["tests"].append({"name": "Has enough commands for square", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Good! You used enough commands!")
        else:
            results["tests"].append({"name": "Has enough commands for square", "passed": False})
            results["feedback"].append("❌ A square needs 8 commands: FD RT FD RT FD RT FD RT")
        results["total"] += 1
        
        # Test 2: Returns close to starting position
        start_pos = self.positions[0]
        end_pos = self.positions[-1]
        distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
        
        if distance < 30:
            results["tests"].append({"name": "Shape closes properly", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Excellent! Your shape closes!")
        else:
            results["tests"].append({"name": "Shape closes properly", "passed": False})
            results["feedback"].append("❌ Make sure all sides are equal length")
        results["total"] += 1
        
        # Test 3: Uses 90-degree turns
        right_angle_count = 0
        for cmd in self.commands_used:
            if 'RT 90' in cmd or 'LT 90' in cmd:
                right_angle_count += 1
        
        if right_angle_count >= 3:
            results["tests"].append({"name": "Uses 90-degree angles", "passed": True})
            results["passed"] += 1
            results["feedback"].append("✅ Perfect! You used 90-degree angles!")
        else:
            results["tests"].append({"name": "Uses 90-degree angles", "passed": False})
            results["feedback"].append("❌ Squares need RT 90 or LT 90 for corners")
        results["total"] += 1
        
        return results
    
    def close(self):
        """Close turtle graphics"""
        if self.screen:
            try:
                self.screen.bye()
            except:
                pass

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
            # Reset evaluator for new evaluation
            self.evaluator.reset_graphics()
            results = self.evaluator.evaluate_day(code, day)
            
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

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        # Console mode
        print("FMSLogo Code Evaluator - Console Mode")
        print("=" * 40)
        
        evaluator = FMSLogoEvaluator()
        
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
            
            # Display results (same logic as GUI)
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
