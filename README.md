# 项目文档（《数据库设计》课程）

## 选课系统数据库设计

![ER.png](./doc/requirement/ER.png)

## 从ER图到表结构

### 实体集

+ 课程信息 course (<u>course_id</u>, title, credits, dept_name)
+ 开课信息 section (<u>course_id</u>, <u>section_id</u>, time, classroom_no, lesson, limit, day)

+ 学生信息 student(<u>student_id</u>,student_name, student_major, student_dept_name, student_total_credit)
+ 账户信息 account (<u>ID</u>, password, role)
+ 教室信息 classroom (classroom_no,capacity)
+ 考试信息 exam (<u>course_id</u>, <u>section_id</u>, exam_classroom_no, exam_day, type, start_time, end_time, open_note_flag)
+ 教师信息 instructor (<u>instructor_id</u>, instructor_name, instructor_class, dept_name)

### 关系集

+ 教师 & 开课 ：教授 teaches (<u>instructor_id</u>, <u>course_id</u>, <u>section_id</u>)
+ 学生 & 开课 ：选课 takes (course_id, section_id, student_id, grade, drop_flag)
+ 学生 & 开课：申请 application (<u>course_id</u>, <u>section_id</u>, <u>student_id</u>, status, application_reason, if_drop)


## 函数依赖与范式分析
+ 所有关系的属性的域都是原子的，不包含任何组合属性，所以上述关系模式都属于第一范式。

+ 没有任何非主属性部分依赖于键，所以也符合第二范式。

+ 没有任何非主属性传递依赖于键，所以符合第三范式。

+ 没有任何属性传递依赖于键，所以符合BC范式。

综上，我们设计的关系模式属于BC范式。


