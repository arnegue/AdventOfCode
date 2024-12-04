#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <sstream>


//  cl.exe /Zi /EHsc /nologo /FeC:\Git\AdventOfCode\Year2024\Day01\output\main.exe C:\Git\AdventOfCode\Year2024\Day01\main.cpp
int FindAppearances(std::string filePath)
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

    int totalAppearances = 0;
    for (int leftVal: left) {
        int appearanceRight = right.count(leftVal);
        totalAppearances += (leftVal * appearanceRight);
        std::cout << "leftVal: " << leftVal << " | appearanceRight: " << appearanceRight << " | " << (leftVal * appearanceRight) << "\n";
    }
   
    std::cout << "FINISHED. Total Appearances: " << totalAppearances << "\n";
    return totalAppearances;
}


int main()
{
    if (FindAppearances("test_input.txt") != 31) {
        std::cout << "ERROR: in test\n";
    }
    
    if (FindAppearances("input") != 23384288) {
        std::cout << "ERROR: in input\n";
    };
    return 0; 
}