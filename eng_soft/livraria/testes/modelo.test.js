const bd = require('../bd/bd_utils.js');
const modelo = require('../modelo.js');

beforeEach(() => {
  bd.reconfig('./bd/esmforum-teste.db');
  // limpa dados de todas as tabelas
  bd.exec('delete from perguntas', []);
  bd.exec('delete from respostas', []);
});

test('Testando banco de dados vazio', () => {
  expect(modelo.listar_perguntas().length).toBe(0);
});

test('Testando cadastro de três perguntas', () => {
  modelo.cadastrar_pergunta('1 + 1 = ?');
  modelo.cadastrar_pergunta('2 + 2 = ?');
  modelo.cadastrar_pergunta('3 + 3 = ?');
  const perguntas = modelo.listar_perguntas(); 
  expect(perguntas.length).toBe(3);
  expect(perguntas[0].texto).toBe('1 + 1 = ?');
  expect(perguntas[1].texto).toBe('2 + 2 = ?');
  expect(perguntas[2].num_respostas).toBe(0);
  expect(perguntas[1].id_pergunta).toBe(perguntas[2].id_pergunta-1);
});


// My tests

// test('Testando cadastro de respostas, IDs e num de respostas', () => {
//   id_pergunta = modelo.cadastrar_pergunta('O que é teste?');

//   num_respostas = modelo.get_num_respostas(id_pergunta);
//   expect(num_respostas).toBe(0);

//   id_resposta = modelo.cadastrar_resposta(id_pergunta, 'Teste é teste');

//   num_respostas2 = modelo.get_num_respostas(id_pergunta);
//   expect(num_respostas2).toBe(1);

//   pergunta = modelo.get_pergunta(id_pergunta);
//   respostas = modelo.get_respostas(id_pergunta);

//   expect(pergunta.texto).toBe('O que é teste?');

//   expect(respostas[0].id_resposta).toBe(id_resposta);

//   modelo.cadastrar_resposta(id_pergunta, 'TESTE_TESTE');

//   num_respostas3 = modelo.get_num_respostas(id_pergunta);
//   expect(num_respostas3).toBe(2);
// });

test('Cadastro de resposta', () => {
  const id_pergunta = modelo.cadastrar_pergunta('O que é teste?');
  const id_resposta = modelo.cadastrar_resposta(id_pergunta, 'Teste é teste');

  const respostas = modelo.get_respostas(id_pergunta);

  expect(respostas[0].id_resposta).toBe(id_resposta);
  expect(respostas[0].texto).toBe('Teste é teste');
});

test('Checar ID de resposta e pergunta', () => {
  const id_pergunta = modelo.cadastrar_pergunta('O que é teste?');
  const id_resposta = modelo.cadastrar_resposta(id_pergunta, 'Teste é teste');

  const pergunta = modelo.get_pergunta(id_pergunta);
  const respostas = modelo.get_respostas(id_pergunta);

  expect(pergunta.texto).toBe('O que é teste?');
  expect(respostas[0].id_resposta).toBe(id_resposta);
});

test('Checar número de respostas', () => {
  const id_pergunta = modelo.cadastrar_pergunta('O que é teste?');

  let num_respostas = modelo.get_num_respostas(id_pergunta);
  expect(num_respostas).toBe(0);

  modelo.cadastrar_resposta(id_pergunta, 'Teste é teste');

  let num_respostas2 = modelo.get_num_respostas(id_pergunta);
  expect(num_respostas2).toBe(1);

  modelo.cadastrar_resposta(id_pergunta, 'TESTE_TESTE');

  let num_respostas3 = modelo.get_num_respostas(id_pergunta);
  expect(num_respostas3).toBe(2);
});