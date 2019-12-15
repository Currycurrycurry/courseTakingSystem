##################################Constants#################################################
# AUTHORIZATION
ROOT_ROLE = 0
STUDENT_ROLE = 1
INSTRUCTOR_ROLE = 2

# APPLICATION STATUS
STATUS_PENDING = 0 # submitted successfully
STATUS_PASSED = 1
STATUS_UNPASSED = -1

# EXCEL FILE 
STUDENT_FILE = 1
COURSE_FILE = 2
SCORE_FILE = 3
SECTION_FILE = 4
INSTRUCTOR_FILE = 5

# SEARCH KEY
SEARCH_BY_SECTION = 1
SEARCH_BY_DEPT = 2
SEARCH_BY_INSTRUCTOR = 3
SEARCH_BY_NAME = 4


ITEM_NUM_FOR_ONE_PAGE = 15

GRADE_DICT = {'A':4.0,'A-':3.7,'B+':3.3,
            'B':3.0,'B-':2.7,'C+':2.3,'C':2.0,
            'C-':1.7,'D':1.3,'D-':1.0,'F':0,'P':0}