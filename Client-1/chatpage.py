import tkinter as tk

def message():
    message_text = message_input.get()
    message_textarea.insert(tk.END, message_text + '\n')

    message_input.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Sock-Talk")

# Increase window size
root.geometry("500x400")

# Create frame
frame = tk.Frame(root)
frame.grid(row=0, column=0, padx=20, pady=20)

# Header
header_label = tk.Label(frame, text="SOCKET CHATTING", font=("Helvetica", 20, "bold"))
header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Message input form
message_label = tk.Label(frame, text="Enter your message:", font=("Helvetica", 12))
message_label.grid(row=1, column=0, sticky="w")

message_input = tk.Entry(frame, width=40, font=("Helvetica", 12))
message_input.grid(row=1, column=1, sticky="w", padx=(10, 0))

# Buttons
button_frame = tk.Frame(frame)
button_frame.grid(row=2, column=0, columnspan=2, pady=20)

submit_button = tk.Button(button_frame, text="SUBMIT", bg="green", fg="white", width=15, font=("Helvetica", 12), command=message)
submit_button.pack(side=tk.LEFT, padx=(0, 10))

clear_button = tk.Button(button_frame, text="CLEAR", bg="red", fg="white", width=15, font=("Helvetica", 12), command=lambda: message_input.delete(0, tk.END))
clear_button.pack(side=tk.LEFT)

# Message textarea
message_textarea_label = tk.Label(frame, text="MESSAGES:", font=("Helvetica", 12))
message_textarea_label.grid(row=3, column=0, sticky="w", pady=(20, 10))

message_textarea = tk.Text(frame, width=60, height=12, font=("Helvetica", 12))
message_textarea.grid(row=4, column=0, columnspan=2, pady=(0, 10))

# Configure grid weights for responsiveness
root.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(4, weight=1)

# Function to handle form submission
def submit_message(event=None):
    message()
    return "break"

# Binding Enter key to submit message
root.bind("<Return>", submit_message)

# Run the main event loop
root.mainloop()
