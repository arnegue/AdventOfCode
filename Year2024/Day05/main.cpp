#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <regex>
#include <sstream>
#include <tuple>
#include <vector>

using Rule = std::tuple<int, int>;

int FindOccurrences(std::string &searchString, std::string regex)
{
    std::regex words_regex(regex);
    auto words_begin = std::sregex_iterator(searchString.begin(), searchString.end(), words_regex);
    auto words_end = std::sregex_iterator();
    return std::distance(words_begin, words_end);
}

void extractRules(std::vector<Rule> &rules, std::string input)
{
    std::regex ruleRegex("^(\\d+)\\|(\\d+)\n");

    auto rulBegin = std::sregex_iterator(input.begin(), input.end(), ruleRegex);
    auto rulEnd = std::sregex_iterator();

    std::cout << "Found " << std::distance(rulBegin, rulEnd) << " rules\n";

    for (std::sregex_iterator i = rulBegin; i != rulEnd; ++i)
    {
        std::smatch match = *i;
        int leftVal = std::stoi((*i)[1].str());
        int rightVal = std::stoi((*i)[2].str());
        Rule rule = {leftVal, rightVal};
        rules.emplace_back(rule);
    }
}

void extractPageUpdates(std::vector<std::vector<int>> &updates, std::string input)
{
    // cut off rules
    std::size_t dns = input.find("\n\n");
    std::string pages = input.substr(dns + 2);

    const std::regex pagesRegex("\\d+");

    // Iterate through each line
    std::size_t foundNewLine = pages.find("\n");
    while (foundNewLine != std::string::npos)
    {
        std::vector<int> update;
        std::string page = pages.substr(0, foundNewLine);

        auto rulBegin = std::sregex_iterator(page.begin(), page.end(), pagesRegex);
        auto rulEnd = std::sregex_iterator();
        for (std::sregex_iterator i = rulBegin; i != rulEnd; ++i)
        {
            int myInti = std::stoi((*i).str());
            update.emplace_back(myInti);
        }

        updates.emplace_back(update);
        pages = pages.substr(foundNewLine + 1);
        foundNewLine = pages.find("\n");
    }
}

inline int FindNumberInVector(const std::vector<int> &vector, const int search)
{
    int i = 0;
    for (int val : vector)
    {
        if (search == val)
        {
            return i;
        }
        i++;
    }
    return -1;
}

inline bool NumberInVector(const std::vector<int> &vector, const int search)
{
    return FindNumberInVector(vector, search) >= 0;
}

std::vector<Rule> GetRulesNeededForUpdate(const std::vector<Rule> &rules, const std::vector<int> &update)
{
    std::vector<Rule> retRules;
    for (Rule rule : rules)
    {
        // if both rule numbers are in update -> add rule
        int left = std::get<0>(rule);
        int right = std::get<1>(rule);
        if (NumberInVector(update, left) && NumberInVector(update, right))
        {
            retRules.emplace_back(rule);
        }
    }
    return retRules;
}

bool AreRulesApplied(const std::vector<Rule> &rules, const std::vector<int> &update)
{
    for (Rule rule : rules)
    {
        int left = std::get<0>(rule);
        int right = std::get<1>(rule);

        int leftIdx = FindNumberInVector(update, left);
        int rightIdx = FindNumberInVector(update, right);

        if (leftIdx < 0 || rightIdx < 0)
        {
            continue;  // Rule doesn't apply to this specific update
        }
        else if (leftIdx > rightIdx)
        {
            return false;
        }
    }
    return true;
}

int OrderCorrectlyGetMiddleSum(const std::vector<Rule> &rules, std::vector<int> &update)
{
    while (!AreRulesApplied(rules, update))
    {
        for (Rule rule : rules)
        {
            int left = std::get<0>(rule);
            int right = std::get<1>(rule);

            int leftIdx = FindNumberInVector(update, left);
            int rightIdx = FindNumberInVector(update, right);

            if (leftIdx < 0 || rightIdx < 0)
            {
                continue; // Rule doesn't apply to this specific update
            }
            else if (leftIdx > rightIdx)
            {
                // Swap values
                int rightVal = update[rightIdx];
                int leftVal = update[leftIdx];
                update[leftIdx] = rightVal;
                update[rightIdx] = leftVal;
            }
        }
    }
    return update[update.size() / 2];
}

int Update(std::string filepath)
{
    std::ifstream inFile;
    inFile.open(filepath); // open the input file
    std::stringstream strStream;
    strStream << inFile.rdbuf();               // read the file
    std::string fileContent = strStream.str(); // str holds the content of the file

    std::vector<Rule> rules = {};
    extractRules(rules, fileContent);

    std::vector<std::vector<int>> updates = {};
    extractPageUpdates(updates, fileContent);

    int updateMiddleSum = 0;
    int incorrectMiddleSum = 0;
    int updateI = 0;
    for (std::vector<int> update : updates)
    {
        std::cout << "Rules are ";
        std::vector<Rule> neededRules = GetRulesNeededForUpdate(rules, update);
        if (AreRulesApplied(neededRules, update))
        {
            int middleVal = update[update.size() / 2];
            updateMiddleSum += middleVal;
        }
        else
        {
            incorrectMiddleSum += OrderCorrectlyGetMiddleSum(rules, update);
            std::cout << "not ";
        }
        std::cout << "applied for update " << updateI << std::endl;
        updateI++;
    }

    std::cout << "Update sum: " << updateMiddleSum << " IncorrectSum: " << incorrectMiddleSum << std::endl;
    return updateMiddleSum;
}

int main()
{
    if (Update("input/test_input") != 143) // 123 incorrect
    {
        std::cout << "Error in test_input " << std::endl;
    }
    if (Update("input/input") != 5391) // 6142 incorrect
    {
        std::cout << "Error in test_input " << std::endl;
    }

    return 0;
}