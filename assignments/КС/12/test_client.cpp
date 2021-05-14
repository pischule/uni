#include <stdio.h>
#include <winsock2.h>
#include <iostream>
#include <chrono>

#pragma comment(lib, "ws2_32.lib") //Winsock Library

#define SERVER "127.0.0.1" //ip address of udp server
#define BUFLEN 512		   //Max length of buffer
#define PORT 8888		   //The port on which to listen for incoming data

int main(int argc, char **argv)
{
	struct sockaddr_in si_other;
	int s, slen = sizeof(si_other);
	char buf[BUFLEN];
	char message[BUFLEN];
	WSADATA wsa;

	int number_of_packets = 1024;
	int size_of_packet = BUFLEN;
	int reply_count = 0;
	bool wait_confirm = false;

	if (argc < 3) {
		std::cout << "Usage: test_client nubmer_of_packets size_of_packet wait_conirm\n";
		return 1;
	}

	number_of_packets = atoi(argv[1]);
	size_of_packet = atoi(argv[2]);
	wait_confirm = atoi(argv[3]) != 0;

	if (size_of_packet > BUFLEN)
	{
		std::cerr << "too large packet size\n";
		return 1;
	}

	//Initialise winsock
	printf("\nInitialising Winsock...");
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		printf("Failed. Error Code : %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}
	printf("Initialised.\n");

	//create socket
	if ((s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == SOCKET_ERROR)
	{
		printf("socket() failed with error code : %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}

	//setup address structure
	memset((char *)&si_other, 0, sizeof(si_other));
	si_other.sin_family = AF_INET;
	si_other.sin_port = htons(PORT);
	si_other.sin_addr.S_un.S_addr = inet_addr(SERVER);

	char *packet = new char[size_of_packet];

	auto start = std::chrono::steady_clock::now();
	for (int i = 0; i < number_of_packets; ++i)
	{
		if (sendto(s, packet, size_of_packet, 0, (struct sockaddr *)&si_other, slen) == SOCKET_ERROR)
		{
			printf("sendto() failed with error code : %d", WSAGetLastError());
			exit(EXIT_FAILURE);
		}

		if (wait_confirm)
		{
			memset(buf, '\0', BUFLEN);
			//try to receive some data, this is a blocking call
			if (recvfrom(s, buf, BUFLEN, 0, (struct sockaddr *)&si_other, &slen) == SOCKET_ERROR)
			{
				printf("recvfrom() failed with error code : %d", WSAGetLastError());
				exit(EXIT_FAILURE);
			}
			else
			{
				++reply_count;
			}
		}
	}
	auto end = std::chrono::steady_clock::now();
	auto diff = end - start;

	std::cout << "Sent " << number_of_packets << " packets\n"
			  << "with " << size_of_packet << " size\n"
			  << "received " << reply_count << " packets"
			  << "\n";

	std::cout << "Duration: ";
	std::cout << std::chrono::duration <double, std::milli> (diff).count() << " ms" << std::endl;

	closesocket(s);
	WSACleanup();

	return 0;
}