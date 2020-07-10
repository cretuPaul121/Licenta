fetch('http://localhost:5000/isLoggedIn').then(res => res.json()).then(res=>{
    document.getElementById('wlcm').innerText = 'Bun venit ' + res['nume'] + ' pe pagina doctorilor!';

    console.log(res)
});



