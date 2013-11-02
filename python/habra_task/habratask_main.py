"""
Recently I have seen this article http://habrahabr.ru/post/200190/
so I have decided to find the solution of this task by myself.

Short description of this task for a case if the link above will be broken:
 1. we have a two-dimensional positive integer numbers array
 2. if we will display this data in the manner of a walls (see image below)
 then we need to calculate the volume which could be filled by an imaginary water ?
                ___                                      ___
               |7 7|_                                   |7 7|_
    _          |    6|                       _          |    6|
   |5|         |     |   fill with water    |5|x x x x x|     |  volume is
   | |  _      |     |  ---------------->   | |x x x x x|     | ----------->  19
  _| | |3|  _  |     |                     _| |x|3|x x x|     |
 |2  |_| |_|2|_|     |                    |2  |x| |x|2|x|     |
 |____1___1___1______|                    |____1___1___1______|
  0 1 2 3 4 5 6 7 8 9                      0 1 2 3 4 5 6 7 8 9

My solution is:
 1. We are moving step by step from left to right.
 2. If we are stepping down then we put the previous cell value with the current cell index into stack.
 3. If we are stepping up then:
 3.1. We are popping one value from the stack and flood all cells between stacked index and current step index up to
    the floodLevel = min(stackedValue, currentValue).
 3.2. Increase Result value in the next way:
        result += (currentStepIndex - stackedIndex) * (min(stackedValue, currentValue) - prevValue)
 3.3. calculate difference between currentValue and stackedValue. If the currentValue > stackedValue then pop next
    value from the stack and repeat steps (3.1 - 3.3). If the currentValue < stackedValue then put this stackedValue
    with its stackedIndex back to stack.

That's all, we will always have a filled holes from the left, and the highest wall which we were visited before will be
always stored on the bottom of this stack (of course if it wasn't already filled up to its edge, in that case the stack
would be empty).

"""
import random

def generateData():
    """  Generates source data for this exercise  """
    # data = [2, 5, 1, 3, 1, 2, 1, 7, 7, 6]
    data = [int(10 * random.random()) for i in xrange(10)]
    return data


def calculate(data):
    """  Main program algorithm with some debug instruments  """
    stack = []
    result = 0
    prevVal = 0
    filledCells = {}  # for debug purpose only

    for col in range(0, len(data)):
        val = data[col]
        if val < prevVal:
            stack.append((col, prevVal))
        elif val > prevVal:
            while len(stack) > 0 and val > prevVal:
                stackItem = stack.pop(-1) if val >= stack[-1][1] else stack[-1]
                floodLevel = min(val, stackItem[1])
                result += (col - stackItem[0]) * (floodLevel - prevVal)
                if __debug__:
                    for row, cell in [(row, cell) for row in range(prevVal, floodLevel) for cell in range(stackItem[0], col)]:
                        filledCells[row, cell] = True
                    display(data, filledCells, col, stack, result)
                prevVal = floodLevel
        prevVal = val
    display(data, filledCells, len(data) - 1, stack, result)


def display(data, filledCells, step, stack, result):
    """  Renders current state of program execution in a human readable format  """
    maxValue = max(data)
    colCount = len(data)
    valueWidth = len(str(maxValue))
    stackHeight = 5

    text = ''
    for row in range(maxValue + 1, -1, -1):
        emptyFill = '_' if row == 0 else ' '
        line = ''
        line += '|' if data[0] > row else emptyFill  # put left side of first column
        for col in range(0, colCount):
            # fill inner column space
            if filledCells.has_key((row, col)):  # fill cell with water
                line += ('{:' + emptyFill + '^' + str(valueWidth) + '}').format('x')
            elif data[col] == row + 1:
                line += ('{:' + emptyFill + '>' + str(valueWidth) + '}').format(data[col])
            elif data[col] == row:
                line += '_' * valueWidth
            else:
                line += emptyFill * valueWidth
            # add right column border
            if ((col < colCount - 1 and (data[col] <= row < data[col + 1] or data[col] > row >= data[col + 1]))
                    or (col == colCount - 1 and data[col] > row)):
                line += '|'
            elif col < colCount - 1 and data[col] == data[col + 1] == row:
                line += '_'
            else:
                line += emptyFill
        text += line + '\n'
    # fill bottom row with an indexes of array
    for col in range(0, colCount):
        text += (' {:>' + str(valueWidth) + '}').format(col)
    text += ' \n'
    # add current step indicator
    for col in range(0, colCount):
        text += (' {:^' + str(valueWidth) + '}').format('^' if col == step else ' ')
    text += " \n"
    # render stack
    text += '\nstack:\n'
    colIndexWidth = len(str(len(data)))
    for row in range(max(len(stack), stackHeight), 0, -1):
        if row >= len(stack):
            text += '[' + (' ' * (colIndexWidth + valueWidth + 4)) + ']\n'
        else:
            text += ('[ {1:>' + str(colIndexWidth) + '}, {1:>' + str(valueWidth) + '} ]\n').format(stack[row][0], stack[row][1])
    text += '[' + ('_' * (colIndexWidth + valueWidth + 4)) + ']\n'

    # render sum
    text += '\nresult = {0}'.format(result)

    print text


if __name__ == '__main__':
    data = generateData()
    calculate(data)
