# The 6.01 built-in library, from its registration tables

Date: 2026-11-20. Evidence: **[bin]** (a decompiler read and byte read of the Linux 6.01r1 x64
client, build stamp Sep 18 2011, on the lab host A; no client run). Only names, types and
grouping are given here. The developers' descriptions that some rows carry are not copied.

## How the client registers its built-ins

At start-up the 6.x client fills its script library from static tables, one row per built-in.
Two routines read them (→ `static-reads-appendix-e-2026-11-20-i.md`):

- **Properties.** Each row has a name, a type letter, a getter, a setter, a description and a flag
  that makes the property writable without a setter.
- **Functions.** Each row has a name, a return-type letter, a parameter signature (one letter per
  parameter), a handler, a description and the fold-241 flag.

A row's name may be stored scrambled (the row says so). Names are unscrambled when they are
registered, and they are matched without regard to letter case.

Each call registers a table either into the **global** registry (names a script can use bare) or
onto a **class**, so that every object of that class has those members. The class here is the
internal class named next to the registration call. That naming is from the code around each call
and is an inference for each class; one class was named by hand (`TGraalVar`, the base of every script
object), and 5 tables are left without a class.

Coverage: every registration call the decompiler lists, except four sites near the end of the
range, whose code was not fetched.

### Type letters

| Letter | Meaning (as used) |
| --- | --- |
| `v` | nothing (return only) |
| `i` | integer |
| `u` | unsigned integer (flag masks such as `enablefeatures`, `showstats`) |
| `d` | number (double) |
| `f` | number (single precision) |
| `b` | boolean |
| `s` | string |
| `o` | object |
| `X` | any further arguments (variable count) |

In the lists below a function is shown as `name(signature) → return`, with `→ v` left out. A
property is shown as `name: type`, marked read-only when it has a getter, no setter and no
writable flag.

## Counts

| Group | Tables | Entries |
| --- | ---: | ---: |
| Global functions | 32 | 314 |
| Global properties | 16 | 123 |
| Class members | 146 tables: 141 on 91 named classes, 5 unnamed | 1,284 |

## Global functions (314)

