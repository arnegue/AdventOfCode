#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <set>
#include <utility>
#include <sstream>
#include <vector>
#include <tuple>

using Equation = std::tuple<int, std::vector<int>>;

std::vector<std::vector<int>> GetEquation(std::string lineToParse)
{
    const std::regex pagesRegex("\\d+");
    std::vector<std::vector<int>> equations;

    auto rulBegin = std::sregex_iterator(lineToParse.begin(), lineToParse.end(), pagesRegex);
    auto rulEnd = std::sregex_iterator();

    for (std::sregex_iterator i = rulBegin; i != rulEnd; ++i)
    {
        std::smatch match = *i;
        int leftVal = std::stoi((*i)[1].str());
        int rightVal = std::stoi((*i)[2].str());
    }
}

int GetSumPossibleEquations(std::string filePath)
{
}

int main()
{
    if (GetSumPossibleEquations("input/test_input") != 3749)
    {
        std::cout << "Error in test_input" << std::endl;
    }

    // if (GetSumPossibleEquations("input/input") != 4752)
    // {
    //     std::cout << "Error in input" << std::endl;
    // }

    // if (GetSumPossibleEquations("input/test_input") != 6)
    // {
    //     std::cout << "Error in test_input" << std::endl;
    // }

    // if (GetSumPossibleEquations("input/input") != 1719)
    // {
    //     std::cout << "Error in test_input" << std::endl;
    // }

    return 0;
}
