#include <IUtil.h>
#include <IEnums.h>
#include <cstdio>
#include <cstring>
int main(){
  struct {const char*tok;int id;const char*str;} c[]={
   {"G3D22067",CLVER_5_07,"5.07"},{"G3D14097",CLVER_5_12,"5.12"},{"G3D15010",CLVER_5_24,"5.24"},
   {"G3D26090",CLVER_5_31x,"5.31x"},{"G3D3007A",CLVER_6_015,"6.015"},{"G3D0511C",CLVER_6_037_LINUX,"6.037 (Linux)"},
   {"G3D2204D",CLVER_WORLDS,"Graal Worlds"},{"GNW28015",CLVER_2_31,"2.31"},{"GNW03081",-1,nullptr}};
  int bad=0;
  for(auto&x:c){int id=getVersionID(CString(x.tok)); const char*s=getVersionString(CString(x.tok),PLTYPE_CLIENT);
    printf("%s -> %d (%s)\n",x.tok,id,s?s:"null");
    if(x.id>=0 && (id!=x.id || !s || strcmp(s,x.str))) {bad++;puts("  MISMATCH");}}
  printf("order: 5_12=%d 5_24=%d 5_31x=%d 6_015=%d 2_14=%d\n",CLVER_5_12,CLVER_5_24,CLVER_5_31x,CLVER_6_015,CLVER_2_14);
  if(!(CLVER_5_12<CLVER_5_24 && CLVER_5_24<CLVER_5_31x && CLVER_5_24>CLVER_2_14 && CLVER_5_24<CLVER_6_015)) bad++;
  printf("%s\n",bad?"FAIL":"OK"); return bad;}
