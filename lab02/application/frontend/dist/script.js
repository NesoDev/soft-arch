let getList = async (listNum, school) => {
    const url = "http://127.0.0.1:3000"
    try {
        let response;
        console.log("SOLICITANDO LISTA");
        response = await fetch(`${url}/list/${listNum}/${school}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(`res: ${JSON.stringify(data)}`);
        return data.data;
    } catch (error) {
        console.error('Fetch error:', error);
        return [];
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    let data1 = {cols: [], rows: []};
    let data2 = {cols: [], rows: []};
    let lastBtn = "none";

    let button1 = document.getElementById('btn1');
    let button2 = document.getElementById('btn2');
    let appOpts = document.getElementById('app-options');
    let appSelect = document.getElementById('app-select');
    let canvas = document.getElementById('canvas');
    let footer = document.getElementById('app-footer');

    // Mover el click a dentro del DOMContentLoaded después de los event listeners
    button1.addEventListener('click', async function () {
        console.log("BTN1 PRESSED");
        button1.classList.add('active');
        button2.classList.remove('active');
        canvas.innerHTML = "";
        textContainer = document.createElement('div');
        textContainer.id = "text-container";
        textContainer.innerText = "Cargando...";
        let pFooter = document.createElement('p');
        pFooter.innerText = "( Muestra el número de alumnos por cada Carrera Profesional )";
        footer.innerHTML = "";
        footer.appendChild(pFooter);
        canvas.appendChild(textContainer);
        appOpts.style.display = 'none';
        if (data1.rows.length == 0) {
            data1 = await getList(1, "none");
        }
        if (lastBtn != "btn1") {
            createFillTable(canvas, data1);
        }
        lastBtn = "btn1";
    });

    button2.addEventListener('click', async function () {
        console.log("BTN2 PRESSED");
        button2.classList.add('active');
        button1.classList.remove('active');
        appOpts.style.display = 'block';
        let pFooter = document.createElement('p');
        pFooter.innerText = "( Muestra los alumnos por carrera profesional cuyos alumnos que ingresaron después del 1/1/2021 y que color favorito “no sea Rojo” y cuya edad esté entre 18 y 25 años.)";
        footer.innerHTML = "";
        footer.appendChild(pFooter);
        if (data2.rows.length == 0) {
            data2 = await getList(2, "none");
        }
        data2.rows.forEach(e => {
            opt = document.createElement('option');
            opt.value = e;
            opt.text = e;
            appSelect.appendChild(opt);
        });
        lastBtn = "btn2";
    });

    appSelect.addEventListener('change', async function () {
        console.log("SELECT CHANGED");
        canvas.innerHTML = "";
        textContainer = document.createElement('div');
        textContainer.id = "text-container";
        textContainer.innerText = "Cargando...";
        canvas.appendChild(textContainer);
        let school = appSelect.value;
        school = school.replaceAll(" ", "-");
        data2 = await getList(2, school);
        createFillTable(canvas, data2);
    });

    // Simula un clic en el primer botón después de adjuntar los listener
    button2.click();
    button1.click();
});

let createFillTable = (canvas, data) => {
    let cols = data.cols.length;
    let rows = data.rows.length;
    console.log(`cols: ${cols}, rows: ${rows}`);
    let table = document.createElement('table');
    table.id = "table";
    table.setAttribute('border', '1');
    table.setAttribute('width', '100%');
    table.setAttribute('cellpadding', '0');
    table.setAttribute('cellspacing', '0');
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');
    for (let i = 0; i < cols; i++) {
        let th = document.createElement('th');
        th.innerText = data.cols[i];
        thead.appendChild(th);
    }
    for (let i = 0; i < rows; i++) {
        let tr = document.createElement('tr');
        for (let j = 0; j < cols; j++) {
            let td = document.createElement('td');
            td.innerText = data.rows[i][j];
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(thead);
    table.appendChild(tbody);  
    canvas.innerHTML = ""; 
    canvas.appendChild(table);
}