# load tasks from file
tasks = []

try:
    with open("tasks1.txt", "r") as file:
        for line in file:
            category, task, due_date, status = line.strip().split(",")
            tasks.append([category, task, due_date, status])
except FileNotFoundError:
    pass


while True:

    print("\n===== TO DO LIST MENU =====")
    print("1 Add Task")
    print("2 View Tasks")
    print("3 Mark Task Completed")
    print("4 Remove Task")
    print("5 Show Completed Tasks")
    print("6 Filter by Category")
    print("7 Exit")

    choice = input("Choose option: ")

    # add task
    if choice == "1":

        task = input("Enter task: ")
        due_date = input("Due date (YYYY-MM-DD): ")

        print("Choose category")
        c = input("1 personal\n2 work\n3 shopping\n4 wishlist\n")

        if c == "1":
            category = "personal"
        elif c == "2":
            category = "work"
        elif c == "3":
            category = "shopping"
        elif c == "4":
            category = "wishlist"
        else:
            category = "general"

        status = "Not done"

        tasks.append([category, task, due_date, status])
        print("Task added successfully")

    # view tasks
    elif choice == "2":

        if len(tasks) == 0:
            print("No tasks available")
        else:
            print("\nCurrent Tasks:")
            for i, t in enumerate(tasks):
                print(
                    f"{i+1}. Category: {t[0]} | Task: {t[1]} | Due: {t[2]} | Status: {t[3]}")

    # mark completed
    elif choice == "3":

        try:
            num = int(input("Enter task number: ")) - 1

            if 0 <= num < len(tasks):
                tasks[num][3] = "Done"
                print("Task marked completed")
            else:
                print("Invalid task number")
        except ValueError:
            print("Enter a valid number")

    # remove task
    elif choice == "4":

        try:
            num = int(input("Enter task number to remove: ")) - 1

            if 0 <= num < len(tasks):
                removed = tasks.pop(num)
                print("Removed task:", removed[1])
            else:
                print("Invalid task number")
        except ValueError:
            print("Enter a valid number")

    # show completed tasks
    elif choice == "5":

        print("\nCompleted Tasks:")
        found = False

        for t in tasks:
            if t[3] == "Done":
                print(f"{t[1]} | {t[0]} | Due: {t[2]}")
                found = True

        if not found:
            print("No completed tasks")

    # filter by category
    elif choice == "6":

        cat = input("Enter category (personal/work/shopping/wishlist): ")
        found = False

        for t in tasks:
            if t[0].lower() == cat.lower():
                print(f"{t[1]} | Due: {t[2]} | Status: {t[3]}")
                found = True

        if not found:
            print("No tasks in this category")

    # exit
    elif choice == "7":
        break

    else:
        print("Invalid option")


# save tasks to file
with open("tasks1.txt", "w") as file:
    for t in tasks:
        file.write(f"{t[0]},{t[1]},{t[2]},{t[3]}\n")

print("Tasks saved successfully")
