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
const Position LOOP_DETECTED = {-2, -2};

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

    // Out of bounds X, finished
    if (tempX < 0 || tempX >= map[0].size())
    {
        currentPosition = END_POSITION;
    }
    // Out of bounds Y, finished
    else if (tempY < 0 || tempY >= map.size())
    {
        currentPosition = END_POSITION;
    }
    // Normal movement
    else if (map[tempY][tempX] != '#' && map[tempY][tempX] != '0')
    {
        currentPosition = std::make_tuple(tempX, tempY);
    }
    // Obstacle #0 hit
    else
    {
        // no change, current position stays
    }
}

void MoveUntilObstacle(Map &map, Position &currentPosition, Direction direction, std::set<Position> &visitedPositions, std::set<std::tuple<Position, Direction>> &loopSet)
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

        std::tuple<Position, Direction> currentLD = {currentPosition, direction};
        if (loopSet.find(currentLD) != loopSet.end())
        {
            // LoopDetected
            currentPosition = LOOP_DETECTED;
            return;
        }
        else
        {
            loopSet.emplace(currentLD);
        }

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
    return {{-1, -1}, Direction::SOUTH};
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

int GetAmountVisitedPlaces(std::string filePath, std::set<Position> &visitedPositions)
{
    Map map = GetMap(filePath);
    std::tuple<Position, Direction> pd = GetStartPosition(map);
    Position currentPosition = std::get<0>(pd);
    visitedPositions.emplace(currentPosition);
    Direction direction = std::get<1>(pd);

    std::set<std::tuple<Position, Direction>> loopSet;

    while (currentPosition != END_POSITION)
    {
        MoveUntilObstacle(map, currentPosition, direction, visitedPositions, loopSet);

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

Map GetManipulatedMap(std::string filePath, Position manipulatePosition)
{
    Map map = GetMap(filePath); // TODO read once
    map[std::get<1>(manipulatePosition)][std::get<0>(manipulatePosition)] = '0';
    return map;
}

int GetPossibleLoops(std::string filePath)
{
    std::set<Position> manipulationPosition;
    GetAmountVisitedPlaces(filePath, manipulationPosition);

    std::set<Position> unusedPositionSet;
    int detectedLoops = 0;
    for (std::set<Position>::iterator visitedIterator = manipulationPosition.begin();
         visitedIterator != manipulationPosition.end();
         visitedIterator++)
    {
        Map map = GetManipulatedMap(filePath, *visitedIterator);
        std::tuple<Position, Direction> pd = GetStartPosition(map);

        if (pd == std::tuple<Position, Direction>{{-1, -1}, Direction::SOUTH})
        {
            continue;
        }

        Position currentPosition = std::get<0>(pd);
        Direction direction = std::get<1>(pd);

        std::set<std::tuple<Position, Direction>> loopSet;

        // TOOD now manipulate map
        while (currentPosition != END_POSITION && currentPosition != LOOP_DETECTED)
        {
            MoveUntilObstacle(map, currentPosition, direction, unusedPositionSet, loopSet);

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
        if (currentPosition == LOOP_DETECTED)
        {
            detectedLoops++;
            // std::cout << "LOOP DETECTED" << std::endl;
        }
    }
    std::cout << "Possible Loops " << detectedLoops << " in " << filePath << std::endl;
    return detectedLoops;
}

int main()
{
    std::set<Position> visitedPositions = {};
    if (GetAmountVisitedPlaces("input/test_input", visitedPositions) != 41)
    {
        std::cout << "Error in test_input" << std::endl;
    }
    visitedPositions = {};
    if (GetAmountVisitedPlaces("input/input", visitedPositions) != 4752)
    {
        std::cout << "Error in input" << std::endl;
    }

    if (GetPossibleLoops("input/test_input") != 6)
    {
        std::cout << "Error in test_input" << std::endl;
    }

    if (GetPossibleLoops("input/input") != 1719)
    {
        std::cout << "Error in test_input" << std::endl;
    }

    return 0;
}