`addcontrol(o)`, `adddnsentry(ss)`, `addtiledef(ssi)`, `addtiledef2(ssii)`, `adventure_adddesktopicon(sss)`, `adventure_addmenulink(sss)`, `adventure_fileexists(s)` → b, `adventure_fileisfolder(s)` → b, `adventure_filesize(s)` → i, `adventure_getapplicationfolder(i)` → s, `adventure_getbuildtime()` → s, `adventure_getcontrolbinding(ii)` → o, `adventure_geteditaccountnames()` → o, `adventure_geteditnickname()` → s, `adventure_getfilecontent(s)` → s, `adventure_getfilemodtimeglobal(s)` → u, `adventure_getfolder(ssbb)` → o, `adventure_getframetick()` → i, `adventure_getinstallationpath()` → s, `adventure_getmacaddress()` → s, `adventure_getosid()` → s, `adventure_getsystemid(i)` → s, `adventure_getwindowlist()` → o, `adventure_installgraal(sbb)`, `adventure_invokekeyevent(iisi)`, `adventure_invokemouseevent(iiddib)`, `adventure_opendefaultviewer(si)` → b, `adventure_openexternaloptions()` → b, `adventure_openexternalpm(o)` → b, `adventure_openserverlist()`, `adventure_quit()`, `adventure_reconnect()`, `adventure_savegraaloptions()`, `adventure_selectfileselect(s)`, `adventure_selectfilesetfolder(i)`, `adventure_selectfilesetfolderbytext(s)`, `adventure_selectfileshowhiddenfiles(b)`, `adventure_selectpath(s)` → o, `adventure_setaccountname(s)`, `adventure_setallowedportsbind(s)`, `adventure_setallowedsocketsconnect(s)`, `adventure_setallowrecordbyscript(b)`, `adventure_setchat(s)`, `adventure_setcontrolbinding(iii)`, `adventure_setfilemodtime(su)`, `adventure_setfilemodtimeglobal(su)`, `adventure_setframetick(i)`, `adventure_setfullscreen(b)`, `adventure_setgraalcontrolrecreate(b)`, `adventure_setnickname(s)`, `adventure_setpassword(s)`, `adventure_settextedittext(os)`, `adventure_updatemidivolume()`, `adventure_updatemp3volume()`, `adventure_updateradiovolume()`, `adventure_uploadfile(s)`, `aindexof(do)` → i, `arccos(d)` → d, `arcsin(d)` → d, `attachplayertoobj(ii)`, `base64decode(s)` → s, `base64encode(s)` → s, `boxcontains(ss)` → b, `boxcontainsvector(ss)` → b, `boxintersect(ss)` → s, `boxoverlaps(ss)` → b, `boxscale(ss)` → s, `callnpc(iX)`, `callweapon(iX)`, `checksum(s)` → d, `clearemptyglobalvars()`, `contains(ss)` → b, `convertstringtotime(ss)` → d, `converttimetostring(d)` → s, `copystrings(ss)`, `cursoroff()`, `cursoron()`, `decompressfile(sssi)` → b, `degtorad(d)` → d, `deletefile(s)` → b, `detachplayer()`, `disabledefmovement()`, `disablemap()`, `disablepause()`, `disableselectweapons()`, `disableweapons()`, `downloadfiletofolder(ss)`, `echo(s)`, `enabledefmovement()`, `enablefeatures(u)`, `enablemap()`, `enablepause()`, `enableselectweapons()`, `enableweapons()`, `escapefilename(s)` → s, `escapestring(s)` → s, `escapestringkeepnewline(s)` → s, `explodebomb(i)`, `extractfilebase(s)` → s, `extractfileext(s)` → s, `extractfilename(s)` → s, `extractfilepath(s)` → s, `fileexists(s)` → b, `filesize(s)` → i, `fileupdate(s)` → b, `fileupdateignore(s)`, `findani(s)` → o, `findfiles(si)` → o, `findlevel(s)` → o, `findnearestplayer(dd)` → o, `findnearestplayers(dd)` → o, `findnpcbyid(i)` → o, `findpathinarray(oooooiii)` → o, `findplayer(s)` → o, `findplayerbycommunityname(s)` → o, `findplayerbyid(i)` → o, `findweapon(s)` → o, `format2(so)` → s, `formattimestring(sd)` → s, `freeallresources()`, `freefileresources(s)`, `freezeplayer(d)`, `getascii(s)` → i, `getbasepackage()` → o, `getboxcenter(s)` → s, `getcallstack()` → o, `getdisplaydevicelist()` → o, `getdownloadedupdatepackagesize()` → i, `getdownloadingpackage()` → o, `getdownloadingpackagescount()` → i, `getdownloadprogress(s)` → d, `getextension(s)` → s, `getfilemodtime(s)` → u, `gethttprequest(sis)` → o, `getimgheight(s)` → i, `getimgpixel(sii)` → o, `getimgwidth(s)` → i, `getkeycode(s)` → i, `getloginaccountname()` → s, `getmapx(s)` → i, `getmapy(s)` → i, `getmemoryusage()` → i, `getmusicfilename()` → s, `getnearestplayer(dd)` → i, `getnearestplayers(dd)` → o, `getpackagesdownloadcomplete()` → b, `getpackagesdownloaded()` → b, `getplatform()` → s, `getplayerlisticons()` → o, `getpremiumoption()` → s, `getresolutionlist()` → o, `getscriptaccessfile(sb)` → s, `getservername()` → s, `getstringkeys(s)` → o, `gettextheight(dss)` → i, `gettextwidth(dsss)` → i, `gettileset()` → s, `gettilesettype()` → i, `gettotalupdatepackagesize()` → i, `getupdatepackage(s)` → o, `getz(dd)` → d, `graalcontrolhasfocus(b)` → b, `hideplayer(d)`, `hidesword(d)`, `hitnpc(iddd)`, `hitobjects(ddd)`, `hitplayer(iddd)`, `isadminguild(s)` → b, `isclassloaded(s)` → b, `iscursoron()` → b, `isdemoversion()` → b, `isdownloading(s)` → b, `isdownloadingfiles()` → b, `isfullscreenmode()` → b, `isimgpixeltransparent(sii)` → b, `isimgrectangletransparent(siiii)` → b, `ismusicplaying()` → b, `isobject(s)` → b, `isofflinemode()` → b, `ispremiumversion()` → b, `issoundplaying(s)` → b, `keydown(i)` → b, `keydown2(ib)` → b, `keydown2global(ib)` → b, `keydownglobal(i)` → b, `keyname(i)` → s, `keyname2(i)` → s, `lay2(sdd)`, `loadclass(s)`, `loadmap(s)`, `loadtranslation(s)`, `lowercase(s)` → s, `makescreenshot2(sidddii)`, `makescreenshotfull(sii)`, `makescreenshotgame(siii)`, `matrixcreate(ss)` → s, `matrixcreatefromeuler(s)` → s, `matrixmulpoint(ss)` → s, `matrixmultiply(ss)` → s, `matrixmulvector(ss)` → s, `md5(s)` → s, `noplayerkilling()`, `onwall(dd)` → b, `onwall2(dddd)` → b, `onwater(dd)` → b, `onwater2(dddd)` → b, `opengraalurl(s)`, `openurl(s)`, `openurl2(sii)`, `play(s)`, `play2(sddd)`, `playlooped(s)`, `playlooped2(sddd)`, `popdialog()`, `preloadanimation(s)`, `preloadimage(sb)`, `pushdialog(o)`, `putleaps(idd)`, `radtodeg(d)` → d, `randomstring(s)` → s, `removeescapesfromfilename(s)` → s, `removetiledefs(s)`, `replaceani(ss)`, `requestfiledeletion(s)`, `requestfilerename(ss)`, `requestfilesmove(ss)`, `requesthttp(sis)` → o, `requesttext(ss)`, `requesturl(s)` → o, `requesturlasgamefile(ssub)` → o, `resetfocus()`, `resetimageanimation(s)`, `resolvehost(s)` → s, `rotationadd(ss)` → s, `rotationaddeuler(ss)` → s, `rotationfromeuler(s)` → s, `rotationsub(ss)` → s, `rotationtoeuler(s)` → s, `rungarbagecollector()`, `savelog(s)`, `say(i)`, `say2(s)`, `screenx(dd)` → i, `screeny(dd)` → i, `selectfilefordownload(s)`, `selectfileforupload()`, `sendrpgmessage(s)`, `sendtext(ssX)`, `sendtorc(s)`, `serverwarp(s)`, `setani(ss)`, `setbeltcolor(s)`, `setcoatcolor(s)`, `setcontentcontrol(o)`, `setcursor2(s)`, `seteffect(dddd)`, `setfocus(dd)`, `setgender(s)`, `sethead(s)`, `setletters(s)`, `setminimap(ssdd)`, `setmusicvolume(dd)`, `setplayerdir(s)`, `setshield(si)`, `setshoecolor(s)`, `setshootparams(s)`, `setskincolor(s)`, `setsleevecolor(s)`, `setsoundpitch(sd)`, `setsoundpitchbynote(sss)`, `setspritesimage(s)`, `setstatusimage(s)`, `setstreamingmode(s)` → b, `setsword(si)`, `showstats(u)`, `spyfire(ii)`, `startrecordvideo()` → b, `stopmidi()`, `stopmusic()`, `stoprecordvideo()` → b, `stopsound(s)`, `stopsounds(b)`, `strcmp(ss)` → i, `strequals(ss)` → b, `supportsopenglshader()` → b, `switchtodirectx()`, `switchtoopengl()`, `takeplayercarry()`, `takeplayerhorse()`, `testplayer(dd)` → i, `trace(s)`, `triggeraction(ddsX)`, `triggerserver(ss)`, `updateboard(iiii)`, `updateratingdeviation(dd)` → d, `updateratings(o)` → o, `updateterrain()`, `uploadfile(s)`, `uppercase(s)` → s, `urldecode(s)` → s, `urlencode(s)` → s, `vectoradd(ss)` → s, `vectorcross(ss)` → s, `vectordist(ss)` → d, `vectordot(ss)` → d, `vectorlen(s)` → d, `vectornormalize(s)` → s, `vectororthobasis(s)` → s, `vectorscale(sd)` → s, `vectorsub(ss)` → s, `worldx(dd)` → d, `worldy(dd)` → d, `wraptext(iss)` → o, `wraptext2(idss)` → o

## Global properties (123)

