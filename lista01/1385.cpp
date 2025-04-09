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
    bool valid = soma==stoi(linha[qtd_produtos]);
    return valid;
}

bool valida_string(string str, int depth, int qtd_produtos, int is_tp) {
    if(str.empty()) return false;
    if(str.size() > 1 && str[0] == '0') return false;

    if(str.size() > 6) return false;

    if(!is_tp and qtd_produtos != depth){
        if(stoi(str) >= 1000) return false;
    }

    return true;
}

void rec(string& numbers, int qtd_produtos, int pos, vector<string>& atual, vector<vector<string>> &solutions, int is_tp) {

    if(atual.size() == qtd_produtos + 1){
        // cout << "numbers = " << numbers << endl;
        // for(auto v : atual){
        //     cout << v << " ";
        // }
        // cout << endl;

        // cout << "pos = " << pos << " numbers len = " << numbers.length() << " atual size = " << atual.size() << " qtd prod + 1 = " << qtd_produtos +1 << " valido = " << valida_divisao(atual, qtd_produtos) << endl;
        if(pos == numbers.length() and atual.size() == qtd_produtos+1 and valida_divisao(atual, qtd_produtos)){
            // cout << "inserido" << endl;
            solutions.pb(atual);
        }

        return;
    }

    int faltam = numbers.length() - pos;
    for(int i = 0; i<=faltam; i++){
        string pedaco = numbers.substr(pos, i);
        if(!valida_string(pedaco, atual.size(), qtd_produtos, is_tp)) continue;
        atual.pb(pedaco);
        rec(numbers, qtd_produtos, pos+i, atual, solutions, is_tp);
        atual.pop_back();
    }
    
}

vector<string> processar_linha(string linha, int qtd_produtos, vector<vector<vector<string>>> &possible_solutions, int is_tp){
    vector<string> vetor;

    int idx_final_nome = 0;
    while (isalpha(linha[idx_final_nome])) idx_final_nome++;

    vetor.pb(linha.substr(0, idx_final_nome));


    string numbers = linha.substr(idx_final_nome, linha.length()-idx_final_nome);

    vector<string> divisao;
    vector<vector<string>> solutions;
    rec(numbers, qtd_produtos, 0, divisao, solutions, is_tp);

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

bool verifica(vector<vector<string>> &sol){
    
    // for(auto v : sol){
    //     for(auto w : v){
    //         cout << w << ' ';
    //     }
    //     cout << endl;
    // }
    // cout << endl;

    int num_linhas = sol.size();
    int num_cols = sol[0].size();

    bool valid = true;
    for(int i=0; i<num_cols; i++){
        int soma = 0;
        for(int linha=0; linha<num_linhas-1; linha++){
            soma+=stoi(sol[linha][i]);
        }
        if(soma != stoi(sol[num_linhas-1][i])){
            // cout << "soma = " << soma << " ultimo elemento = " << stoi(sol[sol[i].size()-1][i]) << endl;
            // cout << "entrou falso" << endl;
            valid = false;
            break;
        }
    }
    return valid;
}

bool rec2(vector<vector<vector<string>>>& possible_solutions, vector<vector<string>>& final, int linha_atual){
    if(linha_atual == possible_solutions.size()){

        return verifica(final);
    }

    for(int i = 0; i<possible_solutions[linha_atual].size(); i++){
        final.pb(possible_solutions[linha_atual][i]);
        if(rec2(possible_solutions, final, linha_atual+1)) return true;
        final.pop_back();
    }

    return false;
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
        // cout << "------------------------------" << endl;
        vector<string> cabecalho_parsed;
        vector<vector<vector<string>>> possible_solutions;
        vector<string> nomes;

        string cabecalho;
        getline(cin, cabecalho);

        int qtd_produtos = count_ps(cabecalho);

        cabecalho_parsed = parse_cabecalho(cabecalho, qtd_produtos);
        
        string linha;
        string name_temp = "";

        vector<string> linhas;

        while(name_temp != "TP"){
            getline(cin, linha);
            linhas.pb(linha);
            name_temp = linha.substr(0, 2);
            vector<string> parsed = processar_linha(linha, qtd_produtos, possible_solutions, name_temp=="TP");
            nomes.pb(parsed[0]);
        }

        // for(string& l : linhas){
        //     vector<string> parsed = processar_linha(l, qtd_produtos, possible_solutions);
        //     nomes.pb(parsed[0]);
        //     name = parsed[0];
        // }

        // for(auto v : possible_solutions){
        //     for(auto w : v){
        //         cout << "(";
        //         for(auto y: w){
        //             cout << y << ", ";
        //         }
        //         cout << ")" << "\t";
        //     }
        //     cout << endl;
        // }

        vector<vector<string>> ans;
        rec2(possible_solutions, ans, 0);

        for(string str : cabecalho_parsed){
            cout << str << " ";
        }
        cout << endl;

        int idx = 0;
        for(vector<string> line : ans){
            cout << nomes[idx] << " ";
            idx++;
            for(string str : line){
                cout << str << " ";
            }
            cout << endl;
        }

    }
    
    return 0;
}