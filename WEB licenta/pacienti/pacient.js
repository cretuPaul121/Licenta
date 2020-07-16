var request = new XMLHttpRequest()

var currentDoctor;

let contactBtn;
let textArea = undefined;
let sendBtn = undefined;
let clearBtn = undefined;

function createMailArea(card) {
    textArea = document.createElement('textarea');
    textArea.style.display = 'block';
    textArea.style.marginLeft = '3.5%';
    textArea.style.marginTop = '2%';
    textArea.placeholder = 'Completeaza continutul E-mail-ului...';
    textArea.rows = 10;
    textArea.cols = 80;
    card.appendChild(textArea);

    sendBtn = document.createElement('button');
    sendBtn.textContent = 'Trimite';
    sendBtn.style.marginLeft = '3.5%';
    sendBtn.style.width = '80px';
    sendBtn.style.height = '30px';
    card.appendChild(sendBtn);
    sendBtn.style.display = 'inline';

}

function removeMailArea(card) {
    card.removeChild(textArea);
    card.removeChild(sendBtn);
    textArea = undefined;
    sendBtn = undefined;
}

function createCanvas(holder) {
    let cnv = document.createElement('canvas');
    cnv.width = 1000;
    cnv.height = 500;
    let ctx = cnv.getContext('2d');
    ctx.beginPath();
    ctx.rect(100, 20, 850, 400);
    ctx.strokeStyle = 'blue';
    ctx.stroke();
    holder.appendChild(cnv);
    arr = [];
    arr.push([]);
    arr[0][0] = 100;
    arr[0][1] = 225;
    for (let i = 1; i < 30; i++) {
        arr.push([]);
        arr[i][0] = arr[i - 1][0] + 20;
        arr[i][1] = Math.floor(Math.random() * 200) + 120;
    }
    drawEkg(arr, ctx);
}

function drawEkg(arr, ctx) {
    ctx.beginPath();
    ctx.strokeStyle = '#FF0000';
    ctx.moveTo(arr[0][0], arr[0][1]);
    for (let i = 1; i < arr.length; i++) {
        ctx.lineTo(arr[i][0], arr[i][1]);
    }
    ctx.stroke();
}


fetch('http://localhost:5000/isLoggedIn').then(res => res.json()).then(res => {
    console.log(res);

    if (res['email'] !== undefined) {
        fetch('http://localhost:5000/getCurrPacient').then(rasp => rasp.json()).then(rasp => {
            request.open('GET', 'http://localhost:5000/patient/' + rasp.id, true);

            request.onload = function() {

                var data = JSON.parse(this.response);

                if (request.status >= 200 && request.status < 400) {

                    const root_div = document.getElementById('root')
                    const logo = document.createElement('img')

                    logo.src = 'pacienti_banner.jpg'

                    const container = document.createElement('div')

                    container.setAttribute('class', 'container')

                    root_div.appendChild(logo)
                    root_div.appendChild(container)
                    data = [data[0]];

                    data.forEach((pacient) => {
                        const card = document.createElement('div')
                        card.setAttribute('class', 'card2')

                        const id = document.createElement('h1')
                        id.textContent = "Id pacient: " + pacient.id_pacient

                        const nume = document.createElement('h2')

                        pacient.nume_pacient = pacient.nume_pacient.substring(0, 50)
                        nume.textContent = `${pacient.nume_pacient}`

                        const buton = document.createElement('button')
                        const div_buton = document.createElement('div')

                        div_buton.setAttribute('class', 'container_buton')

                        buton.setAttribute('class', 'buton_vizualizare')
                        buton.innerHTML = "Vizualizare pacient";

                        div_buton.appendChild(buton)
                        container.appendChild(card)


                        card.appendChild(id);
                        card.appendChild(nume);
                        contactBtn = document.createElement('button');
                        contactBtn.textContent = 'Contact';
                        contactBtn.style.marginLeft = '3.5%';
                        contactBtn.style.width = '80px';
                        contactBtn.style.height = '30px';
                        card.appendChild(contactBtn);
                        createMailArea(card);
                        textArea.style.display = 'none';
                        sendBtn.style.display = 'none';
                        contactBtn.addEventListener('click', () => {
                            if (contactBtn.textContent === 'Contact') {
                                textArea.style.display = 'block';
                                sendBtn.style.display = 'block';
                                contactBtn.textContent = 'Inchide';
                            } else {
                                textArea.style.display = 'none';
                                sendBtn.style.display = 'none';
                                textArea.value = '';
                                contactBtn.textContent = 'Contact';
                            }
                        });
                        // card.appendChild(div_buton)

                        let sectionHeader = document.createElement('h2');
                        sectionHeader.style.marginTop = '10px';
                        sectionHeader.textContent = 'Diseases:';
                        card.appendChild(sectionHeader);
                        fetch('http://localhost:5000/pacientDiseases/' + pacient.id_pacient).then(res => res.json()).then((res) => {
                            let listOfDiseases = document.createElement('ol');
                            console.log(res);
                            for (let i = 0; i < res.length; i++) {
                                let node = document.createElement('h2');
                                node.style.marginLeft = '10px';
                                node.textContent = res[i]['nume'] + ' : ' + res[i]['descriere'];
                                card.appendChild(node);
                            }
                            createCanvas(card);
                        });



                    });


                } else {
                    console.log('eroare ')
                }

            }

            request.send();
        });
    }


});