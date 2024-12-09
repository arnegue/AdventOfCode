#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <set>
#include <utility>
#include <sstream>
#include <vector>
#include <tuple>

using Equation = std::tuple<uint64_t, std::vector<uint64_t>>;

Equation GetEquation(std::string lineToParse)
{
    const std::regex pagesRegex("\\d+");

    auto rulBegin = std::sregex_iterator(lineToParse.begin(), lineToParse.end(), pagesRegex);
    auto rulEnd = std::sregex_iterator();
    std::sregex_iterator i = rulBegin;
    std::vector<uint64_t> numbers;

    uint64_t result = std::stoull((*i)[0].str());
    i++;
    for (i; i != rulEnd; ++i)
    {
        std::smatch match = *i;
        numbers.emplace_back(std::stoi((*i)[0].str()));
    }
    return {result, numbers};
}

uint64_t EquationIsPossible(Equation &eq)
{
    uint64_t result = 0;
    const uint64_t target = std::get<0>(eq);
    std::vector<uint64_t> results;
    std::vector<uint64_t> numbers = std::get<1>(eq);
    for (auto n : numbers)
    {
        if (results.size() == 0)
        {
            results.emplace_back(n);
            continue;
        }
        std::vector<uint64_t> resultsToAdd;
        for (auto res : results)
        {
            auto add = res + n;
            auto mul = res * n;
            if (add <= target)
            {
                resultsToAdd.emplace_back(add);
            }
            if (mul <= target)
            {
                resultsToAdd.emplace_back(mul);
            }
        }
        results = resultsToAdd;
    }

    for (auto result : results)
    {
        if (result == target)
        {
            return true;
        }
    }

    return false;
}

uint64_t GetSumPossibleEquations(std::string filePath)
{
    std::string myline;
    std::ifstream myfile(filePath);
    uint64_t sumPossibilities = 0;
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 0;
    }

    // Horizontally
    while (std::getline(myfile, myline))
    {
        Equation eq = GetEquation(myline);
        if (EquationIsPossible(eq))
        {
            uint64_t result = std::get<0>(eq);
            std::cout << "Equation with result " << std::get<0>(eq) << " is possible" << std::endl;
            sumPossibilities += result;
        }
    }
    std::cout << "Sum possibilities " << sumPossibilities << std::endl;
    return sumPossibilities;
}

int main()
{
    if (GetSumPossibleEquations("input/test_input") != 3749)
    {
        std::cout << "Error in test_input" << std::endl;
    }

    if (GetSumPossibleEquations("input/input") != 4122618559853)
    {
        std::cout << "Error in input" << std::endl;
    }

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
