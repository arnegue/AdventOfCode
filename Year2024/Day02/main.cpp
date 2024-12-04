#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <sstream>
#include <vector>

bool LevelIsSafeP1(std::vector<int>& level)
{
    bool isSafe = true;

    bool firstRun = true;
    int previousNumber;
    bool creaseSet = false;
    bool isIncreasing;
    for (int number : level)
    {
        if (!firstRun)
        {
            if (!creaseSet)
            {
                isIncreasing = previousNumber < number;
                creaseSet = true;
            }

            // Swap of increase/decrease
            int diff = previousNumber - number;
            if ((isIncreasing && diff > 0) || (!isIncreasing && diff < 0))
            {
                isSafe = false;
                break;
            }

            // 1 <= diff >= 3
            diff = abs(diff);
            if (diff < 1 || diff > 3)
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

void copyVectorLeaveOut(std::vector<int>& input, std::vector<int>& output, int leaveOutIndex) {
    for (int i = 0; i < input.size(); i++) {
        if (leaveOutIndex != i) {
            output.push_back(input[i]);
        }
    }        
}

bool LevelIsSafeP2(std::vector<int>& level)
{
    bool isSafe = LevelIsSafeP1(level);
    if (!isSafe)
    {
        for (int i = 0; i < level.size(); i++)
        {
            std::vector<int> copyLevel;
            // Copy vector but leave out i
            copyVectorLeaveOut(level, copyLevel, i);
            isSafe = LevelIsSafeP1(copyLevel);
            if (isSafe) {
                break;
            }
        }
    }
    return isSafe;
}

//  cl.exe /Zi /EHsc /nologo /FeC:\Git\AdventOfCode\Year2024\Day01\output\main.exe C:\Git\AdventOfCode\Year2024\Day01\main.cpp
int FindSafeLevels(std::string filePath, bool part1)
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

        // Extract numbers from the line
        while (lineStream >> nextNumber)
        {
            level.emplace_back(nextNumber);
        }

        if (part1)
        {
            if (LevelIsSafeP1(level))
            {
                safeLevels += 1;
            }
        }
        else
        {
            if (LevelIsSafeP2(level))
            {
                safeLevels += 1;
            }
        }
    }

    std::cout << "FINISHED. FindSafeLevels: " << safeLevels << "\n";
    return safeLevels;
}

int main()
{
    if (FindSafeLevels("input/test_input", true) != 2)
    {
        std::cout << "ERROR: in test\n";
    }

    if (FindSafeLevels("input/input", true) != 321)
    {
        std::cout << "ERROR: in input\n";
    };

    if (FindSafeLevels("input/test_input", false) != 4)
    {
        std::cout << "ERROR: in test\n";
    }

    if (FindSafeLevels("input/input", false) != 4)
    {
        std::cout << "ERROR: in input\n";
    }
    return 0;
}