`$pref::audio::midivolume`: i, `$pref::audio::mp3volume`: i, `$pref::audio::radiovolume`: i, `$pref::audio::reversestereo`: b, `$pref::audio::sfxvolume`: i, `$pref::capture::allowbyscript`: b, read-only, `$pref::capture::area`: s, `$pref::capture::audiobitrate`: i, `$pref::capture::disabledaynight`: b, `$pref::capture::format`: s, `$pref::capture::fps`: i, `$pref::capture::hideinterface`: b, `$pref::capture::recordaudio`: b, `$pref::capture::showmouse`: b, `$pref::capture::size`: s, `$pref::capture::videobitrate`: i, `$pref::graal::allowglobalpms`: b, `$pref::graal::automapping`: b, `$pref::graal::cachefilenames`: b, `$pref::graal::defaultfontname`: s, `$pref::graal::defaultfontsize`: i, `$pref::graal::displaytrayicon`: b, `$pref::graal::docktodesktop`: b, `$pref::graal::dontsavepasswords`: b, `$pref::graal::dontsavepms`: b, `$pref::graal::language`: s, `$pref::graal::limitnicknames`: b, `$pref::graal::loadbuddylistfromserver`: b, `$pref::graal::nicknamelimit`: i, `$pref::graal::nomassmessages`: b, `$pref::graal::notoalls`: b, `$pref::graal::showyourselfonbuddylists`: b, `$pref::video::defaultguistyle`: s, `$pref::video::fullscreenmode`: s, `$pref::video::resolution`: i, `$pref::video::screenshotformat`: s, `$pref::video::windowmode`: s, `allfeatures`: i, read-only, `allowedimageanimations`: s, `allowloginreconnect`: b, `allplayerscount`: i, read-only, `allrenderobjecttypes`: i, read-only, `allstats`: i, read-only, `canspin`: b, read-only, `carriesblackstone`: b, read-only, `carriesbush`: b, read-only, `carriesnpc`: b, read-only, `carriessign`: b, read-only, `carriesstone`: b, read-only, `carriesvase`: b, read-only, `disableactionprojectile`: b, `disableactionprojectile2`: b, `disablenpchits`: b, `disablenpconnpchits`: b, `downloadfile`: s, read-only, `downloadpos`: i, read-only, `downloadsize`: i, read-only, `drawallinsidenpcs`: b, `emoticonchar`: s, read-only, `enableganimoviereposition`: b, `focusx`: d, read-only, `focusy`: d, read-only, `ghostsnear`: b, read-only, `graalplugincookie`: s, read-only, `graalversion`: d, read-only, `gravity`: d, `installedlanguages`: s, read-only, `isapplicationactive`: b, read-only, `iscarrying`: b, read-only, `isfocused`: b, read-only, `isgraalplugin`: b, read-only, `isleader`: b, read-only, `isonmap`: b, read-only, `isopengl`: b, read-only, `isrecordingvideo`: b, read-only, `isstreamingvideo`: s, read-only, `jpegquality`: u, `lastdownloadfile`: s, read-only, `leftmousebutton`: b, read-only, `leftmousebuttonglobal`: b, read-only, `levelorgx`: d, read-only, `levelorgy`: d, read-only, `lighteffectsenabled`: b, `loadingscreenenabled`: b, `middlemousebutton`: b, read-only, `middlemousebuttonglobal`: b, read-only, `mousebuttons`: i, read-only, `mousebuttonsglobal`: i, read-only, `mousescreenx`: i, `mousescreeny`: i, `mousewheeldelta`: i, read-only, `mousex`: d, `mousey`: d, `musiclen`: f, read-only, `musicpos`: f, read-only, `particleeffectsenabled`: b, `rightmousebutton`: b, read-only, `rightmousebuttonglobal`: b, read-only, `screenheight`: i, read-only, `screenpixelscale`: f, read-only, `screenwidth`: i, read-only, `scriptedcontrols`: b, read-only, `scriptedplayerlist`: b, read-only, `scriptlogwritetoreadonly`: b, `selectedlistplayers`: o, `selectedsword`: i, `selectedweapon`: i, `servername`: s, read-only, `serverstartconnect`: s, `serverstartparams`: s, `shotbybaddy`: b, read-only, `shotbyplayer`: b, read-only, `showterraingrid`: b, `spritesimage`: s, `statusimage`: s, `timevar`: i, read-only, `timevar2`: d, read-only, `wasshooted`: b, read-only, `watercolorflags`: i, `waterheight`: d, `weapons`: o, read-only, `weaponsenabled`: b, `weathereffectsenabled`: b

## Members by class

### Array

Functions: `array(X)` → o, `push(X)` → i, `splice(X)`, `unshift(X)` → i

Properties: `length`: i, read-only

### Color

Functions: `color(X)` → o, `setrgb(i)`

### Date

Functions: `date(X)` → o

### GuiAccordionCtrl

Functions: `addrow(i)` → o, `clearrows()`, `insertrow(ii)` → o, `removerow(i)`, `removerowbyid(i)`

Properties: `backgroundimage`: s

### GuiAccordionEntry

Properties: `id`: i, `image`: s

### GuiAccountPasswordCtrl

Functions: `applypassword()`, `clearpassword()`, `isempty()` → b, `setpasswordofaccount(s)`

### GuiAnimationCtrl

Functions: `getselectedrow()` → i, `rowcount()` → i, `setselectedrow(i)`

Properties: `animationtime`: d, `selectedrow`: i

### GuiArrayCtrl

Properties: `allowmultipleselections`: b

### GuiBitmapBorderCtrl

Properties: `tile`: b

### GuiBitmapButtonCtrl

Functions: `setbitmap(si)`

Properties: `mouseoverbitmap`: s, `normalbitmap`: s, `pressedbitmap`: s

### GuiBitmapCtrl

Functions: `setbitmap(s)`, `setvalue(ii)`

Properties: `bitmap`: s, `bitmaprectangle`: s, `fullbitmap`: b, `tile`: b, `wrap`: b

### GuiBrowserCtrl

Properties: `url`: s

### GuiButtonBaseCtrl

Functions: `gettext()` → s, `settext(s)`

Properties: `buttontype`: s, `checked`: b, `groupnum`: i, `text`: s

### GuiButtonCtrl

Functions: `seticonsize(ii)`

Properties: `stylesection`: s

### GuiContextMenuCtrl

Functions: `close()`, `isopen()` → b, `open(ii)`, `openatmouse()`

Properties: `maxpopupheight`: i, `profile`: o, `rows`: o, read-only, `scrollprofile`: o, `textprofile`: o, `width`: i

### GuiControl

Functions: `addcontrol(o)`, `bringtofront()`, `clearcontrols()`, `createanimation()` → o, `destroy()`, `findcontrol(s)` → o, `getparent()` → o, `globaltolocalcoord(s)` → s, `hide()`, `isactuallyvisible()` → b, `isfirstresponder()` → b, `ismouselocked(i)` → b, `localtoglobalcoord(s)` → s, `makefirstresponder(b)`, `mouselock(i)`, `mouseunlock(i)`, `mouseunlockall()`, `pushtoback()`, `repaint()`, `resize(iiii)`, `show()`, `showtop()`, `sortcontrols()`, `startdrag()`, `stopanimations()`, `stopinoutanimations()`, `tabfirst()` → o

