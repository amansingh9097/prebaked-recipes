from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Make sure chrome driver is in your path,
# full download totorial on official python selenium website.

# Start broswer with sudoku.com
driver = webdriver.Chrome()
driver.get("https://sudoku.com/")
assert "Sudoku" in driver.title

# Select expert difficulty
dificulty_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "difficulty-label"))
    )
dificulty_select.click()
# Expert mode is 4th item in the dropdown
t = dificulty_select.find_elements_by_tag_name("li")[3]
t.click()

# Continously solve forever
# Remove loop to only solve once
while True:
    time.sleep(2)  # Wait for expert mode to load
    gameTable = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "game-table"))
        )
    allCells = gameTable.find_elements_by_class_name("game-cell")

    # loop through all cells to get their initial value
    i = 0
    sudokuTable = [[]]
    for x, cell in enumerate(allCells):
        if x % 9 == 0 and x != 0:
            sudokuTable.append([])
            i += 1
        value = cell.find_element_by_class_name("cell-value")
        try:
            text = value.find_element_by_tag_name("svg")
        except:
            sudokuTable[i].append(0)
            continue
        # Could have used a dictionary but used if statements for prototyping
        # I get the width of the chracters and assign their value based on that
        # as there is no way to get the raw value from source html.
        w, h = (text.get_attribute("width"), text.get_attribute("height"))
        w = int(w)
        h = int(h)
        if w == 12:
            sudokuTable[i].append(1)
        elif w == 20:
            if h == 30:
                sudokuTable[i].append(7)
            else:
                sudokuTable[i].append(2)
        elif w == 21:
            if h == 31:
                sudokuTable[i].append(5)
            else:
                sudokuTable[i].append(3)
        elif w == 22:
            # Both the number 6 and 8 have the save width and height
            # Therefore I look at their svg path in child node.
            s = text.find_element_by_tag_name("path").get_attribute("d")[0:6]
            if s == "M10.96":
                sudokuTable[i].append(6)
            else:
                sudokuTable[i].append(8)
        elif w == 23:
            sudokuTable[i].append(9)
        else:
            sudokuTable[i].append(4)

    # The actual solver is made by Tech with Tim, as my main focus was learning selenium
    # Credit Link: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
    def solve(bo):
        find = find_empty(bo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(bo, i, (row, col)):
                bo[row][col] = i

                if solve(bo):
                    return True

                bo[row][col] = 0

        return False

    def valid(bo, num, pos):
        # Check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if bo[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i, j)  # row, col

        return None

    backup_table = list(map(list, sudokuTable))
    solve(sudokuTable)

    # I couldn't get selenium to type numbers as there is no clear textbox
    # Thankfully there was a numpad :)
    numpad = driver.find_elements_by_class_name("numpad-item")
    # Replaces all 0's with their solved value
    for yp, y in enumerate(backup_table):
        for xp, x in enumerate(y):
            if x == 0:
                allCells[yp*9 + xp].click()
                numpad[sudokuTable[yp][xp] - 1].click()
        # Selenium might generate an error if it can't click on the cell
        # This is especially true on lower resolution displays
        # Lower this value if that's the case, to trigger a scroll earlier
        if yp == 6:
            driver.execute_script("arguments[0].scrollIntoView();", gameTable)

    play_again = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "button-play"))
        )
    # Waits 2 seconds and resets the game
    # Remove if you only want to solve once
    time.sleep(2)
    driver.execute_script("arguments[0].click();", play_again)
