function logout() {
    return axios({
        url: api.logout,
        type: 'post',
    })
}

function login(data) {
    return axios({
        url: api.login,
        type: 'post',
        data: data
    })
}