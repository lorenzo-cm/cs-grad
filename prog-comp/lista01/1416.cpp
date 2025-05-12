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
    
int main(){ 

    int t, p;

    while(cin >> t >> p){
        if(t == 0) break;

        // cout << "===========================" << endl;
        vector<pair<int, int>> times(t);
        vector<vector<pair<int, int>>> empatados(p+1);

        for(int i = 0; i<t; i++){
            int problemas_resolvidos = 0;
            int a = 0;
            int b = 0;

            for(int j = 0; j<p; j++){
                int tentativas;
                char tempo[10];
                scanf("%d/%s", &tentativas, &tempo);

                if (tempo[0] != '-'){
                    problemas_resolvidos++;
                    a += tentativas - 1;
                    b += atoi(tempo);
                }
            }
            empatados[problemas_resolvidos].pb({a*20+b, i});
            times[i] = {a, b};
        }

        // for(auto e : empatados){
        //     cout << "Size problema empatado: " << e.size() << endl;
        //     for(auto par : e){
        //             cout << par.f << ", " << par.s << " | ";
        //     }
                
        //     cout << endl;    
        // }

        int lower = 1;
        int upper = INF;
        bool break_loop = false;
        for(int i = 0; i<empatados.size() && !break_loop; i++){

            if(empatados[i].empty()) continue;
            
            sort(empatados[i].begin(), empatados[i].end());

            for (int j = 0; j < empatados[i].size() - 1; j++){
                int idx_time_a = empatados[i][j].s;
                int idx_time_b = empatados[i][j+1].s;

                auto [a1, b1] = times[idx_time_a];
                auto [a2, b2] = times[idx_time_b];

                // cout << "A_1: " << a1 << " B_1: " << b1 << endl;
                // cout << "A_2: " << a2 << " B_2: " << b2 << endl;

                if(a1 == a2) continue;

                int num = b2 - b1;
                int den = a1 - a2;

                if (den == 0) {
                    continue;
                }

                int ep = num / den;
                int resto = num % den;

                // cout << "num: "<< num << " den: " << den << " epInt: " << epInt << endl;

                if ( (ep > 20) || (ep == 20 && resto != 0) ) {
                    // cout << "Caiu 1 -> " << ep << " com resto " << resto << endl;
                    if (resto == 0) {
                        upper = min(upper, ep - 1);
                    } else {
                        upper = min(upper, ep);
                    }

                } else if (ep < 20) {
                    // cout << "Caiu 2 -> " << epInt << " com resto " << resto << endl;
                    lower = max(lower, ep + 1);

                } else {
                    // cout << "Caiu 3 -> " << ep << " com resto " << resto << endl;
                    lower = 20;
                    upper = 20;
                    break_loop = true;
                    break;
                }

                // cout << endl;
            }
        }

        string upper_str = upper < INF ? to_string(upper) : "*";
        
        cout << lower << " " << upper_str << endl;
    }
    
    return 0;
}