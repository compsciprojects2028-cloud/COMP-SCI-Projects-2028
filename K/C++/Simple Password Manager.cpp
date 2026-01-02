#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <conio.h>

struct Entry {
    std::string site;
    std::string username;
    std::string password;
};

void showMenu();
std::string getPassword();
bool authenticate();
bool parseInt(const std::string& input, int& result);
void loadEntries(std::vector<Entry>& entries);
void saveEntries(const std::vector<Entry>& entries);
void addEntry(std::vector<Entry>& entries);
void viewEntries(const std::vector<Entry>& entries);
void deleteEntry(std::vector<Entry>& entries);

int main()
{
    std::vector<Entry> entries;

    if (!authenticate()) return 0;
    loadEntries(entries);

    std::string userInput;
    int menuChoice;


    do {
        showMenu();
        std::getline(std::cin, userInput);

        if (!parseInt(userInput, menuChoice)) {
            std::cout << "Invalid input\n";
            continue;
        }

        switch (menuChoice) {
        case 1:
            addEntry(entries);
            break;

        case 2:
            std::cout << "\nEntries: \n";
            viewEntries(entries);
            break;

        case 3:
            deleteEntry(entries);
            break;

        case 4:
            saveEntries(entries);
            std::cout << "Entries saved. Goodbye!\n";
            break;
        }

    } while (menuChoice != 4);
    
    return 0;
}

void showMenu() {
    std::cout << "\nPassword Manager\n";
    std::cout << "1. Add Entry\n";
    std::cout << "2. View Entries\n";
    std::cout << "3. Delete Entry\n";
    std::cout << "4. Save and Exit\n";
    std::cout << "Choice: ";
}

std::string getPassword() {
    std::string password;
    char ch;

    while (true) {
        ch = _getch(); //gets a char without printing it out to the console (Windows only!)

        if (ch == 13) { // Enter key
            std::cout << "\n";
            break;
        }
        else if (ch == 8) { // Backspace
            if (!password.empty()) {
                password.pop_back();
                std::cout << "\b \b"; // erase character from console
            }
        }
        else {
            password += ch;
            std::cout << '*';
        }
    }
    return password;
}

bool authenticate() {
    const std::string masterPassword = "secret123";
    std::cout << "Enter master password: ";
    std::string input = getPassword();

    if (input == masterPassword) {
        return true;
    }
    else {
        std::cout << "Incorrect password!\n";
        return false;
    }
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

void loadEntries(std::vector<Entry>& entries) {
    std::ifstream file("entries.txt");
    if (!file.is_open()) return; // No file yet, nothing to load

    std::string line;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string site, username, password;

        if (!std::getline(ss, site, '|')) continue;
        if (!std::getline(ss, username, '|')) continue;
        if (!std::getline(ss, password, '|')) continue;

        entries.push_back({ site, username, password });
    }

    file.close();
}

void saveEntries(const std::vector<Entry>& entries) {
    std::ofstream file("entries.txt");
    if (!file.is_open()) {
        std::cout << "Failed to save entries!\n";
        return;
    }

    for (const auto& e : entries) {
        file << e.site << "|" << e.username << "|" << e.password << "\n";
    }

    file.close();
}

void addEntry(std::vector<Entry>& entries) {
    Entry e;
    std::cout << "Site: ";
    std::getline(std::cin, e.site);
    std::cout << "Username: ";
    std::getline(std::cin, e.username);
    std::cout << "Password: ";
    e.password = getPassword();
    entries.push_back(e);
}

void viewEntries(const std::vector<Entry>& entries) {
    if (entries.empty()) {
        std::cout << "No entries found.\n";
        return;
    }

    for (size_t i = 0; i < entries.size(); ++i) {
        std::cout << i + 1 << ". " << entries[i].site << " | " << entries[i].username << '\n';
    }
}

void deleteEntry(std::vector<Entry>& entries) {
    if (entries.empty()) {
        std::cout << "No entries to delete.\n";
        return;
    }

    // Show Entries
    viewEntries(entries);

    std::cout << "Enter the number of the entry you want to delete: ";
    std::string input;
    std::getline(std::cin, input);

    int choice;
    if (!parseInt(input, choice)) {
        std::cout << "Invalid input\n";
        return;
    }

    if (choice < 1 || choice > static_cast<int>(entries.size())) {
        std::cout << "Choice out of range!\n";
        return;
    }

    entries.erase(entries.begin() + (choice - 1));
    std::cout << "Entry deleted.\n";
}
