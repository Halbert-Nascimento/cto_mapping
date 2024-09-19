// Selecionar elementos
const form = document.getElementById('formCasal');
const nome1 = document.getElementById('nome1');
const nome2 = document.getElementById('nome2');
const mensagem = document.getElementById('mensagem');
const btn_criar_site = document.querySelectorAll('.btn_criar_site');
const link_musica = document.getElementById('link_musica');
const data = document.getElementById('data');
const time = document.getElementById('time');
const imgCarrossel = document.getElementById('imgCarrossel');

// Pegar componentes do preview
const preview_titulo = document.getElementById('preview_titulo');
const preview_nome1 = document.getElementById('preview_nome1');
const preview_nome2 = document.getElementById('preview_nome2');
const preview_mensagem = document.getElementById('preview_mensagem');
const preview_link_musica = document.getElementById('preview_link_musica');
const preview_cont_anos = document.getElementById('preview_cont_anos');

// Função para enviar o formulário
function criarSite(event) {
  event.preventDefault(); // Prevenir o envio padrão

  // Realizar validações
  if (!validarNome(nome1) || !validarNome(nome2)) {
    alert('Preencha os nomes dos noivos!');
    return;
  }

  // Submeter o formulário via JavaScript
  console.log('Enviando arquivos... Aguarde!');
  form.submit();
  console.log('Arquivos enviados com sucesso!');
  console.log('Site criado com sucesso!');
}

// Adicionar evento aos botões
btn_criar_site.forEach(botao => {
  botao.addEventListener('click', criarSite);
});

// Função para atualizar o preview cont_anos
function atualizarPreview() {
  preview_cont_anos.innerHTML = calcularAnos();
}

// Eventos de input para atualizar o preview
nome1.addEventListener('input', () => preview_nome1.innerHTML = nome1.value);
nome2.addEventListener('input', () => preview_nome2.innerHTML = nome2.value);
mensagem.addEventListener('input', () => preview_mensagem.innerHTML = mensagem.value);
data.addEventListener('input', atualizarPreview);
time.addEventListener('input', atualizarPreview);

// Função para calcular anos de casados
function calcularAnos() {
  const hora = time.value ? time.value : '00:00';
  const data_casamento = new Date(`${data.value}T${hora}`);
  const data_atual = new Date();
  const diferenca = data_atual - data_casamento;

  const anos = Math.floor(diferenca / (1000 * 60 * 60 * 24 * 365));
  const meses = Math.floor((diferenca % (1000 * 60 * 60 * 24 * 365)) / (1000 * 60 * 60 * 24 * 30));
  const dias = Math.floor((diferenca % (1000 * 60 * 60 * 24 * 30)) / (1000 * 60 * 60 * 24));
  const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
  const segundos = Math.floor((diferenca % (1000 * 60)) / 1000);

  if (anos < 1 && meses > 0) {
    return `<br>${meses} meses, ${dias} dias, ${horas} horas, ${minutos} minutos e ${segundos} segundos de nós!`;
  }
  if (anos < 1 && meses < 1) {
    return `<br>${dias} dias, ${horas} horas, ${minutos} minutos e ${segundos} segundos de nós!`;
  }
  return `${anos} anos, ${meses} meses, ${dias} dias, ${horas} horas, ${minutos} minutos e ${segundos} segundos de nós!`;
}

// Função para atualizar as imagens do carrossel
function atualizarImagem() {
  const input = document.getElementById('foto');
  imgCarrossel.innerHTML = '';

  Array.from(input.files).forEach((imagem, i) => {
    const reader = new FileReader();
    reader.onload = event => {
      const novaImagem = document.createElement('img');
      novaImagem.src = event.target.result;
      novaImagem.classList.add('carousel-image');
      novaImagem.alt = `Imagem ${i + 1}`;
      imgCarrossel.appendChild(novaImagem);
    };
    reader.readAsDataURL(imagem);
  });

  setTimeout(() => {
    atualizarCarousel();
    if (TotalImagens > 1) {
      trocarImagemAutomaticamente();
    }
  }, 100);
}

// Atualizar a lista de imagens e reiniciar o carrossel
function atualizarCarousel() {
  imagens = document.querySelectorAll('.carousel-image');
  TotalImagens = imagens.length;
  currentIndex = 0;
  imagens[currentIndex].classList.add('active');
}

// Função para trocar a imagem automaticamente
function trocarImagemAutomaticamente() {
  setInterval(() => {
    imagens[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % imagens.length;
    imagens[currentIndex].classList.add('active');
  }, 2000); // 2 segundos (2000 milissegundos)
}

// Adicionar evento para atualizar imagens
document.getElementById('foto').addEventListener('change', atualizarImagem);

// Controle do carrossel
let currentIndex = 0;
let imagens = document.querySelectorAll('.carousel-image');
let TotalImagens = imagens.length;

const prev = document.getElementById('prev');
const next = document.getElementById('next');

if (next) {
  next.addEventListener('click', () => {
    imagens[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % TotalImagens;
    imagens[currentIndex].classList.add('active');
  });
}

if (prev) {
  prev.addEventListener('click', () => {
    imagens[currentIndex].classList.remove('active');
    currentIndex = (currentIndex - 1 + TotalImagens) % TotalImagens;
    imagens[currentIndex].classList.add('active');
  });
}

imagens[currentIndex].classList.add('active');

// Função para validar o nome
function validarNome(nome) {
  return nome.value.trim() !== '';
}
