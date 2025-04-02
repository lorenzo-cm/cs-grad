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
    int m;
    while(cin >> m){
        if(m == 0) break;
        cin.ignore();

        string f;
        getline(cin, f);

        unordered_map<char, int> char2count;
        int l = 0;
        int max_tam = 0, curr_tam = 0;
        int used = 0;
        for(int r = 0; r<f.length(); r++){

            char curr_char = f[r];

            if(char2count[curr_char] && char2count.count(curr_char) > 0){
                char2count[curr_char] += 1;
                curr_tam += 1;
            }

            else if(used < m){
                char2count[curr_char] += 1;
                curr_tam++;
                used++;
            }
            
            else {
                while(used == m){
                    char left_char = f[l];
                    char2count[left_char]--;
                    curr_tam--;
                    if(char2count[left_char] == 0){
                        used--;
                    }
                    l++;
                }

                char2count[curr_char] = 1;
                curr_tam++;
                used++;
            }

            max_tam = max(max_tam, curr_tam);          
        }

        cout << max_tam << endl;
    }
    
    return 0;
}