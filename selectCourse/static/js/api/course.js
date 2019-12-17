function searchCourse(params) {
    return axios({
        url: api.search,
        type: 'get',
        params:params
    })
}

function getMyCourses(params) {
    return axios({
        url: api.studentCourseTb,
        type: 'get',
        params:params
    })
}
function selectCourse(data) {
    return axios({
        url: api.select,
        type: 'post',
        data:data
    })
}

function applyCourse(data) {
    return axios({
        url: api.applyCourse,
        type: 'post',
        data: data
    })
}

function getMyApplyCourse(params) {
    return axios({
        url: api.myApplyCourse,
        type: 'get',
        params:params
    })
}
function getMyCoursesGrade(params) {
    return axios({
        url: api.coursesGrade,
        type: 'get',
        params: params
    })
}