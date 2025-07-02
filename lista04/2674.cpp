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

void crivo(int max, vector<bool>& is_prime){
    is_prime[0] = is_prime[1] = false;
    for(int i = 2; i * i <= max; i++){
        if(is_prime[i]){
            for(int j = i * i; j <= max; j += i){
                is_prime[j] = false;
            }
        }
    }
}

bool todos_digitos_primos(int n){
    while(n > 0){
        int digit = n % 10;
        if(digit != 2 && digit != 3 && digit != 5 && digit != 7){
            return false;
        }
        n /= 10;
    }
    return true;
}

int main(){ _

    vector<bool> is_prime(1e5 + 1, true);
    crivo(1e5, is_prime);

    int n;
    while(cin >> n){
        if(is_prime[n]){
            if(todos_digitos_primos(n)) cout << "Super" << endl;
            else cout << "Primo" << endl;
        }
        
        else cout << "Nada" << endl;

    }
    return 0;
}
