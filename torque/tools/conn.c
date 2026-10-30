// Injected into a running 5.12 Graal.exe (Wine): calls the engine export connectToGraalServer(name, host, int port)
// so the client joins a server without a login server, then calls runGraal3DEngine every 15 ms, because under Wine
// the launcher stops calling it after its DirectDraw re-init faults. Con::printf (0x1000a220) is hooked into conn.log.
// conn.cfg holds "name|host|port"; "3 " names are 3D servers.
#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
typedef int (__cdecl *CF)(const char*,const char*,int);
typedef void (__cdecl *RF)(void);
static FILE*f; static volatile LONG nex;
#include <stdarg.h>
static void __cdecl myprintf(const char*fmt,...){va_list a;va_start(a,fmt);fprintf(f,"con: ");vfprintf(f,fmt,a);fputc('\n',f);fflush(f);va_end(a);}
static void hook(void*at,void*to){DWORD o;VirtualProtect(at,5,PAGE_EXECUTE_READWRITE,&o);unsigned char*b=at;b[0]=0xE9;*(int*)(b+1)=(char*)to-(char*)at-5;VirtualProtect(at,5,o,&o);FlushInstructionCache(GetCurrentProcess(),at,5);}
static LONG CALLBACK veh(PEXCEPTION_POINTERS e){
  if(InterlockedIncrement(&nex)<40){fprintf(f,"exc %08lx at %p tid %lu\n",e->ExceptionRecord->ExceptionCode,e->ExceptionRecord->ExceptionAddress,GetCurrentThreadId());fflush(f);}
  return EXCEPTION_CONTINUE_SEARCH;}
static DWORD WINAPI go(LPVOID x){
  f=fopen("Z:\\home\\claude\\w512\\inj\\conn.log","a");
  char cfg[512]="3 Seihai Test|127.0.0.1|14800";
  FILE*c=fopen("Z:\\home\\claude\\w512\\inj\\conn.cfg","r"); if(c){fgets(cfg,sizeof cfg,c);fclose(c);}
  char *n=strtok(cfg,"|\r\n"),*h=strtok(0,"|\r\n"),*p=strtok(0,"|\r\n");
  HMODULE m=0; CF fn=0; RF run=0;
  HANDLE sn=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());MODULEENTRY32 me={sizeof me};
  for(BOOL ok=Module32First(sn,&me);ok;ok=Module32Next(sn,&me)){FARPROC a=GetProcAddress(me.hModule,"connectToGraalServer");
    if(a){m=me.hModule;fn=(CF)a;run=(RF)GetProcAddress(me.hModule,"runGraal3DEngine");}}
  fprintf(f,"=== conn4 tid %lu eng %p connect %p run %p\n",GetCurrentThreadId(),m,fn,run);fflush(f);
  AddVectoredExceptionHandler(1,veh); hook((void*)0x1000a220,myprintf);
  if(!fn||!run){fclose(f);return 0;}
  int r=fn(n,h,atoi(p)); fprintf(f,"connect returned %d flag3d=%d\n",r,*(unsigned char*)0x10406d91);fflush(f);
  Sleep(3000);
  for(int i=0;i<3000;i++){ if(i%100==0){fprintf(f,"frame %d\n",i);fflush(f);} run(); Sleep(15);} 
  fprintf(f,"done\n");fclose(f);return 0;}
BOOL WINAPI DllMain(HINSTANCE i,DWORD r,LPVOID x){if(r==DLL_PROCESS_ATTACH)CreateThread(0,0,go,0,0,0);return TRUE;}
