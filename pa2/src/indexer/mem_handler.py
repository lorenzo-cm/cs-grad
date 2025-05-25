from os import makedirs
from threading import Lock
import json
import gc

from src.utils import current_mem, debug_logger, progress_logger

class MemHandler:
    def __init__(self, mem_limit, corpus_path, index_dir,
                 inv_idx: dict[str, list[tuple[int, int]]],
                 doc_idx: dict[int, dict],
                 lexicon: dict[str, dict],
                 access_structures_lock: Lock,
                 num_threads=16,
                 lines_limit=None):
        # estrategia: uma thread por vez consumira o leitor do corpus
        # 1- thread solicitara leitura
        # 2- verifica se tem espaco para ler
        #   2.1- se não tiver, flush
        # 3- a leitura retorna um doc
        
        self.mem_limit = mem_limit*1024*1024
        self.corpus_path = corpus_path
        
        self.inv_idx = inv_idx
        self.doc_idx = doc_idx
        self.lexicon = lexicon
        
        self.num_threads = num_threads
        
        self.lines_limit = lines_limit
        
        # Preparar caminho de salvamento dos arquivos de index
        self.index_dir = index_dir
        self.inv_idx_prefix = 'inv_idx'
        self.doc_idx_prefix = 'doc_idx'
        
        # ensure index dir alredy exists
        makedirs(self.index_dir, exist_ok=True)
        
        # 10 mb -> size word = 25 b -> * 10k -> 250000 -> 0.25 mb -> bastante folga
        # nos meus experimentos, alocar 1000 docs é equivalente a aumentar cerca de 0.6 mb (upper bound)
        # Supondo N threads, em que cada uma le apenas um doc por vez, terei N*0.6/1000 de memoria gasta
        # Supondo um texto de 10k -> posso ter 10k entradas com uma ocorrencia o que daria cerca de:
        # tupla com dois ints
        # (8+8+overhead) * 10k + overhead =  160k + overhead ~= 200k bytes = 0.2 mb
        # Na pratica, observei em media 3256 bytes por doc a mais no inv idx
        # Entao eu teria por thread um custo realistico de N*0.6/1000 mb + N*0.2 mb
        # Consideraremos N*0.3 mb como aproximacao
        # Considerando o custo do doc idx, que é mt menor, considerarei N*0.5 mb
        # Como o lexico nao é salvo, ele fica sempre na memória e isso pode ser um problema
        # No entanto, como ele não é mt complexo, ele pode se comportar bem
        # Nos meus experimentos, obtive cerca de 100k palavras rodando com uma fração dos documentos
        # Expandindo radicalmente para 1mi, faremos a approx. Considere que o lexico salva apenas 2 atributos:
        # qtd de docs que o termo apareceu, quantidade de vezes que o termo apareceu
        # 10⁶ * (8+8+overhead_da_tupla_e_lista) + overhead+dicionario <= 10
        # No entando tem o custo de transformar esse doc em index
        # self.MEM_TO_READ = self.num_threads*0.5 * 1024*1024
        
        # Esse safeguard eh para a memoria alocada pelo OS nao chegar mt perto do limite
        self.MEM_SAFEGUARD = min(50*1024*1024, self.mem_limit/10)
        
        # Percent of memlimit allocated
        self.PERCENT_ALLOCATED = 0.9
        
        # 1000 docs a mais -> upper bound = 24 mb
        self.len_to_save = 1000 * (self.PERCENT_ALLOCATED * 0.9) * mem_limit / 24
        self.increase_len_to_save = 500 # upper bound = 12 mb
        debug_logger.debug(f'INIT - Len to save: {self.len_to_save}')

        # Locks
        self.io_lock = Lock()
        self.access_structures_lock = access_structures_lock
        
        # Ler corpus linha por linha
        self.file = open(corpus_path, 'r', encoding='utf-8')
        self.file_iter = iter(self.file)
        
        # Salvar inv idx
        self.seq = 0
        
        # Lines count
        self.count_lines = 0
        

    def read_line(self) -> str | None:
        """
        Entrega uma única linha do corpus de forma thread-safe.
        *Retorna None* quando o arquivo termina.
        """
        with self.io_lock:
            
            if current_mem() >= self.mem_limit:
                raise MemoryError(f'Memory allocated surpases the limit. Current memory: {current_mem() / (1024*1024)} mb')
            
            if self.lines_limit is not None and self.count_lines >= self.lines_limit:
                return None
            
            self.count_lines += 1
            
            if self.count_lines % 50000 == 0:
                progress_logger.info(f'Progress: {self.count_lines} - Memory: {current_mem() / (1024*1024)}')
            
            if len(self.inv_idx) >= self.len_to_save:
                self._flush_and_save()
                
            line = next(self.file_iter, None)
                        
            return line


    def _flush_and_save(self):
        """
        Função para liberar memória
        Ela salva a lista invertida
        Não precisa dar flush no resto:
        - Document index pode ser salvo a cada iteração sem problemas
        - Term lexicon não é tão grande e daria trabalho p ser guardado
        """
        with self.access_structures_lock:
            debug_logger.debug(f'FLUSH - Current_mem: {current_mem() / (1024*1024)} mb --- Count lines: {self.count_lines}')
            
            # Se tiver muita memoria sobrando, ir aumentando
            # Isso não parece funcionar pq o current_mem() nao consegue pegar as desalocacoes
            # Se tem memoria disponivel do que memoria usada
            if (self.PERCENT_ALLOCATED * self.mem_limit) - (self.MEM_SAFEGUARD) > current_mem():
                self.len_to_save += max(self.increase_len_to_save, 0) # prevent negative values of increase len to save
                debug_logger.debug(f'UPDATE - UP - Len to save: {self.len_to_save}, Increase len to save: {self.increase_len_to_save}')
            
            else:
                self.len_to_save -= 100 # upper bound = 2.4 mb
                self.increase_len_to_save -= 50
                debug_logger.debug(f'UPDATE - UP - Len to save: {self.len_to_save}, Increase len to save: {self.increase_len_to_save}')
                        
            self._flush_inv_idx()
            self._flush_doc_idx()
            self._flush_lexicon()
                    
            self.seq += 1
            
            gc.collect()

            debug_logger.debug(f'AFTER FLUSH --- current_mem: {current_mem() / (1024*1024)} mb')
    
    def _flush_inv_idx(self) -> None:
        path = f"{self.index_dir}/{self.inv_idx_prefix}_{self.seq:03d}"
        with open(path, "w", encoding="utf-8") as f:

            # sort alphabetically
            for term in sorted(self.inv_idx.keys()):
                postings = self.inv_idx[term]

                # sort doc_id
                postings.sort(key=lambda pair: pair[0])

                doc_freq_str = " ".join(
                    f"{doc_id}:{freq}" for doc_id, freq in postings
                )
                f.write(f"{term} {doc_freq_str}\n")

        self.inv_idx.clear()
    
    def _flush_doc_idx(self) -> None:
        with open(f'{self.index_dir}/{self.doc_idx_prefix}.jsonl', "a", encoding="utf-8") as f:
            for key, values in self.doc_idx.items():
                json.dump({key: values}, f, ensure_ascii=False)
                f.write("\n")
                
        self.doc_idx.clear()
                
                
    def _flush_lexicon(self) -> None:
        path = f"{self.index_dir}/lexicon_{self.seq:03d}.jsonl"
        with open(path, "w", encoding="utf-8") as f:

            # sort alphabetically
            for term in sorted(self.lexicon):
                entry = self.lexicon[term]

                json.dump({term: entry}, f, ensure_ascii=False)
                f.write("\n")

        self.lexicon.clear()
