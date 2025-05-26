#include <bits/stdc++.h>

using namespace std;

#define _ ios_base::sync_with_stdio(0);cin.tie(0);
#define endl '\n'
#define f first
// #define s second
#define pb push_back
#define vecint vector<int>

typedef long long ll;

const int INF = 0x3f3f3f3f;
const ll LINF = 0x3f3f3f3f3f3f3f3fll;

int solve(string s){
    int count_ones = 0;
    
    for(int i = 0; i< s.length(); i++){
        if(s[i] == '1') count_ones++;
    }

    return count_ones;
}


int main(){ _
    int t;
    cin >> t;
    for(int i = 0; i<t; i++){
        string s;
        cin >> s;
        cout << solve(s) << endl;
    }

    
    return 0;
}