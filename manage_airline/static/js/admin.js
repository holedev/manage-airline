const btnAccepts = document.querySelectorAll(".accept")
const btnDels = document.querySelectorAll(".delete")

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