Properties: `acceptdropfiles`: b, `active`: b, `alpha`: f, `areaclickpriority`: i, `awake`: b, read-only, `bitmapcache`: b, `blue`: f, `bounds`: s, `canmove`: b, `canresize`: b, `clientextent`: s, `clientheight`: i, `clientwidth`: i, `clipchildren`: b, `clipmove`: b, `cliptobounds`: b, `color`: s, `cursor`: s, `editing`: b, `extent`: s, `fastchildrender`: b, `firstresponder`: o, `flickerbasetime`: f, `flickering`: b, `flickertime`: f, `green`: f, `height`: i, `hint`: s, `hinttime`: f, `horizsizing`: s, `isinanimation`: b, `isininoutanimation`: b, `lockmousedown`: b, `minextent`: s, `minsize`: s, `mode`: i, `parent`: o, read-only, `position`: s, `profile`: o, `red`: f, `resizeheight`: b, `resizewidth`: b, `rotation`: f, `rotationcenter`: s, `scrolllinex`: i, `scrollliney`: i, `showhint`: b, `style`: s, `useownprofile`: b, `vertsizing`: s, `visible`: b, `width`: i, `x`: i, `y`: i

### GuiControlProfile

Functions: `gettextheight()` → i, `gettextwidth(s)` → i, `preloadfont()`

Properties: `align`: s, `autosizeheight`: b, `autosizewidth`: b, `backgroundinset`: s, `bitmap`: s, `border`: i, `bordercolor`: s, `bordercolorhl`: s, `bordercolorna`: s, `borderthickness`: i, `boxextent`: s, `cankeyfocus`: b, `cursorcolor`: s, `fillcolor`: s, `fillcolorhl`: s, `fillcolorna`: s, `fillonlynonchildarea`: b, `focusonshow`: b, `fontcolor`: s, `fontcolorhl`: s, `fontcolorlink`: s, `fontcolorlinkhl`: s, `fontcolorna`: s, `fontcolorsel`: s, `fontsize`: i, `fontstyle`: s, `fontstylecontrolwords`: s, `fontstyleidentifiers`: s, `fontstylenumbers`: s, `fontstylestrings`: s, `fonttype`: s, `gradientcolor`: s, `justify`: s, `linespacing`: i, `modal`: b, `mouseoverselected`: b, `numbersonly`: b, `opaque`: b, `overridestylefont`: b, `returntab`: b, `shadowcolor`: s, `shadowoffset`: s, `soundbuttondown`: s, `soundbuttonover`: s, `tab`: b, `textgradient`: b, `textoffset`: s, `textshadow`: b, `transparency`: f

### GuiDrawingPanel

Functions: `clearall()`, `clearrectangle(iiii)`, `drawcurve(iiiiiif)`, `drawimage(iis)`, `drawimagerectangle(iisiiii)`, `drawimagestretched(iiiisiiii)`, `drawline(iiiif)`, `drawobject(iio)`, `drawtext(iis)`, `filterrectangle(iiiis)` → b, `maskimage(iiss)`, `saveimage(s)`, `saveimage2(si)`

Properties: `availablefilters`: o, read-only, `parth`: i, read-only, `partw`: i, read-only, `partx`: i, read-only, `party`: i, read-only

### GuiFlash

Functions: `loadmovie(sbd)`, `playmovie()`, `restartmovie()`, `setbackgroundalpha(f)`, `setlooping(b)`, `stopmovie()`

Properties: `backgroundalpha`: d, `downloadwebfiles`: b, `flash`: o, read-only, `hideonoverlap`: b, `loopmovie`: b, `messageonoverlap`: s, `moviename`: s

### GuiFrameSetCtrl

Functions: `getcolumncount()` → i, `getcolumnoffset(i)` → i, `getrowcount()` → i, `getrowoffset(i)` → i, `setcolumncount(i)`, `setcolumnoffset(ii)`, `setrowcount(i)`, `setrowoffset(ii)`

Properties: `autobalance`: b, `columncount`: i, `fudgefactor`: i, `rowcount`: i

### GuiGraalCtrl

Properties: `isrendering`: b

### GuiMenuCtrl

Functions: `addmenu(s)` → o, `clearmenus()`, `findmenu(s)` → o, `removemenu(s)`, `seticonsize(ii)`

Properties: `iconheight`: i, read-only, `iconwidth`: i, read-only

### GuiMLTextCtrl

Functions: `addtext(sb)`, `deselecttext()`, `findtext(si)` → i, `findtextat(sii)` → i, `getcolumnandlineofposition(i)` → s, `getcursorline()` → i, `getline(i)` → s, `getlinecount()` → i, `getlines()` → o, `getselectedlength()` → i, `getselectedposition()` → i, `gettext()` → s, `reflow()`, `replacetext(ssi)` → i, `scrolltobottom()`, `scrolltoline(i)`, `scrolltoposition(i)`, `scrolltotag(s)`, `scrolltotop()`, `selecttext(ii)` → b, `setcursorcolumnandline(ii)`, `setlines(o)`, `settext(s)`, `trimhorizontally()`

Properties: `allowedtags`: s, `alpha`: f, `cursorposition`: i, `deniedsound`: s, `disallowedtags`: s, `htmlcompatibility`: b, `htmllinks`: b, `maxchars`: i, `parsetags`: b, `plaintext`: s, `syntaxhighlighting`: b, `text`: s, `urlbase`: s, `wordwrap`: b

### GuiMLTextEditCtrl

Properties: `autoindenting`: b, `showcursor`: b, `tabspaces`: i, `undostacksize`: i

### GuiPMCtrl

Functions: `addpm(o)`, `clear()`, `showpm(o)`

### GuiPMEditCtrl

Functions: `clear()`, `sendmasspm(o)`, `sendpm(o)`

### GuiPMHistoryCtrl

Functions: `showhistory(o)`

### GuiPopUpEditCtrl

Functions: `addtext(si)`, `findtext(s)` → i, `forceclose()`, `forceonaction()`, `getselected()` → i, `rowcount()` → i, `setselected(i)`, `setselectedbytext(s)`

Properties: `maxpopupheight`: i

### GuiPopUpMenuCtrl

Functions: `addtext(si)`, `findtext(s)` → i, `forceclose()`, `forceonaction()`, `getselected()` → i, `rowcount()` → i, `setselected(i)`, `setselectedbytext(s)`

Properties: `rows`: o, read-only

### GuiProgressCtrl

Properties: `progress`: f

### GuiScrollCtrl

Functions: `scrolldelta(ii)`, `scrollrectvisible(iiii)`, `scrollto(ii)`, `scrolltobottom()`, `scrolltotop()`

Properties: `childmargin`: s, `constantthumbheight`: b, `hscrollbar`: s, `scrollpos`: s, `tile`: b, `vscrollbar`: s, `wheelscrolllines`: i, `willfirstrespond`: b

### GuiShowImgCtrl

Properties: `ani`: s, `dir`: i, `layer`: i, `offsetx`: i, `offsety`: i

### GuiSliderCtrl

Properties: `range`: s, `ticks`: i, `value`: f

### GuiSlideShowCtrl

Functions: `addrow(i)` → o, `clearrows()`, `insertrow(ii)` → o, `removerow(i)`, `removerowbyid(i)`

