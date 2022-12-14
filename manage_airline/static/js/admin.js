const btnAccepts = document.querySelectorAll(".accept")
const btnDels = document.querySelectorAll(".delete")
const submitBtn = document.querySelector('.submit-btn')
const airportF = document.querySelector('#airport-from')
const airportT = document.querySelector('#airport-to')
const timeS = document.querySelector('#time-start')
const timeE = document.querySelector('#time-end')
const quan1st = document.querySelector('#quantity-1st')
const quan2nd = document.querySelector('#quantity-2nd')
const btnAdd = document.querySelector('.add-abw')


btnAccepts.forEach(btn => {
    btn.onclick = (e) => {
        e.stopPropagation()
        return Swal.fire({
          title: 'Nhập giá tiền lịch chuyến bay',
          input: 'text',
          inputAttributes: {
            autocapitalize: 'off'
          },
          showCancelButton: true,
          confirmButtonText: 'Duyệt',
          showLoaderOnConfirm: true,
          preConfirm: (price) => {
            return fetch(`/api/flight_schedule/add/${btn.dataset.id}`, {
                method: 'post',
                body: JSON.stringify({
                    price
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error(response.statusText)
                }
                return response.json()
              })
              .catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          },
          allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
          if (result.isConfirmed) {
            Swal.fire({
              title: "Duyệt thành công!",
            })
            document.querySelector(`#tr-${result?.value.data}`).remove()
          }
        })
    }
})

btnDels.forEach(btn => {
    btn.onclick = (e) => {
        e.stopPropagation()
        return Swal.fire({
          title: 'Chắc chắn xoá? Hành động này không thể hoàn tác?',
          text: "You won't be able to revert this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Xoá',
          cancelButtonText: 'Huỷ',
          preConfirm: (price) => {
            return fetch(`/api/flight_schedule/delete/${btn.dataset.id}`, {
                method: 'post',
                headers: {
                    "Content-Type": "application/json"
                }
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error(response.statusText)
                }
                return response.json()
              })
              .catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          },
          allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
          if (result.isConfirmed) {
            Swal.fire(
              'Deleted!',
              'Your file has been deleted.',
              'success'
            )
            document.querySelector(`#tr-${result?.value.data}`).remove()
          }
        })
    }
})

const addAirportBw = (max) => {
    const abws = document.querySelectorAll(".airport-between")
    const current = abws.length
    if (current < max) {
        const html = `
            <div class="row airport-between mt-3">
                <div class="col-lg-3">
                    <label for="airport-bw-${current}" class="form-label">Sân bay trung gian ${current + 1}:
                    </label>
                    <input required name="airport_bw_${current}" type="text" class="form-control" id="airport-bw-${current}" list="airports">
                </div>
                <div class="col-lg-3">
                    <label for="airport-bw-stay-${current}" class="form-label">Thời gian dừng (giờ):</label>
                    <input required name="airport_bw_stay_${current}" min="0" type="number" class="form-control" id="airport-bw-stay-${current}">
                </div>
                <div class="col-lg-6">
                    <label for="airport-bw-note-${current}" class="form-label">Ghi chú:</label>
                    <input name="airport_bw_note_${current}" type="text" class="form-control" id="airport-bw-note-${current}">
                </div>
            </div>
        `
        if (current) {
            abws[current - 1].insertAdjacentHTML("afterend", html)
        } else {
            const row = document.querySelector('.row2.row')
            row.insertAdjacentHTML("afterend", html)
        }
        btnAdd.innerHTML = `Thêm STG (Còn lại ${max - current - 1})`
        document.querySelector('.del-abw').innerHTML = `Xoá STG (${current + 1})`
    }
}

const delAirportBw = () => {
    const abws = document.querySelectorAll(".airport-between")
    const btn = document.querySelector('.del-abw')
    const current = abws.length
    if (current) {
        abws[current - 1].remove()
        btn.innerHTML = `Xoá STG (${current - 1})`
        btnAdd.innerHTML = `Thêm STG (Còn lại ${parseInt(btnAdd.dataset.max) - current + 1})`
    }
}

