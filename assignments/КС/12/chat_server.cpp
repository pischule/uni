#include "winsock2.h"
#include <iostream>
#include <conio.h>
#include <sstream>

using namespace std;
#define MYPORT 9009 // the port users will be connecting to

int main()

{

	WSADATA wsaData;

	WSAStartup(MAKEWORD(2, 2), &wsaData);

	SOCKET sock;

	sock = socket(AF_INET, SOCK_DGRAM, 0);

	char broadcast = '1';

	//     This option is needed on the socket in order to be able to receive broadcast messages

	//   If not set the receiver will not receive broadcast messages in the local network.

	if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0)

	{

		cout << "Error in setting Broadcast option";

		closesocket(sock);

		return 0;
	}

	struct sockaddr_in Recv_addr;

	struct sockaddr_in Sender_addr;

	int len = sizeof(struct sockaddr_in);

	char recvbuff[50];

	int recvbufflen = 50;

	char sendMSG[] = "Broadcast message from READER";

	Recv_addr.sin_family = AF_INET;

	Recv_addr.sin_port = htons(MYPORT);

	Recv_addr.sin_addr.s_addr = INADDR_ANY;

	if (bind(sock, (sockaddr *)&Recv_addr, sizeof(Recv_addr)) < 0)

	{

		cout << "Error in BINDING" << WSAGetLastError();

		_getch();

		closesocket(sock);

		return 0;
	}

	while (true)
	{

		recvfrom(sock, recvbuff, recvbufflen, 0, (sockaddr *)&Sender_addr, &len);

		ostringstream oss;
		oss << (char* ) inet_ntoa(Sender_addr.sin_addr) << ":" << ntohs(Sender_addr.sin_port) << ": " << recvbuff << "\n";
		strcpy(recvbuff, oss.str().c_str());
		cout << oss.str();

		
   		Sender_addr.sin_family       = AF_INET;
		Sender_addr.sin_addr.s_addr = inet_addr("127.255.255.255");
		if (sendto(sock, recvbuff, recvbufflen, 0, (sockaddr *)&Sender_addr, sizeof(Sender_addr)) < 0)

		{

			cout << "Error in Sending." << WSAGetLastError();
			closesocket(sock);
			return 0;
		}
	}

	closesocket(sock);

	WSACleanup();
}


// #include<stdio.h>
// #include<winsock2.h>
// #include <iostream>
// #include <sstream>

// #pragma comment(lib,"ws2_32.lib") //Winsock Library

// #define BUFLEN 512	//Max length of buffer
// #define PORT 8888	//The port on which to listen for incoming data

// int main()
// {
// 	SOCKET s;
// 	struct sockaddr_in server, si_other;
// 	int slen , recv_len;
// 	char buf[BUFLEN];
// 	WSADATA wsa;

// 	slen = sizeof(si_other) ;
	
// 	//Initialise winsock
// 	printf("\nInitialising Winsock...");
// 	if (WSAStartup(MAKEWORD(2,2),&wsa) != 0)
// 	{
// 		printf("Failed. Error Code : %d",WSAGetLastError());
// 		exit(EXIT_FAILURE);
// 	}
// 	printf("Initialised.\n");
	
// 	//Create a socket
// 	if((s = socket(AF_INET , SOCK_DGRAM , 0 )) == INVALID_SOCKET)
// 	{
// 		printf("Could not create socket : %d" , WSAGetLastError());
// 	}
// 	ULONG bc = 1;
// 	if ((setsockopt(s, SOL_SOCKET, SO_BROADCAST, (char*) &bc,sizeof(ULONG)) == SOCKET_ERROR)) {
// 		printf("setsockopt() failed with error code : %d" , WSAGetLastError());
// 		exit(EXIT_FAILURE);
// 	}
// 	printf("Socket created.\n");
	
// 	//Prepare the sockaddr_in structure
// 	server.sin_family = AF_INET;
// 	server.sin_addr.s_addr = INADDR_ANY;
// 	server.sin_port = htons( PORT );
	
// 	//Bind
// 	if( bind(s ,(struct sockaddr *)&server , sizeof(server)) == SOCKET_ERROR)
// 	{
// 		printf("Bind failed with error code : %d" , WSAGetLastError());
// 		exit(EXIT_FAILURE);
// 	}
// 	puts("Bind done");

// 	//keep listening for data
// 	while(1)
// 	{
// 		printf("Waiting for data...");
// 		fflush(stdout);
		
// 		//clear the buffer by filling null, it might have previously received data
// 		memset(buf,'\0', BUFLEN);
		
// 		//try to receive some data, this is a blocking call
// 		if ((recv_len = recvfrom(s, buf, BUFLEN, 0, (struct sockaddr *) &si_other, &slen)) == SOCKET_ERROR)
// 		{
// 			printf("recvfrom() failed with error code : %d" , WSAGetLastError());
// 			exit(EXIT_FAILURE);
// 		}
		
// 		//print details of the client/peer and the data received
// 		printf("Received packet from %s:%d\n", inet_ntoa(si_other.sin_addr), ntohs(si_other.sin_port));
// 		printf("Data: %s\n" , buf);

// 		std::ostringstream oss;
// 		oss << (char* ) inet_ntoa(si_other.sin_addr) << ":" << ntohs(si_other.sin_port) << ": " << buf;
// 		strcpy(buf, oss.str().c_str());
		
// 		//now reply the client with the same data
// 		if (sendto(s, buf, BUFLEN, 0, (struct sockaddr*) &si_other, slen) == SOCKET_ERROR)
// 		{
// 			printf("sendto() failed with error code : %d" , WSAGetLastError());
// 			exit(EXIT_FAILURE);
// 		}
// 	}

// 	closesocket(s);
// 	WSACleanup();
	
// 	return 0;
// }