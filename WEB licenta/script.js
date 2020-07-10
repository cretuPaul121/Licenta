

function generateContent(){
	
	let elements = [];
	let btn = document.createElement('button');

	for(let i=0;i<5;i++){
		elements.push(document.createElement("input"));
	}
	elements[0].type = "text";
	elements[0].placeholder = "Introduceti Iedentificatorul";
	elements[1].type = "text";
	elements[1].placeholder = "Introduceti Numele";
	elements[2].type = "text";
	elements[2].placeholder = "Introduceti Specializarea";
	elements[3].type = "email";
	elements[3].placeholder = "Email";
	elements[4].type = "password";
	elements[4].placeholder = "Parola";
	let container = document.getElementsByClassName('form-box')[0];
	for(let i=0;i<5;i++){
		elements[i].style.display = 'block';
		elements[i].style.marginTop = "30px";
		elements[i].style.marginLeft = "25%";
		elements[i].style.width = "50%";
		elements[i].style.height="8%";
		elements[i].id = "id"+i;
		container.appendChild(elements[i]);
	}
	btn.style.marginTop = "30px";
	btn.style.height = "6%";
	btn.style.width = "30%";
	btn.textContent = "Submit";
	container.appendChild(btn);

	btn.addEventListener('click',()=>{
		
		let box = document.getElementsByClassName('form-box')

		let textInputs = []
		let doctor ={}
		let empty = false

		for(let i=0;i<5;i++){
			let x = document.getElementById("id"+i).value
			textInputs.push(x)
		}

		for(let i=0;i<5;i++){
			if(textInputs[i] === '') empty  = true
		}	

		if(empty){
			const p = document.createElement('h2')

			p.setAttribute('color', 'red')
			p.setAttribute('text-transform', 'uppercase')
			p.value = 'Completati va rog toate campurile necesare'
			
			alert('completeaza toate campurile')
			return;
		}

		doctor.doctor_id = parseInt(textInputs[0])
		doctor.nume = textInputs[1]
		doctor.specializare = textInputs[2]
		doctor.email = textInputs[3]
		doctor.parola = textInputs[4]

	
		const options = {
			method: 'POST',
			body: JSON.stringify(doctor),
			headers:{
				'Content-Type':'application/json'
			}
		}

		fetch('http://10.127.127.1:5000/addDoctor', options).then(res => res.json()).then((res)=>{
			alert("Inregistrare cu succes")
			window.location.href = 'login.html'
		});


	
	});
}

generateContent();