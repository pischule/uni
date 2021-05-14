#include <iostream>
#include <winsock2.h>

using namespace std;

int main() {
    WSADATA data;

    if (WSAStartup(MAKEWORD(2, 2), &data) != 0) {
        cerr << "Problems with WSAStartup" << endl;
        WSACleanup();
        return 1;
    }

    cout << "Search information about host by hostname and host ip:  " << endl;
    const int length = 255;
    char name[length];

    if (gethostname(name, length) == 0) {
        cout << endl << "Localhost name: " << name << endl << endl;
    } else {
        cout << "Can't get localhost name" << endl << endl;
    }

    string address;
    cout << "Enter host name/address: ";
    cin >> address;

    HOSTENT *host;
    ULONG addr = inet_addr(address.c_str());

    if (addr != INADDR_NONE) {
        host = gethostbyaddr((char *) &addr, sizeof(ULONG), AF_INET);
    } else {
        host = gethostbyname(address.c_str());
    }

    if (host == NULL) {
        cerr << "No information about host" << endl;
        WSACleanup();
        return 0;
    }

    cout << "Host name: " << host->h_name << endl;
    for (int i = 0; host->h_aliases[i] != NULL; ++i) {
        cout << "Alias name: " << host->h_aliases[i] << endl;
    }

    for  (int i = 0; host->h_addr_list[i] != NULL; ++i) {
        cout << inet_ntoa(*(in_addr *) host->h_addr_list[i]) << endl;
    }

    WSACleanup();
    return 0;
}
