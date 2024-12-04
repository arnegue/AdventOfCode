#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <regex>
#include <sstream>
#include <vector>

int FindOccurrences(std::string &searchString, std::string regex)
{
    std::regex words_regex(regex);
    auto words_begin = std::sregex_iterator(searchString.begin(), searchString.end(), words_regex);
    auto words_end = std::sregex_iterator();
    return std::distance(words_begin, words_end);
}

int FindXMAS(std::string &searchString)
{
    // Forward
    int occurrences = FindOccurrences(searchString, "XMAS");
    // Backward
    occurrences += FindOccurrences(searchString, "SAMX");
    return occurrences;
}

// TODO direction! (NW to SW | NE to SE)
std::string getDiagonalString(std::vector<std::string> &horizontalLines, std::vector<std::string> &verticalLines, int startX, int endX, int startY, int endY, bool direction)
{
    std::string diagStr = "";
    int x, y;
    if (direction)
    {
        for (x = startX, y = startY; x < endX && y < endY; x++)
        {
            diagStr += horizontalLines[x][y];
            y++;
        }
    }
    else
    {
        y = endY - startY - 1;
        for (x = startX; x < endX && y >= 0; x++)
        {
            diagStr += horizontalLines[x][y];
            y--;
        }
    }
    return diagStr;
}

int FindXMASOccurrences(std::string filePath, bool part1)
{
    std::string myline;
    std::ifstream myfile(filePath);
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 1;
    }

    int xmasCount = 0;

    std::vector<std::string> horizontalLines;
    std::vector<std::string> verticalLines;

    int lineLength = 0;
    // Horizontally
    while (std::getline(myfile, myline))
    {
        if (lineLength == 0)
        {
            lineLength = myline.length();
        }
        horizontalLines.emplace_back(myline);
        xmasCount += FindXMAS(myline);
    }

    // Vertically
    for (int horiIdx = 0; horiIdx < lineLength; horiIdx++)
    {
        std::string vertString = "";
        for (std::string line : horizontalLines)
        {
            vertString += line[horiIdx];
        }
        verticalLines.emplace_back(vertString);
        xmasCount += FindXMAS(vertString);
    }

    // 1st line Diagonally (left -> right)
    for (int verIdx = 0; verIdx < verticalLines[0].size(); verIdx++)
    {
        std::string diagString = getDiagonalString(horizontalLines, verticalLines, 0, horizontalLines[0].size(), verIdx, verticalLines[0].size(), true);
        xmasCount += FindXMAS(diagString);
    }
    // At this point the first horizontal line's diagonal lines were parsed

    // Other diagonal (left -> right)
    for (int verIdx = 1; verIdx < verticalLines[0].size(); verIdx++)
    {
        std::string diagString = getDiagonalString(horizontalLines, verticalLines, verIdx, horizontalLines[0].size(), 0, verticalLines[0].size(), true);
        int currentCount = FindXMAS(diagString);
        if (currentCount)
        {
            std::cout << "Found XMAS in " << diagString << std::endl;
        }
        xmasCount += currentCount;
    }

    // 1st line Diagonally (right -> left)
    for (int verIdx = 0; verIdx < verticalLines[0].size(); verIdx++)
    {
        std::string diagString = getDiagonalString(horizontalLines, verticalLines, 0, horizontalLines[0].size(), verIdx, verticalLines[0].size(), false);
        xmasCount += FindXMAS(diagString);
    }
    // At this point the first horizontal line's diagonal lines were parsed

    // Other diagonal (right -> left)
    for (int verIdx = 1; verIdx < verticalLines[0].size(); verIdx++)
    {
        int horiIdx = 0;

        // TODO some diagonal lines getting scanned multiple times
        std::string diagString = getDiagonalString(horizontalLines, verticalLines, verIdx, horizontalLines[0].size(), horiIdx, verticalLines[0].size(), false);
        xmasCount += FindXMAS(diagString);
    }

    std::cout << "FINISHED. FindXMASOccurrences: " << xmasCount << "\n";
    return xmasCount;
}

int main()
{
    if (FindXMASOccurrences("input/test_input", true) != 18)
    {
        std::cout << "ERROR: in test\n";
    }

    if (FindXMASOccurrences("input/input", true) != 2583)
    {
        std::cout << "ERROR: in input\n";
    };

    if (FindXMASOccurrences("input/test_input", false) != 4)
    {
        std::cout << "ERROR: in test\n";
    }

    // if (FindXMASOccurrences("input/input", false) != 4)
    // {
    //     std::cout << "ERROR: in input\n";
    // }
    return 0;
}