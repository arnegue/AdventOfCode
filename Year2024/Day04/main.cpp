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

        std::string diagString = getDiagonalString(horizontalLines, verticalLines, verIdx, horizontalLines[0].size(), horiIdx, verticalLines[0].size(), false);
        xmasCount += FindXMAS(diagString);
    }

    std::cout << "FINISHED. FindXMASOccurrences: " << xmasCount << "\n";
    return xmasCount;
}

int findCombi(std::string &line3x3, int horizontalOffset, int line_length, char first, char second, char third, char fourth)
{
    int SIZE_CROSS = 3;
    std::string test_regex;
    char buff[100];

    // Top row
    snprintf(buff, sizeof(buff), "^[A-Z]{%d}%c[A-Z]%c[A-Z]{%d}\n", horizontalOffset, first, second, (line_length - horizontalOffset - SIZE_CROSS));
    std::string regexL1 = buff;

    // A in middle
    snprintf(buff, sizeof(buff), "^[A-Z]{%d}A[A-Z]{%d}\n", horizontalOffset + 1, (line_length - horizontalOffset - SIZE_CROSS + 1));
    std::string regexL2 = buff;

    // Bottom row
    // Top row
    snprintf(buff, sizeof(buff), "^[A-Z]{%d}%c[A-Z]%c[A-Z]{%d}\n", horizontalOffset, third, fourth, (line_length - horizontalOffset - SIZE_CROSS));
    std::string regexL3 = buff;

    test_regex = regexL1 + regexL2 + regexL3;
    return FindOccurrences(line3x3, test_regex); // TODO last regex with \n is bad
}

int findMasXesIn3x3(std::string line3x3)
{
    const int SIZE_CROSS = 3;
    int occurrences = 0;

    int line_length = line3x3.find("\n");

    std::string test_regex;
    int horizontalOffset;
    for (horizontalOffset = 0; horizontalOffset < (line_length - SIZE_CROSS + 1); horizontalOffset++)
    {
        /*
        M M
         A
        S S
        */
        occurrences += findCombi(line3x3, horizontalOffset, line_length, 'M', 'M', 'S', 'S');

        /*
        M S
         A
        M S
        */
        occurrences += findCombi(line3x3, horizontalOffset, line_length, 'M', 'S', 'M', 'S');

        /*
        S M
         A
        S M
        */
        occurrences += findCombi(line3x3, horizontalOffset, line_length, 'S', 'M', 'S', 'M');

        /*
        S S
         A
        M M
        */
        occurrences += findCombi(line3x3, horizontalOffset, line_length, 'S', 'S', 'M', 'M');

        /*char buff[100];
        snprintf(buff, sizeof(buff), "^[A-Z]{%d}M[A-Z]S[A-Z]{%d}\n", horizontalOffset, (line_length - horizontalOffset - SIZE_CROSS));
        std::string regexL1 = buff;

        snprintf(buff, sizeof(buff), "^[A-Z]{%d}A[A-Z]{%d}\n", horizontalOffset + 1, (line_length - horizontalOffset - SIZE_CROSS + 1));
        std::string regexL2 = buff;

        test_regex = regexL1 + regexL2 + regexL1;
        int ocTest = FindOccurrences(line3x3, test_regex); // TODO last regex with \n is bad*/
        // occurrences += ocTest;
    }
    return occurrences;
}

int findMasXes(std::string filePath)
{
    int occurrences = 0;

    std::string myline;
    std::ifstream myfile(filePath);
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 1;
    }

    std::vector<std::string> lines;

    // Horizontally
    while (std::getline(myfile, myline))
    {
        lines.emplace_back(myline);
    }

    for (int lineIndex = 0; lineIndex < lines.size() - 2; lineIndex++)
    {
        std::string line3x3;
        for (int i = 0; i < 3; i++)
        {
            line3x3 += lines[lineIndex + i] + "\n";
        }
        occurrences += findMasXesIn3x3(line3x3);
    }

    std::cout << "FOUND " << occurrences << std::endl;
    return occurrences;
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

    if (findMasXes("input/test_input") != 9)
    {
        std::cout << "ERROR: in test: " << std::endl;
    }

    if (findMasXes("input/input") != 1978) // 1951 too low
    {
        std::cout << "ERROR: in input\n";
    }
    return 0;
}