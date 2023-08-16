window.onload = (e) =>{
    console.log("AAA")
    console.log(document.getElementById("test").getAttribute("url"))
}

function deletePerson(e){
    if(confirm(`Tem certeza que deseja deletar o cadastro de '${e.getAttribute("person_name")}'?\n\tEste processo é irreversível.`)== true){
        document.getElementById("personForm").submit()
    }
}