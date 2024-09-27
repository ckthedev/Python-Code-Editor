import tkinter as tk
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
import sys
import io

# Create a class to redirect stdout and stderr
class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.config(state=tk.DISABLED)
    
    def write(self, string):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, string)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)
    
    def flush(self):
        pass

# Function to execute code and show output in the output area
def run_code():
    code = editor.get("1.0", tk.END)
    # Clear previous output
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.config(state=tk.DISABLED)

    # Redirect stdout and stderr
    sys.stdout = RedirectText(output_area)
    sys.stderr = RedirectText(output_area)

    try:
        exec(code)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

# Function to highlight code syntax using Pygments
def highlight_code(event=None):
    code = editor.get("1.0", tk.END)
    tokens = lex(code, PythonLexer())

    # Remove previous tags
    editor.tag_remove("keyword", "1.0", tk.END)
    editor.tag_remove("builtin", "1.0", tk.END)
    editor.tag_remove("string", "1.0", tk.END)
    editor.tag_remove("comment", "1.0", tk.END)

    editor.mark_set("range_start", "1.0")
    for token_type, value in tokens:
        if token_type in Token.Keyword:
            editor.tag_add("keyword", "range_start", f"range_start + {len(value)}c")
        elif token_type in Token.Name.Builtin:
            editor.tag_add("builtin", "range_start", f"range_start + {len(value)}c")
        elif token_type in Token.String:
            editor.tag_add("string", "range_start", f"range_start + {len(value)}c")
        elif token_type in Token.Comment:
            editor.tag_add("comment", "range_start", f"range_start + {len(value)}c")
        editor.mark_set("range_start", f"range_start + {len(value)}c")

# Setting up the main window
root = tk.Tk()
root.title("Python Code Editor")

# Creating the editor widget for code input
editor = tk.Text(root, wrap="word", font=("Courier New", 12), height=15, bg="#2E1A47", fg="#E1E1E1", insertbackground="#FFFFFF")
editor.pack(expand=1, fill='both')

# Configure syntax highlighting colors
editor.tag_configure("keyword", foreground="#FF79C6")  # Pink for keywords
editor.tag_configure("builtin", foreground="#8BE9FD")  # Light blue for built-in names
editor.tag_configure("string", foreground="#F1FA8C")   # Yellow for strings
editor.tag_configure("comment", foreground="#6272A4")  # Gray-blue for comments

# Creating the run button
run_button = tk.Button(root, text="Run Code", command=run_code)
run_button.pack()

# Creating the output area to display code execution results
output_area = tk.Text(root, wrap='word', font=("Fira Code", 12), height=10, bg="#1D1024", fg="#E1E1E1")
output_area.pack(expand=1, fill='both')

# Binding the syntax highlighting function to the editor
editor.bind("<KeyRelease>", highlight_code)

# Running the main event loop
root.mainloop()
