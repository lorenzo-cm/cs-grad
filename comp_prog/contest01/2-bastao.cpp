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

int main(){ _

    int t; cin >> t;

    for(int i = 0; i<t; i++){
        int n; cin >> n;

        vecint nums(n);

        for(int j = 0; j<n; j++) nums[j] = j;

        int l = 0;
        int r = n-1;

        string s;
        cin >> s;

        vecint ans(n);

        for(int j = n-2; j>=0; j--){

            if(s[j] == '<'){
                ans[j+1] = nums[l];
                l++;
            } 

            else if(s[j] == '>'){
                ans[j+1] = nums[r];
                r--;
            }

        }

        ans[0] = nums[r];


        for(int j = 0; j<n; j++){
            cout << ans[j] + 1 << ' ';
        }
        cout << endl;

    }
    
    return 0;
}