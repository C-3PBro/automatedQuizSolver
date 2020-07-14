# Automated quiz solver (maze of oedipus)
Little python project to automatically solve the maze of oedipus as described on http://holdirdeinenvertrag.de using Selenium and BeautifulSoup.

### The riddle/maze (translated from the website by google translator)
Oedipus, the son of King Laios, has to pick up stones in a labyrinth. The labyrinth is square and measures 7 fields on the x-axis (horizontal) and the y-axis (vertical), whereby the field in the top left corner is labeled x0 / y0. Some fields are obstructed and therefore not accessible.

Each of the stones that Oedipus has to pick up carries a letter. There are 5 stones in total: L, A, I, O and S. In what order does Ödipus collect the stones if he starts at the position (x, y) below and proceeds according to the following algorithm:


BEGIN

     FUNCTION Go (x, y)
     BEGIN
          IF Invalid (x, y) OR Already visited (x, y) THEN
              RETURN
          ENDIF
          Collect (x, y)
          Mark As Visited (x, y)
          Go (x + 1, y) // to the right
          GoTo (x, y + 1) // down
          GoTo (x-1, y) // to the left
          GoTo (x, y-1) // go up
     END
END

### Prerequisites
* Selenium 
* BeautifulSoup

In the code I use the chromdriver.exe (https://sites.google.com/a/chromium.org/chromedriver/downloads/) as a webdriver for Selenium. For the code to run properly, specify the file location of the chromedriver.exe (line 25 in the code). Other packages used in the code are 're' and 'time'. 
