#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;


string recursive(string prefix, string infix){

    int len_string = infix.length();

    // condicao de parada
    if(len_string == 0){
        return "";
    }

    // pego o no central que divide em esquerda e direita
    char root = prefix[0];
    
    // pego o index dele
    int idx_root_infix;

    for(int j=0; j<len_string; j++){
        if(root == infix[j]){
            idx_root_infix = j;
            break;
        }
    }

    // agora sei qual e a parte direta e esquerda do infixo e consequentemente do prefixo

    // infix
    string I_ESQ = infix.substr(0, idx_root_infix);
    string I_DIR = infix.substr(idx_root_infix+1, len_string);

    // prefix
    string P_ESQ = prefix.substr(1, 1+idx_root_infix);
    string P_DIR = prefix.substr(idx_root_infix+1, len_string);

    // recursao
    string recursive_esq = recursive(P_ESQ, I_ESQ);
    string recursive_dir = recursive(P_DIR, I_DIR);

    return recursive_esq + recursive_dir + root;
}



int main(){ 

    int c; cin >> c;

    for(int i = 0; i < c; i++){

        // nodes
        int n; cin >> n;

        // prefixo e infixo
        string s1, s2;
        cin >> s1 >> s2;

        cout << recursive(s1, s2) << endl;

    }

    
    return 0;
}