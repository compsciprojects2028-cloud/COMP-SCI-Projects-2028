#include <iostream>
#include <fstream>
#include <filesystem>

namespace fs = std::filesystem;

void displayMessage();
std::string extractArgument(const std::string& command, size_t startPos);

int main()
{
    fs::path currentPath = fs::current_path();
    std::string command;

    displayMessage();

    while (true) {
        std::cout << currentPath << "> ";
        std::getline(std::cin, command);

        if (command == "exit") {
            break;
        }
        else if (command == "pwd") {
            std::cout << currentPath << "\n";
        }
        else if (command == "help") {
            std::cout << "exit                     Exits the program.\n";
            std::cout << "pwd                      Prints current working diretory.\n";
            std::cout << "ls                       Lists all files and folders in the current directory.\n";
            std::cout << "cd                       Change to another directory e.g(cd newFolder).\n";
            std::cout << "cat                      Prints out the contents of a text file.\n";
            std::cout << "mkdir                    Creates a new directory.\n";
            std::cout << "touch                    Creates an empty file.\n";
            std::cout << "rm                       Deletes a file.\n";
        }
        else if (command == "ls") {
            try {
                for (const auto& entry : fs::directory_iterator(currentPath)) {
                    if (entry.is_directory())
                        std::cout << "[DIR] ";
                    else
                        std::cout << "[FILE] ";

                    std::cout << entry.path().filename() << "\n";
                }
            }
            catch (const fs::filesystem_error& e) {
                std::cout << "Error: " << e.what() << "\n";
            }
        }
        else if (command == "cd" || command.rfind("cd ", 0) == 0) {
            fs::path newPath = currentPath / extractArgument(command, 2);
            if (fs::exists(newPath) && fs::is_directory(newPath)) {
                currentPath = fs::canonical(newPath);
            }
            else {
                std::cout << "Directory not found.\n";
            }
        }
        else if (command == "cat" || command.rfind("cat ", 0) == 0) {
            std::string filename = extractArgument(command, 3);
            fs::path filePath = currentPath / filename;

            if (!fs::exists(filePath)) {
                std::cout << "File does not exist.\n";
            } 
            else if (!fs::is_regular_file(filePath)) {
                std::cout << "Not a regular file.\n";
            }
            else {
                std::ifstream file(filePath);
                if (!file.is_open()) {
                    std::cout << "Failed to open file.\n";
                }
                else {
                    std::string line;
                    while (std::getline(file, line)) {
                        std::cout << line << "\n";
                    }
                }
            }
        }
        else if (command == "mkdir" || command.rfind("mkdir ", 0) == 0) {
            std::string dirName = extractArgument(command, 5);

            if (dirName.empty()) {
                std::cout << "No directory name specified.\n";
                continue;
            }

            fs::path newDir = currentPath / dirName;

            if (fs::exists(newDir)) {
                std::cout << "Directory already exists.\n";
            }
            else {
                if (fs::create_directory(newDir)) {
                    std::cout << "Directory created.\n";
                }
                else {
                    std::cout << "Failed to create directory.\n";
                }
            }
        }
        else if (command == "touch" || command.rfind("touch ", 0) == 0) {
            std::string filename = extractArgument(command, 5);

            if (filename.empty()) {
                std::cout << "No file specified.\n";
                continue;
            }

            fs::path filePath = currentPath / filename;

            if (fs::exists(filePath)) {
                std::cout << "File already exists.\n";
                continue;
            }

            std::ofstream file(filePath);
            if (!file.is_open()) {
                std::cout << "Failed to create the file.\n";
            }
            else {
                std::cout << "File created.\n";
            }
        }
        else if (command == "rm" || command.rfind("rm ", 0) == 0) {
            std::string target = extractArgument(command, 3);

            if (target.empty()) {
                std::cout << "No file specified.\n";
                continue;
            }

            fs::path targetPath = currentPath / target;

            if (!fs::exists(targetPath)) {
                std::cout << "File does not exist.\n";
                continue;
            }

            if (!fs::is_regular_file(targetPath)) {
                std::cout << "Not a regular file.\n";
                continue;
            }

            std::cout << "Are you sure you want to delete \"" << target << "\"? [y/N]: ";

            std::string confirm;
            std::getline(std::cin, confirm);

            if (confirm != "y" && confirm != "Y") {
                std::cout << "Deletion cancelled.\n";
                continue;
            }

            if (fs::remove(targetPath)) {
                std::cout << "File deleted.\n";
            }
            else {
                std::cout << "Failed to delete file.\n";
            }
        }
        else {
            std::cout << "Unknown command.\n";
        }
    }   
    return 0;
}

void displayMessage() {
    std::cout << "******** C++ Mini Shell ********\n";
    std::cout << "Type \"help\" for list of commands\n\n";
}

std::string extractArgument(const std::string& command, size_t startPos) {
    std::string arg = command.substr(startPos);

    while (!arg.empty() && arg.front() == ' ')
        arg.erase(arg.begin());

    while (!arg.empty() && arg.back() == ' ')
        arg.pop_back();

    if (arg.size() >= 2 && arg.front() == '"' && arg.back() == '"') {
        arg = arg.substr(1, arg.size() - 2);
    }
    return arg;
}