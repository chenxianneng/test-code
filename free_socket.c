/*  This program, server4.c, begins in similar vein to our last server,
    with the notable addition of an include for the signal.h header file.
    The variables and the procedure of creating and naming a socket are the same.  */

#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/msg.h>

#define MAX_TEXT 512

struct my_msg_st {
    long int my_msg_type;
    char some_text[MAX_TEXT];
};

int main()
{
    int server_sockfd, client_sockfd;
    int server_len, client_len;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;

    server_sockfd = socket(AF_INET, SOCK_STREAM, 0);

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(9734);
    server_len = sizeof(server_address);
    bind(server_sockfd, (struct sockaddr *)&server_address, server_len);

    listen(server_sockfd, 5);

    signal(SIGCHLD, SIG_IGN);
    int count = 0;    
    while(1) {
        char ch;

        printf("server waiting\n");

        client_len = sizeof(client_address);
        client_sockfd = accept(server_sockfd, 
                               (struct sockaddr *)&client_address, &client_len);

        printf("%d\n", ++count);

        if(fork() == 0) {
            //´´½¨ÏûÏ¢¶ÓÁÐ
            int running = 1;
            struct my_msg_st some_data;
            int msgid;
            char buffer[BUFSIZ];

            msgid = msgget((key_t)1234, 0666 | IPC_CREAT);

            if (msgid == -1) {
                fprintf(stderr, "msgget failed with error: %d\n", errno);
                exit(EXIT_FAILURE);
            }
            
            while(1){
                int i_size = read(client_sockfd, &ch, 1);
                
                if(i_size > 0){
                    ch++;
                    write(client_sockfd, &ch, 1);                                        
                }
                else{
                    if£¨errno != EINTR£©{
                            close(client_sockfd);
                            //printf("sockfd:%d closed\n", client_sockfd);
                            exit(0);                            
                        }
                }
            }
        }
        else {
            close(client_sockfd);
        }
    }
}
