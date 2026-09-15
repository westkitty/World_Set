#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/stat.h>

static int is_port_open(int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return 0;
    struct sockaddr_in sin;
    sin.sin_family = AF_INET;
    sin.sin_port = htons(port);
    sin.sin_addr.s_addr = inet_addr("127.0.0.1");
    int res = connect(sock, (struct sockaddr *)&sin, sizeof(sin));
    close(sock);
    return (res == 0);
}

int main(int argc, char *argv[]) {
    // 1. Ensure local background HTTP server is running on port 8000
    if (!is_port_open(8000)) {
        system("nohup /opt/homebrew/bin/python3 -m http.server 8000 --directory '/Users/andrew/World_Set' >/dev/null 2>&1 &");
        for (int i = 0; i < 30; i++) {
            usleep(50000); // 50ms
            if (is_port_open(8000)) break;
        }
    }

    // 2. Launch in standalone dedicated wrapper window
    const char *url = "http://localhost:8000/index.html";
    if (access("/Applications/Google Chrome.app", F_OK) == 0) {
        char cmd[512];
        snprintf(cmd, sizeof(cmd), "/usr/bin/open -na 'Google Chrome' --args --app='%s' --window-size=1440,900", url);
        system(cmd);
    } else if (access("/Applications/Brave Browser.app", F_OK) == 0) {
        char cmd[512];
        snprintf(cmd, sizeof(cmd), "/usr/bin/open -na 'Brave Browser' --args --app='%s' --window-size=1440,900", url);
        system(cmd);
    } else {
        char cmd[512];
        snprintf(cmd, sizeof(cmd), "/usr/bin/open -a Safari '%s'", url);
        system(cmd);
    }

    return 0;
}
