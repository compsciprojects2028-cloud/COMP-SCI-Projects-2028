#include <iostream>
#include <vector>
#include <string>

struct Task
{
    std::string description;
    bool completed;

    Task(const std::string& desc)
        : description(desc), completed(false) {}
};

void showMenu()
{
    std::cout << "Todo List Menu:\n\n";
    std::cout << "1. Add Task\n";
    std::cout << "2. View Tasks\n";
    std::cout << "3. Mark Task as Completed\n";
    std::cout << "4. Exit\n";
    std::cout << "\nEnter your choice: ";
}

bool parseInt(const std::string& input, int& result) {
    try {
        size_t pos;
        result = std::stoi(input, &pos);
        return pos == input.size();
    }
    catch (...) {
        return false;
    }
}

int main()
{
    std::vector<Task> tasks;
    std::string desc;
    std::string choice, taskChoice;
    int index, taskIndex, menuChoice;

    do {
        showMenu();
        std::getline(std::cin, choice);

        if (!parseInt(choice, menuChoice)) {
            std::cout << "Invalid input\n\n";
            continue;
        }

        switch (menuChoice) {
        case 1:
            std::cout << "Enter description: ";
            std::getline(std::cin, desc);
			tasks.emplace_back(desc);
            std::cout << "Task added!\n\n";
            break;
        case 2:
			std::cout << "Tasks: \n\n";
            for (size_t i = 0; i < tasks.size(); ++i) {
                char mark = tasks[i].completed ? 'O' : 'X';
                std::cout << i + 1 << ". " << tasks[i].description << " " << mark << '\n';
            }
            std::cout << "\n\n";
            break;
        case 3:
            std::cout << "Enter the the no of the task you want to complete: ";
            std::getline(std::cin, taskChoice);

            if (!parseInt(taskChoice, taskIndex)) {
                std::cout << "Invalid input\n\n";
                break;
            }
            if (taskIndex < 1 || taskIndex > static_cast<int>(tasks.size())) {
                std::cout << "Task number is out of range!\n\n";
                break;
            }

            index = taskIndex - 1;
            tasks[index].completed = true;
            std::cout << "Task completed!\n\n";
            break;
        case 4:
            std::cout << "Exiting the application. Goodbye!\n\n";
			break;
        default:
            std::cout << "Enter a number between 1 - 4" << '\n\n';
        }

    } while (menuChoice != 4);

    return 0;
}