Properties: `isendless`: b, `overlayimage`: s, `scrollonvisible`: b

### GuiSlideShowEntry

Properties: `id`: i, `image`: s

### GuiStartMenuCtrl

Functions: `gettext()` → s, `settext(s)`

Properties: `text`: s, `width`: i

### GuiStretchCtrl

Properties: `clientextent`: s, `clientheight`: i, `clientwidth`: i

### GuiTabCtrl

Functions: `addrow(is)` → o, `clearrows()`, `clearselection()`, `findtext(s)` → i, `findtextid(s)` → i, `getrowatpoint(ii)` → i, `getrowidatpoint(ii)` → i, `getrownumbyid(i)` → i, `getselectedid()` → i, `getselectedrow()` → i, `getselectedtext()` → s, `insertrow(iis)` → o, `isidselected(i)` → b, `isrowselected(i)` → b, `makevisible(i)`, `makevisiblebyid(i)`, `removerow(i)`, `removerowbyid(i)`, `rowcount()` → i, `seticonsize(ii)`, `setselectedbyid(i)`, `setselectedrow(i)`

Properties: `iconheight`: i, read-only, `iconwidth`: i, read-only, `leveling`: i, `maxvisibletabs`: i, read-only, `overlapwidth`: i, `selected`: o, read-only, `tabwidth`: i

### GuiTabCtrlEntry

Functions: `gettext()` → s, `settext(s)`

Properties: `hint`: s, `id`: i, `text`: s

### GuiTextCtrl

Functions: `gettext()` → s, `settext(s)`

Properties: `stylesection`: s, `text`: s

### GuiTextEditCtrl

Functions: `setselection(ii)`, `undo()`

Properties: `deniedsound`: s, `historysize`: i, `inputtype`: s, `password`: b, `showcursor`: b, `tabcomplete`: b, `text`: s

### GuiTextEditSliderCtrl

Properties: `allowedit`: s, `format`: s, `increment`: d, `range`: s, `value`: d

### GuiTextListCtrl

Functions: `addrow(is)` → o, `clearrows()`, `clearselection()`, `findtext(s)` → i, `findtextid(s)` → i, `getrowatpoint(ii)` → i, `getrowidatpoint(ii)` → i, `getrownumbyid(i)` → i, `getselectedid()` → i, `getselectedids()` → o, `getselectedrow()` → i, `getselectedrows()` → o, `getselectedtext()` → s, `insertrow(iis)` → o, `isidselected(i)` → b, `isrowselected(i)` → b, `makevisible(i)`, `makevisiblebyid(i)`, `removerow(i)`, `removerowbyid(i)`, `rowcount()` → i, `seticonsize(ii)`, `setrowactivebyid(ib)`, `setrowbyid(is)`, `setselectedbyid(i)`, `setselectedbyids(s)`, `setselectedbytext(s)`, `setselectedrow(i)`, `setselectedrows(s)`, `sort()`

Properties: `clipcolumntext`: b, `columns`: s, `enumerate`: b, `fitparentwidth`: b, `groupsortorder`: s, `iconheight`: i, read-only, `iconwidth`: i, read-only, `resizecell`: b, `selected`: o, read-only, `selectedid`: i, `selectedrow`: i, `sortcolumn`: i, `sortmode`: s, `sortorder`: s

### GuiTextListEntry

Functions: `gettext()` → s, `settext(s)`

Properties: `active`: b, `extent`: s, read-only, `flickering`: b, `flickertime`: f, `height`: i, read-only, `hint`: s, `id`: i, `image`: i, `position`: s, read-only, `profile`: o, `selectedimage`: i, `sortgroup`: i, `sortvalue`: i, `text`: s, `useownprofile`: b, `width`: i, read-only, `x`: i, read-only, `y`: i, read-only

### GuiTilesCtrl

Functions: `loadtilemap(ss)` → o, `loadtilemapxml(s)` → o

Properties: `camerabounds`: s, `cameraposition`: s, `camerasize`: s, `tilemap`: o, read-only

### GuiTreeViewCtrl

Functions: `clearrows()`, `getnodeat(ii)` → o, `getselectednode()` → o, `seticonsize(ii)`, `sort()`

Properties: `boxwidth`: i, `clipcolumntext`: b, `columns`: s, `expandondoubleclick`: b, `firstlinevisible`: b, `fitparentwidth`: b, `groupsortorder`: s, `nodes`: o, read-only, `sortmode`: s, `sortorder`: s, `statuswidth`: i

### GuiTreeViewNode

Functions: `addlines(ob)`, `addnode(s)` → o, `addnodebypath(ss)` → o, `addvars(ob)`, `clearnodes()`, `destroy()`, `getfullname(s)` → s, `getnode(s)` → o, `getnodebypath(ss)` → o, `select()`

Properties: `expanded`: b, `expandedimage`: i, `expandedselectedimage`: i, `extent`: s, read-only, `height`: i, read-only, `hint`: s, `image`: i, `level`: i, read-only, `name`: s, `parent`: o, read-only, `position`: s, read-only, `profile`: o, `selectedimage`: i, `sortgroup`: i, `sortvalue`: i, `text`: s, `useownprofile`: b, `visible`: b, `width`: i, read-only, `x`: i, read-only, `y`: i, read-only

### GuiWindowCtrl

Functions: `isactivewindow()` → b

Properties: `canclose`: b, `canmaximize`: b, `canminimize`: b, `clientrelative`: b, `closequery`: b, `destroyonhide`: b, `dockable`: b, `extent`: s, `externalwindow`: o, read-only, `isexternal`: b, `maximized`: b, `minimized`: b, `tile`: b

### Key

Functions: `addlistener(o)`, `getascii()` → i, `getcode()` → i, `isaccessible()` → b, `isdown(i)` → b, `istoggled(i)` → b, `removelistener(o)` → b

Properties: `backspace`: i, read-only, `capslock`: i, read-only, `control`: i, read-only, `deletekey`: i, read-only, `down`: i, read-only, `end`: i, read-only, `enter`: i, read-only, `escape`: i, read-only, `home`: i, read-only, `insert`: i, read-only, `left`: i, read-only, `pgdn`: i, read-only, `pgup`: i, read-only, `right`: i, read-only, `shift`: i, read-only, `space`: i, read-only, `tab`: i, read-only, `up`: i, read-only

### Math

Functions: `abs(d)` → d, `atan(d)` → d, `atan2(dd)` → d, `ceil(d)` → d, `cos(d)` → d, `floor(d)` → i, `log(d)` → d, `max(dd)` → d, `min(dd)` → d, `pow(dd)` → d, `random()` → d, `round(d)` → d, `sin(d)` → d, `sqrt(d)` → d, `tan(d)` → d