const openModal = (fId, aF, aT, tS, tE, q1st, q2nd, bwA) => {
    document.querySelector('h5.modal-title').dataset.id = fId
    const rowABs = document.querySelectorAll('.row.airport-between')
    Array.from(rowABs).forEach(r => r.remove())

    airportF.value = `${aF.id} - ${aF.name}`
    airportT.value = `${aT.id} - ${aT.name}`
    timeS.value = tS
    timeE.value = tE
    quan1st.value = q1st
    quan2nd.value = q2nd

    const current = bwA.data.length
    document.querySelector('.del-abw').innerHTML = `Xoá STG (${current})`
    btnAdd.innerHTML = `Thêm STG (Còn lại ${parseInt(btnAdd.dataset.max) - current})`
    bwA.data.forEach((b, index) => {
        const ab = `${b.airport.id} - ${b.airport.name}`
        const html = `
            <div class="row airport-between">
                <div class="col-lg-3">
                    <label for="airport-bw-${index}" class="form-label">Sân bay trung gian:</label>
                    <input required value="${ab}" name="airport_bw_${index}" type="text" class="form-control" id="airport-bw-${index}" list="airports">
                </div>
                <div class="col-lg-3">
                    <label for="airport-bw-stay-${index}" class="form-label">Thời gian dừng (giờ):</label>
                    <input required value="${b.time_stay}" name="airport_bw_stay_${index}" min="0" type="number" class="form-control" id="airport-bw-stay-${index}">
                </div>
                <div class="col-lg-6">
                    <label for="airport-bw-note-${index}" class="form-label">Ghi chú:</label>
                    <input value="${b.note}" name="airport_bw_note_${index}" type="text" class="form-control" id="airport-bw-note-${index}">
                </div>
            </div>
        `
        const rowABs = document.querySelectorAll('.row.airport-between')
        if (rowABs.length) {
            rowABs[rowABs.length - 1].insertAdjacentHTML("afterend", html)
        } else {
            const row = document.querySelector('.row2.row')
            row.insertAdjacentHTML("afterend", html)
        }
    })

}

submitBtn.onclick = () => {
    const checkTime = validateDatetime(new Date(timeS.value)) && new Date(timeE.value).getTime() - new Date(timeS.value).getTime()
    const checkAirport = airportF.value && airportF.value === airportT.value
    const inpR = document.querySelectorAll("input[required]")
    const abws = document.querySelectorAll(".airport-between")

    inpR.forEach(inp => {
        if (!inp.value) {
            inp.focus()
            return Swal.fire("Lỗi", "Vui lòng điền đầy đủ thông tin!", "error");
        }
    })

    if (checkAirport) {
        return Swal.fire("Lỗi", "Bạn đang phí tiền bay về 1 chỗ!", "error");
    }

    if (!checkTime || checkTime <= 0) {
        timeS.focus()
        return Swal.fire("Lỗi", "Thời gian không hợp lệ", "error");
    }

    const ab_list = []
    let error = false
    abws.forEach((ab, index) => {
        const ap_id = ab.querySelector("div:first-child > input").value
        const ap_stay = ab.querySelector("div:nth-child(2) > input").value
        const ap_note = ab.querySelector("div:nth-child(3) > input").value

        if (ap_id && (ap_id == airportF.value || ap_id == airportT.value)) {
            error = true
        }

        const obj = {
            id: index + 1,
            ap_id: ap_id.split(" - ")[0],
            ap_stay,
            ap_note
        }

        ab_list.push(obj)
    })

    if (error) {
        return Swal.fire("Lỗi", "Sân bay trung gian không được trùng nơi đến hoặc nơi đi!", "error");
    }

    const data = {
        "id": document.querySelector('h5.modal-title').dataset.id,
        "airport_from": airportF.value.split(" - ")[0],
        "airport_to": airportT.value.split(" - ")[0],
        "time_start": timeS.value,
        "time_end": timeE.value,
        "quantity_1st": quan1st.value,
        "quantity_2nd": quan2nd.value,
        "ab_list": ab_list
    }

    fetch("/api/flight_schedule", {
        method: 'patch',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        window.location.reload()
        return Swal.fire("Thành công", "Cập nhật lịch chuyến bay thành công!", "success");
    })
}