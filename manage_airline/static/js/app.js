function validateDatetime(datetime) {
    const now = new Date()
    const now_date = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const check = datetime.getTime() - now_date.getTime()
    if (check < 0)
        return false
    return true
}