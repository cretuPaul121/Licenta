var request = new XMLHttpRequest()

var currentDoctor;

fetch('http://localhost:5000/isLoggedIn').then(res => res.json()).then(res => {
    console.log(res);

    if (res['email'] !== undefined) {

        request.open('GET', 'http://localhost:5000/myPacients/' + res['doctor_id'], true);

        request.onload = function() {

            var data = JSON.parse(this.response)

            if (request.status >= 200 && request.status < 400) {

                const root_div = document.getElementById('root')
                const logo = document.createElement('img')

                logo.src = 'pacienti_banner.jpg'

                const container = document.createElement('div')

                container.setAttribute('class', 'container')

                root_div.appendChild(logo)
                root_div.appendChild(container)


                data.forEach((pacient) => {
                    const card = document.createElement('div')
                    card.setAttribute('class', 'card')

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

                    card.appendChild(id)
                    card.appendChild(nume)
                    card.appendChild(div_buton)
                    div_buton.addEventListener('click', () => {
                        alert(pacient.id_pacient);
                        fetch('http://localhost:5000/setPacient/' + pacient.id_pacient).then(res => res.json()).then(res => {
                            window.location.href = 'file:///D:/Work/licentaPaul/Licenta/WEB%20licenta/pacienti/pacient.html';
                        });
                    });

                })


            } else {
                console.log('eroare ')
            }

        }

        request.send();

    }


});