function validateDatetime(datetime) {
    const now = new Date()
    const now_date = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const check = datetime.getTime() - now_date.getTime()
    if (check < 0)
        return false
    return true
}

function setLoading(status) {
    const loading = document.querySelector(".loading-wrap")
    status === 0 ? loading.style.display = "none" : loading.style.display = 'flex'
}

window.onload = () => {
    setLoading(0)
}