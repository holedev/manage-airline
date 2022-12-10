const subBtn = document.querySelector('#submit-btn')
const inps = document.querySelectorAll('form input')
const time_start = document.querySelector('input[type=date]')
const ticket_type = document.querySelector('select#ticket_type')
const ap_from = document.querySelector('input#ap_from')
const ap_to = document.querySelector('input#ap_to')

subBtn.onclick = (e) => {
    e.preventDefault()
    const inpErr = Array.from(inps).find(inp => !inp.value)

    if (inpErr) {
        inpErr.focus()
        return Swal.fire("Lỗi", "Vui lòng nhập đủ thông tin!", "error")
    }

    if (ap_from.value && ap_from.value == ap_to.value) {
        ap_to.focus()
        return Swal.fire("Lỗi", "Bạn đang phí tiền bay về 1 chỗ!", "error")
    }

    if (!validateDatetime(new Date(time_start.value))) {
        time_start.focus()
        return Swal.fire("Lỗi", "Ngày này đã qua không thể đặt vé!", "error")
    }

    const data = {
        airport_from: ap_from.value.split(" - ")[0],
        airport_to: ap_to.value.split(" - ")[0],
        time_start: time_start.value,
        ticket_type: ticket_type.value
    }

    fetch(`/api/flight_schedule/search`, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        window.location.href = '/flight_list'
    })
}