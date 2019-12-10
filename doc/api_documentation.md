# 选课系统后端 API 文档

说明：所有调用的成功状态由返回的 HTTP 状态码表示，`200` 代表调用成功，返回的内容为各 API 自己的返回值，`400` 代表调用失败，返回以下格式的 JSON：

```json
{
    "code": -1 or 1, // 由数字表示的广义错误码，-1为失败，1为成功
    "message": "" // 由字符串表示的特定错误码，不同的api有不同的错误码
}
```

以下为通用错误码：

| 错误码 | 含义 | 可能出现该错误码的 API |
| ---- | ---- | ---- |
| server error | 服务器内部错误 | 全部 |
| unauthorized | 当前用户没有权限执行该操作或session已过期 | 需要特定用户权限的 API |

对于 GET 请求，参数放在 URL 中；对于 POST 请求，参数 放在 body 中。

所有 API 的参数若非特殊说明均为必选参数。

## 登录

POST /selectCourse//login/

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string | 学号或者工号 |
| password | string | 密码 |


### 返回值

```json
{
    "user_name": 黄佳妮,
    "role": 1 // 1-student 2-instructor 0-root
}
```

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| wrong userid | 用户名不存在 |
| wrong password | 密码错误 |
| login successfully | 登陆成功 |

## 登出

 /selectCourse//login/

### 参数列表

不需要参数

### 返回值

无返回值

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| logout successfully | 登出成功 |

## 选课

POST /selectCourse/select/

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string | 学号 |
| course_id | string | 学校课程唯一代码 |
| section_id | string | 课程类别唯一代码 |

### 返回值

无

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| wrong course id | 课程代码错误 |
| wrong section id | 课程类别代码错误 |
| select successfully | 选课成功 |
| course with no vacancy | 课程无余量 |
| already selected | 已经选过该课程 |
| section time conflict | 课程时间冲突｜



## 退课

POST /selectCourse/drop/

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string | 学号 |
| course_id | string | 学校课程唯一代码 |
| section_id | string | 课程类别唯一代码 |

### 返回值

无

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| drop error: haven\'t taken yet | 未选修该课程 |
| drop successfully | 退课成功 |


## 查询已选课列表

POST /selectCourse/checkCourseTable


### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string | 用户 ID（留空则默认获取当前已登录用户的信息） |

### 返回值

```json
{
    "total_num" : 1,
    "sections" : {
        'title': '大气环境科学'
        'course_id': 'ATMO00000003'
        'section_id':1,
        'dept_name':“航空航天系”,
        'credits':2,
        'classroom_no':Z2202,
        'day':2, //周二
        'time':4-5, //第4到第5节
        'lesson':2, //课时 
    }   
}
```

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| show course table | 显示课程信息 |

## 查询所有课程信息(学生和root权限)

POST /selectCourse/checkAllCourses

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string | 用户 ID（留空则默认获取当前已登录用户的信息） |
| current_page_num | int | 当前页数 |


### 返回值

```json
{
    "total_num" : 1,
    "":
    "sections" : {
        'title': '大气环境科学'
        'course_id': 'ATMO00000003'
        'section_id':1,
        'dept_name':“航空航天系”,
        'credits':2,
        'classroom_no':Z2202,
        'day':2, //周二
        'time':4-5, //第4到第5节
        'lesson':2, //课时 
    }   
}
```

### 错误码

无

## 显示学生/教师基本信息

POST /selectCourse/checkPersonalInfo

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string | 用户 ID |


### 返回值

#### 对于学生

```json
{   
    "student_id": "17302010063",
    "student_name": "黄佳妮",
    "student_major": "软件工程",
    "student_dept_name":"软件学院",
    "student_total_creidt":95,
    "student_gpa":4.0,
    "student_grade":[
        {
            "course_id": "MATH1000001",
            "section_id": 1,
            "grade": A,
        }

    ]

}
```

#### 对于教师

```json
{   
    "instructor_id": "SOFT00000001",
    "instructor_name": "王小明",
    "instructor_class": "副教授",
    "dept_name":"软件学院",

}
```



### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| show personal info | 显示用户信息 |

## 搜索课程

