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


void sieve(int max, vector<bool>& is_prime){
    is_prime[0] = is_prime[1] = false;
    for(int i = 2; i * i <= max; i++){
        if(is_prime[i]){
            for(int j = i * i; j <= max; j += i){
                is_prime[j] = false;
            }
        }
    }
}

void compute_divisors(int max, vecint& div_count){
    for(int i = 1; i <= max; i++){
        for(int j = i; j <= max; j += i){
            div_count[j]++;
        }
    }
}

void preprocess(int max, vector<bool>& is_prime, vecint& div_count, vecint& hyperprime_prefix){
    sieve(max, is_prime);
    compute_divisors(max, div_count);

    for(int i = 2; i <= max; i++){
        hyperprime_prefix[i] = hyperprime_prefix[i - 1];
        if(is_prime[div_count[i]]){
            hyperprime_prefix[i]++;
        }
    }
}

int main() { _
    // crivo de eratostenes

    int max = 2000000;

    vector<bool> is_prime(max + 1, true);
    vecint div_count(max + 1, 0);
    vecint hyperprime_prefix(max + 1, 0);

    preprocess(max, is_prime, div_count, hyperprime_prefix);

    int N;
    while(cin >> N){
        cout << hyperprime_prefix[N] << endl;
    }
    
    return 0;
}
