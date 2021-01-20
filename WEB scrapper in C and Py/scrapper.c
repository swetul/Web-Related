// SWETUL PATEL
//SCRAPPER.C

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h> // For getaddrinfo
#include <stdlib.h>
#include <assert.h>

int main(int argc, char* argv[])
{
    //input checking
    if(argc == 0 || argc > 3)
    {
        printf("Input error please try again!\n");
        return -1;
    }

    char* name = argv[1];
    char* attend = argv[2];
    printf("%s", argv[2]);
    // if((strcmp("yes", argv[2])!= 0) || (strcmp("no", argv[2])!= 0))
    // {
    //     printf("Reply to invite with yes or no only!\n");
    //     return -1;
    // }

    printf("%s, %s \n", name, attend);

    //socket section
    char server_message[2000], client_message[2000];
    char address[100];

    memset(server_message, '\0', sizeof(server_message));
    int mySocket;
    int mySocket1;
    struct sockaddr_in server_addr;
    memset(client_message, '\0', sizeof(client_message));

    //create socket
    mySocket = socket(AF_INET, SOCK_STREAM,0);
    mySocket1 = socket(AF_INET, SOCK_STREAM,0);
    if(mySocket < 0)
    {
        printf("Socket not created\n");
        return -1;
    }
    if(mySocket1 < 0)
    {
        printf("Socket1 not created\n");
        return -1;
    }
    printf("Socket created successfully\n");
    struct addrinfo *result;
    struct addrinfo hints;
    memset (&hints, 0, sizeof (hints));
    memset (&result,0, sizeof(result));
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags |= AI_CANONNAME;
    printf("pre \n");
    int out;
    out = getaddrinfo("www-test.cs.umanitoba.ca", NULL, &hints, &result);


        printf("pred \n");
    if(out != 0)
    {
        printf("Error getting site address\n");
        return -1;
    }
    printf("post \n");
    struct sockaddr_in *serverDet = (struct sockaddr_in *)result->ai_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port= htons(80);
    server_addr.sin_addr = serverDet->sin_addr;

    inet_ntop (server_addr.sin_family, &server_addr.sin_addr, address, 100);
    printf("Connecting to %s\n", address);
    if(connect(mySocket, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0)
    {
        printf("unable to connect to server\n");
        return -1;
    }
    printf("connected to server!\n");
    char* request;
    char* req;
    char* host = "\r\nHost: www-test.cs.umanitoba.ca\r\n\r\n";

    req = "POST /~patels15/cgi-bin/A1.cgi HTTP/1.1\r\nConnection: keep-alive\r\nContent-Length: ";
    char* input1 = "Name=";
    char* input2 = "&Attend=";

    char* nameMem = (char *)malloc(strlen(input1) + strlen(name));
    strcpy(nameMem,input1);
    strcat(nameMem, name);
    char* att;

    if(strcmp("yes", attend) == 0)
    {
        att = (char *)malloc(strlen(input2) + strlen(attend));
        strcpy(att,input2);
        strcat(att, attend);
        char* tempVar = (char *)malloc(strlen(att) + strlen(nameMem));
        strcpy(tempVar,nameMem);
        strcat(tempVar, att);
        nameMem = tempVar;
        //free(att);
    }

    //convert length of body from int to string
    int lengt = strlen(nameMem);
    char snum[10];
    sprintf(snum, "%d", lengt);

    request = (char *)malloc(strlen(req) + strlen(host) + strlen(nameMem)+strlen(snum));
    strcpy(request,req);
    strcat(request, snum);
    strcat(request, host);
    strcat(request, nameMem);

    memset(server_message, '\0', sizeof(server_message));
    printf("Sending:\n%s\n", request);

    if(send(mySocket, request, strlen(request), 0) < 0){
        printf("Unable to send message\n");
        return -1;
    }

    // Receive the server's response:
    if(recv(mySocket, server_message, sizeof(server_message), 0) < 0){
        printf("Error while receiving server's msg\n");
        return -1;
    }
    printf("Server's response: %s\n",server_message);

    //making second request
    char* Find1 = "Set-Cookie: Name=";
    char* Find2 = "Set-Cookie: Attend=";

    char* toFind1 = (char*)malloc(strlen(Find1)+strlen(name)+1);
    strcpy(toFind1, Find1);
    strcat(toFind1, name);

    char* toFind2 = (char*)malloc(strlen(Find2)+strlen(attend)+1);
    strcpy(toFind2, Find2);
    strcat(toFind2, attend);
    printf("%s --1\n",toFind1);
    printf("%s --2\n",toFind2);


    assert((strstr(server_message,toFind1)!= NULL));
    assert((strstr(server_message,toFind2)!= NULL));

    char* cookie1 = "Cookie: Name=";
    char* cookie2 = "Attend=";
    char* fCook = (char*)malloc(strlen(cookie1)+strlen(cookie2)+strlen(name)+strlen(attend)+1);
    strcpy(fCook,cookie1);
    strcat(fCook, name);
    strcat(fCook, "; ");
    strcat(fCook, cookie2);
    strcat(fCook, attend);
    strcat(fCook, ";");
    char* reqN = "GET /~patels15/cgi-bin/A1.cgi HTTP/1.1\r\nConnection: keep-alive\r\n";
    char* reques = (char *)malloc(sizeof(req) + sizeof(host) + sizeof(toFind1)+ sizeof(toFind2));

    strcpy(reques, reqN);
    strcat(reques,fCook);
    strcat(reques,host);

    char server_message1[2000];
    memset(server_message, '\0', sizeof(server_message));
//end of making second request
    if(connect(mySocket1, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0)
    {
        printf("unable to connect to server\n");
        return -1;
    }

    printf("Sending:\n%s\n", reques);
    //Send the message to server:
    printf("Sending request, %lu bytes\n\n\n", strlen(reques));


//sending 2nd request
    if(send(mySocket1, reques, strlen(reques), 0) < 0){
        printf("Unable to send message\n");
        return -1;
    }

    // Receive the server's response:
    if(recv(mySocket1, server_message1, sizeof(server_message1), 0) < 0){
        printf("Error while receiving server's msg\n");
        return -1;
    }

    printf("Server's response: %s\n",server_message1);
    close(mySocket);
    close(mySocket1);


    return 0;
}
