let isLogged = false;
let tbIndex = 0;
fetch('http://localhost:5000/isLoggedIn').then(res => res.json()).then(res => {
	console.log(res);
	if(res['email'] !== undefined){
		window.location = 'doctori/doctor_page.html';
	}else{
		dynamicGenerateLogin();
	}
});


function dynamicGenerateLogin() {
	let elements = [];
	elements.push(document.createElement('input'));
	elements.push(document.createElement('input'));
	let btn = document.createElement('button');
	elements[0].type = 'email';
	elements[0].placeholder = 'Email';
	elements[1].type = 'password';
	elements[1].placeholder = 'Password';
	let container = document.getElementsByClassName('form-box')[0];
	for (let i = 0; i < 2; i++) {
		elements[i].style.display = 'block';
		elements[i].style.marginTop = '30px';
		elements[i].style.width = '50%';
		elements[i].style.marginLeft = '25%';
		elements[i].style.height = '8%';
		elements[i].id = 'id' + i;
		container.appendChild(elements[i]);
	}
	btn.style.marginTop = "30px";
	btn.style.height = "6%";
	btn.style.width = "30%";
	btn.textContent = "Login";
	container.appendChild(btn);
	console.log(document.cookie);


	btn.addEventListener('click', () => {

		let mail = document.getElementById('id0').value;
		let password = document.getElementById('id1').value

		if (mail === '' || password === '') {
			alert("completeaza cu spatiile necesare")
			return;
		}


		fetch('http://10.127.127.1:5000/doctor/' + mail+'/'+password).then(res => res.json()).then(resp => {

			if (resp.email === mail && resp.parola === password) {
				console.log("Logare reusita")
				window.location = 'doctori/doctor_page.html';
			}
		})
	});
}

