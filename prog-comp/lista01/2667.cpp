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

    string number;

    cin >> number;

    int sum = 0;

    for(int i=0; i<number.length(); i++){
        sum += int(number[i]);
    }

    cout << sum % 3 << endl;
    
    return 0;
}