import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


def add_participant():
    new_window = tk.Toplevel(root)
    new_window.title("Додати учасника")

    name_label = tk.Label(new_window, text="Ім'я користувача:")
    name_label.grid(row=0, column=0)

    name_entry = tk.Entry(new_window, justify="center")
    name_entry.grid(row=0, column=1)

    score_label = tk.Label(new_window, text="Відсоток від оцінки:")
    score_label.grid(row=1, column=0)

    score_entry = tk.Entry(
        new_window,
        validate="key",
        validatecommand=(validate_score_input_cmd, "%P"),
        justify="center",
    )
    score_entry.grid(row=1, column=1)

    add_button = tk.Button(
        new_window,
        text="Додати",
        command=lambda: add_entry(name_entry.get(), score_entry.get(), new_window),
    )
    add_button.grid(row=2)


def add_entry(name, score, window):
    if name and score:

        tree.insert(
            "",
            tk.END,
            values=(name, score),
        )
        window.destroy()
    else:
        tkinter.messagebox.showwarning(
            "Попередження", "Не введено ім'я або кількість правильних відповідей!"
        )


def calculate_grades():
    total_questions = max_mark_entry.get()
    if not total_questions:
        tkinter.messagebox.showwarning(
            "Попередження", "Не введено максимальний бал за тест!"
        )
        return

    total_questions = int(total_questions)
    if len(tree.get_children()) == 0:
        tkinter.messagebox.showwarning("Попередження", "Не додано жодного користувача!")
        return

    all_grades_calculated = True
    for child in tree.get_children():
        values = tree.item(child)["values"]
        if len(values) < 3 or not values[2]:
            all_grades_calculated = False
            break

    if all_grades_calculated:
        tkinter.messagebox.showinfo("Попередження", "Всі оцінки вже виставлено!")
    else:
        for child in tree.get_children():
            values = tree.item(child)["values"]
            if len(values) < 3 or not values[2]:
                name, score = values[:2]
                grade = (int(score) / 100) * total_questions
                tree.item(child, values=(name, score, round(grade)))


def delete_participant():
    selected_items = tree.selection()
    if selected_items:
        for item in selected_items:
            tree.delete(item)

        # Оновлюємо індекси рядків
        children = tree.get_children()
        for i, child in enumerate(children, start=1):
            tree.item(child, values=(i,) + tree.item(child)["values"][1:])


def validate_numeric_input(input):
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False


def validate_score_input(input):
    if input.isdigit() and 0 <= int(input) <= 100:
        return True
    elif input == "":
        return True
    else:
        return False


root = tk.Tk()
root.title("Підрахунок оцінок за тест")
root.minsize(400, 300)
root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())

validate_numeric_input_cmd = root.register(validate_numeric_input)
validate_score_input_cmd = root.register(validate_score_input)

questions_label = tk.Label(root, text="Максимальний бал за тест:")
questions_label.grid(row=0, column=0)

max_mark_entry = tk.Entry(
    root,
    validate="key",
    validatecommand=(validate_numeric_input_cmd, "%P"),
    justify="center",
)
max_mark_entry.grid(row=0, column=1)

questions_btns_label = tk.Label(root, text="Опції")
questions_btns_label.grid(row=1, column=0)

add_participant_button = tk.Button(
    root, text="Додати учасника", command=add_participant
)
add_participant_button.grid(row=2, column=0)

delete_participant_button = tk.Button(
    root, text="Видалити учасника", command=delete_participant
)
delete_participant_button.grid(row=2, column=1)

calculate_button = tk.Button(root, text="Підрахувати бали", command=calculate_grades)
calculate_button.grid(row=2, column=2)

tree = ttk.Treeview(root, columns=("Name", "Score", "Grade"))
tree.heading("#0", text="")
tree.heading("#1", text="Ім'я")
tree.heading("#2", text="Відсоток")
tree.heading("#3", text="Оцінка")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("#1", anchor="center")
tree.column("#2", anchor="center")
tree.column("#3", anchor="center")

tree.grid(row=3, columnspan=3, pady=10, sticky="nsew")

root.mainloop()
