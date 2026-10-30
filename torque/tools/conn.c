// Injected into a running 5.12 Graal.exe (Wine): calls the engine export connectToGraalServer(name, host, int port)
// so the client joins a server without a login server. conn.cfg holds "name|host|port"; "3 " names are 3D servers.
#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
typedef int (__cdecl *CF)(const char*,const char*,int);
static DWORD WINAPI go(LPVOID x){
  FILE*f=fopen("Z:\\home\\claude\\w512\\inj\\conn.log","a");
  char cfg[512]="3 Seihai Test|127.0.0.1|14800";
  FILE*c=fopen("Z:\\home\\claude\\w512\\inj\\conn.cfg","r"); if(c){fgets(cfg,sizeof cfg,c);fclose(c);}
  char *n=strtok(cfg,"|\r\n"),*h=strtok(0,"|\r\n"),*p=strtok(0,"|\r\n");
  HANDLE s=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());MODULEENTRY32 me={sizeof me};CF fn=0;
  for(BOOL ok=Module32First(s,&me);ok;ok=Module32Next(s,&me)){fprintf(f,"mod %s %p\n",me.szModule,me.modBaseAddr);
    FARPROC a=GetProcAddress(me.hModule,"connectToGraalServer"); if(a){fn=(CF)a;fprintf(f," -> connectToGraalServer %p\n",a);}}
  if(fn){fprintf(f,"calling (%s,%s,%s)\n",n,h,p);fflush(f);fprintf(f,"busy=%d 3dcb=%p startcb=%p conn3d=%p\n",*(unsigned char*)0x10407224,*(void**)0x104066f4,*(void**)0x104066ec,*(void**)0x104066c0);fflush(f);int r=fn(n,h,atoi(p));fprintf(f,"returned %d flag3d=%d port=%d\n",r,*(unsigned char*)0x10406d91,*(int*)0x1040722c);}
  fclose(f);return 0;}
BOOL WINAPI DllMain(HINSTANCE i,DWORD r,LPVOID x){if(r==DLL_PROCESS_ATTACH)CreateThread(0,0,go,0,0,0);return TRUE;}