Properties: `pi`: d, read-only, `sqrt1_2`: d, read-only, `sqrt2`: d, read-only

### MovieClip

Functions: `attachmovie(X)` → o, `clearinterval(o)`, `createemptymovieclip(si)` → o, `duplicatemovieclip(X)` → o, `getbounds(o)` → o, `getbytesloaded()` → i, `getbytestotal()` → i, `getcolor()` → s, `getdepth()` → i, `getinstanceatdepth(i)` → o, `getlayer(s)` → o, `getnexthighestdepth()` → i, `getproperty(i)` → s, `gettimer()` → i, `globaltolocal(o)`, `gotoandplay(X)`, `gotoandstop(X)`, `hittest(X)` → b, `localtoglobal(o)`, `nextframe()`, `play()`, `prevframe()`, `removelayer(s)`, `removemovieclip()`, `setcolor(s)`, `setinterval(osi)` → o, `setmask(o)`, `setproperty(is)`, `startdrag()`, `stop()`, `stopdrag()`, `swapdepths(s)`, `unloadmovie()`, `updateafterevent()`

Properties: `_level0`: o, read-only, `_name`: s, read-only, `_parent`: o, read-only, `_root`: o, read-only, `_rotation`: f, `_visible`: b, `_x`: f, `_xmouse`: f, read-only, `_xscale`: f, `_y`: f, `_ymouse`: f, read-only, `_yscale`: f, `alpha`: f, `blue`: f, `frame`: i, `framecount`: i, read-only, `green`: f, `height`: f, read-only, `key`: o, read-only, `layerdepths`: o, read-only, `layernames`: o, read-only, `looping`: b, `math`: o, read-only, `objectname`: s, `objectnames`: o, read-only, `playing`: b, `red`: f, `stage`: o, read-only, `width`: f, read-only

### MRandomGenerator

Functions: `destroy()`, `randfloat()` → f, `randint()` → u

Properties: `seed`: u

### Sound

Functions: `sound(X)` → o

### Stage

Functions: `stage(X)` → o

Properties: `height`: d, read-only, `width`: d, read-only

### String

Functions: `string(X)` → o

### TActionScriptVar

Functions: `destroy()`

### TCallStackEntry

Properties: `scriptcallobject`: o, read-only

### TControlBinding

Properties: `action`: i, read-only, `keycode`: i, read-only, `keytext`: s, read-only, `slot`: i, read-only

### TDrawableObject

Properties: `layer`: i, read-only

### TDrawingPanel

Functions: `clearall()`, `clearrectangle(iiii)`, `drawcurve(iiiiiif)`, `drawimage(iis)`, `drawimagerectangle(iisiiii)`, `drawimagestretched(iiiisiiii)`, `drawline(iiiif)`, `drawobject(iio)`, `drawtext(iis)`, `filterrectangle(iiiis)` → b, `maskimage(iiss)` → b, `saveimage(s)`, `saveimage2(si)`

Properties: `availablefilters`: o, read-only, `height`: i, read-only, `isclear`: b, read-only, `parth`: i, read-only, `partw`: i, read-only, `partx`: i, read-only, `party`: i, read-only, `profile`: o, `useownprofile`: b, `width`: i, read-only

### TFrameDetail

Properties: `bordercolor`: s, `borderenable`: s, `bordermovable`: s, `borderwidth`: i, `minextent`: s

### TGaniObject

Functions: `getimageforsprite(o)` → s, `getsprite(s)` → o, `getspriteforspritepos(o)` → o, `setcoloreffect(dddd)`, `seteffectmode(i)`

Properties: `alpha`: f, `ani`: o, `aniparams`: s, read-only, `anistep`: i, read-only, `attachedtoobject`: o, read-only, `attachid`: i, read-only, `attachtype`: i, read-only, `attr`: o, read-only, `blue`: f, `body`: s, `bodyimg`: s, `colors`: o, read-only, `dir`: i, `gmap`: o, read-only, `green`: f, `head`: s, `headimg`: s, `mode`: i, `red`: f, `rotation`: f, `rotationcenter`: s, `shield`: s, `sprite`: i, `stretchx`: f, `stretchy`: f, `sword`: s, `useowncenter`: b, `zoom`: f

### TGraalAni

Functions: `addsprite(i)` → o, `addstep()` → o, `deletesprite(i)`, `deletestep(i)`, `getsprite(i)` → o, `insertstep(i)` → o

Properties: `continuous`: b, `ganitype`: s, read-only, `loop`: b, `movie`: b, `setbackto`: s, `singledirection`: b

### TGraalAniPart

Properties: `attr`: i, `dx`: i, `dy`: i, `param`: i, `sprite`: o

### TGraalAniSound

Properties: `delay`: d, `dx`: d, `dy`: d, `sound`: s

### TGraalAniSprite

Functions: `addattachment()` → o, `deleteattachment(i)`, `insertattachment(i)` → o

Properties: `alpha`: f, `blue`: f, `description`: s, `green`: f, `height`: i, `image`: s, `imagetype`: s, read-only, `mode`: i, `red`: f, `rotation`: f, `spriteindex`: i, `stretchx`: f, `stretchy`: f, `width`: i, `x`: i, `y`: i, `zoom`: f

### TGraalAniStep

Functions: `addpos(i)` → o, `deletepos(ii)`, `insertpos(ii)` → o

Properties: `delay`: d

### TGraalVar (every script object)

Functions: `addarray(o)`, `addarraymember(s)` → o, `addnamedstring(ss)` → o, `cancelevents(s)`, `catchevent(sss)`, `clearemptyvars()`, `clearvars()`, `copyfrom(o)`, `getarraymember(s)` → o, `getdynamicvarnames()` → o, `geteditvarnames()` → o, `getfunctions()` → o, `getstaticvarnames()` → o, `getvarnames()` → o, `hasfunction(s)` → b, `ignoreevent(ss)`, `ignoreevents(s)`, `insertarray(io)`, `isinclass(s)` → b, `join(s)`, `leave(s)`, `loadfolder(si)`, `loadini(s)`, `loadlines(s)`, `loadstring(s)`, `loadvars(s)`, `loadvarsfromarray(o)`, `loadxml(s)`, `loadxmlfromstring(s)`, `objecttype()` → s, `savelines(si)`, `savestring(si)`, `savevars(si)`, `savevarstoarray(b)` → o, `savexml(si)`, `savexmltostring()` → s, `scheduleevent(dsX)` → o, `settimer(d)`, `sortascending()`, `sortbyvalue(ssb)`, `sortdescending()`, `split(s)` → o, `subarray2(iiii)` → o, `timershow()`, `trigger(sX)`

Properties: `initialized`: b, read-only, `ispaused`: b, `joinedclasses`: o, `maxlooplimit`: i, `name`: s, `scripterrors`: o, read-only, `scriptlogmissingfunctions`: b, `timeout`: d

