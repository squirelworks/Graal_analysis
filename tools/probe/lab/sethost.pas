program sethost;
{ sethost OLD NEW : lab-only helper for the 1998 Graal betas under Wine.
  Finds every edit control whose text is OLD (the greyed-out dialog server box), enables it and
  sets its text to NEW. The exe itself is not touched (the betas check their own checksum). }
{$mode objfpc}{$apptype console}
uses windows, messages;

var OldT, NewT: AnsiString; Hits: Integer = 0;

function Child(h: HWND; l: LPARAM): BOOL; stdcall;
var buf: array[0..255] of AnsiChar;
begin
  buf[0] := #0;
  SendMessageA(h, WM_GETTEXT, 255, LPARAM(@buf));
  if AnsiString(PAnsiChar(@buf)) = OldT then
  begin
    EnableWindow(h, True);
    SendMessageA(h, WM_SETTEXT, 0, LPARAM(PAnsiChar(NewT)));
    Inc(Hits);
  end;
  Result := True;
end;

function Top(h: HWND; l: LPARAM): BOOL; stdcall;
begin
  EnumChildWindows(h, @Child, 0);
  Result := True;
end;

begin
  OldT := ParamStr(1); NewT := ParamStr(2);
  EnumWindows(@Top, 0);
  WriteLn('sethost: ', Hits, ' edit(s) set');
  if Hits = 0 then Halt(1);
end.
