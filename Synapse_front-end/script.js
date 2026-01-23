let fonte_atual = 15;
const codigo = document.getElementById("code").value;

function mudar_fonte(fonte) {
    document.getElementById("code").style.fontSize = fonte + "px";
    fonte_atual = fonte;
}

function interpretar() {
    linhas = codigo.split("/");
    console.log(linhas)
}