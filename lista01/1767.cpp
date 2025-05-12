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

int main(){ _

    int peso_limite = 50;

    int n; cin >> n;

    for(int i = 0; i<n; i++){

        int pac; // qtd pacotes disponiveis
        cin >> pac;

        vector<pair<int,int>> armazem;
        for(int j = 0; j<pac; j++){

            int qt, peso; // qtd brinquedos e peso de cada pacote
            cin >> qt >> peso;

            pair<int,int> temp;
            temp.f = qt;
            temp.s = peso;

            armazem.pb(temp);
        }

        vector<pair<int, int>> dynamic(peso_limite+1, pair<int, int>({0, 0})); // par => (qtd, pacotes_usados)

        for(int j = 0; j<pac; j++){
            int qtd = armazem[j].f;
            int peso = armazem[j].s;

            for(int k=peso_limite; k>=peso; k--){
                if(dynamic[k].f < dynamic[k-peso].f + qtd){
                    dynamic[k].f = dynamic[k-peso].f + qtd;
                    dynamic[k].s = dynamic[k-peso].s + 1;
                }
            }
        }

        int melhor_peso = 0;
        int melhor_qtd = 0;
        int pacotes_usados = 0;

        for(int j = 0; j<peso_limite+1; j++){
            if(dynamic[j].f > melhor_qtd){
                melhor_qtd = dynamic[j].f;
                pacotes_usados = dynamic[j].s;
                melhor_peso = j;
            }
        }
        
        cout << melhor_qtd << " brinquedos" << endl;
        cout << "Peso: " << melhor_peso << " kg" << endl;
        cout << "sobra(m) " << armazem.size() - pacotes_usados << " pacote(s)" << endl;

        cout << endl;
    }
    
    return 0;
}