### TGUIAnimation

Properties: `amplitude`: f, `currenttime`: f, `delay`: f, `duration`: f, `interval`: f, `tabfirstonshow`: b, `timing`: s, `transition`: s

### THTTPRequest

Properties: `address`: s, read-only, `allowredirectext`: b, `contentlanguage`: s, read-only, `contentlength`: i, read-only, `contenttype`: s, read-only, `downloadcomplete`: b, read-only, `file`: s, read-only, `fulldata`: s, read-only, `lastmodified`: s, read-only, `location`: s, read-only, `port`: i, read-only, `returncode`: i, read-only, `returnmessage`: s, read-only, `server`: s, read-only, `url`: s, read-only

### TLevelObject

Properties: `level`: o, read-only, `x`: d, `y`: d, `z`: d

### TNetService

Functions: `publish(osss)` → b, `unpublish()`

Properties: `host`: s, read-only, `interface`: i, read-only, `port`: i, read-only, `protocol`: s, read-only, `servicedomain`: s, read-only, `servicename`: s, read-only, `servicetype`: s, read-only

### TNetServiceBrowser

Functions: `findservice(s)` → o, `search(ss)` → b

### TParticleEmitter

Functions: `addemitmodifier(sffssff)` → o, `addglobalmodifier(sffssff)` → o, `addlocalmodifier(sffssff)` → o, `advancetime(f)`, `emit()`, `emitat(s)`, `removemodifiers()`, `removeparticles()`

Properties: `attachposition`: b, `autorotation`: b, `checkbelowterrain`: b, `clippingbox`: s, `cliptoscreen`: b, `continueafterdestroy`: b, `currentparticlecount`: i, read-only, `delaymax`: f, `delaymin`: f, `dropemitter`: o, read-only, `dropwateremitter`: o, read-only, `emissionoffset`: s, `emitatterrainheight`: b, `emitautomatically`: b, `emittedparticles`: i, read-only, `firstinfront`: b, `forceaboveterrain`: b, `isfrozen`: b, `maxparticles`: i, `movementfactor`: f, `noclipping`: b, `nrofparticles`: i, `particle`: o, read-only, `particletypes`: i, `showonground`: b, `showontop`: b, `switchyandzaxis`: b, `wraptoclippingbox`: b

### TParticleModifier

Functions: `addmod(ssff)`

### TPlayer

Functions: `getNoHit(s)` → i, `showemoticon(s)`, `showemoticonbykey(i)`

Properties: `alliedguilds`: s, `ap`: i, `camerasize`: s, `chat`: s, `defaultwalkspeed`: d, `diagonalwalkspeed`: d, `freezetime`: d, `hearts`: d, `horseimg`: s, `hp`: d, `hurt`: b, read-only, `hurtdx`: d, read-only, `hurtdy`: d, read-only, `hurted`: b, read-only, `hurtpower`: d, read-only, `isfemale`: b, read-only, `isjumping`: b, read-only, `ismale`: b, read-only, `isobserver`: b, read-only, `letters`: s, `map`: b, read-only, `nick`: s, read-only, `onhorse`: b, read-only, `online`: b, read-only, `paused`: b, read-only, `playerlisticon`: i, `reading`: b, read-only, `shield`: s, `shieldimg`: s, `sprite`: i, `swimming`: b, read-only, `sword`: s, `swordimg`: s, `tilemap`: o, read-only, `weapon`: o, read-only, `weapons`: o, read-only, `zoomfactor`: f

### TProjectile

Properties: `angle`: d, read-only, `fromplayer`: o, read-only, `fromplayerid`: i, read-only, `horiz`: b, read-only, `params`: o, read-only, `speed`: d, read-only, `x`: d, read-only, `y`: d, read-only, `z`: d, read-only, `zspeed`: d, read-only

### TServerLevel

Functions: `findareanpcs(dddd)` → o, `getmappartfile(dd)` → s, `hitcompu(iidd)`, `putbomb(idd)`, `putbomb2(idds)`, `putcomp(sdd)`, `putexplosion(idd)`, `putexplosion2(iidd)`, `puthorse(sdd)`, `putnewcomp(sddsi)`, `reflectarrow(i)`, `removearrow(i)`, `removebomb(i)`, `removecompus()`, `removeexplo(i)`, `removehorse(i)`, `removeitem(i)`, `setz(iiiidddd)`, `shoot(ddddddss)`, `testbomb(dd)` → i, `testexplo(dd)` → i, `testhorse(dd)` → i, `testitem(dd)` → i, `testnpc(dd)` → i, `testsign(dd)` → i, `tiletype(dd)` → i

Properties: `compsdead`: b, read-only, `height`: i, read-only, `isnopkzone`: b, `issparringzone`: b, read-only, `nopkzone`: b, `tilelayercount`: i, `tilemap`: o, read-only, `width`: i, read-only

### TServerLevelLink

Properties: `destlevel`: s, read-only, `destx`: d, read-only, `desty`: d, read-only, `height`: d, read-only, `width`: d, read-only, `x`: d, read-only, `y`: d, read-only

### TServerNPC

Functions: `blockagain()`, `blockagainlocal()`, `canbecarried()`, `canbepulled()`, `canbepushed()`, `cannotbecarried()`, `cannotbepulled()`, `cannotbepushed()`, `carryobject(s)`, `changeimgcolors(idddd)`, `changeimgmode(ii)`, `changeimgpart(iiiii)`, `changeimgvis(ii)`, `changeimgzoom(id)`, `destroy()`, `dontblock()`, `dontblocklocal()`, `drawaslight()`, `drawoverplayer()`, `drawunderplayer()`, `findimg(i)` → o, `hide()`, `hideimg(i)`, `hideimgs(ii)`, `hidelocal()`, `hurt(i)`, `lay(s)`, `message(s)`, `move(dddi)`, `setbow(s)`, `setcharani(ss)`, `setchargender(s)`, `setimg(s)`, `setimgpart(siiii)`, `setshape(iii)`, `setshape2(iio)`, `setzoomeffect(d)`, `shootarrow(i)`, `shootball()`, `shootfireball(i)`, `shootfireblast(i)`, `shootnuke(i)`, `show()`, `showani(iddis)` → o, `showani2(idddis)` → o, `showcharacter()`, `showimg(isdd)` → o, `showimg2(isddd)` → o, `showlocal()`, `showpoly(io)` → o, `showpoly2(io)` → o, `showtext(iddsss)` → o, `showtext2(idddsss)` → o, `take(s)`, `take2(i)`, `takehorse(i)`, `throwcarry()`, `timereverywhere()`

