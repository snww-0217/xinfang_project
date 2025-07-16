document.addEventListener("DOMContentLoaded", function () {
    fetch('/consultation/car_list/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                renderCarList(data.cars);
            } else {
                console.error('获取失败');
            }
        })
        .catch(error => {
            console.error('请求错误：', error);
        });
});

function renderCarList(cars) {
    const carList = document.getElementById('car-list');
    cars.forEach(car => {
        const col = document.createElement('div');
        col.className = 'col-md-4 mb-4';

        const card = document.createElement('div');
        card.className = 'card car-card';

        if (car.image_url) {
            const img = document.createElement('img');
            img.src = car.image_url;
            img.alt = `${car.brand} ${car.model}`;
            img.className = 'card-img-top car-image';
            card.appendChild(img);
        }

        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';

        const title = document.createElement('h5');
        title.className = 'card-title';
        title.textContent = `${car.brand} ${car.model}`;

        const year = document.createElement('p');
        year.className = 'card-text';
        year.textContent = `生产年份：${car.production_year} | 使用年限：${car.usage_years}年`;

        const insurance = document.createElement('p');
        insurance.className = 'card-text';
        insurance.textContent = `保险状态：${car.insurance_status}`;

        const accident = document.createElement('p');
        accident.className = 'card-text';
        accident.textContent = `重大事故：${car.major_accident ? '有' : '无'}`;

        cardBody.appendChild(title);
        cardBody.appendChild(year);
        cardBody.appendChild(insurance);
        cardBody.appendChild(accident);

        card.appendChild(cardBody);
        col.appendChild(card);
        carList.appendChild(col);
    });
}

