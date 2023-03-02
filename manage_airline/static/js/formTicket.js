const addBtn = document.querySelector('#add-customer')
const subBtn = document.querySelector('#sub-customer')
const submitBtn = document.querySelector('#submit-btn')
const price = document.querySelector('.price span')
const select = document.querySelector('form select')

function updatePrice(value) {
    const data = price.innerHTML.split(",")
    let total = ""
    data.forEach(d => {
        total += d
    })
    price.innerHTML = new Intl.NumberFormat().format(parseInt(total) + parseInt(value))
}

packagePrice = 0;

addBtn.onclick = () => {
    const listCustomer = document.querySelectorAll(".customer-info")
    const current = listCustomer.length

    customer = listCustomer[listCustomer.length - 1]
    if (current < 3) {
        const html = `
            <div class="customer-info d-flex gap-4 bg-white p-2 rounded-2 mt-3">
                <div class="flex-grow-1 mb-3">
                    <label for="fullname-${current + 1}" class="fw-bold form-label">Họ và tên: </label>
                    <input placeholder="Nguyễn Văn A" required type="text" minlength="4" name="fullname-${current + 1}" class="fullname-${current + 1} form-control" id="fullname-${current + 1}">
                </div>
                <div class="flex-grow-1 mb-3">
                    <label for="phone-${current + 1}" class="fw-bold form-label">Số điện thoại: </label>
                    <input placeholder="XXXXXXXXXX" required type="text" minlength="10" maxlength="10" name="phone-${current + 1}" class="phone-${current + 1} form-control" id="phone-${current + 1}">
                </div>
                <div class="flex-grow-1 mb-3">
                    <label for="id-${current + 1}" class="fw-bold form-label">CMND/CCCD: </label>
                    <input placeholder="XXXXXXXXXX" required type="text" minlength="10" maxlength="10" name="id-${current + 1}" class="id-${current + 1} form-control" id="id-${current + 1}">
                </div>
            </div>
        `
        customer.insertAdjacentHTML("afterend", html)
        updatePrice(parseInt(price.dataset.price))
    }
}

subBtn.onclick = () => {
    const listCustomer = document.querySelectorAll(".customer-info")
    const current = listCustomer.length
    if (current > 1) {
        listCustomer[current - 1].remove()
        updatePrice(parseInt(-price.dataset.price))
    }
}

select.onchange = (e) => {
    updatePrice(-packagePrice)
    if (e.target.value == 0) {
        packagePrice = 0
    }
    if (e.target.value == 8) {
        packagePrice = 320000
    }
    if (e.target.value == 12) {
        packagePrice = 400000
    }
    updatePrice(packagePrice)
}

submitBtn.onclick = (e) => {
    e.preventDefault()
    const inputList = document.querySelectorAll('form input[required]')
    const inpErr = Array.from(inputList).find(inp => !inp.value)
    if (inpErr) {
        inpErr.focus()
        return Swal.fire("Lỗi", "Vui lòng nhập đủ thông tin!", "error")
    }

    const inpValidateErr = Array.from(inputList).find(inp => inp.value.length < inp.getAttribute('minlength'))

    if (inpValidateErr) {
        inpValidateErr.focus()
        return Swal.fire("Lỗi", `Vui lòng nhập ít nhất ${inpValidateErr.getAttribute('minlength')} kí tự!`, "error")
    }

    function findInp(name) {
        return Array.from(inputList).find(inp => inp.classList.contains(name))
    }

    const customerInfo = []
    const quantityCustomner = (inputList.length - 2) / 3
    Array.from(inputList).forEach((inp, index) => {
        if (index == 2 || index == 5 || index == 8) {
            const obj = {
                id: index,
                name: inp.value,
                phone: inputList[index + 1].value,
                id_customer: inputList[index + 2].value
            }
            customerInfo.push(obj)
        }
    })

    const pathNames = window.location.pathname
    const fId = pathNames[pathNames.length - 1]
    console.log(pathNames)

    const data = {
        contact_info: {
            name: findInp('fullname').value,
            phone: findInp('phone').value
        },
        customers_info: [
            {
                quantity: customerInfo.length,
                data: customerInfo
            }
        ],
        package_price: packagePrice,
        f_id: fId,
        ticket_type: document.querySelector('span.ticket-type').innerHTML,
        total: price.innerHTML,
        user_role: submitBtn.dataset.user
    }

    fetch(`/api/form_ticket/${fId}`, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        if (data.status == 200 && (submitBtn.dataset.user == 'UserRole.STAFF' || submitBtn.dataset.user == 'UserRole.ADMIN')) {
            const inputList = document.querySelectorAll('form input')
            Array.from(inputList).forEach(inp => inp.value=null)
            select.value=0
            price.innerHTML = new Intl.NumberFormat().format(parseInt(price.dataset.price))
            return Swal.fire({
              title: 'Đặt vé thành công. Bạn có muốn đến trang xem vé?',
              showDenyButton: true,
              confirmButtonText: 'Có',
              denyButtonText: "Tiếp tục đặt vé",
            }).then((result) => {
              if (result.isConfirmed) {
                window.location.href = "/preview_ticket/" + submitBtn.dataset.userid
              }
            })

        }
        if (data.status == 200) {
            window.location.href = "/pay/" + data.data
        }
        if (data.status == 500) {
            Swal.fire("Lỗi", data.data, "error")
        }
    })
    .catch(err => {
        Swal.fire("Lỗi", err.data, "error")
    })
}