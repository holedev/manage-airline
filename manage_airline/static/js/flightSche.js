const submitBtn = document.querySelector('.submit-btn')
const start = document.querySelector('#time-start')
const end = document.querySelector('#time-end')
const af = document.querySelector('#airport-from')
const at = document.querySelector('#airport-to')
const quantity1st = document.querySelector('#quantity-1st')
const quantity2nd = document.querySelector('#quantity-2nd')
const dataList = document.querySelector('datalist#airports')

const addAirportBw = (max) => {
    const abws = document.querySelectorAll(".airport-between")
    const btn = document.querySelector('.add-abw')
    const current = abws.length
    if (current < max) {
        abw = abws[abws.length - 1]
        const html = `
            <div class="row airport-between mt-3">
                <div class="col-lg-3">
                    <label for="airport-bw-${current}" class="form-label">Sân bay trung gian ${current + 1}:
                    </label>
                    <input name="airport_bw_${current}" type="text" class="form-control" id="airport-bw-${current}" list="airports">
                </div>
                <div class="col-lg-3">
                    <label for="airport-bw-stay-${current}" class="form-label">Thời gian dừng (giờ):</label>
                    <input name="airport_bw_stay_${current}" min="0" type="number" class="form-control" id="airport-bw-stay-${current}">
                </div>
                <div class="col-lg-6">
                    <label for="airport-bw-note-${current}" class="form-label">Ghi chú:</label>
                    <input name="airport_bw_note_${current}" type="text" class="form-control" id="airport-bw-note-${current}">
                </div>
            </div>
        `
        abw.insertAdjacentHTML("afterend", html)
        btn.innerHTML = `Thêm sân bay trung gian (Còn lại ${max - current - 1})`
    }
}

function checkMinTimeFly(dStart, dEnd) {
    const res = dEnd.getTime() - dStart.getTime()
    return res / (1000 * 60 * 60) >= parseFloat(dataList.dataset.mintimefly)
}

function checkTimeStay(min, max) {
    let error = true
    const abws = document.querySelectorAll(".airport-between")
    abws.forEach(ab => {
        const ap_stay = ab.querySelector("div:nth-child(2) > input").value
        if (parseFloat(ap_stay) > max || parseFloat(ap_stay) < min) {
            error = false
        }
    })
    return error
}

submitBtn.onclick = (e) => {
    e.preventDefault()
    const inpR = document.querySelectorAll("form input[required]")
    const abws = document.querySelectorAll(".airport-between")
    const min = parseFloat(dataList.dataset.mintimestay)
    const max = parseFloat(dataList.dataset.maxtimestay)

    const checkTime =   validateDatetime(new Date(start.value))
                        && new Date(end.value).getTime() - new Date(start.value).getTime()
    const checkAirport = af.value && af.value === at.value

    inpR.forEach(inp => {
        if (!inp.value) {
            inp.focus()
            return Swal.fire("Lỗi", "Vui lòng điền đầy đủ thông tin!", "error");
        }
    })

    if (checkAirport) {
        return Swal.fire("Lỗi", "Bạn đang phí tiền bay về 1 chỗ!", "error");
    }

    if (checkTime <= 0) {
        return Swal.fire("Lỗi", "Thời gian không hợp lệ", "error");
    }

    if (!checkMinTimeFly(new Date(start.value), new Date(end.value))) {
        return Swal.fire("Lỗi", `Thời gian tối thiểu của chuyến bay là ${(dataList.dataset.mintimefly)} giờ!`, "error");
    }

    const ab_list = []
    let error = false
    abws.forEach((ab, index) => {
        const ap_id = ab.querySelector("div:first-child > input").value
        const ap_stay = ab.querySelector("div:nth-child(2) > input").value
        const ap_note = ab.querySelector("div:nth-child(3) > input").value

        if (ap_id && (ap_id == af.value || ap_id == at.value)) {
            error = true
        }

        if (ap_id && ap_stay) {
            const obj = {
                id: index + 1,
                ap_id: ap_id.split(" - ")[0],
                ap_stay,
                ap_note
            }

            ab_list.push(obj)
        }
    })

    if (error) {
        return Swal.fire("Lỗi", "Sân bay trung gian không được trùng nơi đến hoặc nơi đi!", "error");
    }

    if (!checkTimeStay(min, max)) {
        return Swal.fire("Lỗi", `Thời gian dừng phải trong khoảng ${min} - ${max} giờ!`, "error");
    }

    const data = {
        "airport_from": af.value.split(" - ")[0],
        "airport_to": at.value.split(" - ")[0],
        "time_start": start.value,
        "time_end": end.value,
        "quantity_1st": quantity1st.value,
        "quantity_2nd": quantity2nd.value,
        "ab_list": ab_list
    }

    fetch("/api/flight_schedule", {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        window.location.reload()
        return Swal.fire("Thành công", "Thêm lịch chuyến bay thành công!", "success");
    })
}