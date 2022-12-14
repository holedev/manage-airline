const submitBtn = document.querySelector('#submit-btn')
const inputList = document.querySelectorAll('form input')

submitBtn.onclick = (e) => {
    e.preventDefault()
    const inputList = document.querySelectorAll('form input')
    const inpErr = Array.from(inputList).find(inp => !inp.value)
    if (inpErr) {
        inpErr.focus()
        return Swal.fire("Lỗi", "Vui lòng nhập đủ thông tin!", "error")
    }

    const data = {
        number_card: inputList[0].value.trim(),
        mmYY: inputList[1].value.trim(),
        cvcCode: inputList[2].value.trim(),
        name: inputList[3].value.trim(),
    }


    const pathNames = window.location.pathname
    const fId = pathNames[pathNames.length - 1]

    fetch(`/api/pay/${fId}`, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        switch (data.status) {
            case 200:
                window.location.href = "/preview_ticket/" + data.data.id
                break;
            case 500:
                Swal.fire("Lỗi", "Lỗi server!", "error")
                break;
            default:
                break;
        }
    })
    .catch(err => {
        Swal.fire("Lỗi", "Lỗi server!", "error")
    })
}