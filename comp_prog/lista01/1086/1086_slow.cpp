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

int find_complement(const vector<int>& tabuas, int target) {
    // tabuas is in descending order
    int low = 0;
    int high = tabuas.size() - 1;

    while (low <= high) {
        int mid = (low + high) / 2;

        if (tabuas[mid] == target) {
            return mid;
        } else if (tabuas[mid] < target) {
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return -1;
}


int check_row(int tam, vector<int> &tabuas){
    // k * (log n + 2n) 
    for(int i = 0; i < tabuas.size(); i++){

        int complement = tam - tabuas[i];

        if(complement){
            auto complement_idx = find_complement(tabuas, complement);
            if(complement_idx != -1){

                if (complement_idx != i) {
                    if (complement_idx > i) {
                        tabuas.erase(tabuas.begin() + complement_idx);
                        tabuas.erase(tabuas.begin() + i);
                    } else {
                        tabuas.erase(tabuas.begin() + i);
                        tabuas.erase(tabuas.begin() + complement_idx);
                    }
                    return 2;
                }
            }
        }
        else{
            tabuas.erase(tabuas.begin() + i);
            return 1;
        }

    }

    return 0;
}

int check_orientation(int tam1, int tam2, int l, vector<int> tabuas){
    
    vector<int> used(tabuas.size(), 0);

    vector<int> copy_tabuas = tabuas;

    if(tam1 % l != 0){
        return 0;
    }

    int total = 0;
    for(int i = 0; i < tam1/l; i++){
        int tabuas_usadas = check_row(tam2, copy_tabuas);
        if(!tabuas_usadas) return 0;
        total += tabuas_usadas;
    }

    return total;
}

int check_fit(int m, int n, int l, vector<int> tabuas){
    // primeira orientacao
    int result1 = INF;
    if (m % l == 0){
        result1 = check_orientation(m, n, l, tabuas);
        if(result1 == 0){
            result1 = INF;
        }
    }

    // segunda orientacao
    int result2 = INF;
    if (n % l == 0){
        result2 = check_orientation(n, m, l, tabuas);
        if(result2 == 0){
            result2 = INF;
        }
    }

    int min_tabuas = min(result1, result2);
    return min_tabuas;
}


int main(){ _

    while(1){
        // Dimensoes salao MxN
        int m, n;
        cin >> m >> n;

        // passar para cm
        m *= 100;
        n *= 100;

        if(m == 0 and n == 0){
            break;
        }

        // Largura em cm
        int l;
        cin >> l;

        // Tabuas
        int k;
        cin >> k;

        int temp;
        vector<int> comprimentos;
        for(int i = 0; i < k; i++){
            cin >> temp;
            comprimentos.pb(temp*100); // passar para cm
        }

        // Garantir ordem para binary search
        // n log n
        sort(comprimentos.begin(), comprimentos.end(), greater<int>());

        int num_tabuas = check_fit(m, n, l, comprimentos);

        if(num_tabuas < INF){
            cout << num_tabuas << endl;
        }
        else{
            cout << "impossivel" << endl;
        }

    }
    

    
    return 0;
}