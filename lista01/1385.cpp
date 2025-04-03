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
    if(str.size() > 4) return false;
    return true;
}

bool rec(string& numbers, int qtd_produtos, int idx_fator, vector<string>& divisao, int idx_restante_numbers) {
    

    if(idx_fator == qtd_produtos){
        if(idx_restante_numbers >= (int)numbers.size()) return false;
        if(!valida_string(numbers.substr(idx_restante_numbers, numbers.length()))) return false;

        divisao.pb(numbers.substr(idx_restante_numbers, numbers.length()));

        vector<string> temp = {"1020", "1020", "0", "0", "2040"};
        if(divisao == temp){
            
        }

        cout << "Divisao" << endl;
            for(string str : divisao){
                cout << str << " ";
            }
            cout << endl << endl;
        

        if(valida_divisao(divisao, qtd_produtos)) return true;
        else{
            divisao.pop_back();
            return false;
        }
    }

    int remaining_needed = qtd_produtos - idx_fator;

    for(int i=1; i<=3; i++){
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

vector<string> processar_linha(string linha, int qtd_produtos){
    vector<string> vetor;

    int idx_final_nome = 0;
    while (isalpha(linha[idx_final_nome])) idx_final_nome++;
    vetor.pb(linha.substr(0, idx_final_nome));

    string numbers = linha.substr(idx_final_nome, linha.length()-idx_final_nome);
    vector<string> divisao;

    rec(numbers, qtd_produtos, 0, divisao, 0);

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

        string cabecalho;
        getline(cin, cabecalho);

        int qtd_produtos = count_ps(cabecalho);

        relatorio.pb(parse_cabecalho(cabecalho, qtd_produtos));
        
        string linha;
        string name = "";

        while(name != "TP"){
            getline(cin, linha);
            
            vector<string> parsed = processar_linha(linha, qtd_produtos);
            relatorio.pb(parsed);

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