#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <set>
#include <utility>
#include <sstream>
#include <vector>
#include <tuple>

using Map = std::vector<std::vector<int>>;
using Point = std::tuple<int, int>;

Map GetMap(std::string &filePath)
{
    std::string myline;
    std::ifstream myfile(filePath);
    Map map;
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return map;
    }

    while (std::getline(myfile, myline))
    {
        std::vector<int> hLine;
        for (auto ch : myline)
        {
            int i = int(ch) - 48;
            hLine.emplace_back(i);
        }
        map.emplace_back(hLine);
    }
    return map;
}

inline bool PointIsValid(Map &map, Point &point)
{
    int h = std::get<0>(point);
    int v = std::get<1>(point);
    return h < map[0].size() && h >= 0 && v < map.size() && v >= 0;
}

inline int GetMapValue(Map &map, Point &point)
{
    return map[std::get<1>(point)][std::get<0>(point)];
}

inline bool DiffIsOkay(Map &map, Point &first, Point &second)
{
    if (PointIsValid(map, first) && PointIsValid(map, second))
    {
        int firstVal = GetMapValue(map, first);
        int secondVal = GetMapValue(map, second);
        return (secondVal - firstVal) == 1;
    }
    else
    {
        return false;
    }
}

void GetReachableNines(Map &map, int &reachableNines, std::set<Point> &alreadyVisitedPoints, Point &startPoint, bool part1)
{
    int h = std::get<0>(startPoint);
    int v = std::get<1>(startPoint);
    Point testPoint;

    if (part1)
    {
        if (alreadyVisitedPoints.contains(startPoint))
        {
            return;
        }
        alreadyVisitedPoints.emplace(startPoint);
    }
    if (GetMapValue(map, startPoint) == 9) // First visit
    {
        // std::cout << "Found 9 at " << h << "/" << v << std::endl;
        reachableNines++;
        return;
    }

    // Try h+1
    testPoint = std::make_tuple(h + 1, v);
    if (DiffIsOkay(map, startPoint, testPoint))
    {
        GetReachableNines(map, reachableNines, alreadyVisitedPoints, testPoint, part1);
    }

    // Try h-1
    testPoint = std::make_tuple(h - 1, v);
    if (DiffIsOkay(map, startPoint, testPoint))
    {
        GetReachableNines(map, reachableNines, alreadyVisitedPoints, testPoint, part1);
    }
    // Try v+1
    testPoint = std::make_tuple(h, v + 1);
    if (DiffIsOkay(map, startPoint, testPoint))
    {
        GetReachableNines(map, reachableNines, alreadyVisitedPoints, testPoint, part1);
    }

    // Try v-1
    testPoint = std::make_tuple(h, v - 1);
    if (DiffIsOkay(map, startPoint, testPoint))
    {
        GetReachableNines(map, reachableNines, alreadyVisitedPoints, testPoint, part1);
    }
    return;
}

int GetTrailHeadScore(std::string filePath, bool part1)
{
    int score = 0;
    Map map = GetMap(filePath);
    for (int v = 0; v < map.size(); v++)
    {
        for (int h = 0; h < map[0].size(); h++)
        {
            Point startPoint = {h, v};
            if (GetMapValue(map, startPoint) == 0) // Start of a hiking trail found
            {
                int reachableNines = 0;
                std::set<Point> alreadyVisitedPoints;
                GetReachableNines(map, reachableNines, alreadyVisitedPoints, startPoint, part1);
                score += reachableNines;
            }
        }
    }
    std::cout << "Score: " << score << std::endl;
    return score;
}

int main()
{
    if (GetTrailHeadScore("input/test_input", true) != 36)
    {
        std::cout << "Error in test_input" << std::endl;
    }

    if (GetTrailHeadScore("input/input", true) != 822)
    {
        std::cout << "Error in input" << std::endl;
    }

    if (GetTrailHeadScore("input/test_input", false) != 81)
    {
        std::cout << "Error in test_input" << std::endl;
    }

    if (GetTrailHeadScore("input/input", false) != 1801)
    {
        std::cout << "Error in input" << std::endl;
    }

    return 0;
}
