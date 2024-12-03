#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <sstream>
#include <regex>

//  cl.exe /Zi /EHsc /nologo /FeC:\Git\AdventOfCode\Year2024\Day01\output\main.exe C:\Git\AdventOfCode\Year2024\Day01\main.cpp
int GetMultiplicationResults(std::string filePath)
{
    std::string myline;
    std::ifstream myfile(filePath);
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 1;
    }

    int mulAddResult = 0;
    while (std::getline(myfile, myline))
    {
        std::istringstream lineStream(myline);
        std::regex mul_regex("mul\\((\\d+)\\,(\\d+)\\)");

        auto mul_begin = std::sregex_iterator(myline.begin(), myline.end(), mul_regex);
        auto mul_end = std::sregex_iterator();

        std::cout << "Found " << std::distance(mul_begin, mul_end) << " multiplications\n";

        for (std::sregex_iterator i = mul_begin; i != mul_end; ++i)
        {
            std::smatch match = *i;
            std::string match_str = match.str();
            int leftVal = std::stoi((*i)[1].str());
            int rightVal = std::stoi((*i)[2].str());
            int mulResult = leftVal * rightVal;

            std::cout << "mulResult: " << mulResult << "\n";
            mulAddResult += mulResult;
        }
    }

    std::cout << "FINISHED. Multiplication Result: " << mulAddResult << "\n";
    return mulAddResult;
}

int main()
{
    if (GetMultiplicationResults("test_input") != 161)
    {
        std::cout << "ERROR: in test\n";
    }

    if (GetMultiplicationResults("input") != 192767529)
    {
        std::cout << "ERROR: in input\n";
    };
    return 0;
}