#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <sstream>

//  cl.exe /Zi /EHsc /nologo /FeC:\Git\AdventOfCode\Year2024\Day01\output\main.exe C:\Git\AdventOfCode\Year2024\Day01\main.cpp
int GetDistance(std::string filePath)
{
    std::string myline;
    std::ifstream myfile(filePath);
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 1;
    }

    std::multiset<int> left;
    std::multiset<int> right;

    while (std::getline(myfile, myline))
    {
        std::istringstream lineStream(myline);
        int first, second;

        // Extract two integers from the line
        if (lineStream >> first >> second)
        {
            left.insert(first);
            right.insert(second);
        }
    }

    int totalDistance = 0;

    auto left_iterator = left.begin();
    auto right_iterator = right.begin();

    while (left_iterator != left.end() && right_iterator != right.end())
    {
        int leftMember = *left_iterator;
        int rightMember = *right_iterator;

        // std::cout << "Set1: " << leftMember<< ", Set2: " << rightMember << '\n';
        int temp_distance = 0;
        if (rightMember > leftMember)
        {
            temp_distance += (rightMember - leftMember);
        }
        else
        {
            temp_distance += (leftMember - rightMember);
        }

        std::cout << "Temp distance: " << temp_distance << "\n";
        totalDistance += temp_distance;

        ++left_iterator;
        ++right_iterator;
    }

    std::cout << "FINISHED. Total distance: " << totalDistance << "\n";
    return totalDistance;
}

int main()
{
    if (GetDistance("test_input.txt") != 11)
    {
        std::cout << "ERROR: in test\n";
    }

    if (GetDistance("input") != 2176849)
    {
        std::cout << "ERROR: in input\n";
    };
    return 0;
}