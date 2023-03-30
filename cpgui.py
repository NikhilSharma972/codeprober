import tkinter as tk
from tkinter import ttk
from data_dog import  handle_user_question
from data_dog import get_test_cases
from data_dog import preprocess_ruby_project



def handle_ui_action(method_name, action, project_data, result_text):

    if action == "Explain":
        answer = handle_user_question(f"What does the {method_name} method do?", method_name, project_data)
    elif action == "Generate Test Cases":
        test_cases = get_test_cases(method_name, project_data)
        if test_cases:
            answer = "\n".join(test_cases)
        else:
            answer = "Method not found in the project."
    else:
        answer = "Invalid action selected."

  

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, answer)



def main():
    # Create the main window
    root = tk.Tk()
    root.title("Ruby Method Helper")

    # Create and add the UI elements
    method_name_label = ttk.Label(root, text="Enter the method name:")
    method_name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    
    method_name_entry = ttk.Entry(root)
    method_name_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

    action_label = ttk.Label(root, text="Choose an action:")
    action_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    
    action_combobox = ttk.Combobox(root, values=["Explain", "Generate Test Cases"])
    action_combobox.set("Explain")
    action_combobox.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

    result_label = ttk.Label(root, text="Result:")
    result_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

    result_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
    result_text.grid(column=0, row=3, columnspan=2, sticky=tk.W, padx=5, pady=5)


    project_path = './'
    project_data = preprocess_ruby_project(project_path)

    execute_button = ttk.Button(root, text="Execute", command=lambda: handle_ui_action(method_name_entry.get(), action_combobox.get(), project_data, result_text))
    execute_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
