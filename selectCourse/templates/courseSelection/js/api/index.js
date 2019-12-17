let api = {
    logout: 'selectCourse/logout/',
    login: 'selectCourse/login/',

    //about course
    // search: 'selectCourse/search/',
    // select: 'selectCourse/select/',
    // applyCourse: 'selectCourse/submitApplication/',
    // studentCourseTb: 'selectCourse/checkCourseTable/',
    // myApplyCourse: 'selectCourse/checkCourseTable/',
    // coursesGrade: 'selectCourse/checkPersonalInfo/',
    // userInfo: 'users/info'

};

function axios(option){
    let dtd = $.Deferred();
    $.ajax({
        ...option,
        success: function (res) {
            dtd.resolve(res);
        },
        error: function (error) {
            dtd.reject(error);
        }
    });
    return dtd.promise()
}
