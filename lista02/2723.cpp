#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
#define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;


int solve(int n, vecint &w){
    // dp? :S
    // ideia: definir 10 estados representando as possiveis diferencas
    // se tenho diferenca de 3 atual, tento add o peso w e marco 3+w como alcancavel se 3+w for em abs menor que 5
    // se for maior nem preciso trackear pq fica desequilibrado
    // na iteracao seguinte, o estado 3+w que foi alcancavel na iteracao passada deve ser levado em consideracao
    // faco isso p todo w 

    // 11 estados: -5 ate 5
    int offset = 5;

    // vetor de possibilidades
    vecint possible_states(11, 0);
    possible_states[0 + offset] = 1;

    for(int i = 0; i<w.size(); i++){

        // se eh alcancavel
        vecint can_reach(11, 0);

        for (int diff = -5; diff <= 5; diff++) {
            if (!possible_states[diff + offset]) continue;

            int real_diff_a = diff + w[i];
            if (-5 <= real_diff_a && real_diff_a <= 5) can_reach[real_diff_a + offset] = 1;

            int real_diff_b = diff - w[i];
            if (-5 <= real_diff_b && real_diff_b <= 5) can_reach[real_diff_b + offset] = 1;
        }

        if(accumulate(can_reach.begin(), can_reach.end(), 0) == 0) return 0;

        possible_states = can_reach;
        // can_reach.clear();
    }
    
    return 1;
}


int main(){ _

    int T, N;
    cin >> T;

    for(int i = 0; i<T; i++){

        cin >> N;

        vecint w(N);
        for(int j=0; j<N; j++){
            cin >> w[j];
        }

        bool ans = solve(N, w);

        if(ans == 1) cout << "Feliz Natal!" << endl;
        else cout << "Ho Ho Ho!" << endl;
    }
    
    return 0;
}