POST /selectCourse/search

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string | 用户 ID |
| search_type | int | 搜索类型 1/2/3/4分别表示 |
| course_id | string | 根据course_id和section_id进行搜索|
| section_id | int | 根据course_id和section_id进行搜索 |
| title | string | 根据课程名称进行搜索|
| instructor_name | string | 根据教师名字进行搜索 |
| dept_name | string | 根据开课院系进行搜索|


### 返回值

```json
{
    "total_num" : 1,
    "sections" : {
        'title': '大气环境科学'
        'course_id': 'ATMO00000003'
        'section_id':1,
        'dept_name':“航空航天系”,
        'credits':2,
        'classroom_no':Z2202,
        'day':2, //周二
        'time':4-5, //第4到第5节
        'lesson':2, //课时 
    }   
}
```

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| search succeessfully| 搜索成功 |
| no search result| 无搜索结果 |

## 提交选课申请

POST /selectCourse/submitApplication

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string |  |
| course_id | string |  |
| section_id | int |  |
| application_reason | string | 申请理由 |

### 返回值

无

### 错误码

| 错误码 | 含义 |
| ---- | ---- |

| can't apply course which is already applied| 不能申请已申请课程 |
| can't apply selected course| 不能申请已选课程 |
| can't apply dropped course| 不能申请已退的申请通过课程 |
| apply successfully| 提交成功 |
| can't apply course with vacancy| 不能申请有余量课程 |
| exceed the classroom capacity| 不能申请人数已超过教室容量的课程 |


## 处理选课申请

POST /selectCourse/handleApplication

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string |  |
| course_id | string |  |
| section_id | int |  |
| status | int | 处理状态 |

### 返回值

无

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| handle successfully| 处理成功 |



## 查看选课申请

*学生和老师都可查看其对应的选课申请*

POST /selectCourse/handleApplication

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string |  |

### 返回值

```json
{
    "total_num" : 1,
    "applications" : {
        'course_id': 'ATMO00000003'
        'section_id': 1,
        'student_id':"17302010063",
        'status':1, // 0表示提交成功 1表示通过 -1表示不通过
        'application_reason':"I love this course",
        'if_drop':1, //1 表示退过 0 表示没退过
    }   
}
```

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| check application info| 显示选课申请信息 |

## 查看所教授课程（教师权限）

POST /selectCourse/checkTaughtCourses/

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string |  |

### 返回值

```json
{
    "total_num" : 1,
    "sections" : [
        {
        'title': '大气环境科学'
        'course_id': 'ATMO00000003'
        'section_id':1,
        'dept_name':“航空航天系”,
        'credits':2,
        'classroom_no':Z2202,
        'day':2, //周二
        'time':4-5, //第4到第5节
        'lesson':2, //课时 
        },   
    ]
}
```

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| show course table| 显示课程信息 |


## 查看该课程花名册（教师权限）

POST /selectCourse/checkCourseNameList/


### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string |  |

### 返回值

```json
{
    "total_num" : 1,
    "sections" : [
        {
        'title': '大气环境科学'
        'student_id': '17302010063'
        'student_name':"黄佳妮",
        'student_major':“航空航天系”,
        'student_dept_name':"航空航天学院",
        'grade':“A”,
    },
    ]  
}
```

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| show course table| 显示课程信息 |




## 查看课程考试列表（学生权限）

POST /selectCourse/checkExamTable/

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| user_id | string |  |

### 返回值

```json
{
    "total_num" : 1,
    "sections" : [
        {
        'title': '大气环境科学'
        'student_id': '17302010063'
        'student_name':"黄佳妮",
        'student_major':“航空航天系”,
        'student_dept_name':"航空航天学院",
        'grade':“A”,
    },
    ]  
}
```

### 错误码

| 错误码 | 含义 |
| ---- | ---- |
| show course table| 显示课程信息 |



## 自动导入模块

### 下载模版文件（老师）

GET /selectCourse/downloadFile

### 参数列表

| 名称 | 类型 | 描述 |
| ---- | ---- | ---- |
| file_type | int | STUDENT_FILE = 1
COURSE_FILE = 2
SCORE_FILE = 3
SECTION_FILE = 4
INSTRUCTOR_FILE = 5 |


### 导入学生课程成绩（教师权限）

### 导入课程信息（root权限）


### 导入学生信息（root权限）

### 导入教师信息（root权限）

