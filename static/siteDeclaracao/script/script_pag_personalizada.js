//pegar dados do formulario
// const form = document.getElementById('formCasal');
// const nome1 = document.getElementById('nome1');
// const nome2 = document.getElementById('nome2');

// const mensagem = document.getElementById('mensagem');
// const btn_criar_site = document.querySelectorAll('.btn_criar_site');
// const link_musica = document.getElementById('link_musica');
const data = document.getElementById('data');
const time = document.getElementById('time');
// const imagem = document.getElementById('foto');
//** */

//pegar componentes do preview
const preview_titulo = document.getElementById('preview_titulo');
const preview_nome1 = document.getElementById('preview_nome1');
const preview_nome2 = document.getElementById('preview_nome2');
const preview_mensagem = document.getElementById('preview_mensagem');
const preview_link_musica = document.getElementById('preview_link_musica');
// const preview_cont_anos = document.getElementById('preview_cont_anos');
// const preview_imagem = document.getElementById('preview_imagem');
//** */

///###################
//enviar formulario
// function criarSite(event){
//   event.preventDefault();
  
  
//   if (!validarNome(nome1) || !validarNome(nome2)) {
//     alert('Preencha os nomes dos noivos!');
//     return;
//   }

//   form.submit();
//   console.log('Enviando arquivos... Aguarde!');
//   console.log('Arquivos enviados com sucesso!');
//   console.log('Site criado com sucesso!');
  // console.log(`Acesse o site em: https://192.168.10.33:4444/love/${nome1}${nome2}`);
// }

// btn_criar_site.forEach(botao => {
//   botao.addEventListener('click', criarSite);
// });




//############


//função para atualizar o preview cont_anos
function atualizarPreview(){
    preview_cont_anos.innerHTML = calcularAnos();
};
atualizarPreview()

//criar evento de input
// nome1.addEventListener('input', function(){
//     preview_nome1.innerHTML = nome1.value;
// });
// nome2.addEventListener('input', function(){
//     preview_nome2.innerHTML = nome2.value;
// });
// mensagem.addEventListener('input', function(){
//     preview_mensagem.innerHTML = mensagem.value;
// });
// data.addEventListener('input', atualizarPreview);
// time.addEventListener('input', atualizarPreview);

//função para calcular anos de casados data atual calcular os anos meses dias horas minutos e segundos
function calcularAnos() {
  // Função para converter '1 de Setembro de 2024' para '2024-09-01'
  function converterDataBRParaISO(dataBR) {
      const meses = {
          'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
          'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
          'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
      };

      const partes = dataBR.split(' ');
      const dia = partes[0];
      const mes = meses[partes[2]];
      const ano = partes[4];

      // Formato ISO que o Date entende: 'YYYY-MM-DD'
      return `${ano}-${mes}-${dia.padStart(2, '0')}`;
  }

  // Obtendo data e hora
  const hora = time.innerHTML != '' ? time.innerHTML : '00:00';
  const data_casamento_str = converterDataBRParaISO(data.innerHTML); // Convertendo a data
  const data_casamento = new Date(data_casamento_str + 'T' + hora); // Criando o objeto Date

  const data_atual = new Date();
  const diferenca = data_atual - data_casamento;

  // Cálculo de anos, meses, dias, horas, minutos e segundos
  const anos = Math.floor(diferenca / (1000 * 60 * 60 * 24 * 365));
  const meses = Math.floor((diferenca % (1000 * 60 * 60 * 24 * 365)) / (1000 * 60 * 60 * 24 * 30));
  const dias = Math.floor((diferenca % (1000 * 60 * 60 * 24 * 30)) / (1000 * 60 * 60 * 24));
  const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
  const segundos = Math.floor((diferenca % (1000 * 60)) / 1000);

  // Condições para formatar a mensagem
  if (anos < 1 && meses > 0) {
      return `<br>${meses} meses, ${dias} dias, ${horas} horas, ${minutos} minutos e ${segundos} segundos de nós!`;
  }
  if (anos < 1 && meses < 1) {
      return `<br>${dias} dias, ${horas} horas, ${minutos} minutos e ${segundos} segundos de nós!`;
  }

  return `${anos} anos, ${meses} meses, ${dias} dias, ${horas} horas, ${minutos} minutos e ${segundos} segundos de nós!`;
}


//função para pegar as imagens do formulario e enviar para o preview
// function atualizarImagemOriginal(){
//     const imagem = document.getElementById('foto').files[0];
//     const reader = new FileReader();
//     reader.onload = function(){
//         document.getElementById('preview_imagem').src = reader.result;
//     }
//     reader.readAsDataURL(imagem);
// }

//segunda verção fa função atualizar imagem que lida com varios arquivos
// function atualizarImagem() {
//   const input = document.getElementById('foto'); // Campo input do tipo file
//   const imgCarrossel = document.getElementById('imgCarrossel'); // Container do carrossel
//   imgCarrossel.innerHTML = ''; // Limpar o conteúdo anterior para novas imagens

//   // Percorrer os arquivos selecionados pelo usuário
//   for (let i = 0; i < input.files.length; i++) {
//       const imagem = input.files[i];
//       const reader = new FileReader();

//       reader.onload = function(event) {
//           // Criar um novo elemento de imagem
//           const novaImagem = document.createElement('img');
//           novaImagem.src = event.target.result;
//           novaImagem.classList.add('carousel-image'); // Adiciona a classe de estilo
//           novaImagem.alt = `Imagem ${i+1}`; // Definir o alt da imagem

//           // Adicionar a nova imagem no container do carrossel
//           imgCarrossel.appendChild(novaImagem);
//       };

//       reader.readAsDataURL(imagem); // Ler cada imagem como URL de dados
//   }
  // Atualizar a lista de imagens
  //setTimeout() com 100ms para garantir que as imagens tenham sido carregadas no DOM antes de atualizarmos a variável imagens.
//   setTimeout(() => {
//     imagens = document.querySelectorAll('.carousel-image');
//     TotalImagens = imagens.length;
//     currentIndex = 0; // Reiniciar o índice
//     imagens[currentIndex].classList.add('active');
//     if(TotalImagens > 1) {
//       trocarImagemAutomaticamente(); // Iniciar a troca automática de imagens
//     }
// }, 100); // Aguardar a inserção das imagens
// }


//criar evento de input para a imagem
// document.getElementById('foto').addEventListener('input', atualizarImagem);

//caroussel
let currentIndex = 0;
let imagens = document.querySelectorAll('.carousel-image');
let TotalImagens = imagens.length;


const prev = document.getElementById('prev');
const next = document.getElementById('next');
if(next){
  next.addEventListener('click', function(){
    imagens[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % TotalImagens;
    imagens[currentIndex].classList.add('active');
    
  });
}
if(prev){
  prev.addEventListener('click', function(){
    imagens[currentIndex].classList.remove('active');
    currentIndex = (currentIndex - 1 + TotalImagens) % TotalImagens;
    imagens[currentIndex].classList.add('active');
    
  });
}

imagens[currentIndex].classList.add('active');

//função para atualizar as imagens automaticamente
function trocarImagemAutomaticamente() {
  setInterval(function() {
    // Remove a classe 'active' da imagem atual
    imagens[currentIndex].classList.remove('active');
    // Avançar para a próxima imagem
    currentIndex = (currentIndex + 1) % imagens.length;
    // Adicionar a classe 'active' à nova imagem
    imagens[currentIndex].classList.add('active');
  }, 5000); // 2 segundos (2000 milissegundos)
}

trocarImagemAutomaticamente();
//##############
