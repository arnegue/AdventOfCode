#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <sstream>
#include <vector>

bool LevelIsSafe(std::vector<int> level)
{
    bool isSafe = true;

    bool firstRun = true;
    int previousNumber;
    for (int number : level)
    {
        if (!firstRun)
        {
            if ((previousNumber <= number) ||
                (number - previousNumber) > 3)
            {
                isSafe = false;
                break;
            }
        }
        previousNumber = number;
        firstRun = false;
    }
    return isSafe;
}

//  cl.exe /Zi /EHsc /nologo /FeC:\Git\AdventOfCode\Year2024\Day01\output\main.exe C:\Git\AdventOfCode\Year2024\Day01\main.cpp
int FindSafeLevels(std::string filePath)
{
    std::string myline;
    std::ifstream myfile(filePath);
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 1;
    }

    int safeLevels = 0;
    while (std::getline(myfile, myline))
    {
        std::vector<int> level;
        std::istringstream lineStream(myline);
        int nextNumber;

        // Extract numbrers from the line
        while (lineStream >> nextNumber)
        {
            level.emplace_back(nextNumber);
        }

        if (LevelIsSafe(level)) {
            safeLevels += 1;
        }

    }

    std::cout << "FINISHED. FindSafeLevels: " << safeLevels << "\n";
    return safeLevels;
}

int main()
{
    if (FindSafeLevels("input/test_input") != 2)
    {
        std::cout << "ERROR: in test\n";
    }

    if (FindSafeLevels("input") != 23384288)
    {
        std::cout << "ERROR: in input\n";
    };
    return 0;
}