#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <utility>
#include <sstream>
#include <vector>
#include <tuple>

using Position = std::tuple<int, int>;
using Map = std::vector<std::vector<int>>;

const Position END_POSITION = {-1, -1};

enum class Direction
{
    NORTH,
    EAST,
    SOUTH,
    WEST
};

void MoveToNextPosition(Map &map, Position &currentPosition, Direction direction)
{
    int tempX = std::get<0>(currentPosition);
    int tempY = std::get<1>(currentPosition);

    switch (direction)
    {
    case Direction::NORTH:
        tempY--;
        break;
    case Direction::EAST:
        tempX++;
        break;
    case Direction::SOUTH:
        tempY++;
        break;
    case Direction::WEST:
        tempX--;
        break;
    default:
        std::cout << "ERROR weird direction" << std::endl;
        currentPosition = END_POSITION;
    }

    // Out of bounds, finished
    if (tempX < 0 || tempX >= map[0].size())
    {
        currentPosition = END_POSITION;
    }
    else if (tempY < 0 || tempY >= map.size())
    {
        currentPosition = END_POSITION;
    }
    else if (map[tempY][tempX] != '#')
    {
        currentPosition = std::make_tuple(tempX, tempY);
    }
    else
    {
        // obstacle hit #
        // no change, current position stays
    }
}

void MoveUntilObstacle(Map &map, Position &currentPosition, Direction direction, std::set<Position>& visitedPositions)
{

    Position previousPosition = currentPosition;
    while (1)
    {
        MoveToNextPosition(map, currentPosition, direction);

        if (currentPosition == END_POSITION)
        {
            return;
        }
        else if (previousPosition == currentPosition)
        {
            return;
        }
        visitedPositions.emplace(currentPosition);
        previousPosition = currentPosition;
    }
}

std::tuple<Position, Direction> GetStartPosition(const Map &map)
{
    for (int v = 0; v < map.size(); v++)
    {
        for (int h = 0; h < map[0].size(); h++)
        {
            int value = map[v][h];
            if (value == 'v')
            {
                return {{h, v}, Direction::SOUTH};
            }
            else if (value == '^')
            {
                return {{h, v}, Direction::NORTH};
            }
            else if (value == '<')
            {
                return {{h, v}, Direction::EAST};
            }
            else if (value == '>')
            {
                return {{h, v}, Direction::WEST};
            }
        }
    }
    std::cerr << "Error: Unable find start!" << std::endl;
    return {{0, 0}, Direction::SOUTH};
}

Map GetMap(std::string filePath)
{
    Map map;
    std::string myline;
    std::ifstream myfile(filePath);
    if (!myfile)
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return map;
    }

    // Horizontally
    while (std::getline(myfile, myline))
    {
        std::vector<int> horizontalLine;
        for (char character : myline)
        {
            horizontalLine.emplace_back(character);
        }
        map.emplace_back(horizontalLine);
    }
    return map;
}

int GetAmountVisitedPlaces(std::string filePath)
{
    std::set<Position> visitedPositions;
    std::vector<std::vector<int>> mapLines;

    Map map = GetMap(filePath);
    Position currentPosition;
    Direction direction;
    std::tuple<Position, Direction> pd = GetStartPosition(map);
    currentPosition = std::get<0>(pd);
    visitedPositions.emplace(currentPosition);
    direction = std::get<1>(pd);

    while (currentPosition != END_POSITION)
    {
        MoveUntilObstacle(map, currentPosition, direction, visitedPositions);

        // direction += 90
        switch (direction)
        {
        case Direction::NORTH:
            direction = Direction::EAST;
            break;
        case Direction::EAST:
            direction = Direction::SOUTH;
            break;
        case Direction::SOUTH:
            direction = Direction::WEST;
            break;
        case Direction::WEST:
            direction = Direction::NORTH;
            break;
        default:
            std::cout << "ERROR weird direction" << std::endl;
            return 0;
        }
    }
    std::cout << "Visited " << visitedPositions.size() << " in " << filePath << std::endl;
    return visitedPositions.size();
}

int main()
{
    if (GetAmountVisitedPlaces("input/test_input") != 41)
    {
        std::cout << "Error in test_input" << std::endl;
    }

    if (GetAmountVisitedPlaces("input/input") != 4752)
    {
        std::cout << "Error in input" << std::endl;
    }

    return 0;
}
