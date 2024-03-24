import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import os
from random import randint, randrange
import subprocess

def delete_git_log():
    subprocess.run(['git', 'checkout', '--orphan', 'temp_branch'])
    subprocess.run(['git', 'add', '-A'])
    subprocess.run(['git', 'commit', '-m', 'Initial commit'])
    subprocess.run(['git', 'branch', '-D', 'main'])  # Replace 'main' with your branch name
    subprocess.run(['git', 'checkout', '-b', 'main'])  # Replace 'main' with your branch name
    subprocess.run(['git', 'push', '-f', 'origin', 'main'])  # Replace 'main' with your branch name
    subprocess.run(['git', 'gc', '--prune=all'])

def write_log(entry):
    with open('forge_log.txt', 'a+') as f:
        f.writelines(entry + '\n')

def commit_github(date):
    commit_time = f"{date} {random_Time()}"
    commit_message = f"Update {date} at {commit_time}."
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '--date', commit_time, '-m', commit_message])
    write_log(commit_message)

def random_Time():
    random_seconds = randrange(24 * 60 * 60)  # Random number of seconds in a day
    return datetime.timedelta(seconds=random_seconds)

def push_to_remote():
    try:
        subprocess.run(['git', 'push', 'origin', 'HEAD'])
        messagebox.showinfo("Push to Remote", "Changes have been successfully pushed to the remote repository.")
    except Exception as e:
        messagebox.showerror("Push to Remote Error", f"An error occurred while pushing changes: {e}")

def run_script():

    if delete_log_var.get() == 'Yes':
        delete_git_log()

    print_commit_count = print_commit_var.get()
    min_commit_count = min_commit_var.get()
    max_commit_count = max_commit_var.get()
    start_month = start_month_var.get()
    start_day = start_day_var.get()
    start_year = start_year_var.get()
    end_month = end_month_var.get()
    end_day = end_day_var.get()
    end_year = end_year_var.get()

    if min_commit_count <= 0 or max_commit_count <= 0 or min_commit_count > max_commit_count:
        messagebox.showerror("Error", "Invalid commit count range")
        return

    try:
        start_date = datetime.datetime(start_year, start_month, start_day)
        end_date = datetime.datetime(end_year, end_month, end_day)
    except ValueError:
        messagebox.showerror("Error", "Invalid date format")
        return

    if start_date > end_date:
        messagebox.showerror("Error", "Start date cannot be greater than end date")
        return
    
    if print_commit_count not in ['Yes', 'No']:
        messagebox.showerror("Error", "Invalid print_commit_count value")
        return 

    commit_counts = {}
    current_date = start_date

    while current_date <= end_date:
        commit_count = randint(min_commit_count, max_commit_count)

        for _ in range(commit_count):
            commit_github(current_date)

        if print_commit_count == 'Yes':
            commit_counts[current_date.date()] = commit_count
        
        current_date += datetime.timedelta(days=1)

    if print_commit_count == 'Yes':
        commit_count_str = "\n".join([f"{date}: {count} commits" for date, count in commit_counts.items()])
        messagebox.showinfo("Congrats, Forger!", f"Commits You Have Forged:\n{commit_count_str}")

    if auto_push_var.get() == 1:
        push_to_remote()
    else:
        messagebox.showinfo("Reminder", "The changes have updated the git commits in the log but have not been pushed to the remote repository.")
    
    write_log('__________________________________________________')


# Create main window
root = tk.Tk()
root.title("Prepare the Forge(ry)!")

# Create input fields
auto_push_var = tk.IntVar(root, value=0)

auto_push_label = ttk.Label(root, text="Automatically (attempt to) push changes to remote repository?")
auto_push_checkbutton = ttk.Checkbutton(root, variable=auto_push_var, onvalue=1, offvalue=0)

min_commit_var = tk.IntVar(root, value=5)
max_commit_var = tk.IntVar(root, value=15)
print_commit_var = tk.StringVar(root, value='Yes')
delete_log_var = tk.StringVar(root, value='No')

min_commit_label = ttk.Label(root, text="Minimum commit count:")
min_commit_entry = ttk.Entry(root, textvariable=min_commit_var)

max_commit_label = ttk.Label(root, text="Maximum commit count:")
max_commit_entry = ttk.Entry(root, textvariable=max_commit_var)

start_date_label = ttk.Label(root, text="Start Date:")
start_month_var = tk.IntVar(root, value=datetime.datetime.now().month)
start_month_dropdown = ttk.Combobox(root, textvariable=start_month_var, values=list(range(1, 13)), width=3)
start_day_var = tk.IntVar(root, value=datetime.datetime.now().day)
start_day_dropdown = ttk.Combobox(root, textvariable=start_day_var, values=list(range(1, 32)), width=3)
start_year_var = tk.IntVar(root, value=datetime.datetime.now().year)
start_year_dropdown = ttk.Combobox(root, textvariable=start_year_var, values=list(range(2000, 2101)), width=8)

end_date_label = ttk.Label(root, text="End Date:")
end_month_var = tk.IntVar(root, value=datetime.datetime.now().month)
end_month_dropdown = ttk.Combobox(root, textvariable=end_month_var, values=list(range(1, 13)), width=3)
end_day_var = tk.IntVar(root, value=datetime.datetime.now().day)
end_day_dropdown = ttk.Combobox(root, textvariable=end_day_var, values=list(range(1, 32)), width=3)
end_year_var = tk.IntVar(root, value=datetime.datetime.now().year)
end_year_dropdown = ttk.Combobox(root, textvariable=end_year_var, values=list(range(2000, 2101)), width=8)

print_commit_label = ttk.Label(root, text="Show commit count upon completion:")
print_commit_checkbutton = ttk.Checkbutton(root, variable=print_commit_var, onvalue=1, offvalue=0)

delete_log_label = ttk.Label(root, text="Delete existing git log (!!!):")
delete_log_combobox = ttk.Combobox(root, textvariable=delete_log_var, values=['Yes', 'No'])

info_label_1 = ttk.Label(root, text="Note: In order to auto-push, must be in an existing repo")
info_label_2 = ttk.Label(root, text="Note: The following will delete all commit history from the git log (files remain intact)")

run_button = ttk.Button(root, text="Run Script", command=run_script)

# Layout input fields
print_commit_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
print_commit_checkbutton.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

min_commit_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
min_commit_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

max_commit_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
max_commit_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

start_date_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
start_month_dropdown.grid(row=3, column=1, padx=(0,150), pady=5)
start_day_dropdown.grid(row=3, column=1, padx=(100,150), pady=5)
start_year_dropdown.grid(row=3, column=1, padx=(100,5), pady=5)

end_date_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
end_month_dropdown.grid(row=4, column=1, padx=(0,150), pady=5)
end_day_dropdown.grid(row=4, column=1, padx=(100,150), pady=5)
end_year_dropdown.grid(row=4, column=1, padx=(100,5), pady=5)

info_label_1.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

auto_push_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
auto_push_checkbutton.grid(row=6, column=1, padx=5, pady=5, sticky="w")

info_label_2.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

delete_log_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
delete_log_combobox.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

run_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Run the main event loop
root.mainloop()