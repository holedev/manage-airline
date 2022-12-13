const canvas = document.getElementById('canvas');
const canvasContext = document.getElementById('canvas').getContext("2d");

function setStatus(el, status) {
    el.style.display = status
}

function checkType() {
    const canvas = document.querySelector('#canvas')
    if (selectType.value == 1) {
        setStatus(canvas, 'none')
        setStatus(table, 'table')
    }
    if (selectType.value == 2) {
        setStatus(canvas, 'block')
        setStatus(table, 'none')
    }
}

function drawStats(el, labels, data) {
    colors = randColor(data.prices)
    new Chart(el, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: 'Doanh thu',
            data: data.prices,
            borderWidth: 1,
            backgroundColor: colors,
          }, {
            label: 'Vé bán',
            data: data.tickets,
            borderWidth: 1,
            backgroundColor: colors,
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
}

function randColor(arr) {
    arrColor = []
    arr.forEach(item => {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        arrColor.push(`rgb(${r},${g},${b})`);
    })
    return arrColor
}

function editTableData(month, data, totalPrice) {
    const rows = document.querySelectorAll('.r-table')
    rows.forEach(r => r.remove())
    const htmls = data.map(d => {
        return `
            <tr class="r-table text-center">
                <td class="" scope="col">${ d.airport_from.name } → ${ d.airport_to.name }</td>
                <td data-price=${ d.total_price } class="price" scope="col">${new Intl.NumberFormat().format(parseInt(d.total_price))}</td>
                <td scope="col">${ d.total_ticket }</td>
                <td scope="col">${ d.price_rate?.toFixed(2) || 0}</td>
            </tr>
        `
    }).join("")
    document.querySelector('tbody').innerHTML = htmls
    document.querySelector('.title').innerHTML = `BÁO CÁO DOANH THU ${month != 0 ? "THÁNG " + month: "TOÀN BỘ"}`
    document.querySelector('.price-total').innerHTML = new Intl.NumberFormat().format(parseInt(totalPrice))
}

function drawStatsJS(el, data) {
    const labels = []
    const bigData = {
        prices: [],
        tickets: [],
        rates: []
    }

    data.forEach(d => {
        labels.push(`${d.airport_from.name} → ${d.airport_to.name}`)
        bigData.prices.push(d.total_price)
        bigData.tickets.push(d.total_ticket)
        bigData.rates.push(d.price_rate?.toFixed(2))
    })

    drawStats(el, labels, bigData)
}

function getData(month) {
    fetch(`/api/get_stats/${month}`, {
        method: 'post',
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        editTableData(month, data.data, data.total_price)
        document.querySelector("#canvas").remove()
        const canvas = document.createElement("canvas");
        canvas.id = "canvas"
        canvas.className = "w-50 h-50"
        document.querySelector('#wrapCanvas').appendChild(canvas)
        drawStatsJS(canvas, data.data)
        checkType()
    })
}