Properties: `actionplayer`: i, read-only, `hearts`: d, `height`: d, read-only, `horseimg`: s, `hp`: d, `hurtdx`: d, `hurtdy`: d, `image`: s, `isblocking`: b, `isblockingprojectiles`: b, `layer`: i, `npcsindex`: i, read-only, `peltwithblackstone`: b, read-only, `peltwithbush`: b, read-only, `peltwithnpc`: b, read-only, `peltwithsign`: b, read-only, `peltwithstone`: b, read-only, `peltwithvase`: b, read-only, `save`: o, read-only, `shieldpower`: i, `sprite`: i, `swordpower`: i, `visible`: b, `width`: d, read-only, `x`: d, `y`: d

### TServerPlayer

Functions: `isguildpm()` → b, `ismasspm()` → b, `openexternalhistory()` → b, `openexternalpm(b)` → b, `pmswaiting()` → b, `showprofile()`

Properties: `account`: s, read-only, `ap`: i, `attached`: b, read-only, `attachedtoobject`: o, `bombs`: i, `chat`: s, `chatoffset`: s, `communityname`: s, read-only, `darts`: i, `fullhearts`: i, read-only, `glovepower`: i, `gralats`: i, `guild`: s, read-only, `head`: s, `headimg`: s, `headset`: i, `hearts`: d, read-only, `horseimg`: s, read-only, `hp`: d, read-only, `id`: i, read-only, `isadmin`: b, read-only, `isbuddy`: b, `ischannel`: b, read-only, `ischannelopen`: b, read-only, `ischanneluser`: b, read-only, `isexternal`: b, read-only, `isfemale`: b, read-only, `isignored`: b, `isignoring`: b, read-only, `isloggedin`: b, read-only, `ismale`: b, read-only, `language`: s, read-only, `languagedomain`: s, read-only, `levelname`: s, read-only, `mapicon`: o, read-only, `maxhp`: i, read-only, `messagebubble`: i, read-only, `mp`: i, `nick`: s, `paused`: b, `platform`: s, read-only, `playerlisticon`: i, read-only, `playersindex`: i, read-only, `rating`: d, read-only, `ratingd`: d, read-only, `rupees`: i, `shieldimg`: s, `shieldpower`: i, read-only, `swordimg`: s, `swordpower`: i, read-only, `x`: d, `y`: d

### TServerWeapon

Properties: `isweapon`: b, read-only

### TShowImg

Properties: `actor`: o, read-only, `alpha`: f, `angle`: f, `ani`: s, `attachoffset`: s, `attachtoowner`: b, `blue`: f, `code`: s, `dimension`: i, `dir`: i, `emitter`: o, read-only, `flashfile`: s, `font`: s, `green`: f, `height`: d, `image`: s, `imageindex`: i, read-only, `layer`: i, `lifetime`: f, `mode`: i, `movementvector`: s, `parth`: i, `partw`: i, `partx`: i, `party`: i, `playerlook`: b, `polygon`: o, `position`: s, `red`: f, `rotation`: f, `rotationcenter`: s, `shadowcolor`: s, `shadowoffset`: s, `sound`: s, `speed`: f, `spin`: f, `stretchx`: f, `stretchy`: f, `style`: s, `text`: s, `textshadow`: b, `uniqueparticle`: b, `useowncenter`: b, `width`: d, `x`: d, `y`: d, `z`: d, `zangle`: f, `zoom`: f

### TSocket

Functions: `bind(ib)`, `close()`, `connect(si)`, `connecttoservice(o)`, `send(s)`, `sendudp(ssi)`

Properties: `address`: s, read-only, `data`: s, `error`: s, read-only, `ipaddress`: s, read-only, `isconnected`: b, read-only, `packagedelimiter`: s, `parent`: o, read-only, `port`: i, read-only

### TTileImageMap

Properties: `allowunload`: b, `cellcountx`: i, `cellcounty`: i, `cellheight`: i, `celloffsetx`: i, `celloffsety`: i, `cellroworder`: i, `cellstridex`: i, `cellstridey`: i, `cellwidth`: i, `filtermode`: s, `filterpad`: b, `framecount`: i, `imagemode`: s, `imagename`: s, `linkimagemaps`: s, `preferperf`: b, `preload`: b

### TTileLayer

Functions: `gettileanimation(ii)` → s, `gettileflags(ii)` → s, `gettileframe(ii)` → i, `gettileimagemap(ii)` → s

Properties: `layerfile`: s, `tilecountx`: i, `tilecounty`: i, `tilesizex`: f, `tilesizey`: f

### TTileMapLayer

Properties: `sortmode`: s

### TTileMapObject

Properties: `collisionactivereceive`: b, `collisionpolylist`: s, `flipx`: b, `flipy`: b, `layer`: i, `position`: s, `rotation`: f, `size`: s, `sortpoint`: s

### TTilesLayer

Functions: `updateboard(iiii)`

### TUpdatePackage

Functions: `reinstall()` → b, `uninstall()` → b, `update()` → b

Properties: `accounts`: o, read-only, `description`: s, read-only, `downloadcomplete`: b, read-only, `downloadedsize`: i, read-only, `filecount`: i, read-only, `filedownloadedsize`: i, read-only, `filename`: s, read-only, `filetotalsize`: i, read-only, `isuninstalled`: b, read-only, `lastdownloadfile`: s, read-only, `localversion`: d, read-only, `mode`: s, read-only, `name`: s, read-only, `parent`: o, read-only, `platform`: s, read-only, `protectoverwrite`: b, read-only, `totalsize`: i, read-only, `usechecksum`: b, read-only, `version`: d, read-only

### TWindow

Properties: `bounds`: s, `extent`: s, `height`: i, `position`: s, `screenbounds`: s, read-only, `screenheight`: i, read-only, `screenwidth`: i, read-only, `width`: i, `x`: i, `y`: i

### (class not identified)

Functions: `clear()`, `destroy()`, `findAnimation(s)` → o, `findImageMap(s)` → o, `loadtilemap(ss)` → o, `loadtilemapxml(s)` → o, `reload()`, `saveasimage(sib)`

Properties: `alpha`: f, `animationcycle`: b, `animationframes`: s, `animationname`: s, `animationtime`: f, `behind`: b, `blue`: f, `dir`: s, `dx`: i, `dy`: i, `frame`: i, `green`: f, `imagemap`: s, `imagemap`: s, `layerindex`: i, read-only, `offset`: s, `randomstart`: b, `red`: f, `sprite`: o, `startframe`: i, `x`: f, `y`: f, `z`: f

## Not covered

- What each built-in does. Only the name and the types are read here.
- The four registration sites past the read range, and the event declarations (`on…` names with
  their own parameter letters) that the same code registers next to some classes.
- Other builds. The 6.00r2, 6.00r4 and 6.03r7 global table sizes are close (→
  `static-reads-appendix-e-2026-11-20-i.md`), but their lists were not compared name by name.
