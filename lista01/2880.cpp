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

    string s; string p;
    cin >> s; cin >> p;

    int count_crib = 0;

    int end_index = s.size() - p.size() + 1; 

    for(int i = 0; i < end_index; i++){

        for(int j = 0; j<p.size(); j++){
            if(s[i+j] == p[j]){
                break;
            }
            if(j == p.size() - 1) count_crib++;
        }

    }

    cout << count_crib << endl;
    
    return 0;
}