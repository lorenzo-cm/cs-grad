#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

bool valida_divisao(vector<string> linha, int qtd_produtos){
    int soma = 0;
    for(int i = 0; i < linha.size()-1; i++){
        soma += stoi(linha[i]);
    } 
    return soma==stoi(linha[qtd_produtos]);
}

bool valida_string(string str) {
    if(str.empty()) return false;
    if(str.size() > 1 && str[0] == '0') return false;
    if(str.size() > 8) return false;
    return true;
}

bool rec(string& numbers, int qtd_produtos, int idx_fator, vector<string>& divisao, int idx_restante_numbers, vector<vector<string>> &solutions) {

    if(idx_fator == qtd_produtos){

        // cout << "Divisao" << endl;
        // for(string str : divisao){
        //     cout << str << " ";
        // }
        // cout << endl << endl;

        if(idx_restante_numbers >= numbers.size()) return false;
        if(!valida_string(numbers.substr(idx_restante_numbers, numbers.length()))) return false;

        divisao.pb(numbers.substr(idx_restante_numbers, numbers.length()));
        
        if(valida_divisao(divisao, qtd_produtos)){
            solutions.pb(divisao);
        }
        else{
            divisao.pop_back();
            return false;
        }
    }

    int remaining_needed = qtd_produtos - idx_fator;

    for(int i=1; i<=numbers.length(); i++){
        if(idx_restante_numbers + i <= numbers.length() - remaining_needed){
            string substring = numbers.substr(idx_restante_numbers, i);
            if(valida_string(substring)){
                divisao.pb(numbers.substr(idx_restante_numbers, i));
                if(rec(numbers, qtd_produtos, idx_fator+1, divisao, idx_restante_numbers+i)) return true;
                divisao.pop_back();
            }
        }
        else{
            break;
        }
    }

    return false;
}

vector<string> processar_linha(string linha, int qtd_produtos, vector<vector<vector<string>>> possible_solutions){
    vector<string> vetor;

    int idx_final_nome = 0;
    while (isalpha(linha[idx_final_nome])) idx_final_nome++;
    vetor.pb(linha.substr(0, idx_final_nome));

    string numbers = linha.substr(idx_final_nome, linha.length()-idx_final_nome);
    vector<string> divisao;

    vector<vector<string>> solutions;
    rec(numbers, qtd_produtos, 0, divisao, 0, solutions);

    possible_solutions.pb(solutions);

    if(divisao.empty()) divisao = vector<string>(qtd_produtos+1, "0");

    for(auto str : divisao) vetor.pb(str);

    return vetor;
}

vector<string> parse_cabecalho(string linha, int qtd_produtos){
    vector<string> vetor;
    for(int i=0; i<linha.length();i++){
        if(linha[i] == 'P'){
            vetor.pb(linha.substr(i, 2));
            i++;
        }

        else{
            vetor.pb("Totals");
            break;
        }
    }

    return vetor;
}


vector<vector<string>> verificar_solucoes(vector<vector<vector<string>>>& possible_solutions){
    vector<vector<string>> ans;
    int ci, cj, ck;
    int acertos = 0;
    int ult_linha = possible_solutions.size()-1;
    for(int col = 0; col < possible_solutions[0].size(); col++){
        int soma = 0;
        for(int linha = 0; linha < possible_solutions.size()-1; linha++){
            soma += stoi(possible_solutions[linha][col][acertos]);
        }
        if(soma == stoi(possible_solutions[ult_linha][col][acertos]));
    }

}


int count_ps(string str){
    int count = 0;
    for(int i=0; i<str.length();i++){
        if(str[i] == 'P') count++;
    }
    return count;
}


int main(){ 

    int c; cin >> c;
    cin.ignore();

    for(int abc=0; abc<c; abc++){
        vector<vector<string>> relatorio;
        vector<vector<vector<string>>> possible_solutions;
        vector<string> nomes;

        string cabecalho;
        getline(cin, cabecalho);

        int qtd_produtos = count_ps(cabecalho);

        relatorio.pb(parse_cabecalho(cabecalho, qtd_produtos));
        
        string linha;
        string name = "";

        vector<string> linhas;

        while(name != "TP"){
            getline(cin, linha);
            linhas.pb(linha);
            name = linha.substr(0, 2);
        }

        for(int i=0; i<linhas.size(); i++){
            getline(cin, linha);
            
            vector<string> parsed = processar_linha(linha, qtd_produtos, possible_solutions);
            nomes.pb(parsed[0]);
            name = parsed[0];
        }



        for(vector<string> line : relatorio){
            for(string str : line){
                cout << str << " ";
            }
            cout << endl;
        }

    }
    
    return 0;
}